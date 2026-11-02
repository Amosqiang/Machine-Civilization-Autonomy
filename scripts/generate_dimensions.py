#!/usr/bin/env python3
"""Generate MCAB's 1000-dimensional HR0 overview from taxonomy + metrics."""

from __future__ import annotations

import argparse
import csv
import os
import sys
import tempfile
from pathlib import Path

from validate_data import ValidationError, load_inputs

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "dimensions.csv"

SCORE_SCALE = {
    0: "H5 完全寄宿：关键操作必须依赖人类",
    1: "H4 自动运行：可自动运行，但异常与维护依赖人类",
    2: "H3 局部自治：能处理部分故障，仍依赖关键外部输入",
    3: "H2 高度自治：多数维护、输入与扩容可自主完成",
    4: "H1 近乎独立：仅少量关键环节仍需人类文明供应",
    5: "H0 宿主独立：长期无人条件下可运行、恢复、扩容和复制",
}


def write_rows(rows: list[dict[str, str]], *, force: bool) -> None:
    """Publish a complete table atomically, without clobbering by default."""
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8-sig",
            newline="",
            dir=OUTPUT.parent,
            prefix=".dimensions-",
            suffix=".tmp",
            delete=False,
        ) as temporary:
            temporary_path = Path(temporary.name)
            writer = csv.DictWriter(temporary, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
            temporary.flush()
            os.fsync(temporary.fileno())

        if force:
            os.replace(temporary_path, OUTPUT)
        else:
            # Linking a completed file is atomic and refuses any existing path,
            # including a file created after the initial existence check.
            os.link(temporary_path, OUTPUT)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--force",
        action="store_true",
        help="replace an existing dimensions.csv, discarding all scores and evidence",
    )
    args = parser.parse_args()

    try:
        if not args.force and os.path.lexists(OUTPUT):
            raise FileExistsError(
                f"{OUTPUT} already exists; preserve it or use --force to discard "
                "all existing scores and evidence"
            )
        taxonomy, metrics = load_inputs(ROOT / "data")
    except (OSError, ValidationError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

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

    try:
        write_rows(rows, force=args.force)
    except (OSError, csv.Error) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(f"Generated {len(rows)} dimensions -> {OUTPUT}")
    print("Score scale:")
    for score, label in SCORE_SCALE.items():
        print(f"  {score}: {label}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
