# 术语表

> 按主题分组。每条给精确定义、一句直觉、在本库里的落点。符号约定：路径测度 $\mathbb{P},\mathbb{Q}$，边际 $\mu,\nu$，动作 $a$，状态/观测 $s,o$。

## A. Schrödinger Bridge 家族

**Schrödinger Bridge（SB）**——在所有两端边际分别为 $\mu,\nu$ 的路径测度中，与参考测度 $\mathbb{Q}$ 相对熵最小者：$\min\{\mathrm{KL}(\mathbb{P}\|\mathbb{Q}):\mathbb{P}_0=\mu,\mathbb{P}_T=\nu\}$。直觉：给定起终点分布，最像参考过程（通常是布朗运动）的随机演化。在相应存在条件和扩散参考下，解是 Markov 扩散，drift 由参考漂移加一项按扩散系数缩放的梯度修正。→ [Léonard](../papers/1308.0215_leonard_survey/README.md)、[SB Foundations](../papers/2603.18992_sb_foundations/README.md)

**静态-动态等价**——路径 KL 沿端点分解为「端点耦合的 KL」+「给定端点后中间路径的 KL」；后者取零当且仅当中间用参考桥填充。于是 SB 只需优化端点耦合（参考核为相应 Gibbs 形式时对应熵正则 OT），中间用参考桥。这是 SF2M、IMF 及 OT-CFM 中 SB-CFM 构造的依据。

**熵正则 OT / $\epsilon$**——在相应参考核下，SB 的静态形式为 $\min\int c\,d\pi-\epsilon H(\pi)$。布朗参考下 $\epsilon\to0$ 在适当条件下趋于二次 OT，固定端点间趋于直路径；$\epsilon$ 大增加桥噪声，多模态覆盖仍需验证。**$\epsilon$ 谱系**指把它当显式旋钮，在直度与覆盖间连续换挡——SB 相对 MeanFlow 族的核心差异化资产。→ [RSBM](../papers/2604.05673_rsbm/README.md)

**参考过程 $\mathbb{Q}$**——SB 目标里的基准测度，决定「哪条路径便宜」。布朗运动最常见；也可以是预训练模型的路径测度（informed reference）或高熵过程（FLAC）。**不可见性原理**（PRISM）：在线性高斯复原模型的指定祖先采样器中，贝叶斯最优预测 + 无限步、正参考噪声恢复同一后验；参考噪声影响有限步误差。→ [PRISM](../papers/2608.06893_prism/README.md)

**广义 SB（GSB）**——在 SB 目标上加路径费用 $\int\mathbb{E}[V_t(x_t)]dt$ 或把硬终端约束换成终端 KL 惩罚（Soft-SB）或软势 $-\mathbb{E}[\mathcal{G}(x_T)]$（FLAC）。RL 接口就在软势形式：$\mathcal{G}=Q$、$V_t=$ 代价。→ [GSBM](../papers/2310.02233_gsbm/README.md)、[Soft-SB](../papers/2403.01717_soft_sb/README.md)

**Soft-constrained SB 的几何混合定理**——固定初态为 Dirac 点、终端约束换成权重 $\beta$ 的 KL 惩罚后，最优终端分布是目标与无控参考终端的几何混合 $\propto\mu^{\beta/(1+\beta)}\nu^{1/(1+\beta)}$。与 KL 正则策略改进形式相关，但一般初态还需联立求势。→ [Soft-SB](../papers/2403.01717_soft_sb/README.md)

**Reciprocal 过程**——给定区间两端点后区间内外条件独立的过程；参考 reciprocal 类还要求给定两端点后中间路径服从该参考桥。**在指定两端边际与正则条件下，SB 解是唯一既属该参考 reciprocal 类又 Markov 的测度**——IMF 算法的理论基础。

**半桥（half-bridge）**——只钉住一端边际的 KL 最小化问题，解是「上一轮过程时间反演后换起点」。IPF 交替解两个半桥。→ [DSB](../papers/2106.01357_dsb/README.md)

**Girsanov 动能恒等式**——共享初始分布与非零扩散、满足绝对连续及可积条件，参考为（尺度化）布朗运动、受控过程加漂移 $u$ 时，$\mathrm{KL}(\mathbb{P}^u\|\mathbb{Q})=\mathbb{E}\int\frac{\|u\|^2}{2\sigma^2}dt$。路径 KL = 漂移能量，**不算任何密度**。FLAC 用相关动能正则替代显式熵计算，确定性版只给 Wasserstein 约束；GSB-MDPO 用它把邻近项化成加权 drift-MSE。→ [FLAC](../papers/2602.12829_flac/README.md)

