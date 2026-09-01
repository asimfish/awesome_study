# Soft Actor-Critic: Off-Policy Maximum Entropy Deep Reinforcement Learning with a Stochastic Actor

> Haarnoja, Zhou, Abbeel, Levine (UC Berkeley), ICML 2018。[arXiv:1801.01290](https://arxiv.org/abs/1801.01290)

## 一句话

把最大熵目标塞进 off-policy actor-critic，同时拿到探索、多模态与样本效率三样东西，成为连续控制 off-policy 的事实标准。

## 问题与动机

两个痛点：(1) on-policy 方法（TRPO/PPO）每步梯度都要新样本，真机不可承受；(2) 已有 off-policy 方法（DDPG）对超参数极端敏感、确定性 actor 探索差。SAC 的答案：用最大熵框架做 off-policy 的随机策略优化，稳定性和样本效率一起要。

## 方法核心

最大熵目标在标准回报上加策略熵：

$$
J(\pi) = \sum_t \mathbb{E}_{(s_t,a_t)\sim\rho_\pi}\big[r(s_t,a_t) + \alpha\, \mathcal{H}(\pi(\cdot|s_t))\big]
$$

- $\alpha$：温度，权衡回报与熵；$\mathcal{H}$：策略熵。
- soft Bellman backup：$Q(s,a) \leftarrow r + \gamma\, \mathbb{E}_{s'}[V(s')]$，其中 soft value $V(s) = \mathbb{E}_{a\sim\pi}[Q(s,a) - \alpha\log\pi(a|s)]$。
- 策略更新是向 energy-based 目标做 KL 投影：

$$
\pi_{\text{new}} = \arg\min_{\pi'} \mathrm{KL}\Big(\pi'(\cdot|s)\ \Big\|\ \frac{\exp(Q^{\pi_{\text{old}}}(s,\cdot)/\alpha)}{Z(s)}\Big)
$$

最优策略形式是 $\pi^\star(a|s)\propto\exp(Q^\star_{\text{soft}}(s,a)/\alpha)$——一个 Boltzmann 分布。工程上：双 Q 网络取 min 抑制过估计、reparameterization trick 传梯度、squashed Gaussian actor。后续版本（1812.05905）把 $\alpha$ 改为自动调节。

## 实验与证据

- MuJoCo 基准（Hopper/Walker/HalfCheetah/Ant/Humanoid）：全面超过 DDPG、PPO、TD3，尤其 21 维 Humanoid（rllab）上 DDPG 完全学不动而 SAC 稳定收敛。
- 样本效率比 PPO 高一个数量级左右（off-policy replay 的功劳）。
- 消融证明随机 actor（相对确定性）与双 Q 都是必要的；对 reward scale 的敏感性是主要遗留超参问题（后被自动温度解决）。

## 在谱系中的位置

- 上游：soft Q-learning（Haarnoja 2017）建立 energy-based policy 与 max-ent RL 的等价。
- 同代对照：[PPO](../1707.06347_ppo/)（on-policy 线）。
- 下游（本仓库内）：[FLAC](../2602.12829_flac/) 直接把 SAC 的 max-ent 目标重写成对高熵参考过程的广义 Schrödinger Bridge；[Diffusion-QL](../2208.06193_diffusion_ql/) 等 offline 方法沿用其 Q-learning 骨架。

## 与 SB×RL 的关联

这是四篇 RL 经典里与 SB 血缘最近的一篇。max-ent RL 的最优策略是 energy-based 分布，而 SB 的解是对参考测度的指数重加权（Feynman-Kac）——两者是同一个数学对象在动作分布与路径测度两个层面的投影。control-as-inference（Levine 2018）是概念桥，FLAC 把它做成了严格版本：把 SAC 的策略熵换成路径动能正则 $\int\frac{1}{2\sigma^2}\|u\|^2 dt$（Girsanov 恒等式），从而绕开生成式策略算不了的 $\log\pi$。读懂 SAC 的 energy-based 视角，FLAC 的动机就是显然的。

## 局限与批判

- 策略熵项要求 tractable 的 $\log\pi(a|s)$：squashed Gaussian 可以，扩散/流策略不行——SAC 骨架不能直接搬到生成式策略上，这正是 FLAC 要解决的问题。
- 单高斯 actor 表达力有限，多模态动作分布会被平均掉；用混合模型或生成式 actor 替换又撞上面那条。
- 温度 $\alpha$ 的物理含义（探索-利用权衡）与任务尺度耦合，跨任务迁移仍要调。
