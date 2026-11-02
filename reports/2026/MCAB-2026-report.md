# MCAB-2026：工业自我复制的理想要求与当前能力

证据与检索截至：**2026-11-02**。覆盖 **1000** 个维度，登记 **117** 项来源记录、**117** 个唯一URL。

[完整逐维附录](MCAB-2026-dimensions.md) · [交互浏览](MCAB-2026-latest.html) · [CSV](MCAB-2026-dimension-comparison.csv)

本版逐项列出目标能力、当前公开证据、差距、人类依赖和拟议验证要求。完整1000维对照不代表1000项均已获得直接实证。

## 本轮证据状态

| 状态 | 维度数 |
| --- | ---: |
| 限定条件下已有演示 | 35 |
| 部分相关证据 | 226 |
| 本轮检索未确立 | 387 |
| 未知 | 352 |

## 证据与指标对应关系

| 对应关系 | 维度数 |
| --- | ---: |
| 直接对应指标 | 47 |
| 部分对应指标 | 214 |
| 仅提供背景 | 526 |
| 无直接证据 | 213 |

这些是本轮检索证据状态及相关性计数，不是工业闭环比例、达标率或自主性评分。直接相关不代表完整目标达成。

## 分析性综合：当前走到哪一步

以下为基于已核查来源的分析判断，不是额外测量结果或已验证依赖图排名。

这份报告已为10个领域、100个子系统的全部1000个既定维度建立逐项对照。它呈现的是当前公开资料支持的局部能力及验证缺口：AI任务执行、软件恢复、工艺控制、机器人操作和机器交易已有多种进展；本轮检索尚未建立一套在移除人类及人类供应链后，能够自行维持能源、制造关键投入、维修资本设备，并建立具有同等持续生产能力的后代工业系统的完整实证。这个结论是本轮证据范围内的综合判断，不是对技术不可能性的证明，也不是把1000项当作共同必要且充分的复制条件。

### 智能与AI研发：任务持续时间和实验自动化取得进展，长期自主研发闭环仍需单独验证

2026年的长程任务评测、模型技术说明、自动研究与NanoGPT优化研究提供了比旧有演示更具体的证据。评价这些结果时，需要分别记录任务由谁设定、资源由谁提供、错误由机器还是人工复核，以及改进是否能持续进入下一轮。完成受限软件任务或一次模型优化，并不直接验证无人治理、实物扩容或代际工业复制。