**数据处理不等式（路径 KL ≥ 端点 KL）**——$\mathrm{KL}(\mathbb{P}\|\mathbb{Q})\ge\mathrm{KL}(\mathbb{P}_T\|\mathbb{Q}_T)$。约束路径就约束了执行动作分布——path-space RL 的合法性来源。→ [GSB-MDPO](../papers/2603.21621_gsb_mdpo/README.md)

**Feynman-Kac 重加权**——在匹配温度与费用尺度、状态费用给定时，可把参考测度按 $\exp(\mathcal{G}(x_T)-\int V\,dt)$ 重加权后求相应约束问题；固定初始边际仍需保留。硬约束终端边际时，终端势期望已固定；RECAP 的优势条件化、AWR 的指数加权与这种重加权相关，但未证明是它的离散实现。

## B. 求解器

**IPF（Iterative Proportional Fitting / Sinkhorn）**——交替投影到两个边际约束的经典 SB 数值解法。**神经 IPF** = DSB：交替训练前向/反向转移均值网络。缺点：拟合误差让边际漂移。→ [DSB](../papers/2106.01357_dsb/README.md)

**IMF（Iterative Markovian Fitting）**——在 Markov 类与 reciprocal 类之间交替投影：reciprocal 投影保留当前端点耦合、中间用参考桥重填（纯采样）；Markov 投影把桥混合回归成一个 SDE 的 drift（纯回归）。精确投影都保持两端边际，只有 Markov 投影保持全部单时刻边际；神经近似仍会漂移。**α-IMF**（SB Flow）是它的小步幅在线离散化，可共享双向网络、免整轮重训。**D-IMF**（ASBM）是离散时间对抗版。→ [DSBM](../papers/2303.16852_dsbm/README.md)、[SB Flow](../papers/2409.09347_sb_flow/README.md)、[ASBM](../papers/2405.14449_adv_sbm/README.md)

**Bridge matching**——给定端点对，在参考桥上采中间点、回归指向端点的 drift。与 DDPM 都用条件回归，但标签和桥核不同；I2SB 在 paired 数据下免交替求桥，DSBM 把它当 Markov 投影用。

**Simulation-free**——训练不需要 SDE/ODE rollout。SF2M 用静态 OT 耦合（大量实验为批内无熵正则 OT）+ 布朗桥闭式做到；**只指训练**，与推理少步无关。→ [SF2M](../papers/2307.03672_sf2m/README.md)

**Rectification / Reflow**——用当前流生成的端点对重训，理想拟合下新耦合确定、凸位移代价不增，历史最佳直度误差随迭代下降。RSBM 的「桥矫正」借此名，实质是缩放桥方差（$\epsilon$）。→ [Rectified Flow](../papers/2209.03003_rectified_flow/README.md)

**Informative source / 边界即条件**——把结构化信息（退化图、上一 chunk、观测潜表示、sim 轨迹）当桥的起点，也可保留网络条件输入。起点信息有望减少修正负担，少步收益依任务而定。→ [I2SB](../papers/2302.05872_i2sb/README.md)、[BridgePolicy](../papers/2512.07212_bridge_policy/README.md)

## C. 一步生成

**MeanFlow 恒等式**——区间平均速度 $u(z_t,r,t)=\frac{1}{t-r}\int_r^tv\,d\tau$ 满足 $u=v-(t-r)\frac{d}{dt}u$，全导数用一次 JVP 算。免蒸馏训练、一步采样 $z_0=z_1-u(z_1,0,1)$。→ [MeanFlow](../papers/2505.13447_meanflow/README.md)

**边界条件缺失 / IVC**——恒等式是关于 $u$ 的一阶 ODE，只在 $t<r$ 上提供动力学，解可差一项 $C/(r-t)$。瞬时速度约束（$t=r$ 时 $u=v$）作为边界条件补上。→ [MVP](../papers/2602.13810_mvp/README.md)

**梯度饥饿**——MSE 对方向误差的梯度 $\propto\rho\rho^*\sin\alpha$，目标速度模长 $\rho^*$ 小时方向监督变弱，二维实验中先缩模长、方向纠正滞后。精细动作中的低模长训练目标需重点检查；桥漂移在收口段不一定趋零。→ [OMP](../papers/2512.19347_omp/README.md)

