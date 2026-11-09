#!/usr/bin/env python3
"""Validate reviewed evidence and build the local MCAB-2026 comparison report."""

from __future__ import annotations

import argparse
import csv
from datetime import date
import html
import io
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from urllib.parse import urlsplit

from paths import research_dir
from validate_data import ValidationError, load_inputs

ROOT = Path(__file__).resolve().parents[1]
AS_OF = "2026-11-02"
INPUT_NAMES = ("domains_01_03.json", "domains_02_09.json", "domains_04_05.json", "domains_06_07.json", "domains_08_10.json")
STATUS = {
    "demonstrated_limited": "限定条件下已有演示",
    "partial_related_evidence": "部分相关证据",
    "not_established_in_review": "本轮检索未确立",
    "unknown": "未知",
}
RELATION = {"direct_metric": "直接对应指标", "partial_metric": "部分对应指标", "context_only": "仅提供背景", "no_direct_evidence": "无直接证据"}
CONFIDENCE = {"Low": "低", "Medium": "中", "High": "高"}
RECORD_TEXT = ("required_capability", "current_capability", "gap", "human_dependency", "validation_needed")
SOURCE_TEXT = ("source_id", "title", "url", "publisher", "retrieved_at", "source_type", "supporting_excerpt", "verification", "cache_path", "limitations")
IDENTITY_FIELDS = ("dimension_id", "domain_id", "domain", "subsystem_id", "subsystem", "metric_id", "metric", "test_question", "criticality")


class ReportError(ValueError):
    """A report input fails the evidence or completeness contract."""


def require_text(item: dict, fields: tuple[str, ...], context: str) -> None:
    for field in fields:
        if not isinstance(item.get(field), str) or not item[field].strip():
            raise ReportError(f"{context}: {field} must be nonempty text")


def parse_date(value: str, context: str) -> date:
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise ReportError(f"{context}: expected YYYY-MM-DD")
    try:
        return date.fromisoformat(value)
    except ValueError as error:
        raise ReportError(f"{context}: invalid calendar date") from error


def read_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ReportError(f"Cannot read {path}: {error}") from error
    if not isinstance(value, dict):
        raise ReportError(f"{path}: expected a JSON object")
    return value


def load_expected_grid(root: Path) -> dict[str, dict[str, str]]:
    try:
        taxonomy, metrics = load_inputs(root / "data" / "ontology")
    except ValidationError as error:
        raise ReportError(str(error)) from error
    grid = {}
    for subsystem in taxonomy:
        for metric in metrics:
            identifier = f"{subsystem['subsystem_id']}-{metric['metric_id']}"
            if identifier in grid:
                raise ReportError(f"Duplicate expected dimension {identifier}")
            grid[identifier] = {
                **{key: subsystem[key] for key in ("domain_id", "domain", "subsystem_id", "subsystem", "criticality")},
                "dimension_id": identifier,
                "metric_id": metric["metric_id"],
                "metric": metric["metric"],
                "test_question": f"在人类持续参与降为0的条件下，{subsystem['subsystem']}是否具备{metric['metric']}？",
            }
    if len(grid) != 1000:
        raise ReportError("Expected exactly 1000 unique dimensions")
    return grid


def validate_source(source: dict, root: Path, as_of: str, *, verify_cache: bool = False) -> None:
    require_text(source, SOURCE_TEXT, "source")
    identifier = source["source_id"]
    if not re.fullmatch(r"D\d{2}-S\d{2,}", identifier):
        raise ReportError(f"{identifier}: invalid source_id")
    parsed_url = urlsplit(source["url"])
    if parsed_url.scheme != "https" or not parsed_url.netloc or parsed_url.username or parsed_url.password:
        raise ReportError(f"{identifier}: source URL must be a public HTTPS URL")
    if source["source_type"] not in {"Paper", "benchmark", "field-data", "company-doc", "government", "other"}:
        raise ReportError(f"{identifier}: invalid source_type")
    if source["verification"] not in {"full_text", "abstract", "documentation"}:
        raise ReportError(f"{identifier}: invalid verification")
    cutoff = parse_date(as_of, "as_of_date")
    if parse_date(source["retrieved_at"], f"{identifier} retrieved_at") != cutoff:
        raise ReportError(f"{identifier}: retrieved_at must equal the report as_of_date")
    publication = source.get("publication_date")
    if not isinstance(publication, str):
        raise ReportError(f"{identifier}: publication_date must be an ISO date or an empty string")
    if publication and parse_date(publication, f"{identifier} publication_date") > cutoff:
        raise ReportError(f"{identifier}: publication_date is after as_of_date")
    relative = Path(source["cache_path"])
    if relative.is_absolute() or not relative.parts or relative.parts[0] != ".research_cache":
        raise ReportError(f"{identifier}: cache_path must be relative and inside .research_cache")
    cache_root = (root / ".research_cache").resolve()
    path = (root / relative).resolve()
    if not cache_root.is_relative_to(root.resolve()) or not path.is_relative_to(cache_root):
        raise ReportError(f"{identifier}: cache_path escapes the research cache")
    excerpt = " ".join(source["supporting_excerpt"].split())
    has_chinese = bool(re.search(r"[\u3400-\u9fff]", excerpt))
    if (not has_chinese and len(excerpt.split()) > 25) or (has_chinese and (len(excerpt) > 100 or len(re.findall(r"[A-Za-z]+", excerpt)) > 25)):
        raise ReportError(f"{identifier}: supporting_excerpt exceeds the short-quotation limit")
    if verify_cache:
        try:
            cached_text = path.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeError) as error:
            raise ReportError(f"{identifier}: unreadable cache file: {error}") from error
        if excerpt not in " ".join(cached_text.split()):
            raise ReportError(f"{identifier}: supporting_excerpt is absent from cached source text")


