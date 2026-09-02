# Mean Flow Policy with Instantaneous Velocity Constraint for One-step Action Generation (MVP)

> ICLR 2026 (Oral, top 1%)。[arXiv:2602.13810](https://arxiv.org/abs/2602.13810)

## 一句话

平均速度策略（MVP）+ best-of-N 选择做 offline-to-online RL，并证明 MeanFlow 恒等式作为一阶 ODE 缺边界条件导致解不唯一、用瞬时速度约束（IVC）补上——RoboMimic + OGBench 平均成功率 0.88，一步生成同时拿到表达力与速度。

## 问题与动机

流策略在 RL 里表达力强但要在「步数 = 表达力」和「步数 = 计算」之间折中。MeanFlow 承诺原生一步，但两个问题挡在 RL 前面：(1) 策略改进怎么做——MeanFlow 训练是模仿式回归，Q 的梯度往哪传；(2) 恒等式 $u = v-(t-r)\frac{d}{dt}u$ 是关于 $u$ 的一阶 ODE，训练只在 $t<r$ 的区间上提供「动力学」，没有显式边界条件，解不唯一。

## 方法核心

1. **生成-选择即策略**：MVP 一步生成 $N$ 个候选动作，按当前 $Q$ 选最优，「生成 + 选择」整体视为策略 $\pi_\theta$。策略网络只做模仿式的平均速度回归（对 replay buffer 中的动作），**Q 的梯度不穿过生成器**——策略改进完全由 best-of-N 的选择压力驱动。
2. **Theorem 1（策略改进下界）**：在 Q 误差有界、Q 为 Lipschitz、平均流匹配误差 $\epsilon_A$ 有界的假设下，新旧策略的性能差下界分解为 best-of-N 优势增益 $\Delta_1$（严格非负）减去拟合误差项 $\Delta_2$（来自 $\epsilon_Q,\epsilon_A$）——所以降低流匹配误差直接换性能。
3. **Theorem 2 + IVC**：若 $u_\theta$ 在所有 $t<r$ 上完美满足恒等式，学到的场与真实场之差仍可为 $\Delta_u = C(a,r)/(r-t)$ 形式的任意函数——解不唯一。补边界条件：$t=r$ 时平均速度就是瞬时速度 $v=a^*-a(0)$，故
$$\mathcal{L}_{\text{IVC}} = \mathbb{E}_{t,a(t)}\big\|u_\theta(a(t),t,t) - v\big\|^2$$
作为辅助损失，开销可忽略，唯一性与精度同时改善。
4. 加动作 chunking 提升探索与样本效率。

## 实验与证据

- RoboMimic（lift/can/square）+ OGBench（含 cube-triple 等长程稀疏任务），5 seeds：MVP 平均成功率 0.88±0.05，次优 QC 0.46±0.13，FQL/BFN 更低。
- 与基线的一步变体（FQL-Onestep/BFN-Onestep/QC-Onestep）对比：朴素一步化全部失效，说明成绩来自 MeanFlow+IVC 而非「一步」本身。
- 训练与每步推理速度均大幅优于多步流策略基线。
- 评价：基线是最新的 offline-to-online 流方法（FQL/BFN/QC），选得对；但 best-of-N 的 $N$ 与推理开销的权衡没有系统报告——$N$ 个候选 = $N$ 次前向，「一步」的速度优势被稀释。

## 在谱系中的位置

- 上游：[MeanFlow](../2505.13447_meanflow/)、[FQL](../2502.02538_fql/)（被超越的 offline-to-online 流基线）、BFN/QC。
- 平行：[MP1](../2507.10543_mp1/)/[DMPO](../2601.20701_dmpo/)（MeanFlow 进机器人的 BC/PPO 路线）、[MFPO](../2604.14698_mfpo/)（max-ent 路线）。
- 与 [OFP](../2603.12480_ofp/) 对照：OFP 用有限差分绕开 JVP，MVP 用 IVC 补边界——两个对 MeanFlow 训练目标的独立修补。

## 与 SB×RL 的关联

两条直接借鉴：(1) Theorem 2 对 SB 侧的「平均漂移场」同样成立——若把 MeanFlow 恒等式推广到桥上做 one-step SB policy，边界条件的缺失会原样出现，IVC 的桥版本（$t=r$ 时平均漂移 = 桥的条件漂移）是免费的修补；(2) 「Q 不穿过生成器、改进靠选择」的 best-of-N 范式绕开了 log π 也绕开了 pathwise 梯度的方差，对 SB 策略是零成本可用的改进机制——比 GSB-MDPO 的路径重要性比率便宜得多，代价是 $N$ 倍推理。它也标出了 SB 的差异化位置：MVP 的 N 个候选来自同一高斯先验的不同噪声，模式覆盖靠 N 撑；桥式起点 + $\epsilon$ 旋钮能在 $N$ 更小时给出更结构化的候选多样性——这是可测的假设。

## 局限与批判

- best-of-N 推理开销随 $N$ 线性增长，「一步」在部署时是「$N$ 步并行」，真机频率优势要打折。
- 策略改进上限受 Q 的选择能力约束，Q 过估计会系统性选到坏动作（offline RL 的老问题），论文靠 chunking 与保守设置缓解但未根治。
- IVC 只钉住 $t=r$ 一个边界，Theorem 2 的唯一性论证依赖恒等式在其余区间被「完美满足」，实际训练误差下唯一性保证有多强没有定量分析。
- 无真机、无视觉输入。
