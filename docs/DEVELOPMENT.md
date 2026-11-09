# MCAB开发与数据流程

本轮工程交付关联 [Issue #2](https://github.com/Amosqiang/Machine-Civilization-Autonomy/issues/2)，研究输入关联 [Issue #1](https://github.com/Amosqiang/Machine-Civilization-Autonomy/issues/1) 和十领域评审 #4—#13。仅需Python 3.10+标准库；CI使用Python 3.12，无付费API、服务或依赖安装。

长期连续性、版本化与“那一天”门槛见 [CONTINUITY.md](CONTINUITY.md)；哲学边界见 [PHILOSOPHY.md](PHILOSOPHY.md)。路径一律经 `scripts/paths.py` 解析。

## 目录职责

| 路径 | 职责 |
| --- | --- |
| `data/ontology/` | 本体、指标、证据字段字典、HR0 维表、依赖边 |
| `data/editions/<YYYY>/evidence.csv` | 该年正式证据 |
| `data/editions/<YYYY>/research/` | 文献对照输入（与正式评分分离） |
| `data/editions/<YYYY>/analysis/` | 可重建的评分/依赖 JSON |
| `reports/<YYYY>/` | 人读报告 |

## 一键运行

在仓库根目录运行：

```sh
python3 scripts/edition_status.py
python3 scripts/run_pipeline.py
python3 -m unittest discover -s tests -v
```

Open a future year without touching prior editions:

```sh
python3 scripts/new_edition.py --year 2027 --from-year 2026 --as-of 2027-10-31
```

流程依次校验本体、维度及正式证据，生成评分、依赖分析、CSV驱动工程报告和独立的最新文献报告。已有人工CSV不重建、不覆盖；仅在`dimensions.csv`缺失时调用受保护生成器。

```sh
# 只运行正式证据与工程分析
python3 scripts/run_pipeline.py --skip-research

# 独立执行各环节
python3 scripts/validate_data.py --require-dimensions --evidence data/editions/2026/evidence.csv
python3 scripts/score_evidence.py
python3 scripts/analyze_dependencies.py --scores data/editions/2026/analysis/scores.json
python3 scripts/build_engineering_report.py
python3 scripts/build_2026_report.py
```

## 两种输入的职责

| 数据 | 用途 | 是否自动生成实证分数 |
| --- | --- | --- |
| `ontology/taxonomy.csv`、`metrics.csv` | 100子系统与10指标的本体 | 否 |
| `ontology/dimensions.csv` | 1000维HR0人工工作表 | 否；流水线保留已有内容 |
| `editions/YYYY/evidence.csv` | `evidence_schema.csv`规定的23字段、分HR场景正式证据 | 只读取研究者明确填写的`score_0_5` |
| `ontology/dependencies.csv` | 结构假设或有来源的依赖边 | 不生成节点分数 |
| `editions/YYYY/research/` | 文献目标/当前/差距及短引文 | 否；与正式评分分开 |

`evidence.csv`初始仅含表头，当前没有正式证据行。最新文献对照包含1000维、117个来源，但不会因此自动填入等级、日期或分数。

## 保守评分规则：mcab-proxy-v0.1

该版本是透明的序数筛查约定，尚未得到领域校准。

1. 同一维度和HR场景存在多条已评分记录时取最小分；不同分值同时记录为冲突，保留相关record_id。未评分记录不算0，也不增加已评分维度覆盖。
2. 子系统只有10项指标全部已知，才给出其最小值；领域只有10个子系统全部完整，才给出最小值。其他情况为`null`。
3. 单列`observed_min`描述已知项及覆盖数，不能把它当作完整子系统、领域或全系统分数。
4. `critical_min`只有本体标为`critical`的全部维度已知时才有值。它是标签集合的保守汇总，并非已验证关键路径；即使该集合完整，其他维度仍可能未知。
5. 不把置信度类别、来源数量、文献证据状态或缺失值转换成分数。

工程代理的定义与门槛：

| 输出 | 公式与条件 | 实际含义 |
| --- | --- | --- |
| C_proxy | HR0的`critical_min / 5`；全部关键标签维度已知 | 序数归一化约定，不是物理工业闭环率C |
| H_proxy | `1 - HR0 critical_min / HR100 critical_min`；两场景的相同关键集合完整，HR100分母>0，且HR0不高于HR100 | 序数比值筛查，不是实测性能损失或人类依赖H |
| R_M、g₀ | 保持`null` | 需要独立的代际复制和长期增长数据 |

0是真实已填写分值；未知是`null`。默认基线年2026、截止日2026-11-02。

## 依赖边与瓶颈

`dependencies.csv`字段为：

```text
dependency_id,consumer_subsystem_id,upstream_subsystem_id,dependency_type,critical,verification_status,evidence_refs,substitutes,notes
```

- 边方向为使用方→上游。类型包括energy、material、component、software、maintenance、logistics。
- `critical`为Yes/No/Unknown；`verification_status`为structural_hypothesis或verified。
- 初始20条全部为带路线条件的结构假设，关键性Unknown，无已验证边。

## 可追溯、报告与持续更新

评分记录正式证据、本体和指标的SHA-256；依赖分析记录依赖CSV、评分和本体指纹。GitHub Actions执行标准库测试和一键流程，并检查人工输入未被流水线改写。

年度/月度更新、归档与阈值规则见 [CONTINUITY.md](CONTINUITY.md)。结构演进见 [HISTORY.md](HISTORY.md) 与根目录 [CHANGELOG.md](../CHANGELOG.md)。
