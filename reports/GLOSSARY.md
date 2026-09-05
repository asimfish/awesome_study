# 术语表

> 按主题分组。每条给精确定义、一句直觉、在本库里的落点。符号约定：路径测度 $\mathbb{P},\mathbb{Q}$，边际 $\mu,\nu$，动作 $a$，状态/观测 $s,o$。

## A. Schrödinger Bridge 家族

**Schrödinger Bridge（SB）**——在所有两端边际分别为 $\mu,\nu$ 的路径测度中，与参考测度 $\mathbb{Q}$ 相对熵最小者：$\min\{\mathrm{KL}(\mathbb{P}\|\mathbb{Q}):\mathbb{P}_0=\mu,\mathbb{P}_T=\nu\}$。直觉：给定起终点分布，最像参考过程（通常是布朗运动）的随机演化。解是一个 Markov 扩散，drift 由参考过程加一项梯度修正。→ [Léonard](../papers/1308.0215_leonard_survey/README.md)、[SB Foundations](../papers/2603.18992_sb_foundations/README.md)

**静态-动态等价**——路径 KL 沿端点分解为「端点耦合的 KL」+「给定端点后中间路径的 KL」；后者取零当且仅当中间用参考桥填充。于是 SB 只需优化端点耦合（熵正则 OT），中间用参考桥。这是所有「先耦合再匹配」算法（OT-CFM、SF2M、IMF）的依据。

**熵正则 OT / $\epsilon$**——SB 的静态形式 $\min\int c\,d\pi-\epsilon H(\pi)$。$\epsilon\to0$ 退化为 Monge-Kantorovich OT（确定性直路径），$\epsilon$ 大给噪声桥（多模态覆盖）。**$\epsilon$ 谱系**指把它当显式旋钮，在直度与覆盖间连续换挡——SB 相对 MeanFlow 族的核心差异化资产。→ [RSBM](../papers/2604.05673_rsbm/README.md)

**参考过程 $\mathbb{Q}$**——SB 目标里的基准测度，决定「哪条路径便宜」。布朗运动最常见；也可以是预训练模型的路径测度（informed reference）或高熵过程（FLAC）。**不可见性原理**（PRISM）：精确漂移 + 无限步下任何合法参考给同一后验，参考只在有限步预算下有意义。→ [PRISM](../papers/2608.06893_prism/README.md)

**广义 SB（GSB）**——在 SB 目标上加路径费用 $\int\mathbb{E}[V_t(x_t)]dt$ 或把硬终端约束换成软势 $-\mathbb{E}[\mathcal{G}(x_T)]$。RL 接口就在这里：$\mathcal{G}=Q$、$V_t=$ 代价。→ [GSBM](../papers/2310.02233_gsbm/README.md)、[Soft-SB](../papers/2403.01717_soft_sb/README.md)

**Soft-constrained SB 的几何混合定理**——终端约束换成 KL 惩罚后，最优终端分布是目标与参考终端的几何混合 $\propto\mu^{a}\nu^{b}$。翻译到 RL 就是 KL 正则策略改进的闭式解形式。→ [Soft-SB](../papers/2403.01717_soft_sb/README.md)

**Reciprocal 过程**——给定两端点后中间路径服从参考桥、区间内外条件独立的路径测度。**SB 解是唯一既 reciprocal 又 Markov 的测度**——IMF 算法的理论基础。

**半桥（half-bridge）**——只钉住一端边际的 KL 最小化问题，解是「上一轮过程时间反演后换起点」。IPF 交替解两个半桥。→ [DSB](../papers/2106.01357_dsb/README.md)

**Girsanov 动能恒等式**——参考为（尺度化）布朗运动、受控过程加漂移 $u$ 时，$\mathrm{KL}(\mathbb{P}^u\|\mathbb{Q})=\mathbb{E}\int\frac{\|u\|^2}{2\sigma^2}dt$。路径 KL = 漂移能量，**不算任何密度**。FLAC 用它替代策略熵，GSB-MDPO 用它把邻近项化成 drift-MSE。→ [FLAC](../papers/2602.12829_flac/README.md)