def validate_research_files(root: Path, paths: list[Path], expected: dict[str, dict[str, str]], as_of: str = AS_OF, *, verify_cache: bool = False) -> dict:
    """Validate an exact expected grid; tests may inject a smaller explicit grid."""
    parse_date(as_of, "as_of_date")
    records, sources, summaries, search_logs = {}, {}, {}, []
    expected_domains = {row["domain_id"] for row in expected.values()}
    owned_domains: set[str] = set()
    for path in paths:
        document = read_json(path)
        if document.get("as_of_date") != as_of:
            raise ReportError(f"{path.name}: mismatched as_of_date")
        domains = document.get("domain_ids")
        if not isinstance(domains, list) or not domains or any(not isinstance(d, str) for d in domains):
            raise ReportError(f"{path.name}: domain_ids must be a nonempty string list")
        if len(set(domains)) != len(domains) or set(domains) - expected_domains or set(domains) & owned_domains:
            raise ReportError(f"{path.name}: duplicate or unknown domain ownership")
        owned_domains.update(domains)
        for field in ("sources", "records", "domain_summaries", "search_log"):
            if not isinstance(document.get(field), list):
                raise ReportError(f"{path.name}: {field} must be a list")
        if not document["search_log"]:
            raise ReportError(f"{path.name}: search_log must describe the review")
        for source in document["sources"]:
            if not isinstance(source, dict):
                raise ReportError(f"{path.name}: source must be an object")
            validate_source(source, root, as_of, verify_cache=verify_cache)
            identifier = source["source_id"]
            if identifier in sources:
                raise ReportError(f"Duplicate source_id {identifier}")
            sources[identifier] = source
        for record in document["records"]:
            if not isinstance(record, dict):
                raise ReportError(f"{path.name}: record must be an object")
            require_text(record, ("dimension_id",) + RECORD_TEXT, path.name)
            identifier = record["dimension_id"]
            if identifier not in expected:
                raise ReportError(f"Unknown dimension {identifier}")
            if expected[identifier]["domain_id"] not in domains:
                raise ReportError(f"{identifier}: dimension is outside file domain ownership")
            if identifier in records:
                raise ReportError(f"Duplicate dimension {identifier}")
            for field in IDENTITY_FIELDS:
                if field in record and record[field] != expected[identifier][field]:
                    raise ReportError(f"{identifier}: identity field {field} disagrees with the ontology")
            if record.get("assessment_status") not in STATUS or record.get("evidence_relation") not in RELATION or record.get("confidence") not in CONFIDENCE:
                raise ReportError(f"{identifier}: invalid assessment_status, evidence_relation or confidence")
            refs = record.get("source_ids")
            if not isinstance(refs, list) or any(not isinstance(ref, str) or not ref for ref in refs) or len(set(refs)) != len(refs):
                raise ReportError(f"{identifier}: source_ids must be a unique string list")
            if (record["assessment_status"] == "demonstrated_limited" or record["evidence_relation"] in {"direct_metric", "partial_metric"}) and not refs:
                raise ReportError(f"{identifier}: positive evidence assessment requires a source")
            if record["assessment_status"] == "demonstrated_limited" and record["evidence_relation"] != "direct_metric":
                raise ReportError(f"{identifier}: demonstrated_limited requires direct_metric evidence")
            records[identifier] = {**expected[identifier], **record}
        found_summaries = set()
        for summary in document["domain_summaries"]:
            if not isinstance(summary, dict):
                raise ReportError(f"{path.name}: domain summary must be an object")
            require_text(summary, ("domain_id", "summary", "strongest_progress", "principal_gap"), path.name)
            domain = summary["domain_id"]
            if domain not in domains or domain in found_summaries:
                raise ReportError(f"{path.name}: duplicate or unrelated domain summary")
            found_summaries.add(domain)
            summaries[domain] = summary
        if found_summaries != set(domains):
            raise ReportError(f"{path.name}: missing domain summary")
        for entry in document["search_log"]:
            if not isinstance(entry, dict):
                raise ReportError(f"{path.name}: search entry must be an object")
            require_text(entry, ("query", "retrieved_at", "note"), path.name)
            if parse_date(entry["retrieved_at"], "search retrieved_at") != parse_date(as_of, "as_of_date"):
                raise ReportError(f"{path.name}: search retrieved_at must equal as_of_date")
            search_logs.append({"file": path.name, **entry})
    missing = set(expected) - set(records)
    if missing:
        raise ReportError(f"Missing {len(missing)} dimensions: {', '.join(sorted(missing)[:12])}")
    if owned_domains != expected_domains:
        raise ReportError("Incomplete domain ownership")
    for identifier, record in records.items():
        undeclared = set(record["source_ids"]) - set(sources)
        if undeclared:
            raise ReportError(f"{identifier}: undeclared source_ids {', '.join(sorted(undeclared))}")
    return {"as_of_date": as_of, "records": [records[key] for key in expected], "sources": sources, "summaries": summaries, "search_log": search_logs, "cache_verified": verify_cache}