**Flow map / 流映射策略**——任意两时刻间的跳跃算子 $X_{r,t}$，MeanFlow、Shortcut、consistency 都是其参数化特例。→ [FMQ](../papers/2605.12416_fmq/README.md)

**Consistency 蒸馏**——沿同一 PF-ODE 的不同点去噪到同一时刻应重合；从多步教师蒸馏一步或三步学生。两阶段；学生还用示范 DSM 监督，表现并非被教师锁死。→ [Consistency Policy](../papers/2405.07503_consistency_policy/README.md)

**Drift 固定点**——生成器向「被反对称漂移场推一步的自己」回归，把迭代修正内化进参数。→ [DBPO](../papers/2604.03540_dbpo/README.md)

**Dispersive 正则**——鼓励 batch 内隐藏表征分散的正则；MP1 作用于 U-Net 下采样特征，DMPO 作用于观测条件嵌入，不保证无塌缩。→ [MP1](../papers/2507.10543_mp1/README.md)、[DMPO](../papers/2601.20701_dmpo/README.md)

**NFE**——网络前向次数。影响生成耗时；真机 Hz 还取决于感知、通信与执行，1-NFE 也需测端到端延迟，性能锚应改为多模态覆盖等硬指标。

## D. RL 侧接口

**log π 障碍**——生成式策略的动作是 SDE/ODE 终端边际，$\log\pi(a|s)$ 只有 ELBO 或需解 ODE 积分散度，常规动作似然接口受阻，仍可改用路径似然或其他更新目标。本库主线问题。五条绕法见 [DIGEST](DIGEST.md)。

**Denoising-as-MDP / 两层 MDP**——去噪链每步当内层动作，逐步高斯似然可算，PPO 直接套。horizon 乘以步数，DPPO 用去噪折扣调整各步优势。→ [DPPO](../papers/2409.00588_dppo/README.md)

**Mirror descent 策略优化**——$\pi_{k+1}=\arg\max\mathbb{E}[A]-\frac{1}{\eta}\mathrm{KL}(\pi\|\pi_k)$，KL 邻近项显式进目标（TRPO 用反向 KL 约束，PPO clip 不与此目标等价）。路径空间版 = GSB-MDPO。→ [MDPO](../papers/2005.09814_mdpo/README.md)

**Max-ent RL / energy-based 最优策略**——不受策略族限制时 $\pi^*\propto\exp(Q/\alpha)$，为 Boltzmann 分布；与 SB 指数重加权的对应还需核对参考与边界。FLAC 用动能正则接入 actor-critic，确定性版不严格等同最大熵目标。→ [SAC](../papers/1801.01290_sac/README.md)

**Advantage-weighted / 优势条件化**——$\exp(A/\lambda)$ 当 BC 权重（AWR）或二值优势当条件 token（RECAP）。不需要 ratio；AWR 仍需动作对数似然，RECAP 连续动作沿用流匹配。数据覆盖限制单次拟合，在线收集可扩展经验。→ [AWR](../papers/1910.00177_awr/README.md)、[RECAP](../papers/2511.14759_recap/README.md)

**Group-relative advantage**——组内标准化回报当优势，免 critic。→ [GRPO](../papers/2402.03300_grpo/README.md)、[Flow-GRPO](../papers/2505.05470_flow_grpo/README.md)

**噪声空间 RL / Diffusion steering**——冻结解码器，RL 学初始噪声。LP-DS 的残差 + 平均平方扰动预算抑制 latent 偏移与模式坍缩，但不是精确 KL 信赖域。→ [DSRL](../papers/2506.15799_dsrl/README.md)、[LP-DS](../papers/2606.01151_lp_ds/README.md)

**生成-选择（best-of-N）**——MVP 采 N 个候选按 Q 选，Q 梯度不穿生成器；DF-ExpEnse 只在采集期按价值与分歧选候选。FMQ 给在线训练目标提供局部闭式替代，推理仍有候选筛选。→ [MVP](../papers/2602.13810_mvp/README.md)、[DF-ExpEnse](../papers/2606.19656_df_expense/README.md)

**Mode coverage**——策略保持多模态的程度。LP-DS 用 Kozachenko-Leonenko 条件动作熵及多目标、绕障覆盖评测；ASBM 也报告 LPIPS 多样性；本库 [P3](OPEN_PROBLEMS.md) 主张建基准。