**数据处理不等式（路径 KL ≥ 端点 KL）**——$\mathrm{KL}(\mathbb{P}\|\mathbb{Q})\ge\mathrm{KL}(\mathbb{P}_T\|\mathbb{Q}_T)$。约束路径就约束了执行动作分布——path-space RL 的合法性来源。→ [GSB-MDPO](../papers/2603.21621_gsb_mdpo/README.md)

**Feynman-Kac 重加权**——GSB 的最优解等价于把参考测度按 $\exp(\mathcal{G}(x_T)-\int V\,dt)$ 重加权后再求 SB。「奖励塑形 = 改终端势」的严格版本；RECAP 的优势条件化、AWR 的指数加权都可以看作它的离散实现。

## B. 求解器

**IPF（Iterative Proportional Fitting / Sinkhorn）**——交替投影到两个边际约束的经典 SB 数值解法。**神经 IPF** = DSB：交替训练前向/反向 drift 网络。缺点：拟合误差让边际漂移。→ [DSB](../papers/2106.01357_dsb/README.md)

**IMF（Iterative Markovian Fitting）**——在 Markov 类与 reciprocal 类之间交替投影：reciprocal 投影保留当前端点耦合、中间用参考桥重填（纯采样）；Markov 投影把桥混合回归成一个 SDE 的 drift（纯回归）。两步都不动边际，修复了 IPF 的漂移。**α-IMF**（SB Flow）是它的小步幅在线离散化，单网络免重训。**D-IMF**（ASBM）是离散时间对抗版。→ [DSBM](../papers/2303.16852_dsbm/README.md)、[SB Flow](../papers/2409.09347_sb_flow/README.md)、[ASBM](../papers/2405.14449_adv_sbm/README.md)

**Bridge matching**——给定端点对，在参考桥上采中间点、回归指向端点的 drift。与 DDPM 训练同构；I2SB 在 paired 数据下免迭代，DSBM 把它当 Markov 投影用。

**Simulation-free**——训练不需要 SDE/ODE rollout。SF2M 用 minibatch 熵 OT 耦合 + 布朗桥闭式做到；**只指训练**，与推理少步无关。→ [SF2M](../papers/2307.03672_sf2m/README.md)

**Rectification / Reflow**——用当前流生成的端点对重训，耦合的传输代价不增且趋于确定性，路径越来越直。RSBM 的「桥矫正」借此名，实质是缩放桥方差（$\epsilon$）。→ [Rectified Flow](../papers/2209.03003_rectified_flow/README.md)

**Informative source / 边界即条件**——把结构化信息（退化图、上一 chunk、观测潜表示、sim 轨迹）当桥的起点而非网络的条件输入。起点近则路径短、少步稳。→ [I2SB](../papers/2302.05872_i2sb/README.md)、[BridgePolicy](../papers/2512.07212_bridge_policy/README.md)

## C. 一步生成

**MeanFlow 恒等式**——区间平均速度 $u(z_t,r,t)=\frac{1}{t-r}\int_r^tv\,d\tau$ 满足 $u=v-(t-r)\frac{d}{dt}u$，全导数用一次 JVP 算。免蒸馏训练、一步采样 $z_0=z_1-u(z_1,0,1)$。→ [MeanFlow](../papers/2505.13447_meanflow/README.md)

**边界条件缺失 / IVC**——恒等式是关于 $u$ 的一阶 ODE，只在 $t<r$ 上提供动力学，解可差一项 $C/(r-t)$。瞬时速度约束（$t=r$ 时 $u=v$）作为边界条件补上。→ [MVP](../papers/2602.13810_mvp/README.md)

**梯度饥饿**——MSE 对方向误差的梯度 $\propto\rho\rho^*\sin\alpha$，目标速度模长 $\rho^*$ 小时方向几乎得不到监督，网络宁可压模长也不修方向。精细低速动作首当其冲；桥的收口段同病。→ [OMP](../papers/2512.19347_omp/README.md)