def attach_synthesis(bundle: dict, path: Path) -> None:
    """Add an optional explicitly analytical overview with validated citations."""
    if not path.exists():
        return
    synthesis = read_json(path)
    require_text(synthesis, ("overall_assessment",), path.name)
    findings = synthesis.get("findings")
    steps = synthesis.get("next_steps")
    if not isinstance(findings, list) or not findings:
        raise ReportError(f"{path.name}: findings must be a nonempty list")
    if not isinstance(steps, list) or not steps or any(not isinstance(step, str) or not step.strip() for step in steps):
        raise ReportError(f"{path.name}: next_steps must be a nonempty text list")
    for finding in findings:
        if not isinstance(finding, dict):
            raise ReportError(f"{path.name}: finding must be an object")
        require_text(finding, ("title", "text"), path.name)
        refs = finding.get("source_ids")
        if not isinstance(refs, list) or not refs or any(not isinstance(ref, str) or ref not in bundle["sources"] for ref in refs) or len(set(refs)) != len(refs):
            raise ReportError(f"{path.name}: each finding requires unique declared source_ids")
    bundle["synthesis"] = synthesis


def counts(records: list[dict]) -> dict[str, int]:
    return {status: sum(record["assessment_status"] == status for record in records) for status in STATUS}


def relation_counts(records: list[dict]) -> dict[str, int]:
    return {relation: sum(record["evidence_relation"] == relation for record in records) for relation in RELATION}


def escape(value: str) -> str:
    return html.escape(str(value), quote=True)


def md(value: str) -> str:
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\r", " ").replace("\n", "<br>").replace("<", "&lt;").replace(">", "&gt;")


def citations(record: dict, sources: dict, *, markdown: bool = False) -> str:
    if not record["source_ids"]:
        return "无直接来源"
    if markdown:
        return "、".join(f"[{identifier}]({sources[identifier]['url']})" for identifier in record["source_ids"])
    return " ".join(f'<a href="#source-{escape(identifier)}" title="{escape(sources[identifier]["title"])}">[{escape(identifier)}]</a>' for identifier in record["source_ids"])


METHOD_TEXT = """本报告把工业自我复制所需的能力作为目标，与本轮检索到的公开证据逐维比较。required_capability与validation_needed是本研究拟议的操作性目标和验收要求，不是通用工业标准或独立发现的经验事实。目标是研究要求，不是已实现事实；“当前能力”仅代表来源在其特定系统、实验条件和时间范围内支持的内容。

1000维是现有本体的笛卡尔积覆盖，不是1000项独立研究，也不代表1000项能力是联合必要且充分条件。目标要求取决于所选工业系统设计与替代路线：太阳能与核能等能源路线可替代，信用、保险等经济机制也并非任何机器文明都必须采用。完整填表仅表示逐维作了对照，不表示能力已齐备或存在直接证据。

未知不等于0分；“本轮检索未确立”只表示尚未找到足够直接证据，不能推出技术不可能。限定条件下的演示不代表长期、全工况或跨系统闭环。数字复制、自动运行、实验室演示与物理工业再生产分别判断。不同公司的系统、不同年份的实验与不同环境中的成果，不能拼接成已被验证的无人文明。

本轮是有记录的定向公开资料检索，优先原始论文、官方技术文档及实际运行资料，不是穷尽性的系统综述。“最新”仅指截至报告日期、本轮实际取得并核查的公开资料，不承诺检索到全球所有最新进展。检索日志记录查询及范围限制；来源的发布日期未获确认时留空。摘要、公司材料和有限演示的局限保留在来源条目中。

核查的是来源可访问性、文本及日期，未独立复现实验性能。公司文档中的性能是发布方报告的能力。引用短摘录用于核查实际取得的文本，不能自动证明其支持所有相邻主张，仍需领域专家复核。来源按编号登记；同一URL可能因不同摘录多次登记，因此来源记录数与唯一URL数分别报告。完整抓取缓存不随报告分发，使用--verify-cache可在持有本地缓存时复核摘录；默认可仅凭版本库中的短摘录与研究记录重建报告。

assessment_status描述本轮发现的证据状态；evidence_relation描述来源与该指标的对应关系。direct_metric仅表示直接相关，不表示完整目标已达成或获得第三方验证；demonstrated_limited仅表示有限演示，不表示实现完整工业再生产。confidence是定性分析判断的把握程度，不是自主性得分或成功概率；高置信度也可能是对“尚无直接证据”的判断。没有为1000维填造0—5评分，也没有由序数分计算文明自主性。

工业闭环度C、人类依赖H、机器复制数R_M和无人增长率g₀均未估值。完整闭环需要统一系统边界、共同时间尺度、关键投入及替代路径、库存耗尽后表现、维护与灾难恢复、子代系统的同等功能与再复制能力等实证，不能从本表的演示数量或相关论文数量推出。"""


