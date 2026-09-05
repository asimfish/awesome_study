# 十分钟速览：SB × RL × 机器人策略学习

> 本文是全库 51 篇的压缩版。读完应该能回答三个问题：这个方向的核心矛盾是什么、2026 年格局到了哪一步、还有哪里能打。每个判断后面的链接指向支撑它的详细解读。

## 一、核心矛盾：表达力换来了不可算的似然

机器人动作是多模态的（同一状态下从左绕或从右绕都对），高斯 actor 把模式平均成无效动作。Diffusion Policy（[2303.04137](../papers/2303.04137_diffusion_policy/README.md)）用条件去噪生成 action chunk 解决了这个问题，12 任务平均提升 46.9%，成为事实标准；π0、RDT-1B 等 VLA 的动作头沿用扩散/流。

代价是 RL 用不上了。策略梯度、SAC 的熵项、PPO 的 ratio 全都需要 $\log\pi(a|s)$，而生成式策略的动作是 SDE/ODE 的终端边际——似然要么只有 ELBO（[DDPM](../papers/2006.11239_ddpm/README.md)），要么要沿 ODE 积分散度（[Score-SDE](../papers/2011.13456_score_sde/README.md)），在线训练里都不可承受。本库一半的文献在处理这个后果。

## 二、五条绕开 log π 的路线（2026 年全部成型，本库均有代表）

| 路线 | 做法 | 代表 | 代价 |
|---|---|---|---|
| 逐步分解 | 去噪链拆成内层 MDP，每步高斯似然可算 | [DPPO](../papers/2409.00588_dppo/README.md) · [ReinFlow](../papers/2505.22094_reinflow/README.md) · [Flow-GRPO](../papers/2505.05470_flow_grpo/README.md) · [DMPO](../papers/2601.20701_dmpo/README.md) | horizon 乘以步数、credit 均摊、路径比率方差 |
| 路径空间 | KL/熵正则从动作分布搬到路径测度，Girsanov 化成 drift 能量 | [FLAC](../papers/2602.12829_flac/README.md) · [GSB-MDPO](../papers/2603.21621_gsb_mdpo/README.md) | 上界松紧未量化；只有 locomotion 仿真证据 |
| 噪声空间 | 冻结解码器，RL 只学初始噪声 | [DSRL](../papers/2506.15799_dsrl/README.md) · [LP-DS](../papers/2606.01151_lp_ds/README.md) | 只能在解码器支撑集内挑模式 |
| 条件化/加权监督 | 优势当权重或条件 token，训练变监督 | [AWR](../papers/1910.00177_awr/README.md) · [RECAP](../papers/2511.14759_recap/README.md) · [Diffusion-QL](../papers/2208.06193_diffusion_ql/README.md) | 好不过数据里最好的行为 |
| 生成-选择 | 采 N 个候选按 Q 选，或闭式 Q 引导 | [MVP](../papers/2602.13810_mvp/README.md) · [FMQ](../papers/2605.12416_fmq/README.md) · [DF-ExpEnse](../papers/2606.19656_df_expense/README.md) | 推理成本 ×N |

还有一条正面硬算的路线：[MFPO](../papers/2604.14698_mfpo/README.md) 用平均散度网络一次前向近似似然——它与 FLAC 构成 likelihood-approximation vs likelihood-free 的路线之争，目前互不对比。

## 三、三条线索与各自的 2026 现状

**线索一：一步化——步数竞赛已结束。** [MeanFlow](../papers/2505.13447_meanflow/README.md) 的平均速度场恒等式给出免蒸馏的原生 1-NFE，半年内 [MP1](../papers/2507.10543_mp1/README.md)（操纵）→ [DMPO](../papers/2601.20701_dmpo/README.md)（+PPO，>120 Hz 真机）→ [OFP](../papers/2603.12480_ofp/README.md)（免 JVP 自蒸馏）→ [DBPO](../papers/2604.03540_dbpo/README.md)（drift 固定点，105 Hz 双臂）→ VLA 尺度（[ReactVLA](../papers/2606.14255_reactvla/README.md) 0.39B 在 LIBERO 打 4B 的 π0）。2026 年 2-8 月又出了 6 篇。**任何还拿「少步」当卖点的工作都没有位置。**

**线索二：路径空间——理论位已被占，落地半场没人打。** 两个恒等式撑起整条线：Girsanov 动能恒等式（路径 KL = drift 能量，不算密度）与数据处理不等式（路径 KL ≥ 终端动作 KL）。FLAC 用前者替代 SAC 的熵，GSB-MDPO 用后者做 mirror descent 的邻近项。两篇全部是 locomotion 仿真——操纵、视觉、真机全空。

