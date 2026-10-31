#!/usr/bin/env python3
"""Generate MCAB's 1000-dimensional evaluation table from taxonomy + metrics."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TAXONOMY = ROOT / "data" / "taxonomy.csv"
METRICS = ROOT / "data" / "metrics.csv"
OUTPUT = ROOT / "data" / "dimensions.csv"

SCORE_SCALE = {
    0: "H5 完全寄宿：关键操作必须依赖人类",
    1: "H4 自动运行：可自动运行，但异常与维护依赖人类",
    2: "H3 局部自治：能处理部分故障，仍依赖关键外部输入",
    3: "H2 高度自治：多数维护、输入与扩容可自主完成",
    4: "H1 近乎独立：仅少量关键环节仍需人类文明供应",
    5: "H0 宿主独立：长期无人条件下可运行、恢复、扩容和复制",
}


def read_csv(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    taxonomy = read_csv(TAXONOMY)
    metrics = read_csv(METRICS)
    rows = []

    for subsystem in taxonomy:
        for metric in metrics:
            dimension_id = f"{subsystem['subsystem_id']}-{metric['metric_id']}"
            rows.append(
                {
                    "dimension_id": dimension_id,
                    "domain_id": subsystem["domain_id"],
                    "domain": subsystem["domain"],
                    "subsystem_id": subsystem["subsystem_id"],
                    "subsystem": subsystem["subsystem"],
                    "metric_id": metric["metric_id"],
                    "metric": metric["metric"],
                    "test_question": f"在人类持续参与降为0的条件下，{subsystem['subsystem']}是否具备{metric['metric']}？",
                    "criticality": subsystem["criticality"],
                    "score_0_5": "",
                    "confidence_0_1": "",
                    "evidence_date": "",
                    "evidence_type": "",
                    "source": "",
                    "notes": "",
                }
            )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    assert len(taxonomy) == 100, f"Expected 100 subsystems, got {len(taxonomy)}"
    assert len(metrics) == 10, f"Expected 10 metrics, got {len(metrics)}"
    assert len(rows) == 1000, f"Expected 1000 dimensions, got {len(rows)}"
    print(f"Generated {len(rows)} dimensions -> {OUTPUT}")
    print("Score scale:")
    for score, label in SCORE_SCALE.items():
        print(f"  {score}: {label}")


if __name__ == "__main__":
    main()