def html_report(bundle: dict) -> str:
    records, sources = bundle["records"], bundle["sources"]
    domains = {r["domain_id"]: r["domain"] for r in records}
    metrics = {r["metric_id"]: r["metric"] for r in records}
    domain_options = "".join(f'<option value="{escape(key)}">{escape(key)} · {escape(label)}</option>' for key, label in sorted(domains.items(), key=lambda x: int(x[0])))
    metric_options = "".join(f'<option value="{escape(key)}">{escape(key)} · {escape(label)}</option>' for key, label in sorted(metrics.items(), key=lambda x: int(x[0][1:])))
    status_options = "".join(f'<option value="{key}">{label}</option>' for key, label in STATUS.items())
    relation_options = "".join(f'<option value="{key}">{label}</option>' for key, label in RELATION.items())
    cards = "".join(f'<div class="card"><strong>{number}</strong><span>{STATUS[status]}</span></div>' for status, number in counts(records).items())
    relations = "".join(f'<div class="card"><strong>{number}</strong><span>{RELATION[relation]}</span></div>' for relation, number in relation_counts(records).items())
    unique_urls = len({source["url"] for source in sources.values()})
    cache_note = "本次构建已逐条对照本地获取文本核查短摘录。" if bundle.get("cache_verified") else "本次由已登记短摘录重建；未读取私有完整抓取缓存。"
    map_rows = []
    ordered_metrics = sorted(metrics, key=lambda value: int(value[1:]))
    for domain in sorted(domains, key=int):
        cells = []
        for metric in ordered_metrics:
            cell = [record for record in records if record["domain_id"] == domain and record["metric_id"] == metric]
            direct = sum(record["evidence_relation"] == "direct_metric" for record in cell)
            partial = sum(record["evidence_relation"] == "partial_metric" for record in cell)
            opacity = 0.06 + 0.34 * (direct + partial) / max(1, len(cell))
            cells.append(f'<td><button data-map-domain="{escape(domain)}" data-map-metric="{escape(metric)}" style="background:rgba(47,112,157,{opacity:.3f})" title="{escape(domains[domain])} · {escape(metrics[metric])}：{direct}项直接相关、{partial}项部分相关，共{len(cell)}项">{direct}直 / {partial}部<br><small>共{len(cell)}项</small></button></td>')
        map_rows.append(f'<tr><th scope="row">{escape(domain)} · {escape(domains[domain])}</th>{"".join(cells)}</tr>')
    coverage_map = '<div class="table-wrap heatmap"><table><thead><tr><th>文明系统 / 指标</th>' + "".join(f'<th title="{escape(metrics[metric])}">{escape(metric)}<br><small>{escape(metrics[metric])}</small></th>' for metric in ordered_metrics) + '</tr></thead><tbody>' + "".join(map_rows) + '</tbody></table></div>'
    synthesis_section = ""
    if synthesis := bundle.get("synthesis"):
        finding_cards = "".join(f'<article><h3>{escape(finding["title"])}</h3><p>{escape(finding["text"])}</p><p>{citations(finding, sources)}</p></article>' for finding in synthesis["findings"])
        next_steps = "".join(f'<li>{escape(step)}</li>' for step in synthesis["next_steps"])
        synthesis_section = f'<h2>分析性综合：当前走到哪一步</h2><p class="muted">以下为基于已核查来源的分析判断，不是额外的测量结果或已验证依赖图排名。</p><p>{escape(synthesis["overall_assessment"])}</p><div class="domains">{finding_cards}</div><h3>接下来需要验证什么</h3><ol>{next_steps}</ol>'
    summaries = []
    for domain in sorted(domains, key=int):
        summary = bundle["summaries"][domain]
        summaries.append(f'<article><h3>{escape(domain)} · {escape(domains[domain])}</h3><p>{escape(summary["summary"])}</p><p><b>最强进展：</b>{escape(summary["strongest_progress"])}</p><p><b>主要缺口：</b>{escape(summary["principal_gap"])}</p></article>')
    rows = []
    for record in records:
        rows.append(f'''<tr data-domain="{escape(record['domain_id'])}" data-metric="{escape(record['metric_id'])}" data-status="{record['assessment_status']}" data-relation="{record['evidence_relation']}"><th scope="row"><code>{escape(record['dimension_id'])}</code><br>{escape(record['subsystem'])}<br><small>{escape(record['metric'])} · {escape(record['domain'])}</small></th><td>{escape(record['required_capability'])}</td><td>{escape(record['current_capability'])}</td><td>{escape(record['gap'])}<details><summary>人类依赖与决定性验证</summary><p><b>剩余依赖：</b>{escape(record['human_dependency'])}</p><p><b>拟议验证要求：</b>{escape(record['validation_needed'])}</p></details></td><td><span class="status {record['assessment_status']}">{STATUS[record['assessment_status']]}</span><p>{RELATION[record['evidence_relation']]}<br>判断置信度：{CONFIDENCE[record['confidence']]}</p>{citations(record, sources)}</td></tr>''')
    source_sections = []
    for identifier, source in sorted(sources.items()):
        source_sections.append(f'''<article class="source" id="source-{escape(identifier)}"><h3>{escape(identifier)} · <a href="{escape(source['url'])}" target="_blank" rel="noopener noreferrer">{escape(source['title'])}</a></h3><p>{escape(source['publisher'])} · 发布日期：{escape(source['publication_date'] or '未确认')} · 获取：{escape(source['retrieved_at'])} · {escape(source['source_type'])} · 核查范围：{escape(source['verification'])}</p><blockquote>{escape(source['supporting_excerpt'])}</blockquote><p><b>适用边界：</b>{escape(source['limitations'])}</p></article>''')
    search_rows = "".join(f'<tr><td>{escape(entry["file"])}</td><td>{escape(entry["query"])}</td><td>{escape(entry["note"])}</td></tr>' for entry in bundle["search_log"])
    methodology = "".join(f"<p>{escape(paragraph)}</p>" for paragraph in METHOD_TEXT.split("\n\n"))
    return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>MCAB-2026 · 理想要求与当前能力</title><style>