**线索三：桥式先验——上了顶会，但只做了 BC 半场。** 起点带信息则路径短、少步稳：图像上 [I2SB](../papers/2302.05872_i2sb/README.md) 把 NFE 从几百压到 20；导航上 [RSBM](../papers/2604.05673_rsbm/README.md) 用 $\epsilon$ 旋钮 3 步 92%；操纵上 [BridgePolicy](../papers/2512.07212_bridge_policy/README.md)（ICML 2026）从观测先验起步在 52 任务上胜 DP3/FlowPolicy。三篇都没有 RL，BridgePolicy 也没做 few-step。跨域侧 [BDGxRL](../papers/2602.23737_bdg/README.md) 用 DSB 翻译转移做 sim-to-real，但停在低维状态空间。

## 四、SB 剩下的两个差异化资产

一步化吃掉了「SB 能少步」这个卖点。[PRISM](../papers/2608.06893_prism/README.md) 的不可见性原理进一步说明：无限步下换参考过程毫无意义，参考设计只在有限步预算下有价值。于是 SB 的地盘被精确地钉在 few-step 区间，靶子只剩两个：

1. **Informative source（边界即条件）**：从上一 chunk / 观测潜表示 / 粗规划出发，而不是纯噪声。BridgePolicy 证明了红利，PRISM 给了先验噪声该放在哪个维度的第一条可计算规则。
2. **$\epsilon$ 谱系（coverage-straightness 同一旋钮）**：$\epsilon\to0$ 是确定性 OT 直路径（利于少步），$\epsilon$ 大保多模态覆盖。MeanFlow 族只有确定性极限这一端。RSBM 的 Theorem 1 说速度场形式跨整个谱不变——一个网络通吃。

一切不落在这两点上的「SB 包装」工作都会贬值——评审已经不区分 diffusion bridge 与严格 SB（BridgePolicy 用的是 Doob h-变换系）。

## 五、五个无人占位的格子（按可动手程度排序）

详见 [OPEN_PROBLEMS.md](OPEN_PROBLEMS.md) 的实验设计。

1. **One-step SB policy**：MeanFlow 恒等式在桥上的推广 + informative 边界 + $\epsilon$ 谱。零件全有，组合为空。窗口 6-12 个月。
2. **Few-step SB × path-space RL 落到操纵**：GSB-MDPO/FLAC 内核装进 RSBM/BridgePolicy 骨架，对表 DMPO/DBPO——一次补两个空白。
3. **Mode coverage 基准**：[LP-DS](../papers/2606.01151_lp_ds/README.md) 已开始用动作熵量化多模态保持；先定义评测口径的人拿定义权。
4. **像素级 sim-to-real SB**：BDGxRL 框架 + [SB Flow](../papers/2409.09347_sb_flow/README.md) 的规模化能力，竞争最少、工程最重。
5. **RL 加权耦合**：advantage 注入 IMF 的 reciprocal 步或 OT-CFM 的 minibatch 耦合，SB 训练循环里做 RL 的原生形态。

## 六、补检出的两个新判断

**一步时代 path-space 还剩什么？** [FMQ](../papers/2605.12416_fmq/README.md) 的信赖域闭式解 $u^*=u^{\text{ref}}+\eta\,\nabla_aQ/\|\nabla_aQ\|$、LP-DS 的 latent 偏移约束、GSB-MDPO 的路径 KL 是同一优化问题在三个层面的形式；路径 KL 经 Girsanov 就是速度场 L2，所以 FMQ 恰是 GSB-MDPO 邻近项在一步极限下的样子。写清三者关系本身就是一篇有分量的短文。

**共性病理。** [OMP](../papers/2512.19347_omp/README.md) 证明回归速度/漂移场的方法在低模长区间梯度饥饿（方向梯度 ∝ 目标模长），[MVP](../papers/2602.13810_mvp/README.md) 证明 MeanFlow 恒等式作为一阶 ODE 缺边界条件解不唯一。桥匹配在收口段同病——one-step SB policy 必须内置方向对齐与边界约束，否则精细操纵先输在这里。

## 七、怎么用这个库

- 只有两小时：读本文 + 06 类四篇的「与 SB×RL 的关联」节。
- 要选题：读 [OPEN_PROBLEMS.md](OPEN_PROBLEMS.md)，再读对应格子引用的 3-5 篇。
- 要补基础：按 [READING_PATHS.md](READING_PATHS.md) 里对应你背景的路线走。
- 查公式：[SB Foundations](../papers/2603.18992_sb_foundations/README.md) 解读里的章节地图 + [GLOSSARY.md](GLOSSARY.md)。
- 横向比较：[COMPARISON.md](COMPARISON.md) 的三张表。
