# Proximal Policy Optimization Algorithms

> Schulman, Wolski, Dhariwal, Radford, Klimov (OpenAI), arXiv 2017。[arXiv:1707.06347](https://arxiv.org/abs/1707.06347)

## 一句话

把 TRPO 的二阶信赖域约束替换成一个一阶的 ratio 裁剪目标，用十几行代码实现了几乎同等的稳定性，从此成为 on-policy RL 的事实标准。

## 问题与动机

Policy gradient 的核心矛盾：梯度估计只在当前策略附近有效，步子迈大了，新策略跑出数据支持集，优势估计全错，训练崩掉。TRPO 用 KL 硬约束解决这个问题，但要算 Fisher 矩阵与共轭梯度，实现复杂、和参数共享/dropout 等工程组件不兼容。PPO 要的是：TRPO 的稳定性 + 一阶优化器的简单性。

## 方法核心

定义重要性比 $r_t(\theta) = \dfrac{\pi_\theta(a_t|s_t)}{\pi_{\theta_{\text{old}}}(a_t|s_t)}$，PPO-clip 目标为

$$
\mathcal{L}^{\text{CLIP}}(\theta) = \mathbb{E}_t\Big[\min\big(r_t(\theta)\hat{A}_t,\ \text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon)\hat{A}_t\big)\Big]
$$

- $\hat{A}_t$：GAE 估计的优势；$\epsilon$：裁剪半径（论文取 0.2）。
- min 与 clip 的组合构成一个悲观下界（pessimistic bound）：只有当 ratio 向"让目标变好"的方向越界时才被裁掉，向变差方向移动不设限，保证目标是原目标的下界。
- 每批数据可以做多个 epoch 的 minibatch SGD——这是它比 vanilla PG 样本效率高的直接原因。

论文还给了 KL 惩罚版（adaptive KL coefficient），实验证明 clip 版更好。

要点：clip 是启发式，不是 KL 约束的等价物。它只在被采样到的状态-动作对上惩罚 ratio 越界，不提供整体 KL 上界。这个缝隙正是后来 [MDPO](../2005.09814_mdpo/) 把 KL 邻近项显式写回目标的动机。

## 实验与证据

- MuJoCo 连续控制 7 个任务：PPO-clip 在几乎所有任务上优于 TRPO、A2C、CEM 与 vanilla PG，$\epsilon=0.2$ 是最优超参。
- Atari 49 games：与 A2C、ACER 对比，PPO 平均得分居中偏上，但训练墙钟时间与实现复杂度大幅占优。
- Roboschool 人形机器人：展示了当时罕见的复杂连续控制学习能力。

数字本身不惊艳，惊艳的是稳定性/简单性比值——这也是它此后八年霸占默认选项的原因。

## 在谱系中的位置

- 上游：TRPO（KL 硬约束版），策略梯度定理。
- 下游（本仓库内）：[MDPO](../2005.09814_mdpo/) 揭示 clip≈mirror descent 的近似并给出更干净的形式；[GRPO](../2402.03300_grpo/) 在 LLM 场景去掉 critic；[DPPO](../2409.00588_dppo/) 把 PPO 套在扩散策略的去噪链上；[DMPO](../2601.20701_dmpo/) 在一步策略上做 PPO 微调。

## 与 SB×RL 的关联

PPO 是生成式策略 RL 微调的默认外层算法，但它要求 $\log\pi(a|s)$ 可算——高斯 actor 没问题，扩散/流策略只有 ELBO 或需要 ODE 积分，这就是「log π 障碍」。DPPO 的绕法是把每个去噪步当独立动作；SB×RL 的绕法（[GSB-MDPO](../2603.21621_gsb_mdpo/)）是把 KL 邻近项搬到路径空间。理解 PPO 的 clip 与 KL 的确切关系，是判断这些变体谁在真正近似 trust region 的前提。

## 局限与批判

- clip 不等于 trust region：没有 KL 保证，大 batch 下 ratio 分布可以严重漂移，实际稳定性高度依赖实现细节（advantage 归一化、value clipping、学习率退火），"37 个实现细节"是社区公开的梗。
- on-policy 样本效率天花板低，机器人真机场景基本不可用，必须配 sim 或大规模并行。
- 论文对"为什么 clip work"的理论解释很薄，后续大量工作（含 MDPO）都在补这个洞。
