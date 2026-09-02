# Sample from What You See: Visuomotor Policy Learning via Diffusion Bridge with Observation-Embedded SDE (BridgePolicy)

> Liu, Pan, Wang, Zhu, Lu, Zhang, Wang, Shi (上科大 & InstAdapt), ICML 2026。[arXiv:2512.07212](https://arxiv.org/abs/2512.07212)

## 一句话

把观测从「网络的外挂条件」变成「扩散桥的起点」：用语义对齐器把异构观测映到动作对齐的潜空间，采样从观测先验而非高斯噪声出发，52 个仿真任务 + 5 个真机任务全面胜过 DP/DP3/FlowPolicy——informative source 策略第一次拿到顶会主会。

## 问题与动机

Diffusion Policy 一系把观测只当去噪网络的条件输入，生成过程本身仍从各向同性噪声起步：感知与控制的耦合被压在条件注入这一条窄通道上，且起点的零信息量意味着路径长、精度靠步数堆。桥的语言天然对症——让观测成为一端。障碍是维度错配：扩散桥连接的是同形状分布，机器人观测（点云 + 状态）与动作序列既不同模态也不同维度。

## 方法核心

1. **观测嵌入的桥式前向过程**。沿用 UniDB 的随机最优控制（SOC）统一桥框架：把「从动作 $a_0$ 走到观测潜表示 $z_{\text{obs}}$」写成受控 SDE 的最小能量 + 终端惩罚问题（Doob h-变换是其特例）。给定两端，$a_t$ 的条件分布有高斯闭式（形如 I2SB 的桥后验，均值在 $a_0$ 与 $z_{\text{obs}}$ 之间按噪声方差比插值）——训练即在这条桥上采样中间点、回归去噪目标，和 DDPM 训练同构；推理从 $a_T = z_{\text{obs}}$ 出发逆向走到动作。
2. **模态融合 + 语义对齐器**。点云经最远点采样降至 512-2048 点、轻量 MLP 编码；机器人状态另行编码；两者融合后由对齐器映射到与动作序列同形状的潜向量集，并加对齐损失把观测表示拉向动作表示的语义空间——这一步让「异构观测当桥端点」在数学上合法。
3. 总损失 = 桥去噪损失 + $\alpha\cdot$ 对齐损失；NFE 设为 10（与基线一致）。

## 实验与证据

- 52 仿真任务（MetaWorld 四难度 + DexArt + Adroit）：平均成功率 0.74，对比 FlowPolicy 0.68、VITA 0.64、DP3 0.60、DP 0.37；MetaWorld Very Hard 0.79 vs DP3 0.51，Adroit 0.81 vs DP3 0.68。
- 5 个真机任务（开/关烤箱、抓放、倒水、拔插头）：一致优于 DP3/FlowPolicy，定性图显示 DP3 多次尝试才抓到把手而 BridgePolicy 一次到位。
- 消融：模态融合方式与对齐器设计对结果影响显著，说明「让观测合法地成为端点」是关键而非可有可无。

## 在谱系中的位置

- 上游：[I2SB](../2302.05872_i2sb/)（informative 边界的图像先例）、UniDB/Doob h-变换桥、[Diffusion Policy](../2303.04137_diffusion_policy/)（被替代的条件范式）。
- 平行：[RSBM](../2604.05673_rsbm/)（导航侧的桥式先验 + few-step）。
- 本仓库定位：07 类雷达中最重要的一篇——知识库 2026-04 起押注的「边界即条件」路线被 ICML 正面验证。

## 与 SB×RL 的关联

BridgePolicy 证实了 informative source 在操纵任务上的实际红利，但它恰好停在了 SB×RL 最关心的两处之前：(1) **无 few-step**——NFE 固定 10，没有利用桥式起点缩短路径的少步潜力（RSBM 在导航上做到 3 步，操纵上无人做）；(2) **无 RL**——纯模仿，观测先验起步与 path-space RL（GSB-MDPO/FLAC）的组合是空格。注意它用的是 Doob h-变换系的 diffusion bridge 而非熵正则 SB（没有 $\epsilon$ 旋钮），评审并不区分——这既提醒「SB 帽子」正在贬值，也留下了「把 $\epsilon$ 谱系装进 BridgePolicy 骨架」这个可讲清的增量。

## 局限与批判

- 观测→动作的「桥」在语义上是牵强的：观测潜表示与动作分布之间没有自然的传输意义，对齐器实质上是在学一个「伪动作先验」——成立的是「学习的 informative 起点 + 桥式训练」，不是观测与动作之间的最优传输。
- NFE=10 与多步基线打平设置，未评估少步区间的表现——informative 起点的核心优势（少步稳）没有被验证。
- 对齐损失权重 $\alpha$、潜向量集形状等设计的敏感性分析不足。
- 纯 BC，不涉及超越示范；多模态保持无量化。
