# GitHub Issue与当前交付

核对日期：2026-11-02（Asia/Shanghai）。[项目仓库](https://github.com/Amosqiang/Machine-Civilization-Autonomy)的既有Issue是任务主线；最终状态以相应PR、提交和审阅记录为准。

首次核对时有13个开放Issue、没有PR，main为7f80078。本轮在任务分支`codex/mcab-2026-evidence-engineering`保留既有成果，接续工程机制及文献对照。以下是当前分支的交付，不代表已合入main或完成科学验证。

## #2：工程交付主线

[Issue #2](https://github.com/Amosqiang/Machine-Civilization-Autonomy/issues/2)的原评论要求保留已有工作、完成工程余项并形成可审阅PR。

| 原交付项 | 当前分支实现 | 尚需研究与审阅 |
| --- | --- | --- |
| 1. 生成1000维 | 完整工作表、默认覆盖保护、原子写入 | 本体专家审定与变更迁移 |
| 2. 结构与ID校验 | 本体、指标、维度、正式证据与研究JSON校验 | 来源适用性与评分合理性 |
| 3. 正式证据CSV | data/evidence_2026.csv，23字段、初始仅表头 | 分场景实证及人工评分 |
| 4. 评分引擎 | 保守最小值、冲突与完整性规则、明示C/H序数代理 | 领域校准、实测C/H；R_M与g₀未知 |
| 5. 依赖边契约 | data/dependencies.csv，20条路线相关结构假设 | 验证边、关键性、替代及恢复证据 |
| 6. 分析工具 | 完整HR0低分、成对场景代理、关键子图候选、来源报告SPOF断言 | 不推断初始图的真实全系统瓶颈或单点故障 |
| 7. CSV驱动报告 | 工程网页，另保留1000维文献报告 | 空证据表显示未知，不是正式评分基线 |
| 8. 测试与复现 | 一键流水线、标准库测试、开发说明及GitHub Actions | PR审阅及GitHub运行结果 |

命令、公式、完整性门槛和数据流见[开发说明](DEVELOPMENT.md)。关键标签集合最小值与声明验证子图的局部最低分分别输出；两者都不能冒充全工业系统关键路径。工程机制可审阅交付不等于#1的实证基线完成。#2保留至PR审阅验收。

## #1：年度研究基线

[Issue #1](https://github.com/Amosqiang/Machine-Civilization-Autonomy/issues/1)已有1000维逐项目标/当前/差距对照及117个已读取来源。47项直接相关、214项部分相关、526项仅背景、213项无直接证据；相关性不是自主性评分。

正式证据CSV当前没有记录，1000维工作表没有实证分数。五场景资料、E0—E5、评分校准、验证依赖图、瓶颈排名及C/H/R_M/g₀实测估计仍待完成，因此不关闭#1。

原Issue截止日2026-10-31，本次“当前最新”对照按用户要求采用2026-11-02。需要区分冻结基线与滚动对照；未核实发布日期的当前文档不能自动回填为10月31日已知证据。

## #4—#13：十领域评审输入


| Issue | 领域 | 本地研究文件 | 维度数 | 直接 / 部分 / 背景 / 无直接证据 | 引用来源数 | 建议状态 |
| --- | --- | --- | ---: | --- | ---: | --- |
| [#4](https://github.com/Amosqiang/Machine-Civilization-Autonomy/issues/4) | 1. 智能、认知与自主治理 | [`domains_01_03.json`](../data/research/2026/domains_01_03.json) | 100 | 4 / 28 / 23 / 45 | 13 | 文献输入已有本地草稿，等待领域评审 |
| [#5](https://github.com/Amosqiang/Machine-Civilization-Autonomy/issues/5) | 2. 软件与计算基础设施 | [`domains_02_09.json`](../data/research/2026/domains_02_09.json) | 100 | 9 / 27 / 64 / 0 | 12 | 文献输入已有本地草稿，等待领域评审 |
| [#6](https://github.com/Amosqiang/Machine-Civilization-Autonomy/issues/6) | 3. AI研发与模型迭代 | [`domains_01_03.json`](../data/research/2026/domains_01_03.json) | 100 | 9 / 35 / 25 / 31 | 17 | 文献输入已有本地草稿，等待领域评审 |
| [#7](https://github.com/Amosqiang/Machine-Civilization-Autonomy/issues/7) | 4. 能源系统 | [`domains_04_05.json`](../data/research/2026/domains_04_05.json) | 100 | 6 / 13 / 81 / 0 | 15 | 文献输入已有本地草稿，等待领域评审 |
| [#8](https://github.com/Amosqiang/Machine-Civilization-Autonomy/issues/8) | 5. 原材料、化工与资源循环 | [`domains_04_05.json`](../data/research/2026/domains_04_05.json) | 100 | 3 / 18 / 79 / 0 | 14 | 文献输入已有本地草稿，等待领域评审 |
| [#9](https://github.com/Amosqiang/Machine-Civilization-Autonomy/issues/9) | 6. 制造业与资本设备 | [`domains_06_07.json`](../data/research/2026/domains_06_07.json) | 100 | 5 / 14 / 9 / 72 | 12 | 文献输入已有本地草稿，等待领域评审 |
| [#10](https://github.com/Amosqiang/Machine-Civilization-Autonomy/issues/10) | 7. 半导体与计算硬件 | [`domains_06_07.json`](../data/research/2026/domains_06_07.json) | 100 | 0 / 21 / 14 / 65 | 13 | 文献输入已有本地草稿，等待领域评审 |
| [#11](https://github.com/Amosqiang/Machine-Civilization-Autonomy/issues/11) | 8. 机器人、运输与物流 | [`domains_08_10.json`](../data/research/2026/domains_08_10.json) | 100 | 7 / 20 / 73 / 0 | 12 | 文献输入已有本地草稿，等待领域评审 |
| [#12](https://github.com/Amosqiang/Machine-Civilization-Autonomy/issues/12) | 9. 机器经济与资源配置 | [`domains_02_09.json`](../data/research/2026/domains_02_09.json) | 100 | 3 / 21 / 76 / 0 | 15 | 文献输入已有本地草稿，等待领域评审 |
| [#13](https://github.com/Amosqiang/Machine-Civilization-Autonomy/issues/13) | 10. 复制、扩张与文明连续性 | [`domains_08_10.json`](../data/research/2026/domains_08_10.json) | 100 | 1 / 17 / 82 / 0 | 11 | 文献输入已有本地草稿，等待领域评审 |

来源数按各领域实际引用的编号统计，跨领域可能复用；表中对应关系仅表示来源适用性，不表示能力达标。所有领域仍需专家检查本体完整性、指标阈值、人类角色、来源外推、替代路径和评分输入。

## #3：公开协作与发布

[Issue #3](https://github.com/Amosqiang/Machine-Civilization-Autonomy/issues/3)可接收本轮方法、机器可读资料、报告及CI进展。首次核对时description为for up、topics为空、Discussions未开启，许可证未明确。

仓库展示、分支草稿和可审阅PR，与正式基线、版本发布、DOI、预印本及推广分别跟踪。许可证仍需明确代码和数据范围，外部短引文不被视为项目可任意再授权的材料。当前未正式合并或发布，#3保持开放。

## 下一轮优先级

1. 审阅本轮工程PR与CI；以PR和提交链接回填现有Issue进度。
2. 从47项直接及214项部分相关资料核验系统、执行主体、日期与边界，形成正式分场景证据；缺资料时保持未知。
3. 优先补查维修、关键输入、供能、扩容和复制，验证依赖及替代路线。
4. 经领域审阅后校准评分；不以序数工程代理替代实测总指标。
5. 保持滚动文献更新和清楚的版次/截止日，再推进许可证、正式版本和归档任务。
