#!/usr/bin/env python3
"""Build the CSV-driven engineering dashboard; preserve all unknown scores."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import html
import json
import os
from pathlib import Path
import sys
import tempfile

from paths import (
    DEFAULT_YEAR,
    dependencies_csv,
    dependencies_json,
    evidence_csv,
    is_curated_data,
    metrics_csv,
    ontology_dir,
    reports_dir,
    scores_json,
    taxonomy_csv,
)
from validate_data import EVIDENCE_FIELDS, ValidationError, load_inputs, read_table, validate_evidence

ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = ("HR100", "HR50", "HR10", "HR1", "HR0")


def escape(value) -> str:
    return html.escape(str(value), quote=True)


def display(value) -> str:
    return "未知" if value is None else escape(value)


def load_dashboard(evidence: Path, scores_path: Path, dependency_path: Path, *, year: int) -> tuple:
    taxonomy, metrics = load_inputs(ontology_dir())
    validate_evidence(evidence, taxonomy, metrics)
    rows = read_table(evidence, EVIDENCE_FIELDS)
    scores = json.loads(scores_path.read_text(encoding="utf-8"))
    dependencies = json.loads(dependency_path.read_text(encoding="utf-8"))
    if scores.get("input", {}).get("year") != year:
        raise ValidationError(f"This dashboard is the {year} edition; other years require their own report")
    checksum = hashlib.sha256(evidence.read_bytes()).hexdigest()
    if scores.get("input", {}).get("evidence_sha256") != checksum:
        raise ValidationError("Score artifact is stale or belongs to a different evidence CSV; run the pipeline")
    for name, path in (("taxonomy", taxonomy_csv()), ("metrics", metrics_csv())):
        expected = hashlib.sha256(path.read_bytes()).hexdigest()
        if scores["input"].get(f"{name}_sha256") != expected or dependencies.get(f"{name}_sha256") != expected:
            raise ValidationError(f"Analysis uses a stale {name}; run the pipeline")
    if dependencies.get("scores_sha256") != hashlib.sha256(scores_path.read_bytes()).hexdigest():
        raise ValidationError("Dependency artifact is stale or belongs to a different score file; run the pipeline")
    if dependencies.get("dependency_csv_sha256") != hashlib.sha256(dependencies_csv().read_bytes()).hexdigest():
        raise ValidationError("Dependency artifact is stale or belongs to a different dependency CSV; run the pipeline")
    if scores["input"]["evidence_records"] != len(rows):
        raise ValidationError("Score artifact evidence count disagrees with the CSV")
    if len(scores["dimensions"]) != 1000:
        raise ValidationError("Score artifact must retain all 1000 dimensions")
    return taxonomy, rows, scores, dependencies


def render_dashboard(taxonomy, evidence, scores: dict, dependencies: dict, *, year: int) -> str:
    domains = {row["domain_id"]: row["domain"] for row in taxonomy}
    names = {row["subsystem_id"]: row["subsystem"] for row in taxonomy}
    sections = []
    for scenario in SCENARIOS:
        summary = scores["scenarios"][scenario]
        rows = []
        for domain in sorted(domains, key=int):
            identifiers = [key for key in scores["dimensions"] if key.split(".")[0] == domain]
            known = sum(scores["dimensions"][key][scenario] is not None for key in identifiers)
            records = [row for row in evidence if row["domain_id"] == domain and row["human_removal_scenario"] == scenario]
            confidence = Counter(row["confidence"] for row in records)
            rows.append(f'<tr><th>{escape(domain)} · {escape(domains[domain])}</th><td>{known} / {len(identifiers)}</td><td>{display(scores["domains"][domain][scenario])}</td><td>{len(records)}</td><td>高 {confidence["High"]} / 中 {confidence["Medium"]} / 低 {confidence["Low"]}</td></tr>')
        subsystems = "".join(f'<tr><th>{escape(key)} · {escape(names[key])}</th><td>{display(values[scenario])}</td></tr>' for key, values in scores["subsystems"].items())
        hidden = "" if scenario == "HR0" else " hidden"
        sections.append(f'''<section data-scenario="{scenario}"{hidden}><h2>{scenario}：正式证据与评分覆盖</h2>
<p>已评分 {summary['scored_dimensions']} / {summary['total_dimensions']} 维；完整子系统 {summary['scored_subsystems']} / 100；完整领域 {summary['scored_domains']} / 10。冲突维度：{summary['conflict_dimensions']}。</p>
<p>已知项最小值：{display(summary['observed_min'])}（仅描述已知项）；关键标签集合最小值：{display(summary['critical_min'])}，覆盖 {summary['critical_scored_dimensions']} / {summary['critical_total_dimensions']}。本体标签不是已验证关键路径。</p>
<table><thead><tr><th>领域</th><th>已评分维度</th><th>完整领域序数分</th><th>证据记录</th><th>记录置信度类别</th></tr></thead><tbody>{''.join(rows)}</tbody></table>
<details><summary>查看100个子系统分数</summary><table><thead><tr><th>子系统</th><th>完整10指标最小值</th></tr></thead><tbody>{subsystems}</tbody></table></details></section>''')
    proxy_rows = "".join(f'<tr><th>{escape(key)}</th><td>{display(value)}</td><td>{escape(scores["proxy_explanations"][key])}</td></tr>' for key, value in scores["proxies"].items())
    edge_rows = "".join(f'<tr><td>{escape(row["consumer_subsystem_id"])} → {escape(row["upstream_subsystem_id"])}</td><td>{escape(row["verification_status"])}</td><td>{escape(row["critical"])}</td><td>{escape(row["notes"])}</td></tr>' for graph in ("structural_exposure", "verified_graph") for row in dependencies[graph]["edges"])
    rank_sections = []
    for key, title in (("weakest_nodes", "已完整评分子系统的低分项"), ("highest_human_dependence", "成对场景序数依赖代理"), ("possible_bottlenecks", "已声明验证边支持的瓶颈候选")):
        records = dependencies[key]
        content = '<pre>' + escape(json.dumps(records, ensure_ascii=False, indent=2)) + '</pre>' if records else '<p>未知：当前没有足够的完整评分或已验证依赖支持这项分析。</p>'
        rank_sections.append(f'<h3>{title}</h3>{content}')
    assertions = dependencies.get("evidence_reported_single_points_of_failure", [])
    assertions_html = '<pre>' + escape(json.dumps(assertions, ensure_ascii=False, indent=2)) + '</pre>' if assertions else '<p>未知：当前没有证据记录明确报告单点故障。</p>'
    evidence_href = f"../../data/editions/{year}/evidence.csv"
    scores_href = f"../../data/editions/{year}/analysis/scores.json"
    deps_href = f"../../data/editions/{year}/analysis/dependencies.json"
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>MCAB-{year} 工程与证据状态</title><style>
body{{font-family:system-ui,"Noto Sans SC",sans-serif;background:#f4f6f9;color:#203148;line-height:1.7;margin:0}}main{{max-width:1200px;margin:auto;padding:28px}}table{{border-collapse:collapse;width:100%;background:white}}th,td{{text-align:left;padding:12px;border-bottom:1px solid #dce3eb;vertical-align:top;overflow-wrap:anywhere}}.notice{{background:#fff4df;border-left:4px solid #b27020;padding:16px}}a{{color:#155b9b}}select{{padding:10px;font:inherit}}section{{margin:24px 0}}pre{{white-space:pre-wrap;overflow-wrap:anywhere}}[hidden]{{display:none!important}}@media(max-width:650px){{main{{padding:14px}}th,td{{padding:7px;font-size:.8rem}}}}@media print{{select{{display:none}}section[hidden]{{display:block!important}}}}
</style></head><body><main><h1>MCAB-{year}：正式证据与工程分析</h1>
<p>基线年 {escape(scores['input']['year'])} · 截止 {escape(scores['input']['as_of_date'])} · {len(evidence)} 条人工证据记录 · 公式版本 {escape(scores['formula_version'])}</p>
<p><a href="MCAB-{year}-latest.html">查看1000维最新文献对照</a> · <a href="{evidence_href}">正式证据CSV</a> · <a href="{scores_href}">评分JSON</a> · <a href="{deps_href}">依赖分析JSON</a></p>
<div class="notice">正式证据CSV目前可以仅含表头。未知评分始终显示“未知”，文献来源数量、相关性或置信度不会自动转换为评分。下面的C/H仅为约定的序数筛查代理，不是实测工业闭环率或人类依赖；R_M与g₀保持未估计。</div>
<p><label for="scenario">人类参与场景：</label><select id="scenario">{''.join(f'<option{chr(32)+"selected" if value=="HR0" else ""}>{value}</option>' for value in SCENARIOS)}</select></p>{''.join(sections)}
<h2>序数工程代理</h2><table><thead><tr><th>量</th><th>结果</th><th>定义与适用条件</th></tr></thead><tbody>{proxy_rows}</tbody></table>
<h2>依赖与瓶颈分析</h2><p>结构假设边 {dependencies['structural_hypothesis_edge_count']} 条；声明已验证边 {dependencies['verified_edge_count']} 条。边方向为使用方 → 上游。结构连接数量不是失效概率、不可替代性或实际瓶颈排名；单点故障均保持Unknown，直到冗余及替代证据齐备。</p>
<p>已声明验证的关键子图最低序数分：{display(dependencies.get('critical_path_minimum_score'))}。只适用于已列出的关键边端点全部具备评分时，不是全工业系统的关键路径测量。</p>
{''.join(rank_sections)}<h3>证据中明确报告的单点故障断言</h3><p>以下保留原记录及场景，尚未经本工具独立验证；不会用图的连接数量替代证据。</p>{assertions_html}<details><summary>查看依赖边与路线条件</summary><table><thead><tr><th>使用方 → 上游</th><th>证据状态</th><th>关键性</th><th>条件</th></tr></thead><tbody>{edge_rows}</tbody></table></details>
<h2>输入追溯</h2><p>证据CSV SHA-256：<code>{escape(scores['input']['evidence_sha256'])}</code>。本页读取经过校验的CSV、评分及依赖分析；不将文献对照中的推断当作正式评分。</p></main><script>document.getElementById('scenario').addEventListener('change',event=>document.querySelectorAll('[data-scenario]').forEach(section=>section.hidden=section.dataset.scenario!==event.target.value));</script></body></html>'''


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--year", type=int, default=DEFAULT_YEAR)
    parser.add_argument("--evidence", type=Path, default=None)
    parser.add_argument("--scores", type=Path, default=None)
    parser.add_argument("--dependencies", type=Path, default=None)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()
    year = args.year
    evidence = args.evidence if args.evidence is not None else evidence_csv(year)
    scores_path = args.scores if args.scores is not None else scores_json(year)
    dependency_path = args.dependencies if args.dependencies is not None else dependencies_json(year)
    output = args.output if args.output is not None else reports_dir(year) / f"MCAB-{year}-engineering.html"
    temporary = None
    try:
        if output.resolve() in {path.resolve() for path in (evidence, scores_path, dependency_path)}:
            raise ValidationError("Dashboard output must not overwrite an input")
        if is_curated_data(output):
            raise ValidationError("Dashboard output must not overwrite curated data")
        content = render_dashboard(
            *load_dashboard(evidence, scores_path, dependency_path, year=year),
            year=year,
        )
        output.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=output.parent, prefix=".dashboard-", suffix=".tmp", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(content)
        os.replace(temporary, output)
        print(f"Built CSV-driven dashboard -> {output}")
    except (OSError, UnicodeError, ValueError, KeyError, TypeError) as error:
        print(f"Dashboard failed: {error}", file=sys.stderr)
        return 1
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
