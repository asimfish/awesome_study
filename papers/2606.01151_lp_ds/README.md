# Lagrangian Perturbation Diffusion Steering: Latent Reinforcement Learning for Generative Policies (LP-DS)

> Simsir, Oguz (Bilkent), ICML 2026。[arXiv:2606.01151](https://arxiv.org/abs/2606.01151)

## 一句话

给 DSRL 装上信赖域：不再学一个替代先验的 latent 策略，而是学一个受拉格朗日约束的残差噪声扰动 $w=\epsilon+\Delta_\theta(s)$，回报最高提升 25%，同时用动作熵量化证明多模态没被塌掉——噪声空间 RL 的成熟形态，也是「一步/冻结骨干 + RL」时代第一个把 mode coverage 当硬指标的工作。

## 问题与动机

冻结生成式解码器、只在噪声空间做 RL（DSRL）是绕开 log π 障碍最轻量的路线：解码器当黑箱，SAC 学「喂什么噪声」。但 DSRL 学的是一个完整的 latent 策略 $\pi^{\mathcal{W}}(w|s)$，实际上**替换**了预训练先验 $\mathcal{N}(0,I)$，两个失败模式随之而来：latent 漂出解码器训练时见过的高斯支撑（off-manifold 解码，图 2 显示 DSRL 的 latent 模长随训练飙升并伴随性能崩落）；latent 策略把骨干的多模态行为压成单一模式。

## 方法核心

1. **残差参数化**：$w = \epsilon + \Delta_\theta(s)$，$\epsilon\sim\mathcal{N}(0,I)$ 保留，小 MLP 输出状态条件偏移。初始化 $\Delta\approx0$ 时精确恢复 BC 行为；扰动作用在 ODE 积分起点（扩散的 $x_T$ 或流的 $x_n$）+ 确定性解码。
2. **拉格朗日信赖域**：最大化下游价值 $Q(s, \text{dec}(\epsilon+\Delta_\theta(s)))$，约束 $\mathbb{E}_s\|\Delta_\theta(s)\|^2\le\delta$，乘子自动调节——$\delta$ 是「改进 vs 保先验」的显式旋钮（消融 $\delta\in\{0.01,0.05,0.1\}$）。与 DSRL 的硬裁剪（$\|w\|\le100$）不同，约束的是**相对先验的偏移**而非绝对模长。
3. 骨干无关：扩散、flow matching、π0 级 VLA 都能接。

## 实验与证据

- RoboMimic / Gym / Adroit：样本效率、成功率、回报均优于 DSRL 与 DPPO，回报最高 +25%。
- **多模态保持量化**：用 Kozachenko-Leonenko k-近邻熵估计动作空间熵，LP-DS 显著高于无约束噪声操控——四峰玩具任务可视化里 DSRL 塌成一两个模式，LP-DS 在 $\delta$ 小时四峰俱全。
- 扩展验证：diffusion/flow 骨干对照、π0 VLA、仿真适配后 Franka 真机部署。
- 评价：基线（DSRL、DPPO）选得准，熵评测是领域内稀缺的贡献；但 $\delta$ 与任务尺度的关系、以及「熵高=有用多模态」的等价性都只有经验证据。

## 在谱系中的位置

- 上游：[DSRL](../2506.15799_dsrl/)（被修正者）、TRPO/[MDPO](../2005.09814_mdpo/)（信赖域思想，只是搬到了 latent 空间）。
- 平行：[DF-ExpEnse](../2606.19656_df_expense/)（DSRL 的探索侧改进）。
- 对照：[DPPO](../2409.00588_dppo/)/[DMPO](../2601.20701_dmpo/)（改解码器参数的路线）。

## 与 SB×RL 的关联

LP-DS 从两个方向逼近 SB×RL 的地盘：(1) 「对先验的 KL/距离约束下最大化回报」正是 GSB 的一句话表述——LP-DS 在 latent 空间用 L2 信赖域做了它，GSB-MDPO 在路径空间用 KL 做了它，两者是同一优化问题在不同层的近似；把 LP-DS 的 $\|\Delta\|^2$ 换成 Girsanov 意义下的路径动能，就得到「噪声空间 FLAC」。(2) **它把 mode coverage 评测拿上了台面**——SB 若要用「$\epsilon$ 谱系保多模态」当卖点，评测口径必须至少对齐 LP-DS 的熵估计，否则无法对表。对 bridge 起点策略还有一个直接启示：informative 起点本身就是一种「结构化的 $\Delta(s)$」，LP-DS 的信赖域框架可以用来分析桥式先验偏离高斯先验多远才安全。

## 局限与批判

- 改进上限被冻结解码器锁死：RL 只能在骨干的支撑集内挑模式，示范覆盖不到的行为学不出来——与 RECAP 的「只能好到数据最好」是同一个天花板。
- 残差是状态条件、噪声无关的均值偏移，本质上是给先验平移；对需要改变先验形状（方差、相关性）的任务表达力不足。
- 动作熵高不等于任务相关的多模态（可能只是噪声大），论文用玩具任务的峰计数做了佐证，真实任务上没有。
- 真机实验是仿真适配后迁移，不是真机在线 RL。
