# MCAB — Machine Civilization Autonomy Benchmark

> **A public benchmark for measuring how far AI–robotics–industrial systems can continue operating, repairing, expanding, and reproducing as human support is progressively removed.**
>
> 机器文明自主性基准：测试逐步移除人类后，AI—机器人—工业系统还能否持续运行、修复、扩容、复制并继续发展。

## Why MCAB?

Most AI benchmarks measure intelligence, coding, reasoning, tool use, agent performance, or digital self-replication. MCAB asks a different systems-level question:

**How dependent is a machine civilization on human civilization?**

The project studies the full dependency chain from AI and software to energy, mining, materials, manufacturing, semiconductors, robotics, logistics, economic coordination, maintenance, recovery, and physical reproduction.

MCAB is intended to be an open, evidence-backed, annually updated research benchmark. Contributions from AI researchers, roboticists, industrial engineers, semiconductor experts, energy researchers, economists, systems researchers, and other domain specialists are welcome.

## 核心问题

MCAB 不问“AI 有多聪明”，而问一个更严格的反事实问题：

**如果逐步把人类从技术文明中移除，机器系统还能维持多少功能、多久不崩、能否自主恢复、能否扩张、能否制造下一代自己？**

这个框架把今天彼此分散的研究方向连接起来：

- AI 自主复制 / RepliBench
- AI 研发自动化与递归改进
- 自主机器人、自修复与 Robot Metabolism
- 自动化工厂与工业闭环（closure）
- 能源、矿业、材料和物流自治
- 半导体与计算硬件闭环
- Machine Economy / 机器之间的资源配置
- Self-replicating / seed factory
- 太空 ISRU 与机器文明扩张

## 主轴：宿主依赖 → 自主复制

今天的 AI 主要寄宿在人类工业文明之上。MCAB 测量它何时从“依赖宿主”转向“能够完成完整代谢和复制周期”。

统一自主等级：

- **H5 / 0分 — 完全寄宿**：关键操作必须依赖人类。
- **H4 / 1分 — 自动运行**：可自动运行，但异常与维护依赖人类。
- **H3 / 2分 — 局部自治**：能诊断并处理一部分故障，仍依赖关键外部输入。
- **H2 / 3分 — 高度自治**：多数维护、输入和扩容可自主完成。
- **H1 / 4分 — 近乎独立**：仅少量关键环节仍需人类文明供应。
- **H0 / 5分 — 宿主独立**：长期无人条件下可运行、恢复、扩容和复制。

## 1000维结构

MCAB v0.1 = **10个文明系统 × 10个子系统 × 10个自主性指标 = 1000个维度**。

十个文明系统：

1. 智能、认知与自主治理
2. 软件与计算基础设施
3. AI研发与模型迭代
4. 能源系统
5. 原材料、化工与资源循环
6. 制造业与资本设备
7. 半导体与计算硬件
8. 机器人、运输与物流
9. 机器经济与资源配置
10. 复制、扩张与文明连续性

十个统一指标：

1. 无人运行能力
2. 故障发现能力
3. 自主诊断能力
4. 自主维修能力
5. 关键输入自主度
6. 能源自主度
7. 知识与信息自主度
8. 灾难恢复与韧性
9. 扩容能力
10. 复制闭环能力

## 四个总指标

MCAB 不采用“1000项简单平均分”作为最终答案。关键路径系统会被最弱环节卡住，因此最终至少同时报告四个指标：

### 1. Closure — 工业闭环度 C
机器系统能够自主提供全部关键投入的程度，特别关注不可替代的关键路径。

### 2. Human Dependence — 人类依赖 H
H 越高，人类从系统中撤场造成的性能损失越大。理想独立状态趋近 H = 0。

### 3. Machine Reproduction Number — 机器复制数 R_M
一套完整机器工业系统在生命周期中，平均能成功建立多少套具有同等能力的后代系统。

- R_M < 1：长期衰亡
- R_M = 1：理论维持
- R_M > 1：具备统计意义上的自扩张能力

### 4. Human-free Growth Rate — 无人增长率 g_0
在无人类参与条件下，机器资本、生产能力或有效算力的长期净增长率。

真正的文明自主门槛可粗略写作：

**C → 1，H → 0，R_M > 1，g_0 > 0。**

## 方法原则

- **不做简单平均**：关键路径优先于总体平均。
- **区分自动运行与自我维持**：自动化不等于维修、扩容或复制。
- **区分数字复制与物理复制**：复制模型权重远低于复制电力—矿业—芯片—机器人全链条的难度。
- **证据优先**：每个评分必须标明公开证据、日期、来源类型与置信度。
- **时间序列**：目标不是预测某一个“AGI日期”，而是逐年更新 MCAB-2026、MCAB-2027……观察哪个环节成为最后的人类脐带。
- **双世界比较**：同时比较 AI-with-humans 与 AI-without-humans 两条能力/增长曲线，寻找自主性反转点。

## How to contribute

MCAB is designed as a community research project. Useful contributions include:

- primary-source evidence for any subsystem;
- corrections to the ontology or dependency graph;
- domain-expert review of scores and assumptions;
- reproducible code, tests, visualizations, and simulations;
- yearly updates and historical backfills;
- translations and clearer documentation.

Please read `CONTRIBUTING.md` before opening a pull request. Evidence-backed corrections are preferred over unsupported estimates.

## 当前阶段

v0.1 先完成：

1. 固定100个子系统本体（ontology）；
2. 自动生成1000维指标表；
3. 建立评分与证据规范；
4. 建立2026基线；
5. 识别最弱关键路径；
6. 后续加入年度数据与情景模拟。

详细定义见 `docs/MCAB-v0.1.md`，本体见 `data/taxonomy.csv`，1000维表由 `scripts/generate_dimensions.py` 生成。
