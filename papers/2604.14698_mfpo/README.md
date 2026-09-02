# Mean Flow Policy Optimization (MFPO)

> Dong, Zhang, Cheng (中科院自动化所), ICML 2026。[arXiv:2604.14698](https://arxiv.org/abs/2604.14698)

## 一句话

让 MeanFlow 策略进 max-ent RL 的 soft policy iteration：用「平均散度网络」把似然积分变成一次前向、用自归一化重要性采样从 Boltzmann 目标构造训练信号——2 步采样、推理 0.46 ms，打平或超过 16 步扩散基线，训练快约一半。与 FLAC 构成 likelihood-approximation vs likelihood-free 的正面路线之争。

## 问题与动机

扩散/流策略在在线 RL 里表达力强、探索好，但 10-20 步采样让训练与推理都慢。MeanFlow 的平均速度场天然少步，问题是 max-ent 框架要两样东西 MeanFlow 都不直接给：(1) 动作似然 $\log\pi(a|s)$（熵项与 soft Bellman 都要）；(2) 从 Boltzmann 目标 $\propto\exp(Q/\alpha)$ 学策略——而 MeanFlow 训练要目标分布的样本，RL 里没有。

## 方法核心

1. **似然：平均散度网络**。流策略的精确似然是 $\log\pi_\theta(a_0|s) = \log p_1(a_1) + \int_0^1 \nabla\cdot v_\theta(s,a_t,t)\,dt$——要沿轨迹积分瞬时速度场的散度，每步散度又要 $d$ 次反传求 Jacobian 迹。MFPO 照 MeanFlow 的思路定义**时间平均散度**
$$\delta(s,a_t,r,t) = \frac{1}{t-r}\int_r^t \nabla\cdot v_\theta(s,a_\tau,\tau)\,d\tau$$
用网络 $\delta_\omega$ 学它，训练目标由 MeanFlow 式恒等式构造，瞬时散度用 Skilling-Hutchinson 迹估计（$\epsilon^\top \partial_a v\,\epsilon$）无偏估计。推理时 $\log\pi \approx \log p_1 + \delta_\omega(s,a_1,0,1)$，**一次前向拿到似然**。
2. **策略改进：自适应瞬时速度估计**。目标 Boltzmann 分布的条件速度场可写成对目标样本的加权期望（MaxEntDP/SDAC 的结论），MFPO 用当前策略与另一提议分布的混合做自归一化重要性采样估计它，采样比例自适应——把「没有目标样本」变成「有偏但可修正的样本」。
3. 其余是标准 soft actor-critic 骨架 + 自动温度（目标熵系数 $\rho$）。

## 实验与证据

- MuJoCo 5 任务 + DMC 6 个难任务 + HumanoidBench 3 个高维任务，对 6 个扩散/流 RL 基线（DIME、FlowRL、SAC-Flow、MaxEntDP、DACER、QVPO）与 TD3/SAC：打平或超过，5 seeds。
- 效率：2 步采样、0.46 ms/样本，DIME 16 步 0.97 ms；「回报 vs 训练时间」图上 MFPO 落在左上角。
- 消融（HalfCheetah）：平均速度 vs 瞬时速度、平均散度网络 vs 瞬时散度网络 vs 无散度网络、采样比例、目标熵系数——**去掉平均散度网络性能明显掉**，似然近似的质量是决定性的。

## 在谱系中的位置

- 上游：[MeanFlow](../2505.13447_meanflow/)、[SAC](../1801.01290_sac/)（soft policy iteration）、MaxEntDP/SDAC（Boltzmann 条件速度场结论）、[Score-SDE](../2011.13456_score_sde/)（instantaneous change of variables）。
- 正面对手：[FLAC](../2602.12829_flac/)——同为 max-ent 框架下的生成式策略，FLAC 用路径动能上界替代似然，MFPO 硬算似然的近似。
- 与 [DMPO](../2601.20701_dmpo/)（PPO 路线）互补：两者都在 MeanFlow 上做在线 RL，一 off-policy 一 on-policy。

## 与 SB×RL 的关联

MFPO 给 path-space 路线出了一道题：如果似然可以一次前向近似出来，为什么还要绕到路径空间？FLAC 的回答只能是——(1) 近似的偏差在高维动作/长链下不可控（Hutchinson 估计方差随维度涨，散度网络的自举误差没有界）；(2) 动能正则的物理语义给了「探索预算」可解释的旋钮。这些都需要正面对比实验，两篇目前互不引用。MFPO 的平均散度技巧对 SB 侧有直接可借之处：bridge 的似然同样是散度积分，「平均散度网络」可以给 SB 策略一个廉价的似然估计器，让 GRPO/PPO 外壳直接套上——这是 path-space 之外的第二条 SB 策略 RL 化路径。

## 局限与批判

- 似然是近似的近似（散度积分 → 平均散度网络 → Hutchinson 估计），误差没有理论界，全靠消融的经验证据撑。
- 全部 locomotion 仿真，没有操纵/视觉/真机——与 FLAC 相同的短板。
- 2 步而非 1 步：原生一步在 RL 里的稳定性问题被回避了（DMPO/DBPO 的做法不同）。
- 自适应重要性采样的提议分布设计是经验性的，采样比例超参对性能敏感（消融 c 组）。