来源：[D01-S02](https://epoch.ai/publications/mirrorcode-preliminary-results)、[D01-S10](https://openai.com/index/introducing-gpt-6-1-sol/)、[D01-S11](https://openai.com/index/gpt-6-astra/)、[D03-S06](https://www.anthropic.com/research/automated-researchers-mitigate-alignment-failures)、[D03-S07](https://metr.org/blog/2026-07-21-expenditure-horizon/)

### 软件基础设施：自动重启、重调度与恢复可以复用，硬件与供能仍是另一个层次

Kubernetes、Ceph和PyTorch文档记录了服务重启、故障检查、数据恢复及弹性训练等机制。它们直接或部分对应若干软件指标；自主制造服务器、更换损坏存储介质、修复机房供电和建立新设施，需要额外的物理证据。云接口可用或集群可扩配，不能代替关键输入自主供给的验证。

来源：[D02-S01](https://kubernetes.io/docs/concepts/architecture/self-healing/)、[D02-S03](https://docs.ceph.com/en/latest/rados/operations/health-checks/)、[D02-S06](https://docs.pytorch.org/docs/2.15/elastic/run.html)、[D02-S10](https://cluster-api.sigs.k8s.io/user/concepts.html)

### 能源：电网自治与黑启动研究有依据，设备生命周期闭环尚待建立

NLR的自主能源、REORG现场研究及可再生能源黑启动综述支持研究局部调度和恢复能力。应把已测试的网络、能源来源、人工准备与故障范围写清楚，再分别检查燃料或发电设备供给、逆变器和变压器维修、备件生产以及新增设施建设。选用太阳能、风能或其他路线会改变必须闭环的节点。

来源：[D04-S01](https://www.nlr.gov/grid/autonomous-energy)、[D04-S03](https://www.nlr.gov/grid/black-start)、[D04-S04](https://www.nlr.gov/news/detail/program/2026/as-local-power-grows-utilities-reorganize-for-resilience)、[D04-S09](https://www.nature.com/articles/s41467-026-76692-0)

### 材料与化工：自主实验和过程控制不能外推为全材料链自给

2026年的Polybot聚合物合成报道和工业自主控制回顾提供了具体案例；矿业官方资料也记录了生产项目与故障恢复的现实条件。下一步需要把勘探、开采、精炼、高纯化学品、水处理、回收和设备维修逐段相连，检查各段是否依赖人工提供的试剂、耗材、维护和物流。单个实验室或控制回路的自动化，不能覆盖其他材料指标。

来源：[D05-S06](https://www.yokogawa.com/special/planet/stories/boosting_industrial_autonomy_with_AI/)、[D05-S07](https://www.anl.gov/cnm/article/aipowered-autonomous-electronic-polymer-synthesis)、[D05-S11](https://www.riotinto.com/en/news/releases/2026/rio-tinto-celebrates-opening-of-1-4-billion-lithium-projects-in-argentina)、[D05-S12](https://www.riotinto.com/en/news/releases/2026/update-on-oyu-tolgoi-seismic-event)

### 制造与半导体：产线自动化和辅助维护的边界必须保留

加工、焊接、装配和设备监测已有商业产品及运行资料。Lam关于Dextro的官方说明明确写到由晶圆厂技术人员或工程师操作；此类能力可以减少人工步骤，但不能计为无人自主维修。半导体工艺还需要检验设备、材料、计量与维护的供给链。先进光刻、HBM和特定制程是否必要，应由所选后代系统的性能要求决定。

来源：[D06-S01](https://en.dmgmori.com/products/automation)、[D06-S04](https://www.fanucamerica.com/applications/arc-welding)、[D06-S10](https://www.abb.com/global/en/areas/robotics/industries/automotive)、[D07-S10](https://www.lamresearch.com/product/dextro/)、[D07-S11](https://investor.lamresearch.com/2024-12-10-Lam-Research-Introduces-the-Semiconductor-Industrys-First-Collaborative-Robot-for-Fab-Maintenance-Optimization)、[D07-S13](https://news.skhynix.com/en/2026-partners-day-japan/)

### 机器人：参与加工自身零件是有价值的局部进展，预制模块组装的人工控制仍需披露

PI在2026年API测试报道中展示了机器人加工用于其自身装配的隔套，证据范围限于相关加工任务和外部提供的系统条件。Robot Metabolism论文全文的方法部分则说明实体Truss Link实验由操作者通过键盘控制。两者都不能直接支持从矿物、能源、驱动器和计算硬件到完整后代机器人的无人闭环主张。

来源：[D08-S10](https://www.pi.website/blog/api-beta)、[D08-S05](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12266095/fullTextXML)

### 机器经济：自动支付与规则执行已有工具，独立工业经济的实物履约仍需检验

2026年BIS、英格兰银行、Mastercard与机器支付相关资料表明，支付接口、授权、结算和代理交易正继续发展。Agorá等试验同时记录了金融机构和人员参与。应分别验证机器是否自主作出采购决策、交易标的是否由机器生产、交付是否真实完成，以及异常和争议由谁处理；交易笔数本身不能回答这些问题。

来源：[D09-S06](https://www.bis.org/project/agora)、[D09-S14](https://www.bis.org/speeches/20261005-payments-age-ai-agents)、[D09-S15](https://www.bankofengland.co.uk/speech/2026/june/sarah-breeden-panel-at-the-european-central-bank-forum-on-central-banking-2026)、[D09-S17](https://www.mastercard.com/global/en/news-and-trends/press/2026/june/mastercard-launches-agent-pay-for-machines.html)、[D09-S18](https://www.chainalysis.com/blog/x402-agentic-payments-adoption/)

### 完整复制与连续性：需要把资源利用、设施复制及后代持续运行放进同一次验证

NASA的原位资源利用、机器人结构装配和种子工厂研究分别提供了资源转换、模块组装或系统设计依据。报告将它们保留在各自的验证范围内。要确认完整复制，需要声明系统边界和初始库存，完成后代系统的生产与投运，并在撤去人类服务后继续检验其维护、补给和下一代复制能力；本轮资料尚未建立这条整体证据链。

来源：[D10-S01](https://www.nasa.gov/missions/mars-2020-perseverance/nasas-oxygen-generating-experiment-moxie-completes-mars-mission/)、[D10-S02](https://www.nasa.gov/general/robot-team-builds-high-performance-digital-structure-for-nasa/)、[D10-S04](https://ntrs.nasa.gov/citations/19830007077)、[D10-S05](https://ntrs.nasa.gov/citations/20250008988)、[D10-S06](https://www.creativemachineslab.com/self-replication.html)

### 接下来需要验证什么

1. 先选定一套具体的可复制工业系统及性能目标，列出物料、设备、能源和服务清单，标明可替代路线与不适用维度。
2. 优先补查仅有背景或无直接证据的维度；对已有局部证据的维度补充任务边界、故障条件、观察时长和实际人类工时。
3. 建立带证据的依赖图，逐项区分库存延迟失效、可持续再生产、软件资源分配和新增实物产能。
4. 邀请领域专家逐条复核目标要求及来源适用性，再制定指标专属评分阈值；在此之前不生成看似精确的总体自主性分数。
5. 通过受控的人类撤场试验和后代系统持续运行试验验证闭环，再估计C、H、R_M和g₀的区间；缺少数据时继续报告未知。

## 十个文明系统

### 1. 智能、认知与自主治理

截至2026-11-02核验到10月29日论文：代理编程、复杂工作流、跨上下文状态和多代理协调进步明显；WMEval用仿真状态检验物理因果一致性，FutureWorld报告视频世界误差控制进展。证据仍多处于给定任务、仿真和外部工业供给条件，不能拼接为工业HR0。

**最强进展：** 2026 MirrorCode复杂软件自主重实现；Astra可检索旧上下文；Sol多工具工作流；监控与人类判断影响已有现实研究。

**主要缺口：** 局部数字代理能力不能拼接成有供能、硬件、现场执行和跨代连续性的HR0工业控制体系。

本轮状态：限定条件下已有演示 4项；部分相关证据 28项；本轮检索未确立 23项；未知 45项。

来源：[D01-S01](https://metr.org/time-horizons/)、[D01-S02](https://epoch.ai/publications/mirrorcode-preliminary-results)、[D01-S03](https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/)、[D01-S04](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/index.html)、[D01-S05](https://www.anthropic.com/research/building-effective-agents)、[D01-S06](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)、[D01-S07](https://arxiv.org/abs/2305.16291)、[D01-S08](https://metr.org/blog/2026-01-19-early-work-on-monitorability-evaluations/)、[D01-S09](https://www.anthropic.com/research/agents-judgment-calls)、[D01-S10](https://openai.com/index/introducing-gpt-6-1-sol/)、[D01-S11](https://openai.com/index/gpt-6-astra/)、[D01-S12](https://arxiv.org/abs/2610.33894)、[D01-S13](https://arxiv.org/abs/2610.39619)

### 2. 软件与计算基础设施

软件基础设施已具备丰富的声明式控制、容器自愈、存储健康检查、弹性训练、自动证书续期与模型服务功能；这些多为现有硬件上的逻辑自治。AIOpsLab已把故障检测、定位、分析和缓解转成可评估任务，但论文也明确研究代理能力与局限。本次未建立从硬件生产、能源供给到未知故障修复的端到端HR0闭环。

**最强进展：** Kubernetes故障重启和重调度、KServe自动扩缩容、torchrun基于检查点恢复、cert-manager证书续期。

**主要缺口：** 云API分配的资源不等于机器自制物理节点；供电、冷却、半导体与存储设备替换、信任根及开放式运维诊断仍缺乏独立闭环验证。

本轮状态：限定条件下已有演示 0项；部分相关证据 36项；本轮检索未确立 64项；未知 0项。

来源：[D02-S01](https://kubernetes.io/docs/concepts/architecture/self-healing/)、[D02-S02](https://kubernetes.io/docs/concepts/services-networking/)、[D02-S03](https://docs.ceph.com/en/latest/rados/operations/health-checks/)、[D02-S04](https://kubernetes.io/docs/concepts/scheduling-eviction/kube-scheduler/)、[D02-S05](https://kserve.github.io/website/docs/intro)、[D02-S06](https://docs.pytorch.org/docs/2.15/elastic/run.html)、[D02-S07](https://slsa.dev/spec/v1.1/levels)、[D02-S08](https://cert-manager.io/docs/usage/certificate/)、[D02-S09](https://raw.githubusercontent.com/microsoft/AIOpsLab/main/README.md)、[D02-S10](https://cluster-api.sigs.k8s.io/user/concepts.html)、[D02-S12](https://docs.siderolabs.com/talos/v1.14/overview/what-is-talos)、[D02-S13](https://arxiv.org/abs/2501.06706)

### 3. AI研发与模型迭代

截至2026-11-02核验到10月SplatLab与Autonomous Science Bench摘要，支持受限领域内选实验、复现基线、改算法、训练和追溯报告的新进展；2026对齐研究也有自动方法改进。但实验室服务、GPU、评测框架与研究价值判断仍有外部支持；人工复测不算代理自主诊断。

**最强进展：** 2026-10受限科研流程与预算实验决策、8月自动对齐循环、经人工复测的NanoGPT优化，以及报告可由Lean检查的大型形式化成果。

**主要缺口：** 尚未证明研究链能持续自主补充物理投入，并把跨轮创新稳定转成后代工业体系的净增长。

本轮状态：限定条件下已有演示 9项；部分相关证据 35项；本轮检索未确立 25项；未知 31项。

来源：[D01-S01](https://metr.org/time-horizons/)、[D01-S02](https://epoch.ai/publications/mirrorcode-preliminary-results)、[D01-S08](https://metr.org/blog/2026-01-19-early-work-on-monitorability-evaluations/)、[D01-S10](https://openai.com/index/introducing-gpt-6-1-sol/)、[D01-S11](https://openai.com/index/gpt-6-astra/)、[D01-S12](https://arxiv.org/abs/2610.33894)、[D03-S01](https://arxiv.org/abs/2504.08066)、[D03-S02](https://arxiv.org/abs/2505.18705)、[D03-S03](https://arxiv.org/abs/2504.01848)、[D03-S04](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/)、[D03-S05](https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/)、[D03-S06](https://www.anthropic.com/research/automated-researchers-mitigate-alignment-failures)、[D03-S07](https://metr.org/blog/2026-07-21-expenditure-horizon/)、[D03-S08](https://www.anthropic.com/research/claude-shaped-science)、[D03-S09](https://www.anthropic.com/research/formalizing-fermats-last-theorem)、[D03-S10](https://arxiv.org/abs/2610.30468)、[D03-S11](https://arxiv.org/abs/2610.18449)

### 4. 能源系统

能源领域已能在特定场景自动优化、控制和恢复配电供给。2026 REORG现场验证及黑启动综述表明控制层和局部韧性取得进展，但功率设备制造、线路实体修复、燃料与备件供给、工程建设尚无本轮可核验的整链HR0证明。

**最强进展：** 预装分布式资源的供需协调、配电成岛和失网恢复；特定工业气体单元自主控制。

**主要缺口：** 从算法控制跨到发电—输配电—维修—新设施施工及关键材料/器件自供，尤其不能把遥控机器人维修或2029投运计划记成当前自主复制。

本轮状态：限定条件下已有演示 6项；部分相关证据 13项；本轮检索未确立 81项；未知 0项。

来源：[D04-S01](https://www.nlr.gov/grid/autonomous-energy)、[D04-S02](https://www.nlr.gov/grid/solar-wind-forecasting)、[D04-S03](https://www.nlr.gov/grid/black-start)、[D04-S04](https://www.nlr.gov/news/detail/program/2026/as-local-power-grows-utilities-reorganize-for-resilience)、[D04-S05](https://www.pnnl.gov/energy-storage)、[D04-S06](https://www.japan.go.jp/kizuna/2025/08/robots_ai_wind_turbine_maintenance.html)、[D04-S07](https://www.yokogawa.com/us/news/press-releases/2025/2025-10-29)、[D04-S08](https://www.nlr.gov/grid/grid-forming-inverter-controls)、[D04-S09](https://www.nature.com/articles/s41467-026-76692-0)、[D04-S10](https://www.yokogawa.com/eu/news/press-releases/2026/2026-02-10/)、[D04-S11](https://www.yokogawa.com/eu/news/press-releases/2026/2026-03-05/)、[D05-S01](https://koboldmetals.com/science/)、[D05-S06](https://www.yokogawa.com/special/planet/stories/boosting_industrial_autonomy_with_AI/)、[D05-S11](https://www.riotinto.com/en/news/releases/2026/rio-tinto-celebrates-opening-of-1-4-billion-lithium-projects-in-argentina)、[D05-S13](https://www.ornl.gov/brace/)

### 5. 原材料、化工与资源循环

采运、选冶过程控制、高纯硅生产及特定材料合成存在自动化或局部自治。2026 Polybot和横河文章提供新的公开记录，2026锂项目与矿区事故公告同时显示现实产业仍由人员、供应商及安全审查组织支撑。

**最强进展：** 特定化工控制回路、实验室聚合物逆向设计合成、矿山部分运输钻孔及机器人电池拆解。

**主要缺口：** 原矿到高纯电子材料与全品类化学品的可持续供料、设备自主维修、污染控制、灾后复产和多代回收—再制造链；尤其光刻胶/电子特气无人闭环本轮仍缺直接证据。

本轮状态：限定条件下已有演示 3项；部分相关证据 18项；本轮检索未确立 79项；未知 0项。

来源：[D04-S07](https://www.yokogawa.com/us/news/press-releases/2025/2025-10-29)、[D05-S01](https://koboldmetals.com/science/)、[D05-S02](https://www.riotinto.com/en/about/innovation)、[D05-S03](https://www.metso.com/portfolio/advanced-process-control/)、[D05-S04](https://www.metso.com/products-and-services/digitalization/digital-solutions-for-metals-refining/)、[D05-S05](https://www.wacker.com/cms/en-us/press-and-media/press/press-releases/2025/press-releases-detail-2025-257922.html)、[D05-S06](https://www.yokogawa.com/special/planet/stories/boosting_industrial_autonomy_with_AI/)、[D05-S07](https://www.anl.gov/cnm/article/aipowered-autonomous-electronic-polymer-synthesis)、[D05-S08](https://www.veoliawatertechnologies.com/en/hubgrade-digital-solutions)、[D05-S09](https://www.ornl.gov/news/automated-disassembly-line-aims-make-battery-recycling-safer-faster/)、[D05-S10](https://www.nature.com/articles/s41586-023-06734-w)、[D05-S11](https://www.riotinto.com/en/news/releases/2026/rio-tinto-celebrates-opening-of-1-4-billion-lithium-projects-in-argentina)、[D05-S12](https://www.riotinto.com/en/news/releases/2026/update-on-oyu-tolgoi-seismic-event)、[D05-S13](https://www.ornl.gov/brace/)

### 6. 制造业与资本设备

已核验资料显示加工、焊接、绕线、装配和测量存在成熟的限定工位自动化；2026年GROB展示柔性机器人单元与生产流监控，SKF新增陶瓷工艺研发整合。多数证据来自OEM产品页或公司新闻，缺少完全去除人类后的生命周期试验。

**最强进展：** 已设置工艺下的自动重复生产、机内测量、装配检测与数字化设计监控。

**主要缺口：** 刀具/母机/精密传动和电子控制等上游制造，设备物理修复、工艺专家替代、能源厂务以及无人建厂；工厂会生产产品不同于工厂会复制自身。

本轮状态：限定条件下已有演示 5项；部分相关证据 14项；本轮检索未确立 9项；未知 72项。

来源：[D06-S01](https://en.dmgmori.com/products/automation)、[D06-S02](https://www.fanucamerica.com/industries/die-cast-foundry-mold)、[D06-S03](https://www.eos.info/metal-solutions/metal-printers)、[D06-S04](https://www.fanucamerica.com/applications/arc-welding)、[D06-S05](https://www.grobgroup.com/en/products/product-range/electromobility/)、[D06-S06](https://www.grobgroup.com/en/products/product-range/winding-and-inserting-technology/)、[D06-S07](https://news.cision.com/skf/r/skf-accelerates-hybrid-bearing-leadership-with-new-ceramic-process-laboratory,c4411601)、[D06-S08](https://www.renishaw.com/en/machine-tool-probes--6073)、[D06-S09](https://www.grobgroup.com/en/news-media/detail/article/grob-showcases-the-future-of-manufacturing-at-amb-2026/)、[D06-S10](https://www.abb.com/global/en/areas/robotics/industries/automotive)、[D06-S11](https://www.siemens.com/global/en/products/software/digital-twin.html)、[D07-S09](https://blogs.nvidia.com/blog/nvidia-manufacture-american-made-ai-supercomputers-us/)

### 7. 半导体与计算硬件

TSMC当前页面确认N2于2025Q4、N3C于2026量产；SK hynix2026年10月公告HBM4出货。先进工艺、检测计量与部分机器人维护均有现实产品证据，但供应商协作和人员维护并未消除。

**最强进展：** 纳米级工艺控制、自动检测和数据分析，以及Dextro对特定刻蚀维护任务的精密自动化。

**主要缺口：** Dextro官方资料仍明确由工程师或技术员操作；高纯材料、光刻/沉积/刻蚀工具、计量基准、能源与整厂重建的HR0链未证实。尖端节点/HBM是所选架构条件，不能当作所有自复制路线的必要前提。

本轮状态：限定条件下已有演示 0项；部分相关证据 21项；本轮检索未确立 14项；未知 65项。

来源：[D07-S01](https://www.siltronic.com/en/products.html)、[D07-S02](https://www.asml.com/en/technology/lithography-principles)、[D07-S03](https://www.lamresearch.com/products/our-products/)、[D07-S04](https://www.appliedmaterials.com/us/en/semiconductor/products.html)、[D07-S05](https://www.kla.com/products)、[D07-S06](https://www.tsmc.com/english/dedicatedFoundry/technology/cowos)、[D07-S07](https://news.skhynix.com/en/q3-2026-business-results/)、[D07-S08](https://www.tsmc.com/english/dedicatedFoundry/technology/logic/l_2nm)、[D07-S09](https://blogs.nvidia.com/blog/nvidia-manufacture-american-made-ai-supercomputers-us/)、[D07-S10](https://www.lamresearch.com/product/dextro/)、[D07-S11](https://investor.lamresearch.com/2024-12-10-Lam-Research-Introduces-the-Semiconductor-Industrys-First-Collaborative-Robot-for-Fab-Maintenance-Optimization)、[D07-S12](https://blogs.sw.siemens.com/electronics-semiconductors/2026/08/13/ai-driven-predictive-maintenance-solving-semiconductor-fab-uptime-challenges/)、[D07-S13](https://news.skhynix.com/en/2026-partners-day-japan/)

### 8. 机器人、运输与物流

已核验资料显示限定场景自主移动、操作和物流已具有实验或商业部署证据；2026机器人基础模型进一步展示泛化、记忆和参与自身零件加工。故障适应与模块重构不能等同于完整物理维修，更不能消除芯片、电机、备件、能源和人类运营依赖。

**最强进展：** 2026-10-13 PI展示Axol为自身装配隔套去毛刺；π0.7(2026-04-16)展示组合泛化；Waymo截至2026-06报告2.713亿无驾驶员里程。

**主要缺口：** 从限定任务的无人执行，跨越到无人维修、部件制造、能源自供以及完整机器人和运输基础设施的再生产。

本轮状态：限定条件下已有演示 7项；部分相关证据 20项；本轮检索未确立 3项；未知 70项。

来源：[D08-S01](https://www.pi.website/blog/pi07)、[D08-S02](https://www.pi.website/research/memory)、[D08-S03](https://deepmind.google/models/gemini-robotics/)、[D08-S04](https://www.nature.com/articles/s44182-025-00031-6)、[D08-S05](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12266095/fullTextXML)、[D08-S06](https://www.aboutamazon.com/news/operations/amazon-million-robots-ai-foundation-model)、[D08-S07](https://waymo.com/safety/impact/)、[D08-S08](https://www.yara.com/knowledge-grows/yara-birkeland-two-years-on/)、[D08-S09](https://www.flyzipline.com/technology)、[D08-S10](https://www.pi.website/blog/api-beta)、[D08-S11](https://arxiv.org/abs/2609.26157)、[D10-S06](https://www.creativemachineslab.com/self-replication.html)

### 9. 机器经济与资源配置

预测、排程、库存补货、影子价格、链上治理和机器支付均有公开软件或真实试验进展。2026年资料显示Chronos云部署、x402实际链上活动、Mastercard机器支付服务发布，以及Agorá实值跨币种测试；它们不能直接拼接为无人机器经济。尤其Agorá明确保留人工合规、外汇确认和大量机构人员。

**最强进展：** 机器可通过x402程序化购买API资源；Agorá在2026年7月完成约80万瑞郎实值测试。对交易活动的统计不能等同于机器独立所有权、生产或再投资。

**主要缺口：** 资源和资本的真实生产、长期信用支撑、事故核赔、争议裁决和宏观稳定仍未获得HR0证据；程序化交易持续寄宿于人类货币、商家和工业体系。

本轮状态：限定条件下已有演示 0项；部分相关证据 24项；本轮检索未确立 76项；未知 0项。

来源：[D09-S01](https://raw.githubusercontent.com/amazon-science/chronos-forecasting/main/README.md)、[D09-S02](https://docs.scipy.org/doc/scipy/reference/optimize.linprog-highs.html)、[D09-S03](https://docs.x402.org/introduction)、[D09-S04](https://docs.openzeppelin.com/contracts/5.x/governance)、[D09-S05](https://developers.google.com/optimization/scheduling/job_shop)、[D09-S06](https://www.bis.org/project/agora)、[D09-S07](https://www.odoo.com/documentation/19.0/applications/inventory_and_mrp/purchase.html)、[D09-S08](https://www.odoo.com/documentation/19.0/applications/inventory_and_mrp/inventory/warehouses_storage/replenishment/reordering_rules.html)、[D09-S09](https://docs.nexusmutual.io/)、[D09-S10](https://www.bis.org/publications/aer-2025/next-generation-monetary-financial-system)、[D09-S12](https://arxiv.org/abs/2510.15821)、[D09-S14](https://www.bis.org/speeches/20261005-payments-age-ai-agents)、[D09-S15](https://www.bankofengland.co.uk/speech/2026/june/sarah-breeden-panel-at-the-european-central-bank-forum-on-central-banking-2026)、[D09-S17](https://www.mastercard.com/global/en/news-and-trends/press/2026/june/mastercard-launches-agent-pay-for-machines.html)、[D09-S18](https://www.chainalysis.com/blog/x402-agentic-payments-adoption/)

### 10. 复制、扩张与文明连续性

可核验进展主要是预制模块组装、局部机器人重构、原位制氧和空间资产服务；它们是完整自复制的组件技术，尚不足以据此给出文明闭环度、完整工业复制数或代际时间。

**最强进展：** MOXIE在火星16次制氧累计122g；ARMADAS在地面自主组装预制体素米尺度结构并纠错；模块机器人实现有外部积木补给的后代组装。

**主要缺口：** 缺少由闭环原料和能源供应支撑、能制造全部关键设备和下一代生产体系的多代工业运行验证；R_M和g_0必须保持未知。

本轮状态：限定条件下已有演示 1项；部分相关证据 17项；本轮检索未确立 13项；未知 69项。

来源：[D08-S01](https://www.pi.website/blog/pi07)、[D08-S02](https://www.pi.website/research/memory)、[D08-S04](https://www.nature.com/articles/s44182-025-00031-6)、[D08-S05](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12266095/fullTextXML)、[D08-S06](https://www.aboutamazon.com/news/operations/amazon-million-robots-ai-foundation-model)、[D10-S01](https://www.nasa.gov/missions/mars-2020-perseverance/nasas-oxygen-generating-experiment-moxie-completes-mars-mission/)、[D10-S02](https://www.nasa.gov/general/robot-team-builds-high-performance-digital-structure-for-nasa/)、[D10-S03](https://www.jpl.nasa.gov/missions/cadre/)、[D10-S04](https://ntrs.nasa.gov/citations/19830007077)、[D10-S05](https://ntrs.nasa.gov/citations/20250008988)、[D10-S06](https://www.creativemachineslab.com/self-replication.html)

## 方法与解释边界

本报告把工业自我复制所需的能力作为目标，与本轮检索到的公开证据逐维比较。required_capability与validation_needed是本研究拟议的操作性目标和验收要求，不是通用工业标准或独立发现的经验事实。目标是研究要求，不是已实现事实；“当前能力”仅代表来源在其特定系统、实验条件和时间范围内支持的内容。

1000维是现有本体的笛卡尔积覆盖，不是1000项独立研究，也不代表1000项能力是联合必要且充分条件。目标要求取决于所选工业系统设计与替代路线：太阳能与核能等能源路线可替代，信用、保险等经济机制也并非任何机器文明都必须采用。完整填表仅表示逐维作了对照，不表示能力已齐备或存在直接证据。

未知不等于0分；“本轮检索未确立”只表示尚未找到足够直接证据，不能推出技术不可能。限定条件下的演示不代表长期、全工况或跨系统闭环。数字复制、自动运行、实验室演示与物理工业再生产分别判断。不同公司的系统、不同年份的实验与不同环境中的成果，不能拼接成已被验证的无人文明。

本轮是有记录的定向公开资料检索，优先原始论文、官方技术文档及实际运行资料，不是穷尽性的系统综述。“最新”仅指截至报告日期、本轮实际取得并核查的公开资料，不承诺检索到全球所有最新进展。检索日志记录查询及范围限制；来源的发布日期未获确认时留空。摘要、公司材料和有限演示的局限保留在来源条目中。

核查的是来源可访问性、文本及日期，未独立复现实验性能。公司文档中的性能是发布方报告的能力。引用短摘录用于核查实际取得的文本，不能自动证明其支持所有相邻主张，仍需领域专家复核。来源按编号登记；同一URL可能因不同摘录多次登记，因此来源记录数与唯一URL数分别报告。完整抓取缓存不随报告分发，使用--verify-cache可在持有本地缓存时复核摘录；默认可仅凭版本库中的短摘录与研究记录重建报告。

assessment_status描述本轮发现的证据状态；evidence_relation描述来源与该指标的对应关系。direct_metric仅表示直接相关，不表示完整目标已达成或获得第三方验证；demonstrated_limited仅表示有限演示，不表示实现完整工业再生产。confidence是定性分析判断的把握程度，不是自主性得分或成功概率；高置信度也可能是对“尚无直接证据”的判断。没有为1000维填造0—5评分，也没有由序数分计算文明自主性。

工业闭环度C、人类依赖H、机器复制数R_M和无人增长率g₀均未估值。完整闭环需要统一系统边界、共同时间尺度、关键投入及替代路径、库存耗尽后表现、维护与灾难恢复、子代系统的同等功能与再复制能力等实证，不能从本表的演示数量或相关论文数量推出。

## 检索日志

| 分组 | 检索查询 | 范围与限制 |
| --- | --- | --- |
| domains_01_03.json | METR time horizon AI agents 2026 2025 long tasks | Bing RSS返回明显不相关结果，未把其当作证据或完整覆盖。 |
| domains_01_03.json | RepliBench AI self replication benchmark 2025 2026 | Bing RSS返回明显不相关结果，未把其当作证据或完整覆盖。 |
| domains_01_03.json | AI Scientist v2 Sakana automated scientific discovery 2025 2026 | Bing RSS返回明显不相关结果，未把其当作证据或完整覆盖。 |
| domains_01_03.json | AI research automation benchmark PaperBench 2025 2026 | Bing RSS返回明显不相关结果，未把其当作证据或完整覆盖。 |
| domains_01_03.json | AI agents multi agent coordination governance benchmark 2026 2025 | Bing RSS返回明显不相关结果，未把其当作证据或完整覆盖。 |
| domains_01_03.json | AI causal reasoning world models benchmark 2026 2025 | Bing RSS返回明显不相关结果，未把其当作证据或完整覆盖。 |
| domains_01_03.json | Google DeepMind AlphaEvolve 2025 2026 algorithm discovery | Bing RSS返回明显不相关结果，未把其当作证据或完整覆盖。 |
| domains_01_03.json | Google DeepMind AI co scientist 2025 2026 | Bing RSS返回明显不相关结果，未把其当作证据或完整覆盖。 |
| domains_01_03.json | OpenAI frontier science research benchmark 2026 | Bing RSS返回明显不相关结果，未把其当作证据或完整覆盖。 |
| domains_01_03.json | AI agents long term memory goal persistence benchmark 2025 2026 | Bing RSS返回明显不相关结果，未把其当作证据或完整覆盖。 |
| domains_01_03.json | RepliBench | Bing RSS返回明显不相关结果，未把其当作证据或完整覆盖。 |
| domains_01_03.json | "PaperBench" | Bing RSS返回明显不相关结果，未把其当作证据或完整覆盖。 |
| domains_01_03.json | "AI Scientist" | Bing RSS返回明显不相关结果，未把其当作证据或完整覆盖。 |
| domains_01_03.json | "AlphaEvolve" | Bing RSS返回明显不相关结果，未把其当作证据或完整覆盖。 |
| domains_01_03.json | "METR" "2026" | Bing RSS返回明显不相关结果，未把其当作证据或完整覆盖。 |
| domains_01_03.json | "AI co-scientist" | Bing RSS返回明显不相关结果，未把其当作证据或完整覆盖。 |
| domains_01_03.json | "long term memory" "benchmark" | Bing RSS返回明显不相关结果，未把其当作证据或完整覆盖。 |
| domains_01_03.json | ti:RepliBench | arXiv API按提交时间查询，逐项筛查日期和主题；只将另行实际读取的资料纳入证据。 |
| domains_01_03.json | all:"autonomous scientific discovery" | arXiv API按提交时间查询，逐项筛查日期和主题；只将另行实际读取的资料纳入证据。 |
| domains_01_03.json | all:"multi agent" AND all:governance | arXiv API按提交时间查询，逐项筛查日期和主题；只将另行实际读取的资料纳入证据。 |
| domains_01_03.json | all:"world model" AND all:causal | arXiv API按提交时间查询，逐项筛查日期和主题；只将另行实际读取的资料纳入证据。 |
| domains_01_03.json | 浏览METR Research当前索引与time-horizons，跟进2026 MirrorCode、Expenditure Horizon、monitorability原始报告 | 官方索引有2026研究；time-horizons于2026-09-08停止主动更新，不声称覆盖全部最新模型。 |
| domains_01_03.json | 浏览OpenAI Research当前索引，实际读取2026-09-29 GPT-6.1 Sol及2026-09-03 GPT-6 Astra发布 | 保留厂商选定评测和研究环境限制；不将高基准分变为工业闭环分。 |
| domains_01_03.json | 浏览Anthropic Research当前索引，读取2026自动对齐、费马形式化、Claude-shaped science和10月27日专家判断随机试验 | 当前检索命中10月2026资料；未独立复现厂商实验或保证检索穷尽。 |
| domains_01_03.json | 核验AI Scientist-v2、AI-Researcher、PaperBench原始arXiv摘要，AlphaEvolve、AI co-scientist、Genie3、AutoGen、Voyager与记忆工程原始页面 | 较早原始研究用于说明能力与依赖，不冒充2026最新最高性能；只读摘要的论文标为abstract。 |
| domains_01_03.json | arXiv API按日期检索autonomous scientific discovery、world model AND causal，跟进WMEval、FutureWorld、SplatLab、Autonomous Science Bench原始摘要 | 实际核验2026-10-13至10-29的原始摘要；未运行代码、未复现实验，也不宣称搜索穷尽。 |
| domains_02_09.json | AI autonomous cloud infrastructure AIOps 2026 benchmark official | Bing RSS返回大量首关键词泛化结果，仅作为发现尝试，未据此声称穷尽检索。 |
| domains_02_09.json | machine economy autonomous payments x402 2026 official | Bing RSS返回大量首关键词泛化结果，仅作为发现尝试，未据此声称穷尽检索。 |
| domains_02_09.json | SAP procurement autonomous agents 2026 official | Bing RSS返回大量首关键词泛化结果，仅作为发现尝试，未据此声称穷尽检索。 |
| domains_02_09.json | Amazon Chronos 2 forecasting 2025 official | Bing RSS返回大量首关键词泛化结果，仅作为发现尝试，未据此声称穷尽检索。 |
| domains_02_09.json | BIS Project Agora 2026 tokenisation official | Bing RSS返回大量首关键词泛化结果，仅作为发现尝试，未据此声称穷尽检索。 |
| domains_02_09.json | IMF stablecoin runs 2025 2026 financial stability | Bing RSS返回大量首关键词泛化结果，仅作为发现尝试，未据此声称穷尽检索。 |
| domains_02_09.json | autonomous cloud infrastructure AIOps benchmark 2026 | Brave搜索检出2026资料；仅将已抓取核验的原始来源纳入证据，营销和二手文章未直接用作能力达标证明。 |
| domains_02_09.json | machine economy agentic payments x402 2026 | Brave搜索检出2026资料；仅将已抓取核验的原始来源纳入证据，营销和二手文章未直接用作能力达标证明。 |
| domains_02_09.json | autonomous procurement inventory agent 2026 | Brave搜索检出2026资料；仅将已抓取核验的原始来源纳入证据，营销和二手文章未直接用作能力达标证明。 |
| domains_02_09.json | systemic financial risk autonomous agents 2026 BIS | Brave搜索检出2026资料；仅将已抓取核验的原始来源纳入证据，营销和二手文章未直接用作能力达标证明。 |
| domains_02_09.json | 直接核验官方项目滚动文档和2026更新索引：Kubernetes/KServe/Talos/PyTorch/Chronos/x402/BIS/Bank of England | 本次是有边界的公开资料检索，不声称检索覆盖所有厂商、语言和未公开系统；有些文档无可确定发布日期，日期留空。 |
| domains_04_05.json | NREL autonomous energy grid black start 2025 2026 | Bing RSS结果主要停留在首词或机构主页、与完整检索式不符；未作为能力证据，随后改用Brave和机构原文导航。 |
| domains_04_05.json | DOE autonomous robotics power line maintenance 2025 2026 | Bing RSS结果主要停留在首词或机构主页、与完整检索式不符；未作为能力证据，随后改用Brave和机构原文导航。 |
| domains_04_05.json | NREL solar resource forecasting artificial intelligence 2025 | Bing RSS结果主要停留在首词或机构主页、与完整检索式不符；未作为能力证据，随后改用Brave和机构原文导航。 |
| domains_04_05.json | Rio Tinto autonomous haulage 2025 2026 mining | Bing RSS结果主要停留在首词或机构主页、与完整检索式不符；未作为能力证据，随后改用Brave和机构原文导航。 |
| domains_04_05.json | Komatsu autonomous haulage 2025 2026 | Bing RSS结果主要停留在首词或机构主页、与完整检索式不符；未作为能力证据，随后改用Brave和机构原文导航。 |
| domains_04_05.json | Metso autonomous mineral processing flotation control | Bing RSS结果主要停留在首词或机构主页、与完整检索式不符；未作为能力证据，随后改用Brave和机构原文导航。 |
| domains_04_05.json | BASF autonomous chemical plant 2025 2026 | Bing RSS结果主要停留在首词或机构主页、与完整检索式不符；未作为能力证据，随后改用Brave和机构原文导航。 |
| domains_04_05.json | Wacker polysilicon electronic grade production semiconductor | Bing RSS结果主要停留在首词或机构主页、与完整检索式不符；未作为能力证据，随后改用Brave和机构原文导航。 |
| domains_04_05.json | Nature autonomous laboratory materials 2025 2026 | Bing RSS结果主要停留在首词或机构主页、与完整检索式不符；未作为能力证据，随后改用Brave和机构原文导航。 |
| domains_04_05.json | Veolia autonomous water treatment artificial intelligence 2025 | Bing RSS结果主要停留在首词或机构主页、与完整检索式不符；未作为能力证据，随后改用Brave和机构原文导航。 |
| domains_04_05.json | DOE robotic battery recycling 2025 | Bing RSS结果主要停留在首词或机构主页、与完整检索式不符；未作为能力证据，随后改用Brave和机构原文导航。 |
| domains_04_05.json | NREL autonomous inverter grid stability 2025 2026 | Bing RSS结果主要停留在首词或机构主页、与完整检索式不符；未作为能力证据，随后改用Brave和机构原文导航。 |
| domains_04_05.json | autonomous energy grid control black start NLR 2026 | Brave检索后访问原始发布机构页面核验；保留有限检索范围，不声称穷尽全部最新研究。检索缓存位于.research_cache/domains_04_05/brave_search.json。 |
| domains_04_05.json | robot power line wind turbine repair autonomous 2025 2026 official | Brave检索后访问原始发布机构页面核验；保留有限检索范围，不声称穷尽全部最新研究。检索缓存位于.research_cache/domains_04_05/brave_search.json。 |
| domains_04_05.json | autonomous drilling fuel processing refinery Yokogawa 2025 2026 | Brave检索后访问原始发布机构页面核验；保留有限检索范围，不声称穷尽全部最新研究。检索缓存位于.research_cache/domains_04_05/brave_search.json。 |
| domains_04_05.json | Rio Tinto Komatsu autonomous mining 2026 2025 | Brave检索后访问原始发布机构页面核验；保留有限检索范围，不声称穷尽全部最新研究。检索缓存位于.research_cache/domains_04_05/brave_search.json。 |
| domains_04_05.json | autonomous mineral exploration AI 2026 2025 KoBold | Brave检索后访问原始发布机构页面核验；保留有限检索范围，不声称穷尽全部最新研究。检索缓存位于.research_cache/domains_04_05/brave_search.json。 |
| domains_04_05.json | Wacker electronic grade polysilicon production 2025 2026 | Brave检索后访问原始发布机构页面核验；保留有限检索范围，不声称穷尽全部最新研究。检索缓存位于.research_cache/domains_04_05/brave_search.json。 |
| domains_04_05.json | Yokogawa autonomous chemical plant 2025 2026 | Brave检索后访问原始发布机构页面核验；保留有限检索范围，不声称穷尽全部最新研究。检索缓存位于.research_cache/domains_04_05/brave_search.json。 |
| domains_04_05.json | autonomous polymer synthesis laboratory 2025 2026 | Brave检索后访问原始发布机构页面核验；保留有限检索范围，不声称穷尽全部最新研究。检索缓存位于.research_cache/domains_04_05/brave_search.json。 |
| domains_04_05.json | robot battery recycling ORNL 2025 2026 | Brave检索后访问原始发布机构页面核验；保留有限检索范围，不声称穷尽全部最新研究。检索缓存位于.research_cache/domains_04_05/brave_search.json。 |
| domains_04_05.json | Veolia Hubgrade artificial intelligence water treatment 2026 2025 | Brave检索后访问原始发布机构页面核验；保留有限检索范围，不声称穷尽全部最新研究。检索缓存位于.research_cache/domains_04_05/brave_search.json。 |
| domains_04_05.json | NLR grid; Rio Tinto news; Yokogawa 2026 press releases; PNNL energy storage 官方目录逐级导航 | 核验2026-09-30 REORG现场报告、2026-08-17黑启动综述、2026-01-27 Polybot及2026-10-29/30矿业公告；剔除只返回404内容的HTTP200页面。 |
| domains_06_07.json | site:fanucamerica.com zero downtime manufacturing | Bing RSS返回明显不相关结果，不作为证据；随后通过OEM官方站点导航核验实际来源。 |
| domains_06_07.json | site:asml.com 2026 annual report lithography | Bing RSS返回明显不相关结果，不作为证据；随后通过OEM官方站点导航核验实际来源。 |
| domains_06_07.json | site:skhynix.com HBM4 mass production 2026 | Bing RSS返回明显不相关结果，不作为证据；随后通过OEM官方站点导航核验实际来源。 |
| domains_06_07.json | site:siemens.com 2026 autonomous manufacturing factory | Bing RSS返回明显不相关结果，不作为证据；随后通过OEM官方站点导航核验实际来源。 |
| domains_06_07.json | site:skf.com autonomous bearing manufacturing | Bing RSS返回明显不相关结果，不作为证据；随后通过OEM官方站点导航核验实际来源。 |
| domains_06_07.json | 2026 autonomous manufacturing predictive maintenance machine tool self repair | Brave检索后核验实际主来源。行业博客与SEO宣传不作为自治能力已实现证据。SEMI2026PM白皮书PDF返回403，未按已读全文引用。 |
| domains_06_07.json | 2026 semiconductor autonomous fab equipment maintenance robotics | Brave检索后核验实际主来源。行业博客与SEO宣传不作为自治能力已实现证据。SEMI2026PM白皮书PDF返回403，未按已读全文引用。 |
| domains_06_07.json | 2026 autonomous bearing manufacturing SKF | Brave检索后核验实际主来源。行业博客与SEO宣传不作为自治能力已实现证据。SEMI2026PM白皮书PDF返回403，未按已读全文引用。 |
| domains_06_07.json | 2026 sensor manufacturing automation quality metrology | Brave检索后核验实际主来源。行业博客与SEO宣传不作为自治能力已实现证据。SEMI2026PM白皮书PDF返回403，未按已读全文引用。 |
| domains_06_07.json | Lam Research fab maintenance robot 2026 official | Brave检索后核验实际主来源。行业博客与SEO宣传不作为自治能力已实现证据。SEMI2026PM白皮书PDF返回403，未按已读全文引用。 |
| domains_06_07.json | SEMI autonomous fab preventive maintenance automation white paper 2026 | Brave检索后核验实际主来源。行业博客与SEO宣传不作为自治能力已实现证据。SEMI2026PM白皮书PDF返回403，未按已读全文引用。 |
| domains_06_07.json | SKF accelerates hybrid bearing leadership new ceramic process laboratory 2026 | Brave检索后核验实际主来源。行业博客与SEO宣传不作为自治能力已实现证据。SEMI2026PM白皮书PDF返回403，未按已读全文引用。 |
| domains_06_07.json | 官方首页与产品导航：DMG MORI、GROB、FANUC、ABB、ASML、Lam、Applied、KLA、TSMC、Siltronic、SK hynix | 直接读取公开正文及官方最新新闻索引。检索非穷尽，产品无明确日期时不以网页版权、元数据修改日期推定首次实现年份；未将供应商声称等同独立长期试验。 |
| domains_08_10.json | robot metabolism self replication Columbia 2025 2026 Science Advances | Bing RSS结果多退化为首词泛化匹配，不能据此声称最新文献已穷尽；保留原始结果缓存。 |
| domains_08_10.json | NASA ARMADAS autonomous robotic assembly 2025 2026 | Bing RSS结果多退化为首词泛化匹配，不能据此声称最新文献已穷尽；保留原始结果缓存。 |
| domains_08_10.json | robotics autonomous maintenance warehouse 2026 latest | Bing RSS结果多退化为首词泛化匹配，不能据此声称最新文献已穷尽；保留原始结果缓存。 |
| domains_08_10.json | NASA MOXIE oxygen Mars 2023 2025 ISRU | Bing RSS结果多退化为首词泛化匹配，不能据此声称最新文献已穷尽；保留原始结果缓存。 |
| domains_08_10.json | autonomous self replicating seed factory industrial closure 2025 2026 | Bing RSS结果多退化为首词泛化匹配，不能据此声称最新文献已穷尽；保留原始结果缓存。 |
| domains_08_10.json | Waymo autonomous driver safety impact 2026 | Bing RSS结果多退化为首词泛化匹配，不能据此声称最新文献已穷尽；保留原始结果缓存。 |
| domains_08_10.json | Amazon DeepFleet million robots 2025 | Bing RSS结果多退化为首词泛化匹配，不能据此声称最新文献已穷尽；保留原始结果缓存。 |
| domains_08_10.json | Gemini Robotics 1.5 2025 autonomous manipulation | Bing RSS结果多退化为首词泛化匹配，不能据此声称最新文献已穷尽；保留原始结果缓存。 |
| domains_08_10.json | https://search.brave.com/search?q=NASA+ARMADAS+autonomous+assembly+2025+2026&source=web | Brave结果用于发现来源；具体事实均从另行获取的原始页面核验，不将搜索片段作为证据。 |
| domains_08_10.json | https://search.brave.com/search?q=Yara+Birkeland+2026+autonomous+Kongsberg&source=web | Brave结果用于发现来源；具体事实均从另行获取的原始页面核验，不将搜索片段作为证据。 |
| domains_08_10.json | https://search.brave.com/search?q=self+replicating+robot+factory+2026+physical+replication&source=web | Brave结果用于发现来源；具体事实均从另行获取的原始页面核验，不将搜索片段作为证据。 |
| domains_08_10.json | https://search.brave.com/search?q=robot+self+modeling+2026+self+repair+Nature+2025&source=web | Brave结果用于发现来源；具体事实均从另行获取的原始页面核验，不将搜索片段作为证据。 |
| domains_08_10.json | https://www.pi.website/blog ; https://deepmind.google/models/gemini-robotics/ | 直接浏览发布者研究索引发现2026-03、04、10月更新；现行Gemini Robotics2页未见可靠发布日期。 |

## 来源目录与核查短摘录

来源中的具体证据边界优先于标题、宣传或概括性结论。发布日期未知时明确保留未知。

### D01-S01 · Task-Completion Time Horizons of Frontier AI Models - METR

- 出处：[METR](https://metr.org/time-horizons/)
- 发布：未确认；获取：2026-11-02；类型：benchmark；核查范围：documentation。
- 核查文本：`.research_cache/domains_01_03/metr.txt`

> Measurements above 16 hrs are unreliable with our current task suite

**适用限制：** 页面没有明确首次发布日期；LAST UPDATED为2026-09-08，此后停止主动更新。该日期不是全部模型测量日期，也不覆盖全部当前模型；软件任务分布与工业HR0不同。

### D01-S02 · MirrorCode: evidence AI can already do some weeks-long coding tasks | Epoch AI

- 出处：[Epoch AI / METR](https://epoch.ai/publications/mirrorcode-preliminary-results)
- 发布：2026-04-10；获取：2026-11-02；类型：benchmark；核查范围：full_text。
- 核查文本：`.research_cache/domains_01_03/mirrorcode_epoch.txt`

> provided there is a detailed, checkable specification

**适用限制：** 初步基准；人类工期为估计值；可检查规格下的软件重实现，不是连续无人运行数周。

### D01-S03 · Genie 3: A new frontier for world models — Google DeepMind

- 出处：[Google DeepMind](https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/)
- 发布：2025-08-05；获取：2026-11-02；类型：company-doc；核查范围：full_text。
- 核查文本：`.research_cache/domains_01_03/genie3.txt`

> The model can currently support a few minutes of continuous interaction, rather than extended hours.

**适用限制：** 厂商研究展示；交互视频世界不等于可验证工业因果模型；页面修改日期不当成能力发布日期。

### D01-S04 · AgentChat — AutoGen

- 出处：[Microsoft](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/index.html)
- 发布：未确认；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_01_03/multiagent.txt`

> AgentChat is a high-level API for building multi-agent applications.

**适用限制：** 软件接口文档，未给出长期无人工业协作可靠性；文档无明确发布日期。

### D01-S05 · Building effective AI agents \ Anthropic

- 出处：[Anthropic](https://www.anthropic.com/research/building-effective-agents)
- 发布：2024-12-19；获取：2026-11-02；类型：company-doc；核查范围：full_text。
- 核查文本：`.research_cache/domains_01_03/agents.txt`

> Agents can be used for open-ended problems where it’s difficult or impossible to predict the required number of steps

**适用限制：** 厂商工程建议而非工业HR0实验；强调环境反馈和人工检查点。

### D01-S06 · Effective context engineering for AI agents \ Anthropic

- 出处：[Anthropic](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)
- 发布：2025-09-29；获取：2026-11-02；类型：company-doc；核查范围：full_text。
- 核查文本：`.research_cache/domains_01_03/context.txt`

> After context resets, the agent reads its own notes and continues multi-hour training sequences or dungeon explorations.

**适用限制：** 厂商工程案例，跨上下文记忆不等于灾后恢复或跨代目标稳定。

### D01-S07 · [2305.16291] Voyager: An Open-Ended Embodied Agent with Large Language Models

- 出处：[Voyager authors / arXiv](https://arxiv.org/abs/2305.16291)
- 发布：2023-05-25；获取：2026-11-02；类型：Paper；核查范围：abstract。
- 核查文本：`.research_cache/domains_01_03/voyager.txt`

> Voyager is able to utilize the learned skill library in a new Minecraft world to solve novel tasks from scratch

**适用限制：** Minecraft虚拟环境、GPT-4接口与预建游戏，不证明现实工业跨设备迁移。

### D01-S08 · Early work on monitorability evaluations - METR

- 出处：[METR](https://metr.org/blog/2026-01-19-early-work-on-monitorability-evaluations/)
- 发布：2026-01-22；获取：2026-11-02；类型：benchmark；核查范围：full_text。
- 核查文本：`.research_cache/domains_01_03/metrmonitor.txt`

> A common approach to detect unwanted AI behavior is to use an AI model as a monitor.

**适用限制：** 原型监控评测；检测与绕过在特定任务中测量，不等于自主治理可靠性。

### D01-S09 · How AI agents shape experts’ judgment calls \ Anthropic

- 出处：[Anthropic](https://www.anthropic.com/research/agents-judgment-calls)
- 发布：2026-10-27；获取：2026-11-02；类型：company-doc；核查范围：full_text。
- 核查文本：`.research_cache/domains_01_03/judgment.txt`

> Across the four analytical choices, analysts went with their agent’s lean 86% of the time.

**适用限制：** 61名分析者的随机试验；反映人类判断受代理影响，不能当作治理独立或正确决策的成功率。

### D01-S10 · Introducing GPT-6.1 Sol | OpenAI

- 出处：[OpenAI](https://openai.com/index/introducing-gpt-6-1-sol/)
- 发布：2026-09-29；获取：2026-11-02；类型：company-doc；核查范围：full_text。
- 核查文本：`.research_cache/domains_01_03/sol2026.txt`

> AI agents are tested on end-to-end workflows using 47 tools across sales, marketing, operations, support, finance, and HR.

**适用限制：** 厂商选定基准；47工具工作流和研究任务进步不是自主制定生存目标或能源、硬件闭环。

### D01-S11 · GPT-6 Astra: A new generation of intelligence | OpenAI

- 出处：[OpenAI](https://openai.com/index/gpt-6-astra/)
- 发布：2026-09-03；获取：2026-11-02；类型：company-doc；核查范围：full_text。
- 核查文本：`.research_cache/domains_01_03/astra2026.txt`

> Earlier context windows remain searchable

**适用限制：** 厂商发布与研究环境测量；可搜索上下文和代理编程不证明现实工业HR0连续性。

### D01-S12 · [2610.33894] WMEval: Evaluating Interactive World Models Grounded on Physical Simulations

- 出处：[WMEval authors / arXiv](https://arxiv.org/abs/2610.33894)
- 发布：2026-10-24；获取：2026-11-02；类型：Paper；核查范围：abstract。
- 核查文本：`.research_cache/domains_01_03/wmeval.txt`

> We introduce WMEval, a comprehensive benchmark that evaluates interactive world models against Unity-based physical simulations.

**适用限制：** 仅核验原始摘要，未复现实验；Unity仿真真值不是现实工业测量，v2修订于2026-10-27。

### D01-S13 · [2610.39619] FutureWorld: A Plug-and-Play Causal Next-State Predictor for Interactive Video World Exploration

- 出处：[FutureWorld authors / arXiv](https://arxiv.org/abs/2610.39619)
- 发布：2026-10-29；获取：2026-11-02；类型：Paper；核查范围：abstract。
- 核查文本：`.research_cache/domains_01_03/futureworld.txt`

> We integrate C-NCP into four base generators

**适用限制：** 仅核验摘要；作者报告的视频生成误差积累改进，不是模型自主修复工艺因果错误。

### D02-S01 · Kubernetes Self-Healing | Kubernetes

- 出处：[Kubernetes Authors](https://kubernetes.io/docs/concepts/architecture/self-healing/)
- 发布：2025-11-20；获取：2026-11-02；类型：other；核查范围：documentation。
- 核查文本：`.research_cache/domains_02_09/D02-S01.txt`

> Kubernetes is designed with self-healing capabilities that help maintain the health and availability of workloads.

**适用限制：** 官方滚动文档；日期为页面最后修改日。仅证明声明式工作负载恢复机制，不证明操作系统或硬件物理维修。

### D02-S02 · Services, Load Balancing, and Networking | Kubernetes

- 出处：[Kubernetes Authors](https://kubernetes.io/docs/concepts/services-networking/)
- 发布：未确认；获取：2026-11-02；类型：other；核查范围：documentation。
- 核查文本：`.research_cache/domains_02_09/D02-S02.txt`

> The Kubernetes network model is built out of several pieces:

**适用限制：** 网络模型文档，不是无人铺设链路或修理交换机的运行证据。

### D02-S03 · Health Checks — Ceph Documentation

- 出处：[Ceph Authors](https://docs.ceph.com/en/latest/rados/operations/health-checks/)
- 发布：未确认；获取：2026-11-02；类型：other；核查范围：documentation。
- 核查文本：`.research_cache/domains_02_09/D02-S03.txt`

> Each health check has a unique identifier.

**适用限制：** latest文档可能对应开发版本；说明存储健康检查与处置条件，不证明磁盘自主制造或更换。

### D02-S04 · Kubernetes Scheduler | Kubernetes

- 出处：[Kubernetes Authors](https://kubernetes.io/docs/concepts/scheduling-eviction/kube-scheduler/)
- 发布：未确认；获取：2026-11-02；类型：other；核查范围：documentation。
- 核查文本：`.research_cache/domains_02_09/D02-S04.txt`

> A scheduler watches for newly created Pods that have no Node assigned.

**适用限制：** 说明已供给节点上的逻辑调度，不证明物理算力来源独立。

### D02-S05 · Welcome to KServe | KServe

- 出处：[KServe Authors](https://kserve.github.io/website/docs/intro)
- 发布：未确认；获取：2026-11-02；类型：other；核查范围：documentation。
- 核查文本：`.research_cache/domains_02_09/D02-S05.txt`

> Scale to zero when idle, handle traffic spikes automatically, and manage hundreds of models efficiently.

**适用限制：** 项目功能文档；扩缩容指已存在云或集群资源，不等于制造新增GPU。

### D02-S06 · torchrun (Elastic Launch) — PyTorch 2.15 documentation

- 出处：[PyTorch Contributors](https://docs.pytorch.org/docs/2.15/elastic/run.html)
- 发布：未确认；获取：2026-11-02；类型：other；核查范围：documentation。
- 核查文本：`.research_cache/domains_02_09/D02-S06.txt`

> On failures or membership changes ALL surviving workers are killed immediately.

**适用限制：** 当前stable链接跳转到2.15文档；明确需要应用检查点，不代表训练硬件维修自治。

### D02-S07 · SLSA • Security levels

- 出处：[SLSA Authors](https://slsa.dev/spec/v1.1/levels)
- 发布：未确认；获取：2026-11-02；类型：other；核查范围：documentation。
- 核查文本：`.research_cache/domains_02_09/D02-S07.txt`

> Provenance describes what entity built the artifact, what process they used, and what the inputs were.

**适用限制：** 安全规范的分级和构件溯源定义，不是自动修补漏洞或完全自治的实测结果。

### D02-S08 · Certificate resource - cert-manager Documentation

- 出处：[cert-manager Authors](https://cert-manager.io/docs/usage/certificate/)
- 发布：未确认；获取：2026-11-02；类型：other；核查范围：documentation。
- 核查文本：`.research_cache/domains_02_09/D02-S08.txt`

> that the certificate is auto-renewed before it expires

**适用限制：** 证书自动续期仍依赖已配置发行者、身份与基础设施；不等于全面自主网络防御。

### D02-S09 · AIOpsLab official repository README

- 出处：[Microsoft / AIOpsLab Contributors](https://raw.githubusercontent.com/microsoft/AIOpsLab/main/README.md)
- 发布：未确认；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_02_09/D02-S09.txt`

> AIOpsLab supports any remote kubernetes cluster that your

**适用限制：** 项目README描述部署与检测、定位、分析、缓解任务；框架存在不表示代理全部通过。

### D02-S10 · Concepts - The Cluster API Book

- 出处：[Kubernetes Cluster API Authors](https://cluster-api.sigs.k8s.io/user/concepts.html)
- 发布：未确认；获取：2026-11-02；类型：other；核查范围：documentation。
- 核查文本：`.research_cache/domains_02_09/D02-S10.txt`

> A MachineHealthCheck defines the conditions when a Node should be considered missing or unhealthy.

**适用限制：** Machine是基础设施提供者管理的资源；API重建虚机或主机不等于机器人生产设备。

### D02-S12 · What is Talos Linux? - Sidero Documentation

- 出处：[Sidero Labs](https://docs.siderolabs.com/talos/v1.14/overview/what-is-talos)
- 发布：未确认；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_02_09/D02-S12.txt`

> Talos is managed by a single, declarative gRPC API.

**适用限制：** 旧入口跳转到v1.14；说明操作系统API管理，不是端到端无人运维长期验证。

### D02-S13 · [2501.06706] AIOpsLab: A Holistic Framework to Evaluate AI Agents for Enabling Autonomous Clouds

- 出处：[AIOpsLab Research Authors / arXiv](https://arxiv.org/abs/2501.06706)
- 发布：2025-01-12；获取：2026-11-02；类型：Paper；核查范围：abstract。
- 核查文本：`.research_cache/domains_02_09/D02-S13.txt`

> we provide insights into their capabilities and limitations in handling complex operational tasks in cloud environments.

**适用限制：** 仅核验论文摘要和项目文档；未从摘要推断特定成功率或真实工业HR0表现。

### D03-S01 · [2504.08066] The AI Scientist-v2: Workshop-Level Automated Scientific Discovery via Agentic Tree Search

- 出处：[AI Scientist-v2 authors / arXiv](https://arxiv.org/abs/2504.08066)
- 发布：2025-04-10；获取：2026-11-02；类型：Paper；核查范围：abstract。
- 核查文本：`.research_cache/domains_01_03/scientist2paper.txt`

> This system iteratively formulates scientific hypotheses, designs and executes experiments, analyzes and visualizes data, and autonomously authors scientific manuscripts.

**适用限制：** 作者报告的系统研究；三篇投稿中一篇达到workshop接受标准；不是全面独立科研或工业复制。

### D03-S02 · [2505.18705] AI-Researcher: Autonomous Scientific Innovation

- 出处：[AI-Researcher authors / arXiv](https://arxiv.org/abs/2505.18705)
- 发布：2025-05-24；获取：2026-11-02；类型：Paper；核查范围：abstract。
- 核查文本：`.research_cache/domains_01_03/airesearcher.txt`

> from literature review and hypothesis generation to algorithm implementation and publication-ready manuscript preparation

**适用限制：** 作者评测的自动化研究流程；未独立复核代码或取得全链HR0实验数据。

### D03-S03 · [2504.01848] PaperBench: Evaluating AI's Ability to Replicate AI Research

- 出处：[OpenAI / arXiv](https://arxiv.org/abs/2504.01848)
- 发布：2025-04-02；获取：2026-11-02；类型：Paper；核查范围：abstract。
- 核查文本：`.research_cache/domains_01_03/paperbenchpaper.txt`

> achieves an average replication score of 21.0%

**适用限制：** 这是2025发布时已测模型的平均复现分数，绝不是2026最新模型或全部科研的能力上限。

### D03-S04 · AlphaEvolve: A Gemini-powered coding agent for designing advanced algorithms — Google DeepMind

- 出处：[Google DeepMind](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/)
- 发布：2025-05-14；获取：2026-11-02；类型：company-doc；核查范围：full_text。
- 核查文本：`.research_cache/domains_01_03/alphaevolve.txt`

> automated evaluators

**适用限制：** 厂商算法搜索报告；依赖人类定义评价函数和既有计算设施；未证明递归工业闭环。

### D03-S05 · Accelerating scientific breakthroughs with an AI co-scientist

- 出处：[Google Research](https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/)
- 发布：2025-02-19；获取：2026-11-02；类型：company-doc；核查范围：full_text。
- 核查文本：`.research_cache/domains_01_03/coscientist.txt`

> a multi-agent AI system built with Gemini 2.0 as a virtual scientific collaborator

**适用限制：** 与科学家合作的生物医学研究案例，实验与研究价值确认仍有人类参与。

### D03-S06 · Automated researchers can reliably mitigate alignment failures \ Anthropic

- 出处：[Anthropic](https://www.anthropic.com/research/automated-researchers-mitigate-alignment-failures)
- 发布：2026-08-28；获取：2026-11-02；类型：company-doc；核查范围：full_text。
- 核查文本：`.research_cache/domains_01_03/autoalignment.txt`

> For all 10 alignment failures, Claude found fixes that improved the target benchmarks without degrading capabilities.

**适用限制：** 厂商限定10类失败、预定能力评测与监控约束；未检验后续广泛RL后的持久性或现实长期效果。

### D03-S07 · Expenditure Horizon: Measuring Optimization Ability, with an Application to NanoGPT - METR

- 出处：[METR](https://metr.org/blog/2026-07-21-expenditure-horizon/)
- 发布：2026-07-21；获取：2026-11-02；类型：benchmark；核查范围：full_text。
- 核查文本：`.research_cache/domains_01_03/expenditure.txt`

> GPT-5.5 and Opus-4.8 show significant improvements over the baseline

**适用限制：** NanoGPT小规模训练优化、初步高开销轨迹；改进须再验证，作者认为总体增益仍有限。

### D03-S08 · Claude-shaped science \ Anthropic

- 出处：[Anthropic / Matthew Schwartz](https://www.anthropic.com/research/claude-shaped-science)
- 发布：2026-10-01；获取：2026-11-02；类型：company-doc；核查范围：full_text。
- 核查文本：`.research_cache/domains_01_03/claudescience.txt`

> most scientific progress comes from real-world data that has to be acquired, understood, and checked

**适用限制：** 个人研究者与领域专家合作的BootLoops案例，不是无人工策划与验证的科研闭环。

### D03-S09 · Formalizing Fermat's Last Theorem  \ Anthropic

- 出处：[Anthropic](https://www.anthropic.com/research/formalizing-fermats-last-theorem)
- 发布：2026-09-04；获取：2026-11-02；类型：company-doc；核查范围：full_text。
- 核查文本：`.research_cache/domains_01_03/fermats.txt`

> Claude worked largely autonomously over 11 days to write the proof in the Lean programming language.

**适用限制：** 厂商形式化案例；有偶尔高层人类指令、专门Prove2Me脚手架与大量算力；未独立运行证明核验。

### D03-S10 · [2610.30468] SplatLab: Autonomous Scientific Discovery for 3DGS Research

- 出处：[SplatLab authors / arXiv](https://arxiv.org/abs/2610.30468)
- 发布：2026-10-21；获取：2026-11-02；类型：Paper；核查范围：abstract。
- 核查文本：`.research_cache/domains_01_03/splatlab.txt`

> binds every reported number to a logged training run

**适用限制：** 仅核验作者摘要；3DGS限定子领域、预建脚手架与GPU，尚未独立复现，不证明科研工业闭环。

### D03-S11 · [2610.18449] Autonomous Science Bench: Evaluating AI Agents for Autonomous Scientific Discovery

- 出处：[Autonomous Science Bench authors / arXiv](https://arxiv.org/abs/2610.18449)
- 发布：2026-10-13；获取：2026-11-02；类型：Paper；核查范围：abstract。
- 核查文本：`.research_cache/domains_01_03/autoscience.txt`

> the best configuration succeeds in 67% of trials

**适用限制：** 仅核验原始摘要；六类有预算任务、144次初步试验，lab service不等于实体实验室自主建造和维护。

### D04-S01 · Autonomous Energy Systems | Grid Modernization | NLR

- 出处：[National Laboratory of the Rockies](https://www.nlr.gov/grid/autonomous-energy)
- 发布：未确认；获取：2026-11-02；类型：government；核查范围：documentation。
- 核查文本：`.research_cache/domains_04_05/aeg2.txt`

> NLR developed and tested effective optimization and

**适用限制：** 技术综述包含试验与示范；并非全网长期无人运行记录。

### D04-S02 · Solar and Wind Forecasting | Grid Modernization | NLR

- 出处：[National Laboratory of the Rockies](https://www.nlr.gov/grid/solar-wind-forecasting)
- 发布：未确认；获取：2026-11-02；类型：government；核查范围：documentation。
- 核查文本：`.research_cache/domains_04_05/forecast2.txt`

> WindView is an open-source situational awareness and decision support platform

**适用限制：** 页面只有更新日期；预测与决策支持不等于自主勘探和设备保障。

### D04-S03 · Black Start | Grid Modernization | NLR

- 出处：[National Laboratory of the Rockies](https://www.nlr.gov/grid/black-start)
- 发布：未确认；获取：2026-11-02；类型：government；核查范围：documentation。
- 核查文本：`.research_cache/domains_04_05/black.txt`

> Black start is the ability of generation to restart parts of the power system

**适用限制：** 研究与方法说明，不是整条供电工业链无人重建的实证。

### D04-S04 · As Local Power Grows, Utilities Reorganize for Resilience | NLR

- 出处：[National Laboratory of the Rockies](https://www.nlr.gov/news/detail/program/2026/as-local-power-grows-utilities-reorganize-for-resilience)
- 发布：2026-09-30；获取：2026-11-02；类型：government；核查范围：documentation。
- 核查文本：`.research_cache/domains_04_05/newgrid26.txt`

> REORG recovered power according to plans.

**适用限制：** 现场短时失网恢复；初始硬件、柴油、UPS与工程部署由人提供；页面更新脚注早于正文日期，以正文发表日期为准。

### D04-S05 · Energy Storage | PNNL

- 出处：[Pacific Northwest National Laboratory](https://www.pnnl.gov/energy-storage)
- 发布：未确认；获取：2026-11-02；类型：government；核查范围：documentation。
- 核查文本：`.research_cache/domains_04_05/pnnl.txt`

> Our research teams support field deployments

**适用限制：** 官方研究能力介绍，不是储能制造维护和供料闭环的验证。

### D04-S06 · Robots and AI Take Wind Turbine Maintenance Tech to New Heights | The Government of Japan - JapanGov -

- 出处：[Government of Japan](https://www.japan.go.jp/kizuna/2025/08/robots_ai_wind_turbine_maintenance.html)
- 发布：2025-10-24；获取：2026-11-02；类型：government；核查范围：documentation。
- 核查文本：`.research_cache/domains_04_05/windrobot.txt`

> An operator uses remote control to guide a repair robot as it fixes damage to a blade.

**适用限制：** 政府对企业案例的介绍；维修当时仍由地面操作员遥控，未来全自主为目标。

### D04-S07 · Aramco and Yokogawa Achieve a Major Milestone with Commissioning of Multiple Autonomous Control AI Agents at Major Gas Facility | Yokogawa America

- 出处：[Yokogawa Electric Corporation](https://www.yokogawa.com/us/news/press-releases/2025/2025-10-29)
- 发布：2025-10-29；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_04_05/yokogas.txt`

> directly and autonomously control and optimize acid gas removal (AGR) operations

**适用限制：** 厂商联合项目公告，初步结果仍在详细评估；仅气体脱酸单元控制，非无人燃料供应链。

### D04-S08 · Grid-Forming Inverter Controls | Grid Modernization | NLR

- 出处：[National Laboratory of the Rockies](https://www.nlr.gov/grid/grid-forming-inverter-controls)
- 发布：未确认；获取：2026-11-02；类型：government；核查范围：documentation。
- 核查文本：`.research_cache/domains_04_05/gridforming.txt`

> NLR is developing grid-forming controls for distributed inverters

**适用限制：** 研发综述，不证明逆变器自主制造、故障维修或所有电网拓扑的可用性。

### D04-S09 · Power distribution system blackstart restoration using renewable energy | Nature Communications

- 出处：[Nature Communications](https://www.nature.com/articles/s41467-026-76692-0)
- 发布：2026-08-17；获取：2026-11-02；类型：Paper；核查范围：full_text。
- 核查文本：`.research_cache/domains_04_05/naturegrid26.txt`

> If an unverified device is the sole path to a critical load

**适用限制：** 综述归纳黑启动约束与方法；不是作者完成完全无人电网重建的试验。

### D04-S10 · Yokogawa and ANYbotics to Integrate OpreX Robot Management Core Software with ANYmal Robotic Inspection Solutions | Yokogawa Europe

- 出处：[Yokogawa Electric Corporation](https://www.yokogawa.com/eu/news/press-releases/2026/2026-02-10/)
- 发布：2026-02-10；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_04_05/robot26.txt`

> ANYmal is an autonomous and remotely operable four-legged inspection robot

**适用限制：** 合作与集成公告含已有产品描述；自主巡检不等于机械维修，爆炸环境型号部分部署为原型。

### D04-S11 · Yokogawa to Provide Power Plant Controller and Batteries for Cosmo Eco Power's Wind Power Plant in Northern Japan | Yokogawa Europe

- 出处：[Yokogawa Electric Corporation](https://www.yokogawa.com/eu/news/press-releases/2026/2026-03-05/)
- 发布：2026-03-05；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_04_05/power26.txt`

> is expected to start operation in 2029.

**适用限制：** 供货订单及2029投运计划，不能算2026已投产或机器人建厂能力。

### D05-S01 · Science - KoBold Metals

- 出处：[KoBold Metals](https://koboldmetals.com/science/)
- 发布：未确认；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_04_05/koboldscience.txt`

> Machine Prospector model predictions include quantified uncertainty

**适用限制：** 公司科学方法说明；AI辅助地质团队决策，不是无人勘探、取样、设备自维持验证。

### D05-S02 · Innovation | Global

- 出处：[Rio Tinto](https://www.riotinto.com/en/about/innovation)
- 发布：未确认；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_04_05/rioinnovation.txt`

> We were at the forefront of automation – trucks, trains and drills – and remote operations

**适用限制：** 公司技术概览；自动运输钻孔与远程运营不能推出矿山完全无人维护。

### D05-S03 · Advanced Process Control - Metso

- 出处：[Metso](https://www.metso.com/portfolio/advanced-process-control/)
- 发布：未确认；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_04_05/metso.txt`

> APC manages multiple process variables within operational limits

**适用限制：** 供应商产品说明；未提供本来源可独立复核的长期无人选矿运营数据。

### D05-S04 · Metso Digital for Metals refining - Metso

- 出处：[Metso](https://www.metso.com/products-and-services/digitalization/digital-solutions-for-metals-refining/)
- 发布：未确认；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_04_05/metals.txt`

> digital services such as training and connected analytics.

**适用限制：** 冶炼数字化产品与服务范围说明，包含人员培训与运行支持；不是自主修厂供料验证。

### D05-S05 · WACKER commissions new production line for semiconductor-grade polysilicon at Burghausen site - Wacker Chemie AG

- 出处：[Wacker Chemie AG](https://www.wacker.com/cms/en-us/press-and-media/press/press-releases/2025/press-releases-detail-2025-257922.html)
- 发布：2025-07-17；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_04_05/wacker3.txt`

> Sophisticated automation improves process stability and product purity

**适用限制：** 厂商投产公告，新增约150岗位；高纯硅自动化不等于无人化学品、设备和电力闭环。

### D05-S06 · Boosting Industrial Autonomy with AI | Yokogawa Electric Corporation

- 出处：[Yokogawa Electric Corporation](https://www.yokogawa.com/special/planet/stories/boosting_industrial_autonomy_with_AI/)
- 发布：2026-01-26；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_04_05/yokochemical.txt`

> autonomously and safely control a plant for 35 days

**适用限制：** 2026回顾文章描述2022开始的化工控制试验及后续采用；35天自主控制不等于所有维护原料无人。

### D05-S07 · AI-powered autonomous electronic polymer synthesis | Argonne National Laboratory

- 出处：[Argonne National Laboratory](https://www.anl.gov/cnm/article/aipowered-autonomous-electronic-polymer-synthesis)
- 发布：2026-01-27；获取：2026-11-02；类型：government；核查范围：documentation。
- 核查文本：`.research_cache/domains_04_05/polymer.txt`

> Polybot, a polymer design platform, enabled AI-driven decision-making within a modular, closed-loop workflow

**适用限制：** 官方研究摘要；局限电致变色聚合物设计合成，不涵盖所有塑料橡胶、吨级生产或设备复制。

### D05-S08 · Hubgrade digital solutions | Veolia Water Technologies

- 出处：[Veolia Water Technologies](https://www.veoliawatertechnologies.com/en/hubgrade-digital-solutions)
- 发布：未确认；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_04_05/hubgrade.txt`

> Hubgrade is the combination of digital tools and the expertise of Veolia employees

**适用限制：** 产品页明确结合人类专家；数字孪生优化不等于无人供水、膜更换或上游药剂供应。

### D05-S09 · Automated disassembly line aims to make battery recycling safer, faster – Oak Ridge National Lab

- 出处：[Oak Ridge National Laboratory](https://www.ornl.gov/news/automated-disassembly-line-aims-make-battery-recycling-safer-faster/)
- 发布：2021-08-16；获取：2026-11-02；类型：government；核查范围：documentation。
- 核查文本：`.research_cache/domains_04_05/recycledemo.txt`

> Researchers at the Department of Energy’s Oak Ridge National Laboratory have developed a robotic disassembly system

**适用限制：** 历史原型示范，本次重新核验；需先人工拆解建模，不等于商业规模全废物闭环。

### D05-S10 · An autonomous laboratory for the accelerated synthesis of inorganic materials | Nature

- 出处：[Nature](https://www.nature.com/articles/s41586-023-06734-w)
- 发布：2023-11-29；获取：2026-11-02；类型：Paper；核查范围：full_text。
- 核查文本：`.research_cache/domains_04_05/alab.txt`

> The XRD sample holders must be cleaned manually

**适用限制：** 公开全文现已修订，显示17天实现36/57目标；需人工装料、清洁及处理硬件异常，非高纯工业供料闭环。

### D05-S11 · Rio Tinto celebrates opening of $1.4 billion lithium projects in Argentina | Global

- 出处：[Rio Tinto](https://www.riotinto.com/en/news/releases/2026/rio-tinto-celebrates-opening-of-1-4-billion-lithium-projects-in-argentina)
- 发布：2026-10-29；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_04_05/riolithium26.txt`

> Both projects achieved first production in the second quarter ahead of plan

**适用限制：** 人类组织的锂产能扩建与爬坡公告；不是自主建造或复制矿化工生产线。

### D05-S12 · Update on Oyu Tolgoi seismic event | Global

- 出处：[Rio Tinto](https://www.riotinto.com/en/news/releases/2026/update-on-oyu-tolgoi-seismic-event)
- 发布：2026-10-30；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_04_05/rioseismic26.txt`

> Underground operations at the Oyu Tolgoi copper mine in Mongolia are being progressively restarted

**适用限制：** 安全审查后恢复的具体矿区事件；不反映所有矿山，但不能当作无需人类灾后决策的证据。

### D05-S13 · Battery Remanufacturing and Automating Circular Economies (BRACE) Lab – Oak Ridge National Lab

- 出处：[Oak Ridge National Laboratory](https://www.ornl.gov/brace/)
- 发布：未确认；获取：2026-11-02；类型：government；核查范围：documentation。
- 核查文本：`.research_cache/domains_04_05/recycle.txt`

> Integrating machine vision systems and industrial automation tools to autonomously defeat joining mechanisms

**适用限制：** 实验室能力与研究方向介绍；没有完整循环的材料收率、外部投入和多代无人持续性数据。

### D06-S01 · Automation of CNC Machines - DMG MORI

- 出处：[DMG MORI](https://en.dmgmori.com/products/automation)
- 发布：未确认；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_06_07/dmg.txt`

> This applies to unmanned night and weekend shifts

**适用限制：** 产品或公司自述，非独立HR0长期试验；网页检索日期不等于能力首次实现日期。

### D06-S02 · Die Cast Robots | Foundry & Mold Machine Robots |… | FANUC America

- 出处：[FANUC America](https://www.fanucamerica.com/industries/die-cast-foundry-mold)
- 发布：未确认；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_06_07/fanuc_cast.txt`

> FANUC has the industry's leading casting robots for die cast product handling, foundry robots, and molding machine tending robots.

**适用限制：** 产品或公司自述，非独立HR0长期试验；网页检索日期不等于能力首次实现日期。

### D06-S03 · Metal 3D Printer | EOS | EOS GmbH

- 出处：[EOS](https://www.eos.info/metal-solutions/metal-printers)
- 发布：未确认；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_06_07/eos.txt`

> Both systems share the same automated platform with job changeovers in under 30 minutes

**适用限制：** 产品或公司自述，非独立HR0长期试验；网页检索日期不等于能力首次实现日期。

### D06-S04 · Arc Welding Robots & Robotic Welding Systems | FANUC America

- 出处：[FANUC America](https://www.fanucamerica.com/applications/arc-welding)
- 发布：未确认；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_06_07/fanuc_weld.txt`

> FANUC arc welding robots help manufacturers improve weld quality, productivity and consistency with reliable robotic automation for MIG, TIG, plasma

**适用限制：** 产品或公司自述，非独立HR0长期试验；网页检索日期不等于能力首次实现日期。

### D06-S05 · Electromobility - GROB

- 出处：[GROB](https://www.grobgroup.com/en/products/product-range/electromobility/)
- 发布：未确认；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_06_07/grob_motor.txt`

> GROB offers you an integrated concept for tomorrow's components through its MODULAR, FLEXIBLE and SCALEABLE electric powertrain SOLUTIONS.

**适用限制：** 产品或公司自述，非独立HR0长期试验；网页检索日期不等于能力首次实现日期。

### D06-S06 · Machines and Systems for Electric Motor Production - GROB

- 出处：[GROB](https://www.grobgroup.com/en/products/product-range/winding-and-inserting-technology/)
- 发布：未确认；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_06_07/grob_winding.txt`

> Fully automatic solution

**适用限制：** 产品或公司自述，非独立HR0长期试验；网页检索日期不等于能力首次实现日期。

### D06-S07 · SKF accelerates hybrid bearing leadership with new Ceramic Process Laboratory - SKF

- 出处：[SKF (official press release via Cision)](https://news.cision.com/skf/r/skf-accelerates-hybrid-bearing-leadership-with-new-ceramic-process-laboratory,c4411601)
- 发布：2026-10-19；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_06_07/skf_lab.txt`

> By bringing powder formulation, compaction, sintering, and surface finishing all together

**适用限制：** 公司研发实验室启用新闻，证明工艺研发整合，不证明无人生产或自行制造全部设备。

### D06-S08 · Probing and tool measurement systems for machine tools

- 出处：[Renishaw](https://www.renishaw.com/en/machine-tool-probes--6073)
- 发布：未确认；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_06_07/renishaw_mt.txt`

> Workpiece and tool measurement can happen before, during, and after machining tasks.

**适用限制：** 产品或公司自述，非独立HR0长期试验；网页检索日期不等于能力首次实现日期。

### D06-S09 · GROB Showcases the Future of Manufacturing at AMB 2026Detail - GROB

- 出处：[GROB](https://www.grobgroup.com/en/news-media/detail/article/grob-showcases-the-future-of-manufacturing-at-amb-2026/)
- 发布：2026-10-08；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_06_07/grob_latest.txt`

> the entire flow of parts in production can be digitally tracked, controlled, and monitored.

**适用限制：** 2026年展会展示与公司新闻，不能外推为完整工厂无人运行或量产验证。

### D06-S10 · Automotive | ABB

- 出处：[ABB](https://www.abb.com/global/en/areas/robotics/industries/automotive)
- 发布：未确认；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_06_07/abb_assembly.txt`

> our inspection systems detect and prevent defective parts from entering the production line.

**适用限制：** 产品或公司自述，非独立HR0长期试验；网页检索日期不等于能力首次实现日期。

### D06-S11 · Digital Twin | Siemens

- 出处：[Siemens](https://www.siemens.com/global/en/products/software/digital-twin.html)
- 发布：未确认；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_06_07/siemens.txt`

> Digital twins in manufacturing create virtual replicas of production processes, equipment and entire factory operations.

**适用限制：** 产品或公司自述，非独立HR0长期试验；网页检索日期不等于能力首次实现日期。

### D07-S01 · Products – Siltronic / perfect silicon solutions

- 出处：[Siltronic](https://www.siltronic.com/en/products.html)
- 发布：未确认；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_06_07/siltronic.txt`

> The wafers are manufactured from monocrystalline silicon ingots that have been made using either the Czochralski process (CZ) or the float

**适用限制：** 产品或公司自述，非独立HR0长期试验；网页检索日期不等于能力首次实现日期。

### D07-S02 · Lithography principles - Technology | ASML

- 出处：[ASML](https://www.asml.com/en/technology/lithography-principles)
- 发布：未确认；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_06_07/asml.txt`

> ASML systems rely on data from sensors as well as diffraction-based and electron beam measurements to optimize chip production.

**适用限制：** 产品或公司自述，非独立HR0长期试验；网页检索日期不等于能力首次实现日期。

### D07-S03 · Our Products | Lam Research

- 出处：[Lam Research](https://www.lamresearch.com/products/our-products/)
- 发布：未确认；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_06_07/lam.txt`

> Creating the tiny, complex chips used in these devices involves the repetition of a core set of processes and includes hundreds

**适用限制：** 产品或公司自述，非独立HR0长期试验；网页检索日期不等于能力首次实现日期。

### D07-S04 · Productsproduct-matrix-animationDocument

- 出处：[Applied Materials](https://www.appliedmaterials.com/us/en/semiconductor/products.html)
- 发布：未确认；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_06_07/applied.txt`

> Our equipment can deposit layers of material on a wafer’s surface to change the properties of the material

**适用限制：** 产品或公司自述，非独立HR0长期试验；网页检索日期不等于能力首次实现日期。

### D07-S05 · Products | KLA

- 出处：[KLA](https://www.kla.com/products)
- 发布：未确认；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_06_07/kla.txt`

> Our process-control and process-enabling solutions are designed to boost the innovation speed of the electronics industry.

**适用限制：** 产品或公司自述，非独立HR0长期试验；网页检索日期不等于能力首次实现日期。

### D07-S06 · CoWoS® - Taiwan Semiconductor Manufacturing Company Limited

- 出处：[TSMC](https://www.tsmc.com/english/dedicatedFoundry/technology/cowos)
- 发布：未确认；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_06_07/tsmc.txt`

> This wafer level system integration platform offers wide range of interposer sizes, number of HBM cubes, and package sizes.

**适用限制：** 该CoWoS介绍含2019年历史规格；仅证明封装技术路径，不把其中HBM2规格当作2026年前沿。

### D07-S07 · SK hynix Announces 3Q26 Financial Results – SK hynix NewsroomSK hynix Newsroom | SK hynix Announces 3Q26 Financial Results

- 出处：[SK hynix](https://news.skhynix.com/en/q3-2026-business-results/)
- 发布：2026-10-28；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_06_07/skhynix_q3.txt`

> By product, DRAM results were driven by a significant increase in sales of server DDR5 while HBM4 shipments began in earnest.

**适用限制：** 公司2026Q3业绩新闻中的出货陈述，未独立核验产量，不等于无人制造；未来扩产与Q4预测单列为计划。

### D07-S08 · 2nm Technology - Taiwan Semiconductor Manufacturing Company Limited

- 出处：[TSMC](https://www.tsmc.com/english/dedicatedFoundry/technology/logic/l_2nm)
- 发布：未确认；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_06_07/tsmc_n2.txt`

> TSMC’s 2nm (N2) technology has started volume production in 4Q25 as planned.

**适用限制：** 当前官方技术页；量产时间取正文，不使用明显占位的1970网页元数据。量产不等于HR0自治。

### D07-S09 · NVIDIA to Manufacture American-Made AI Supercomputers in US for First Time | NVIDIA Blog

- 出处：[NVIDIA](https://blogs.nvidia.com/blog/nvidia-manufacture-american-made-ai-supercomputers-us/)
- 发布：2025-04-14；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_06_07/nvidia.txt`

> The AI chip and supercomputer supply chain is complex and demands the most advanced manufacturing, packaging, assembly and test technologies.

**适用限制：** 2025年公司公告，区分已开始的晶片生产与当时计划中的服务器工厂；不把12至15个月后预期当成已实现。

### D07-S10 · Dextro™ - Lam Research

- 出处：[Lam Research](https://www.lamresearch.com/product/dextro/)
- 发布：未确认；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_06_07/dextro.txt`

> Delivered as part of a term-based service contract, cobots working with humans provide the ideal synergy

**适用限制：** 产品或公司自述，非独立HR0长期试验；网页检索日期不等于能力首次实现日期。

### D07-S11 · Lam Research Introduces the Semiconductor Industry's First Collaborative Robot for Fab Maintenance Optimization - Dec 10, 2024

- 出处：[Lam Research](https://investor.lamresearch.com/2024-12-10-Lam-Research-Introduces-the-Semiconductor-Industrys-First-Collaborative-Robot-for-Fab-Maintenance-Optimization)
- 发布：2024-12-10；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_06_07/dextro_release.txt`

> Dextro is a mobile unit with a robotic arm operated by a fab technician or engineer.

**适用限制：** 官方发布称已部署多个晶圆厂，同时明确由技术员或工程师操作；仅支持部分维护任务机器人化。

### D07-S12 · AI-driven predictive maintenance: Solving semiconductor fab uptime challenges - Electronics & Semiconductors

- 出处：[Siemens](https://blogs.sw.siemens.com/electronics-semiconductors/2026/08/13/ai-driven-predictive-maintenance-solving-semiconductor-fab-uptime-challenges/)
- 发布：2026-08-13；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_06_07/siemens_pm.txt`

> LLM-supported troubleshooting helps retain and transfer shop-floor knowledge

**适用限制：** 供应商技术博客与宣称收益，不是独立长期HR0试验；提前告警、排故建议仍由维护团队执行。

### D07-S13 · SK hynix Hosts First Partners Day in Japan, Sharing Business Direction with Key Local Partners – SK hynix NewsroomSK hynix Newsroom | SK hynix Hosts First Partners Day in Japan, Sharing Business Direction with Key Local Partners

- 出处：[SK hynix](https://news.skhynix.com/en/2026-partners-day-japan/)
- 发布：2026-10-30；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_06_07/skhynix_partners.txt`

> close collaboration with our materials, components, and equipment partners is key to semiconductor competitiveness.

**适用限制：** 产业供应链协作的现实证据；证明外部合作存在，不量化每个工序的人类参与比例。

### D08-S01 · A Steerable Model with Emergent Capabilities

- 出处：[Physical Intelligence](https://www.pi.website/blog/pi07)
- 发布：2026-04-16；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_08_10/pi07.txt`

> it can follow new language commands and perform tasks that were never seen in its training data.

**适用限制：** 开发者自报的具体机器人实验；泛化不等于无需人类训练、维修和供能。

### D08-S02 · VLAs with Long and Short-Term Memory

- 出处：[Physical Intelligence](https://www.pi.website/research/memory)
- 发布：2026-03-03；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_08_10/pimemory.txt`

> track of tasks up to fifteen minutes in length, keep both short-term and

**适用限制：** 记忆增强操作任务最长约十五分钟；不能外推到设备寿命或跨代连续性。

### D08-S03 · Gemini Robotics — Google DeepMind

- 出处：[Google DeepMind](https://deepmind.google/models/gemini-robotics/)
- 发布：未确认；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_08_10/deepmindrobotics.txt`

> Gemini Robotics 2 is the next step on our journey towards general, useful robotics.

**适用限制：** 现行产品页未给出发布日期或独立工业长期运行记录；仅记录核验日可见的模型声明。

### D08-S04 · Egocentric visual self-modeling for autonomous robot dynamics prediction and adaptation | npj Robotics Close banner Close banner

- 出处：[npj Robotics / Nature Portfolio](https://www.nature.com/articles/s44182-025-00031-6)
- 发布：2025-06-13；获取：2026-11-02；类型：Paper；核查范围：full_text。
- 核查文本：`.research_cache/domains_08_10/naturefull.txt`

> Notably, the robot can autonomously detect anomalies, such as damaged components, and adapt its behavior, showcasing resilience in dynamic environments.

**适用限制：** 12自由度机器人实验的损伤识别和行为适应；不是机械部件自我制造与更换。

### D08-S05 · Robot metabolism: Toward machines that can grow by consuming other machines

- 出处：[Science Advances / AAAS (Europe PMC full text)](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12266095/fullTextXML)
- 发布：2025-07-16；获取：2026-11-02；类型：Paper；核查范围：full_text。
- 核查文本：`.research_cache/domains_08_10/metabolismxml.txt`

> The Truss Links were operator controlled in all physical Truss Link experiments using a custom keyboard interface.

**适用限制：** 全文方法明确全部物理Truss Link实验由操作者键盘控制。模块生长/重构以已有机电模块为材料，不能证明自主维修、由原料制造模块或工业闭环。

### D08-S06 · Amazon deploys over 1 million robots and launches new AI foundation model

- 出处：[Amazon](https://www.aboutamazon.com/news/operations/amazon-million-robots-ai-foundation-model)
- 发布：2025-07-01；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_08_10/amazon.txt`

> Amazon has deployed its one millionth robot in its operations.

**适用限制：** 公司部署规模与DeepFleet声明；同文明确机器人与员工协作，并需要可靠性、维修、工程岗位。

### D08-S07 · Safety Impact

- 出处：[Waymo](https://waymo.com/safety/impact/)
- 发布：未确认；获取：2026-11-02；类型：field-data；核查范围：documentation。
- 核查文本：`.research_cache/domains_08_10/waymo.txt`

> Through June 2026, Waymo has driven 271.3M rider-only miles without a human driver

**适用限制：** 公司持续更新的公开运行数据，截至2026年6月；驾驶无驾驶员不等于无远程支持、车队维修或道路供应。

### D08-S08 · Yara Birkeland, two years on | Yara International

- 出处：[Yara International](https://www.yara.com/knowledge-grows/yara-birkeland-two-years-on/)
- 发布：2024-05-01；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_08_10/yaratwoyears.txt`

> Yara Birkeland is not completely autonomous yet, mooring of the ship is still done manually,

**适用限制：** HTML发布日期为2024-05-01、可见正文显示April28及后续2026展望，存在更新日期不清的问题；仅据页面确认有人监督与系泊边界，不断言2026仍完全相同。

### D08-S09 · Autonomous Delivery Technology | Zipline

- 出处：[Zipline](https://www.flyzipline.com/technology)
- 发布：未确认；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_08_10/zipline.txt`

> Each Zipline flies up to 70 mph on a direct path, independent of ground traffic.

**适用限制：** 当前公司技术页面，未给出发布日期、无人维护指标或闭环制造证据；飞行和配送技术不能代替维修供能闭环。

### D08-S10 · Frontier Models for Every Robot: Announcing our API beta

- 出处：[Physical Intelligence](https://www.pi.website/blog/api-beta)
- 发布：2026-10-13；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_08_10/piapi.txt`

> Here, Axol deburrs spacers used in its own assembly,

**适用限制：** 2026年10月开发者应用展示；自身部件去毛刺仅是一个工序，数据收集、微调、网络和云推理仍依赖人类企业。

### D08-S11 · [2609.26157] Toward User-Mediated Self-Repair in Ubiquitous Robots Through Goal-Oriented Agentic AI

- 出处：[arXiv](https://arxiv.org/abs/2609.26157)
- 发布：未确认；获取：2026-11-02；类型：Paper；核查范围：abstract。
- 核查文本：`.research_cache/domains_08_10/arxivrepairabs.txt`

> Toward User-Mediated Self-Repair in Ubiquitous Robots Through Goal-Oriented Agentic AI

**适用限制：** 预印本讨论以语言指导非专家人类维修；不能作为HR0物理自修复的正面证据。页面标示时间与标识符年月不一致，因此不填写推定发表日。

### D09-S01 · Chronos: Pretrained Models for Time Series Forecasting

- 出处：[Amazon Science / Chronos Contributors](https://raw.githubusercontent.com/amazon-science/chronos-forecasting/main/README.md)
- 发布：未确认；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_02_09/D09-S01.txt`

> zero-shot support for univariate, multivariate, and covariate-informed forecasting tasks.

**适用限制：** README含2026-06-05云部署更新；发布日期采用单独论文来源，不将云端可用性视为物理自治。

### D09-S02 · linprog(method=’highs’) — SciPy v1.18.0 Manual

- 出处：[SciPy Developers](https://docs.scipy.org/doc/scipy/reference/optimize.linprog-highs.html)
- 发布：未确认；获取：2026-11-02；类型：other；核查范围：documentation。
- 核查文本：`.research_cache/domains_02_09/D09-S02.txt`

> Linear programming: minimize a linear objective function subject to linear equality and inequality constraints using one of the HiGHS solvers.

**适用限制：** v1.18.0文档构建日2026-06-19；构建日不等于算法首次发布或自治工业部署。

### D09-S03 · Welcome to x402 - x402

- 出处：[x402 Foundation / Contributors](https://docs.x402.org/introduction)
- 发布：未确认；获取：2026-11-02；类型：other；核查范围：documentation。
- 核查文本：`.research_cache/domains_02_09/D09-S03.txt`

> Native support for machine-to-machine payments

**适用限制：** 开放协议及程序化支付流程说明；交易依赖链、资金、服务提供者和计算基础设施。

### D09-S04 · How to set up on-chain governance | OpenZeppelin Docs OpenZeppelin Logo Ethereum Icon GitHub Icon OpenZeppelin Logo GitHub Icon Anthropic

- 出处：[OpenZeppelin](https://docs.openzeppelin.com/contracts/5.x/governance)
- 发布：未确认；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_02_09/D09-S04.txt`

> create proposals, vote for them, and execute them

**适用限制：** Governor合约执行既定治理流程；提案形成、投票参与与物理执法是否无人均未获证明。

### D09-S05 · The Job Shop Problem  |  OR-Tools  |  Google for Developers Google Google

- 出处：[Google OR-Tools](https://developers.google.com/optimization/scheduling/job_shop)
- 发布：未确认；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_02_09/D09-S05.txt`

> The job shop scheduling problem involves optimizing the allocation of machines to tasks within multiple jobs

**适用限制：** 约束求解教学实例；证明计算排程方法，不证明自主工厂的完整生产控制。

### D09-S06 · Project Agorá | Bank for International Settlements

- 出处：[Bank for International Settlements](https://www.bis.org/project/agora)
- 发布：2026-05-27；获取：2026-11-02；类型：government；核查范围：full_text。
- 核查文本：`.research_cache/domains_02_09/D09-S06.txt`

> Project Agorá conducted RVT in July 2026.

**适用限制：** 项目页显示Last updated2026-05-27但已包含July2026实值测试和2026-10-29相关更新；正文仍明确人为合规、外汇确认与操作窗口。

### D09-S07 · Purchase — Odoo 19.0 documentation

- 出处：[Odoo](https://www.odoo.com/documentation/19.0/applications/inventory_and_mrp/purchase.html)
- 发布：未确认；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_02_09/D09-S07.txt`

> helps keep track of purchase agreements, quotations, and purchase orders.

**适用限制：** Odoo19功能文档，采购软件不等于供应商、制造、交付和合同执行实现HR0。

### D09-S08 · Reordering rules — Odoo 19.0 documentation

- 出处：[Odoo](https://www.odoo.com/documentation/19.0/applications/inventory_and_mrp/inventory/warehouses_storage/replenishment/reordering_rules.html)
- 发布：未确认；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_02_09/D09-S08.txt`

> request for quotation (RFQ) is created when the reordering rule is triggered.

**适用限制：** 最低/最高库存触发补货单的机制，不证明实际库存、供应链或仓储物理自治。

### D09-S09 · Getting Started | Nexus Mutual Documentation

- 出处：[Nexus Mutual](https://docs.nexusmutual.io/)
- 发布：未确认；获取：2026-11-02；类型：company-doc；核查范围：documentation。
- 核查文本：`.research_cache/domains_02_09/D09-S09.txt`

> Members pool capital, buy cover against on-chain and real world risks

**适用限制：** 相互保险协议为成员治理和裁量理赔；不是无人核赔或无人重建工厂的证据。

### D09-S10 · III. The next-generation monetary and financial system

- 出处：[Bank for International Settlements](https://www.bis.org/publications/aer-2025/next-generation-monetary-financial-system)
- 发布：2025-06-29；获取：2026-11-02；类型：government；核查范围：full_text。
- 核查文本：`.research_cache/domains_02_09/D09-S10.txt`

> Stablecoins also fare poorly on singleness and elasticity.

**适用限制：** 央行年度经济报告的制度分析；不提供机器经济宏观自治实测。

### D09-S12 · [2510.15821] Chronos-2: From Univariate to Universal Forecasting

- 出处：[Chronos-2 Research Authors / arXiv](https://arxiv.org/abs/2510.15821)
- 发布：2025-10-17；获取：2026-11-02；类型：Paper；核查范围：abstract。
- 核查文本：`.research_cache/domains_02_09/D09-S12.txt`

> a pretrained model capable of handling univariate, multivariate, and covariate-informed forecasting tasks in a zero-shot manner.

**适用限制：** 论文摘要提供预测任务与基准范围；不将预测性能外推为生产执行或工业闭环。

### D09-S14 · Payments in the age of AI agents | Bank for International Settlements

- 出处：[Christopher J Waller / Federal Reserve, hosted by BIS](https://www.bis.org/speeches/20261005-payments-age-ai-agents)
- 发布：2026-10-05；获取：2026-11-02；类型：government；核查范围：full_text。
- 核查文本：`.research_cache/domains_02_09/D09-S14.txt`

> Market participants broadly agree that agentic commerce is in an early phase

**适用限制：** 2026-10-05官方演讲；区分agent-assisted和agent-delegated，仍依赖授权、责任和欺诈控制。

### D09-S15 · Agents of change − speech by Sarah Breeden | Bank of England – the UK's central bank

- 出处：[Bank of England / Sarah Breeden](https://www.bankofengland.co.uk/speech/2026/june/sarah-breeden-panel-at-the-european-central-bank-forum-on-central-banking-2026)
- 发布：2026-06-30；获取：2026-11-02；类型：government；核查范围：full_text。
- 核查文本：`.research_cache/domains_02_09/D09-S15.txt`

> The financial system looks likely therefore to evolve quickly into one that operates more autonomously

**适用限制：** 官方演讲中的趋势、风险和政策讨论，不是已建立自治机器经济的实证结果。

### D09-S17 · Mastercard launches Agent Pay for Machines to unlock super-fast, always-on payments | Mastercard Global

- 出处：[Mastercard](https://www.mastercard.com/global/en/news-and-trends/press/2026/june/mastercard-launches-agent-pay-for-machines.html)
- 发布：2026-06-10；获取：2026-11-02；类型：company-doc；核查范围：full_text。
- 核查文本：`.research_cache/domains_02_09/D09-S17.txt`

> these transactions are programmatic, always-on and executed between systems

**适用限制：** 服务提供者发布公告；多处使用will/envisions未来表述，不能当作已完成独立机器经济的证据。

### D09-S18 · Inside x402: 100M Agentic Payments on Base - Chainalysis Chainalysis

- 出处：[Chainalysis](https://www.chainalysis.com/blog/x402-agentic-payments-adoption/)
- 发布：2026-06-03；获取：2026-11-02；类型：company-doc；核查范围：full_text。
- 核查文本：`.research_cache/domains_02_09/D09-S18.txt`

> Much of the growth was driven by meme coin farming activity.

**适用限制：** 按链上x402交互识别交易的商业分析；交易量不等于独立机器主体数量或实物经济活动。

### D09-S19 · x402 and Agentic Commerce: Redefining Autonomous Payments in Financial Services | AWS for Industries

- 出处：[Amazon Web Services](https://aws.amazon.com/blogs/industries/x402-and-agentic-commerce-redefining-autonomous-payments-in-financial-services/)
- 发布：2026-03-15；获取：2026-11-02；类型：company-doc；核查范围：full_text。
- 核查文本：`.research_cache/domains_02_09/D09-S19.txt`

> x402 and Agentic Commerce: Redefining Autonomous Payments in Financial Services

**适用限制：** 供应商架构文章，更新于2026-05-11；不视为无人在场的端到端工业运行验证。

### D10-S01 · NASA’s Oxygen-Generating Experiment MOXIE Completes Mars Mission - NASA

- 出处：[NASA](https://www.nasa.gov/missions/mars-2020-perseverance/nasas-oxygen-generating-experiment-moxie-completes-mars-mission/)
- 发布：2023-09-06；获取：2026-11-02；类型：government；核查范围：documentation。
- 核查文本：`.research_cache/domains_08_10/moxie.txt`

> MOXIE has generated a total of 122 grams of oxygen

**适用限制：** 火星大气制氧的特定设备试验，共16次运行；并未完成氧液化储存、设备再制造或全资源链闭环。

### D10-S02 · Robot Team Builds High-Performance Digital Structure for NASA - NASA

- 出处：[NASA](https://www.nasa.gov/general/robot-team-builds-high-performance-digital-structure-for-nasa/)
- 发布：2024-01-17；获取：2026-11-02；类型：government；核查范围：documentation。
- 核查文本：`.research_cache/domains_08_10/armadasdemo.txt`

> The system builds and error-corrects on its own with no machine vision or external means of measurement,

**适用限制：** 地面技术演示，外供预制体素、结构计划与机器人；太阳能/栖居地等多为后续计划或艺术概念图。

### D10-S03 · CADRE | NASA Jet Propulsion Laboratory (JPL)

- 出处：[NASA Jet Propulsion Laboratory](https://www.jpl.nasa.gov/missions/cadre/)
- 发布：未确认；获取：2026-11-02；类型：government；核查范围：documentation。
- 核查文本：`.research_cache/domains_08_10/cadre.txt`

> Status
Future

**适用限制：** 核验页面仍标示Future；三车月面协作是计划中的技术验证，不能写作已完成月面自主扩张。

### D10-S04 · Advanced Automation for Space Missions - NASA Technical Reports Server (NTRS)

- 出处：[NASA](https://ntrs.nasa.gov/citations/19830007077)
- 发布：1982-11-01；获取：2026-11-02；类型：government；核查范围：abstract。
- 核查文本：`.research_cache/domains_08_10/ntrsseed.txt`

> The feasibility of using machine intelligence, including automation and robotics, in future space missions was studied.

**适用限制：** 历史研究报告的概念与可行性讨论，不是已建成种子工厂或当代工业复制运行证据。

### D10-S05 · In-Space Servicing, Assembly, and Manufacturing (ISAM) State of Play -  2025 Edition - NASA Technical Reports Server (NTRS)

- 出处：[NASA](https://ntrs.nasa.gov/citations/20250008988)
- 发布：2025-10-01；获取：2026-11-02；类型：government；核查范围：abstract。
- 核查文本：`.research_cache/domains_08_10/nasaisam2025.txt`

> In-space Servicing, Assembly, and Manufacturing (ISAM) can vastly expand the performance, availability,

**适用限制：** 2025状态综述的公开摘要，服务/组装延长资产寿命不能直接证明从原料复制全部工业体系。

### D10-S06 · Self Replication - Creative Machines Lab - Columbia University

- 出处：[Columbia University Creative Machines Lab](https://www.creativemachineslab.com/self-replication.html)
- 发布：未确认；获取：2026-11-02；类型：other；核查范围：documentation。
- 核查文本：`.research_cache/domains_08_10/selfreplab.txt`

> except for replenishing building blocks at the two 'feeding' locations circled in red.

**适用限制：** 实验室项目页包含2005年四模块机器人复制；模块由外部补给，约2.5分钟是给定模块的组装时间，不能充当完整工业代际时间。
