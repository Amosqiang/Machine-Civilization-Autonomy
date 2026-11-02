# MCAB开发与数据流程

本轮工程交付关联 [Issue #2](https://github.com/Amosqiang/Machine-Civilization-Autonomy/issues/2)，研究输入关联 [Issue #1](https://github.com/Amosqiang/Machine-Civilization-Autonomy/issues/1) 和十领域评审 #4—#13。仅需Python 3.10+标准库；CI使用Python 3.12，无付费API、服务或依赖安装。

## 一键运行

在仓库根目录运行：

```sh
python3 scripts/run_pipeline.py
python3 -m unittest discover -s tests -v
```

流程依次校验本体、维度及正式证据，生成评分、依赖分析、CSV驱动工程报告和独立的最新文献报告。已有人工CSV不重建、不覆盖；仅在`dimensions.csv`缺失时调用受保护生成器。

```sh
# 只运行正式证据与工程分析
python3 scripts/run_pipeline.py --skip-research

# 独立执行各环节
python3 scripts/validate_data.py --require-dimensions --evidence data/evidence_2026.csv
python3 scripts/score_evidence.py
python3 scripts/analyze_dependencies.py --scores data/analysis/2026/scores.json
python3 scripts/build_engineering_report.py
python3 scripts/build_2026_report.py
```

分析输出在`data/analysis/2026/`，网页在`reports/2026/`。评分和依赖输出使用原子替换；命令拒绝把分析输出写入人工维护的数据文件。已有评分、依赖或报告不会因输入校验失败而被当作有效新结果。

## 两种输入的职责

| 数据 | 用途 | 是否自动生成实证分数 |
| --- | --- | --- |
| `taxonomy.csv`、`metrics.csv` | 100子系统与10指标的本体 | 否 |
| `dimensions.csv` | 1000维HR0人工工作表 | 否；流水线保留已有内容 |
| `evidence_2026.csv` | `evidence_schema.csv`规定的23字段、分HR场景正式证据 | 只读取研究者明确填写的`score_0_5` |
| `dependencies.csv` | 结构假设或有来源的依赖边 | 不生成节点分数 |
| `research/2026/domains_*.json` | 文献目标/当前/差距及短引文 | 否；与正式评分分开 |

`evidence_2026.csv`初始仅含表头，当前没有正式证据行。最新文献对照包含1000维、117个来源，但不会因此自动填入等级、日期或分数。正式记录应限定系统、时间和场景；可在`notes`注明相关研究来源编号（例如`D08-S10`），以维度ID与文献对照关联。未经核实的发布日期仍未知，不能改填报告截止日；没有直接证据也不能为了通过校验改作E0。

文献对照的四类证据相关性不等于E0—E5，更不等于0—5分。正式评分应由研究者按工作规范及可比实验条件逐项确认；避免把不同设备、工厂、版本及时间边界混成一个实证系统。

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

0是真实已填写分值；未知是`null`。H的零分母或单调性异常均给出未知及原因，不夹取成看似有效的数值。序数差和比值不具备已校准的物理量含义；正式C/H估计仍属于后续研究。

默认基线年2026、截止日2026-11-02；其他年份或晚于截止日的记录会失败。评分器可指定`--year`与`--as-of`，本轮工程网页仅接受2026版。完整年度迁移仍需独立版本规划。

## 依赖边与瓶颈

`dependencies.csv`字段为：

```text
dependency_id,consumer_subsystem_id,upstream_subsystem_id,dependency_type,critical,verification_status,evidence_refs,substitutes,notes
```

- 边方向为使用方→上游。类型包括energy、material、component、software、maintenance、logistics。
- `critical`为Yes/No/Unknown；`verification_status`为structural_hypothesis或verified。verified要求来源引用，但校验器不替代领域审查。
- 初始20条全部为带路线条件的结构假设，关键性Unknown，无已验证边。来源于本体结构的判断不冒充实证依赖。
- 分别输出结构假设图、声明验证图、上下游可达范围和强连通分量。工业循环依赖合法，不要求图是DAG。
- `weakest_nodes`只列完整HR0子系统的序数低分；`highest_human_dependence`只在完整HR100/HR0成对且满足分母与单调性条件时输出序数代理。
- 瓶颈候选要求完整评分及声明验证的关键边。`critical_path_minimum_score`仅在这些关键边的全部端点具备HR0分数时取局部最小值；它不代表全工业系统关键路径或完整依赖图。
- 图节点的单点故障保持Unknown。正式证据中明确填报的Yes断言另列为`evidence_reported_single_points_of_failure`，保留记录、场景、等级、来源和推断说明；它不等于工具独立验证。No不会被外推为不存在单点故障。

## 可追溯、报告与持续更新

评分记录正式证据、本体和指标的SHA-256；依赖分析记录依赖CSV、评分和本体指纹。工程网页核对这些输入，拒绝混用旧分析与更新后的数据。文献报告保留来源、访问日期和短摘录；默认离线重建，持有本地完整缓存时可加`--verify-cache`核查摘录。完整抓取缓存不入库。

GitHub Actions执行标准库测试和一键流程，并检查人工输入未被流水线改写。测试中的合成分数只存在于临时副本，不进入真实2026证据表。

提交采用任务分支与可审阅PR，在描述中关联现有Issue。工程机制、研究文献输入、专家确认和正式年度评分分别报告；只完成部分目标时不自动关闭总Issue。许可证、正式发布、DOI、校准评分及全面验证依赖仍需对应任务继续推进。
