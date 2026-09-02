# SB×RL 前沿趋势报告（2026-09）

> 检索时间 2026-09-01；覆盖 2026 年 2-8 月 arXiv 与 ICML 2026 已发表工作。每条判断附证据指针。
>
> **2026-09-02 更新**：本报告雷达中的 9 篇论文已全部正式入库为 [07 类](../README.md#2026-前沿雷达趋势报告收录的新变量)（每篇配详细解读），另补入 10 篇谱系前作（Rectified Flow、PRISM、Soft-SB、FQL、Consistency Policy、Flow-GRPO、ReinFlow、DSRL、OMP、FMQ）。仓库总量 32→51。下方雷达条目末尾追加了解读链接。

## TL;DR

1. **一步生成已成默认前提**：2026 年 2-8 月至少 6 篇新工作（MVP、MF-VLA、ReactVLA、MFPO、UCA-Flow、LP-DS 的 flow 后端）默认一步/少步，「多步 vs 一步」的争论结束了，竞争转入一步内部的表达力与 RL 兼容性。
2. **「informative source 策略」上了 ICML 主会**：BridgePolicy（ICML 2026）用 diffusion bridge 把观测嵌入生成动力学、从观测先验而非噪声起步——本知识库押的「桥式起点」方向被顶会正面验证，但它没做 few-step、没做 RL，组合空格还在。
3. **max-ent × 生成式策略赛道开始拥挤**：MFPO（ICML 2026）用平均散度网络硬算 MeanFlow 似然进 SAC 框架，与 FLAC 的免似然动能正则形成正面路线之争；「likelihood-free vs likelihood-approximation」将是 2027 上半年的方法论主战场。
4. **多模态保持开始被量化**：LP-DS（ICML 2026）用 Kozachenko-Leonenko 熵估计量化动作分布多样性——mode coverage 硬指标的空窗正在关闭，要用「SB 保多模态」当卖点的工作必须赶在评测标准固化前出手。
5. **工业界确认「无策略梯度 RL」路线**：Physical Intelligence 的 π*0.6/RECAP 用优势条件化（advantage conditioning）绕开 log π 做真实世界 VLA 改进——与学术界的 path-space 路线殊途同归，都在回避生成式策略的似然。

## 一、新论文雷达（2026 年 2 月后）

### A. 一步/少步策略（MeanFlow 族扩张）

- **MVP: Mean Flow Policy with Instantaneous Velocity Constraint**（[arXiv:2602.13810](https://arxiv.org/abs/2602.13810)，ICLR 2026 Oral；[解读](../papers/2602.13810_mvp/README.md)）——给平均速度场加瞬时速度边界约束（IVC），修 MeanFlow 缺边界条件的病；RoboMimic+OGBench SOTA。证据强度：中（仿真基准全面）。值得跟：是，IVC 是对 MeanFlow 恒等式的实质补丁。
- **MF-VLA: Mean-Flow based One-Step VLA**（[arXiv:2603.01469](https://arxiv.org/abs/2603.01469)，2026-03；[解读](../papers/2603.01469_mf_vla/README.md)）——MeanFlow 动作头进 VLA，真机比 SmolVLA 快 8.7 倍。证据强度：中弱（成功率仅「相当」）。值得跟：作为格局信号看。
- **ReactVLA**（[arXiv:2606.14255](https://arxiv.org/abs/2606.14255)，2026-06；[解读](../papers/2606.14255_reactvla/README.md)）——改进版 MeanFlow（iMF）+ 注意力残差路由，LIBERO/真机延迟 <38.6 ms，胜 SmolVLA/π0。证据强度：中。值得跟：iMF 的改动值得读。
- **UCA-Flow**（[arXiv:2608.16153](https://arxiv.org/abs/2608.16153)，2026-08；[解读](../papers/2608.16153_uca_flow/README.md)）——条件与动作统一进单一 token 序列联合演化，一步生成，平均成功率超最强基线 9.3 pp，比 MP1 快 2.3 倍。证据强度：中强。值得跟：是，条件-动作联合建模可能是一步策略的下一个共识组件。
- **MFPO: Mean Flow Policy Optimization**（[arXiv:2604.14698](https://arxiv.org/abs/2604.14698)，ICML 2026；[解读](../papers/2604.14698_mfpo/README.md)）——MeanFlow 策略进 max-ent RL：平均散度网络近似似然积分 + 自适应瞬时速度估计，MuJoCo/DMC/HumanoidBench 打平或超扩散基线、2 步采样、训练快 ~50%。证据强度：强（ICML + 开源）。**必须跟：与 FLAC 构成 likelihood-approx vs likelihood-free 的直接路线对决。**

### B. Bridge × 具身

- **BridgePolicy: Sample from What You See**（[arXiv:2512.07212](https://arxiv.org/abs/2512.07212)，ICML 2026，ShanghaiTech；[解读](../papers/2512.07212_bridge_policy/README.md)）——观测嵌入 SDE 动力学的 diffusion bridge 策略：从观测先验起步而非噪声，语义对齐器解决观测-动作维度错配；52 仿真任务 + 5 真机任务胜 DP/DP3/FlowPolicy。证据强度：强。**必须跟：informative source 策略的顶会锚点，且明确留下 few-step 与 RL 两个空格。**
- （对照）**RSBM**（本仓库已收录，IEEE TMM）仍是 few-step SB 具身唯一正式文献；BDGxRL 后 sim-to-real SB×RL 未检索到直接后续——该线竞争格局依旧未恶化。

### C. RL 微调路线演化

- **π*0.6 / RECAP**（[arXiv:2511.14759](https://arxiv.org/abs/2511.14759)，Physical Intelligence；[解读](../papers/2511.14759_recap/README.md)）——优势条件化：价值函数打分 → 二值优势 token 条件化 VLA → 推理时永远条件"positive"；免策略梯度、免似然；真实家庭叠衣/装箱/做咖啡，最难任务吞吐翻倍、失败率减半。证据强度：强（真实部署级）。必须跟：工业界对 log π 障碍的答案。
- **LP-DS: Lagrangian Perturbation Diffusion Steering**（[arXiv:2606.01151](https://arxiv.org/abs/2606.01151)，ICML 2026；[解读](../papers/2606.01151_lp_ds/README.md)）——DSRL 的修正：学状态条件的残差噪声扰动 + 拉格朗日信赖域，防 latent 漂出高斯支撑与模式塌缩；RoboMimic/Gym/Adroit 回报最高 +25%，且用 KL 熵估计器量化了行为多样性保持。证据强度：强。值得跟：噪声空间 RL 的成熟形态 + mode coverage 评测先例。
- **DF-ExpEnse**（[arXiv:2606.19656](https://arxiv.org/abs/2606.19656)，2026-06；[解读](../papers/2606.19656_df_expense/README.md)）——DSRL 的探索增强（batch 候选动作按探索兴趣选择）。证据强度：中。可选跟。

### D. 入库时补检到的相关新作

- **FMQ: Aligning Flow Map Policies with Optimal Q-Guidance**（[arXiv:2605.12416](https://arxiv.org/abs/2605.12416)，2026-05；[解读](../papers/2605.12416_fmq/README.md)）——流映射策略统一框架 + 信赖域下 Q 引导的闭式更新，超 MVP 21.3%。**它无意中回答了「一步时代 path-space 邻近项还剩什么」：剩下的就是平均速度场上的信赖域。**
- **PRISM**（[arXiv:2608.06893](https://arxiv.org/abs/2608.06893)，2026-08；[解读](../papers/2608.06893_prism/README.md)）——SB 参考过程设计理论：不可见性原理（参考只在有限步预算下有意义）+ 有限步最优噪声谱。把 SB 的差异化钉死在 few-step 区间。
- **OMP**（[arXiv:2512.19347](https://arxiv.org/abs/2512.19347)，v3 2026-06；[解读](../papers/2512.19347_omp/README.md)）——诊断 MeanFlow 低速区的梯度饥饿，方向对齐修补；对 bridge matching 收口段同样适用。
- 校正：MVP 实为 **ICLR 2026 Oral（top 1%）**，且是 offline-to-online RL 方法（best-of-N 选择 + IVC），不只是训练目标修补——一步族在 RL 侧的分量比雷达初稿估计的更重。

## 二、趋势判断

1. **一步化完成范式化，竞争焦点转向「一步内部」**。现象：半年 6+ 篇一步策略，MeanFlow 族从操纵（MP1/DMPO）扩到 VLA（MF-VLA/ReactVLA）与 RL（MVP/MFPO）。证据：雷达 A 组。含义：任何 SB 策略工作把「少步」当主卖点都会被拒；SB 必须卖一步化做不到的东西——informative source、ε 旋钮、耦合结构。
2. **log π 障碍的四条解法路线成型且开始互相对表**。现象：似然近似（MFPO 的散度网络）、路径空间（FLAC/GSB-MDPO）、噪声空间（DSRL→LP-DS）、条件化监督（RECAP）四条路线各有 2026 年的强代表。证据：雷达 A/C 组。含义：2027 年的评审共识将要求新方法与至少两条既有路线正面对比；path-space 路线目前唯一没有真机与操纵证据，是它的软肋也是补位机会。
3. **informative source 从理念变成主会成果，但只做了 BC 半场**。现象：BridgePolicy 证明观测先验起步在 52 任务上稳定优于噪声起步。证据：雷达 B 组。含义：「bridge 起点 + few-step + RL 微调」的完整技术栈每一环都有文献而组合无人做，竞争窗口预计 6-12 个月。
4. **多模态保持从口号走向指标**。现象：LP-DS 用熵估计器量化行为多样性，DMPO/OFP 等一步工作仍无此评测。证据：雷达 C 组。含义：先把 mode coverage 基准做出来的人拿定义权；SB 的 ε 谱系是天然的实验变量。
5. **工业界与学术界在「绕开似然」上合流**。现象：RECAP（优势条件化）与 GSB-MDPO（路径邻近）从不同出发点得到同一结论——不要碰终端似然。证据：雷达 C 组。含义：SB×RL 的理论价值叙事应该从「解决 log π」升级为「给绕开 log π 的做法提供测度论语义与保证」。

## 三、空白与机会（按可动手程度排序）

1. **One-step SB policy**：MeanFlow 恒等式在桥上的推广（平均漂移场 + informative 边界）。每个零件都有文献（MeanFlow/BridgePolicy/RSBM），组合为空。窗口 6-12 个月（BridgePolicy 组或 MeanFlow 族任何一家都可能顺手做掉）。
2. **Few-step SB × path-space RL**：把 GSB-MDPO/FLAC 内核装进 RSBM/BridgePolicy 的骨架，落到操纵任务对表 DMPO/DBPO。path-space 路线缺操纵与真机证据，这一步同时补位。
3. **Mode coverage 基准**：借 LP-DS 的熵估计 + ε 谱系做系统评测，「一步化的多模态代价」是所有一步工作共同的未答问题。
4. **Sim-to-real 视觉级 SB 翻译**：BDGxRL 停在低维状态，SB Flow 的规模化能力没人接到像素级 sim-to-real + RL。该线自 2026-02 后无新对手，窗口最长但工程最重。
5. **策略感知的桥 / RL 加权耦合**：把 advantage 注入 IMF 的 reciprocal 步端点采样（或 OT-CFM 的 minibatch 耦合），SB 训练循环里做 RL 的原生形态，纯算法空格。

## 四、风险

1. **「SB 帽子」贬值加速**：BridgePolicy 用的是 diffusion bridge（Doob h-变换一系）而非严格 SB，评审已不区分——纯换 loss 的 SB 包装论文死刑，必须有 ε 谱系/耦合结构层面的差异化实验。
2. **path-space 理论位饱和**：FLAC/GSB-MDPO/GSB-PPO（同组 v1）已把「path-KL 上界终端 KL」的直接用法占完，再做纯理论框架没有位置，只剩具身落地。
3. **MeanFlow 族的车轮战**：半年 6 篇的速度意味着任何「对表 MeanFlow」的实验节在投稿时就过时，写作策略上应对表「路线」而非单篇。
4. **一步化可能吃掉 ε 旋钮的价值**：如果 UCA-Flow 式的联合建模把一步质量推到与多步无差，「few-step 区间的 coverage-straightness 权衡」这个 SB 卖点的适用区间会收窄——需要尽快用实验确认 ε 在 1-3 步区间是否仍有可测收益。

## 附：检索记录

- 2026-09-01，WebSearch：`Schrödinger bridge reinforcement learning policy arXiv 2026`（命中 GSB-MDPO v1/v2）
- 2026-09-01，WebSearch：`one-step flow policy robot manipulation RL arXiv 2026 June July August`（命中 OFP、UCA-Flow）
- 2026-09-01，WebSearch：`Schrödinger bridge robot navigation manipulation sim-to-real arXiv 2026`（命中 RSBM v3、RoboSimGS）
- 2026-09-01，WebSearch：`"mean flow" OR "MeanFlow" policy reinforcement learning VLA arXiv 2026`（命中 MF-VLA、ReactVLA、MVP、MP1）
- 2026-09-01，WebSearch：`MFPO "Mean Flow Policy Optimization" arXiv`（命中 2604.14698 + ICML 2026 代码库）
- 2026-09-01，WebSearch：`VLA reinforcement learning fine-tuning 2026 π0.6 RECAP`（命中 2511.14759 + PI 官方博客）
- 2026-09-01，WebSearch：`bridge policy Schrödinger bridge imitation ICML NeurIPS 2026`（命中 BridgePolicy ICML 2026 + ICLR 撤稿前身）
- 2026-09-01，WebSearch：`latent noise space RL diffusion policy DSRL follow-up 2026`（命中 LP-DS、DF-ExpEnse）
- 未检索到：SB×RL 的 NeurIPS 2026 已接收清单（会议九月后才放榜）；BDGxRL 的直接后续（确认该线仍空）。