**Flow map / 流映射策略**——任意两时刻间的跳跃算子 $X_{r,t}$，MeanFlow、Shortcut、consistency 都是其参数化特例。→ [FMQ](../papers/2605.12416_fmq/README.md)

**Consistency 蒸馏**——沿同一 PF-ODE 的不同点去噪到同一时刻应重合；从多步教师蒸馏一步学生。两阶段、上限受教师锁定。→ [Consistency Policy](../papers/2405.07503_consistency_policy/README.md)

**Drift 固定点**——生成器向「被反对称漂移场推一步的自己」回归，把迭代修正内化进参数。→ [DBPO](../papers/2604.03540_dbpo/README.md)

**Dispersive 正则**——batch 内状态表征互斥的对比式损失，防一步生成的表征塌缩。→ [MP1](../papers/2507.10543_mp1/README.md)、[DMPO](../papers/2601.20701_dmpo/README.md)

**NFE**——网络前向次数。真机控制频率的直接决定量；1-NFE 时 Hz 由 backbone 决定，性能锚应改为多模态覆盖等硬指标。

## D. RL 侧接口

**log π 障碍**——生成式策略的动作是 SDE/ODE 终端边际，$\log\pi(a|s)$ 只有 ELBO 或需解 ODE 积分散度，策略梯度/熵正则/ratio 全部失效。本库主线问题。五条绕法见 [DIGEST](DIGEST.md)。

**Denoising-as-MDP / 两层 MDP**——去噪链每步当内层动作，逐步高斯似然可算，PPO 直接套。horizon 乘以步数、credit 均摊。→ [DPPO](../papers/2409.00588_dppo/README.md)

**Mirror descent 策略优化**——$\pi_{k+1}=\arg\max\mathbb{E}[A]-\frac{1}{\eta}\mathrm{KL}(\pi\|\pi_k)$，KL 邻近项显式进目标（TRPO 是约束版、PPO clip 是启发式近似）。路径空间版 = GSB-MDPO。→ [MDPO](../papers/2005.09814_mdpo/README.md)

**Max-ent RL / energy-based 最优策略**——$\pi^*\propto\exp(Q/\alpha)$，Boltzmann 分布；与 SB 解的指数重加权是同一对象在动作/路径两层的投影。FLAC 把它做成严格版。→ [SAC](../papers/1801.01290_sac/README.md)

**Advantage-weighted / 优势条件化**——$\exp(A/\lambda)$ 当 BC 权重（AWR）或二值优势当条件 token（RECAP）。只需 BC 梯度，不需要 ratio；上限是数据里最好的行为。→ [AWR](../papers/1910.00177_awr/README.md)、[RECAP](../papers/2511.14759_recap/README.md)

**Group-relative advantage**——组内标准化回报当优势，免 critic。→ [GRPO](../papers/2402.03300_grpo/README.md)、[Flow-GRPO](../papers/2505.05470_flow_grpo/README.md)

**噪声空间 RL / Diffusion steering**——冻结解码器，RL 学初始噪声。LP-DS 的残差 + 信赖域修正防 latent 漂移与模式坍缩。→ [DSRL](../papers/2506.15799_dsrl/README.md)、[LP-DS](../papers/2606.01151_lp_ds/README.md)

**生成-选择（best-of-N）**——采 N 个候选按 Q 选，改进靠选择压力，Q 梯度不穿生成器。FMQ 给出信赖域下的闭式替代。→ [MVP](../papers/2602.13810_mvp/README.md)、[DF-ExpEnse](../papers/2606.19656_df_expense/README.md)

**Mode coverage**——策略保持多模态的程度。目前唯一系统评测是 LP-DS 的 Kozachenko-Leonenko 动作熵；本库 [P3](OPEN_PROBLEMS.md) 主张建基准。