:root{{color-scheme:light;font-family:system-ui,-apple-system,"Noto Sans SC",sans-serif;color:#203148;background:#f4f6f9;line-height:1.65}}body{{margin:0}}main{{max-width:1600px;margin:auto;padding:32px}}h1{{font-size:clamp(1.8rem,4vw,3rem);line-height:1.2}}h2{{margin-top:2.5rem}}a{{color:#155b9b}}small{{color:#53677d}}.eyebrow{{letter-spacing:.12em;color:#447286}}.notice{{border-left:5px solid #b27020;background:#fff4df;padding:16px 20px}}.cards{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:24px 0}}.card,article{{background:#fff;border:1px solid #dce3eb;border-radius:10px;padding:18px}}.card strong{{display:block;font-size:2rem}}.card span{{font-size:.9rem}}.domains{{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}}.controls{{position:sticky;top:0;background:#f4f6f9;padding:12px 0;z-index:2;display:flex;gap:10px;flex-wrap:wrap}}input,select,button{{font:inherit;padding:10px;border:1px solid #b9c8d8;border-radius:6px;background:#fff}}input{{flex:2;min-width:200px}}select{{flex:1;min-width:160px}}button{{cursor:pointer}}.table-wrap{{overflow-x:auto;background:#fff;border:1px solid #dce3eb}}table{{width:100%;border-collapse:collapse;table-layout:fixed;font-size:.9rem}}th,td{{padding:14px;vertical-align:top;text-align:left;border-bottom:1px solid #dce3eb;overflow-wrap:anywhere}}thead th{{background:#e8eef5}}th:first-child{{width:15%}}td{{width:21%}}td:last-child{{width:17%}}code{{font-size:.85rem}}details{{margin-top:12px}}summary{{cursor:pointer;color:#155b9b}}.status{{display:inline-block;padding:3px 7px;border-radius:5px;font-size:.8rem;background:#eef1f5}}.demonstrated_limited{{background:#dff1e7}}.partial_related_evidence{{background:#e2edf9}}.not_established_in_review{{background:#fff0d8}}.source{{margin:12px 0;scroll-margin-top:80px}}blockquote{{border-left:3px solid #b9c8d8;margin-left:0;padding-left:16px}}.muted{{color:#53677d}}[hidden]{{display:none!important}}footer{{margin-top:32px;border-top:1px solid #ccd7e3;padding-top:20px}}
.heatmap table{{table-layout:auto;min-width:1000px}}.heatmap th,.heatmap td{{width:auto;padding:6px;text-align:center}}.heatmap th:first-child{{text-align:left;min-width:160px}}.heatmap button{{font-size:.75rem;white-space:nowrap;padding:7px;width:100%}}
@media(max-width:800px){{main{{padding:18px}}.cards,.domains{{grid-template-columns:repeat(2,1fr)}}table{{min-width:1100px}}.controls{{position:static}}}}
@media print{{:root{{font-size:9pt;background:#fff}}main{{padding:0;max-width:none}}.controls,.downloads,.screen-only{{display:none}}.cards{{grid-template-columns:repeat(4,1fr)}}.domains{{display:block}}article{{break-inside:avoid;margin-bottom:8pt}}.table-wrap{{overflow:visible;border:0}}table{{font-size:7pt;min-width:0}}td,th{{padding:5pt}}thead{{display:table-header-group}}tr{{break-inside:avoid}}details>*{{display:block}}summary{{display:none}}a{{color:inherit}}h2{{break-after:avoid}}@page{{size:A4 landscape;margin:12mm}}}}
</style></head><body><main><div class="eyebrow">MCAB / MACHINE CIVILIZATION AUTONOMY BENCHMARK</div><h1>工业自我复制：理想要求与当前能力</h1><p>截至 <b>{escape(bundle['as_of_date'])}</b> · {len(records)} 个维度 · {len(domains)} 个文明系统 · {len(sources)} 项来源记录 / {unique_urls} 个唯一URL</p><nav class="downloads"><a href="#comparison">查看1000维逐项对照</a> · <a href="#coverage">查看10×10证据覆盖图</a> · <a href="#bibliography">查看来源</a></nav><div class="notice"><b>阅读边界：</b>逐项对照“需要什么”与“已经有什么证据”。没有证据不等于0分；1000维是本体覆盖，不是1000项独立研究或联合必要且充分条件。目标依所选路线而定，局部演示不等于长期工业闭环。C、H、R_M、g₀均未估值。</div><h2>证据与指标的对应关系</h2><div class="cards">{relations}</div><p class="muted">直接相关不表示完整目标达成；完整填表不表示能力齐备。</p><h2>本轮证据状态</h2><div class="cards">{cards}</div><p class="downloads"><a href="MCAB-2026-dimension-comparison.csv">下载完整CSV</a> · <a href="MCAB-2026-report.md">研究报告Markdown</a> · <a href="MCAB-2026-dimensions.md">1000维完整附录</a> · <button onclick="window.print()">打印 / 保存PDF</button></p>{synthesis_section}<h2>十个系统的当前图景</h2><div class="domains">{''.join(summaries)}</div><h2 id="coverage">十个系统 × 十项指标：证据覆盖图</h2><p>每格覆盖该系统的各子系统。<b>直</b>＝直接相关，<b>部</b>＝部分相关；底色仅反映这两类证据的条目数量。<b>证据覆盖≠自主性得分</b>。点击格子查看对应维度。</p>{coverage_map}<h2 id="comparison">逐维对照</h2><p>展开条目可查看具体人类依赖和需要完成的验证。来源编号可跳转至完整出处及适用限制。</p><div class="controls"><input id="query" aria-label="搜索维度" placeholder="搜索关键词、维度编号、能力或人类依赖"><select id="domain" aria-label="文明系统"><option value="">全部系统</option>{domain_options}</select><select id="metric" aria-label="自主性指标"><option value="">全部指标</option>{metric_options}</select><select id="status" aria-label="证据状态"><option value="">全部证据状态</option>{status_options}</select><select id="relation" aria-label="证据对应关系"><option value="">全部对应关系</option>{relation_options}</select><button id="reset">重置</button></div><p id="match-count" aria-live="polite">显示 {len(records)} / {len(records)} 项</p><div class="table-wrap"><table id="dimensions"><thead><tr><th>维度</th><th>本研究拟议的理想要求</th><th>本轮核查到的当前公开能力</th><th>差距、依赖与验证</th><th>证据状态及出处</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div><h2>方法与解释边界</h2>{methodology}<h2 id="bibliography">可检索来源目录</h2><input id="source-query" aria-label="搜索来源" placeholder="搜索来源标题、发布方、编号或适用边界"><p class="muted">{cache_note} 核查来源文本不等于独立复现实验性能。私有完整缓存不随报告分发，HTML 本身无需联网即可浏览。</p><section id="sources">{''.join(source_sections)}</section><h2>检索日志</h2><details><summary>查看全部 {len(bundle['search_log'])} 条检索记录及范围限制</summary><div class="table-wrap"><table><thead><tr><th>研究分组</th><th>查询</th><th>结果及限制</th></tr></thead><tbody>{search_rows}</tbody></table></div></details><footer>MCAB-2026 · 本地研究草稿 · 证据截至 {escape(bundle['as_of_date'])}。</footer></main><script>
const rows=[...document.querySelectorAll('#dimensions tbody tr')];const index=rows.map(row=>row.textContent.toLocaleLowerCase());const query=document.getElementById('query');const domain=document.getElementById('domain');const metric=document.getElementById('metric');const status=document.getElementById('status');const relation=document.getElementById('relation');function filter(){{const q=query.value.trim().toLocaleLowerCase();const exactDimension=/^(?:[1-9]|10)[.](?:[1-9]|10)-m(?:[1-9]|10)$/.test(q);let visible=0;rows.forEach((row,i)=>{{const match=(!q||(exactDimension?row.querySelector('code').textContent.toLocaleLowerCase()===q:index[i].includes(q)))&&(!domain.value||row.dataset.domain===domain.value)&&(!metric.value||row.dataset.metric===metric.value)&&(!status.value||row.dataset.status===status.value)&&(!relation.value||row.dataset.relation===relation.value);row.hidden=!match;if(match)visible++;}});document.getElementById('match-count').textContent=`显示 ${{visible}} / ${{rows.length}} 项`;}}[query,domain,metric,status,relation].forEach(control=>control.addEventListener('input',filter));document.getElementById('reset').addEventListener('click',()=>{{[query,domain,metric,status,relation].forEach(control=>control.value='');filter();}});document.querySelectorAll('[data-map-domain]').forEach(button=>button.addEventListener('click',()=>{{query.value='';status.value='';relation.value='';domain.value=button.dataset.mapDomain;metric.value=button.dataset.mapMetric;filter();document.getElementById('match-count').scrollIntoView({{behavior:'smooth',block:'center'}});}}));const sourceRows=[...document.querySelectorAll('.source')];const sourceIndex=sourceRows.map(row=>row.textContent.toLocaleLowerCase());document.getElementById('source-query').addEventListener('input',event=>{{const q=event.target.value.trim().toLocaleLowerCase();sourceRows.forEach((row,i)=>row.hidden=!sourceIndex[i].includes(q));}});window.addEventListener('hashchange',()=>{{const target=document.getElementById(decodeURIComponent(location.hash.slice(1)));if(target&&target.classList.contains('source')){{document.getElementById('source-query').value='';sourceRows.forEach(row=>row.hidden=false);target.scrollIntoView();}}}});
</script></body></html>'''


def markdown_report(bundle: dict) -> str:
    records, sources = bundle["records"], bundle["sources"]
    lines = ["# MCAB-2026：工业自我复制的理想要求与当前能力", "", f"证据与检索截至：**{bundle['as_of_date']}**。覆盖 **{len(records)}** 个维度，登记 **{len(sources)}** 项来源记录、**{len({source['url'] for source in sources.values()})}** 个唯一URL。", "", "[完整逐维附录](MCAB-2026-dimensions.md) · [交互浏览](MCAB-2026-latest.html) · [CSV](MCAB-2026-dimension-comparison.csv)", "", "本版逐项列出目标能力、当前公开证据、差距、人类依赖和拟议验证要求。完整1000维对照不代表1000项均已获得直接实证。", "", "## 本轮证据状态", "", "| 状态 | 维度数 |", "| --- | ---: |"]
    lines.extend(f"| {STATUS[key]} | {value} |" for key, value in counts(records).items())
    lines.extend(["", "## 证据与指标对应关系", "", "| 对应关系 | 维度数 |", "| --- | ---: |"])
    lines.extend(f"| {RELATION[key]} | {value} |" for key, value in relation_counts(records).items())
    lines.extend(["", "这些是本轮检索证据状态及相关性计数，不是工业闭环比例、达标率或自主性评分。直接相关不代表完整目标达成。"])
    if synthesis := bundle.get("synthesis"):
        lines.extend(["", "## 分析性综合：当前走到哪一步", "", "以下为基于已核查来源的分析判断，不是额外测量结果或已验证依赖图排名。", "", synthesis["overall_assessment"]])
        for finding in synthesis["findings"]:
            lines.extend(["", f"### {finding['title']}", "", finding["text"], "", "来源：" + citations(finding, sources, markdown=True)])
        lines.extend(["", "### 接下来需要验证什么", ""])
        lines.extend(f"{number}. {step}" for number, step in enumerate(synthesis["next_steps"], 1))
    lines.extend(["", "## 十个文明系统"])
    domains = {row["domain_id"]: row["domain"] for row in records}
    for domain in sorted(domains, key=int):
        summary = bundle["summaries"][domain]
        subset = [row for row in records if row["domain_id"] == domain]
        lines.extend(["", f"### {domain}. {domains[domain]}", "", summary["summary"], "", f"**最强进展：** {summary['strongest_progress']}", "", f"**主要缺口：** {summary['principal_gap']}", "", "本轮状态：" + "；".join(f"{STATUS[key]} {value}项" for key, value in counts(subset).items()) + "。", "", "来源：" + citations({"source_ids": sorted({ref for record in subset for ref in record["source_ids"]})}, sources, markdown=True)])
    lines.extend(["", "## 方法与解释边界", "", METHOD_TEXT])
    lines.extend(["", "## 检索日志", "", "| 分组 | 检索查询 | 范围与限制 |", "| --- | --- | --- |"])
    lines.extend(f"| {md(entry['file'])} | {md(entry['query'])} | {md(entry['note'])} |" for entry in bundle["search_log"])
    lines.extend(["", "## 来源目录与核查短摘录", "", "来源中的具体证据边界优先于标题、宣传或概括性结论。发布日期未知时明确保留未知。"])
    for identifier, source in sorted(sources.items()):
        lines.extend(["", f"### {identifier} · {source['title']}", "", f"- 出处：[{source['publisher']}]({source['url']})", f"- 发布：{source['publication_date'] or '未确认'}；获取：{source['retrieved_at']}；类型：{source['source_type']}；核查范围：{source['verification']}。", f"- 核查文本：`{source['cache_path']}`", "", f"> {source['supporting_excerpt']}", "", f"**适用限制：** {source['limitations']}"])
    return "\n".join(lines) + "\n"


def markdown_dimensions(bundle: dict) -> str:
    lines = ["# MCAB-2026完整逐维附录", "", f"截至 {bundle['as_of_date']}，共 {len(bundle['records'])} 项。每项的理想能力是研究要求，当前能力仅为已取得来源支持的有限事实。未知不等于0分。", "", "[方法、系统综述及来源目录](MCAB-2026-report.md) · [交互筛选](MCAB-2026-latest.html)"]
    subsystem = None
    for record in bundle["records"]:
        if subsystem != record["subsystem_id"]:
            subsystem = record["subsystem_id"]
            lines.extend(["", f"## {subsystem} · {record['subsystem']}", "", f"系统：{record['domain']}；关键性标签：{record['criticality']}。", "", "| 维度 / 指标 | 理想要求（本研究拟议） | 当前证据支持的能力 | 差距与人类依赖 | 验证要求（本研究拟议） | 证据状态、关系、判断置信度及出处 |", "| --- | --- | --- | --- | --- | --- |"])
        lines.append("| " + " | ".join((md(f"{record['dimension_id']} · {record['metric']}"), md(record["required_capability"]), md(record["current_capability"]), md(record["gap"]) + "<br>**人类依赖：** " + md(record["human_dependency"]), md(record["validation_needed"]), f"{STATUS[record['assessment_status']]}；{RELATION[record['evidence_relation']]}；{CONFIDENCE[record['confidence']]}。" + citations(record, bundle["sources"], markdown=True))) + " |")
    return "\n".join(lines) + "\n"


def csv_report(bundle: dict) -> str:
    output = io.StringIO(newline="")
    fields = list(IDENTITY_FIELDS) + ["as_of_date", *RECORD_TEXT, "assessment_status", "evidence_relation", "confidence", "source_ids", "source_urls"]
    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()
    for record in bundle["records"]:
        row = {field: record[field] for field in IDENTITY_FIELDS + RECORD_TEXT + ("assessment_status", "evidence_relation", "confidence")}
        row.update(as_of_date=bundle["as_of_date"], source_ids=";".join(record["source_ids"]), source_urls=";".join(bundle["sources"][key]["url"] for key in record["source_ids"]))
        writer.writerow(row)
    return output.getvalue()


def write_reports(bundle: dict, output_dir: Path) -> list[Path]:
    artifacts = {
        "MCAB-2026-latest.html": (html_report(bundle), "utf-8"),
        "MCAB-2026-report.md": (markdown_report(bundle), "utf-8"),
        "MCAB-2026-dimensions.md": (markdown_dimensions(bundle), "utf-8"),
        "MCAB-2026-dimension-comparison.csv": (csv_report(bundle), "utf-8-sig"),
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    staged = []
    try:
        for filename, (content, encoding) in artifacts.items():
            with tempfile.NamedTemporaryFile(mode="w", encoding=encoding, newline="", dir=output_dir, prefix=".mcab-", suffix=".tmp", delete=False) as handle:
                staged.append((Path(handle.name), output_dir / filename))
                handle.write(content)
        for temporary, target in staged:
            os.replace(temporary, target)
    finally:
        for temporary, _ in staged:
            temporary.unlink(missing_ok=True)
    return [output_dir / filename for filename in artifacts]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify-cache", action="store_true", help="verify each short excerpt against the private local source-text cache")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "reports" / "2026", help="directory for the four generated local report artifacts")
    args = parser.parse_args()
    try:
        expected = load_expected_grid(ROOT)
        research = research_dir(2026)
        paths = [research / name for name in INPUT_NAMES]
        bundle = validate_research_files(ROOT, paths, expected, verify_cache=args.verify_cache)
        attach_synthesis(bundle, research / "synthesis.json")
        artifacts = write_reports(bundle, args.output_dir)
    except (ReportError, OSError, UnicodeError, KeyError, csv.Error) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    print(f"Validated {len(bundle['records'])} dimensions and {len(bundle['sources'])} source records as of {AS_OF}.")
    for artifact in artifacts:
        print(artifact)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
