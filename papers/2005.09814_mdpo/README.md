# Mirror Descent Policy Optimization

> Tomar, Shani, Efroni, Ghavamzadeh, ICLR 2022。[arXiv:2005.09814](https://arxiv.org/abs/2005.09814)

## 一句话

把 trust-region 策略优化统一成镜像下降（mirror descent）的 KL 邻近点迭代，证明 PPO 的 clip 只是它的粗糙近似，并给出 on-policy 与 off-policy 两个直接可用的实例。

## 问题与动机

TRPO 说要约束 KL，PPO 说 clip 差不多等价。这两个说法都不精确：TRPO 的硬约束在深度网络上只能近似求解，PPO 的 clip 根本不提供 KL 控制。优化理论里处理这类问题的标准工具是镜像下降——把邻近项直接写进目标而不是当约束。MDPO 的问题是：认真按镜像下降做策略优化，会不会更好？

## 方法核心

镜像下降的策略迭代形式：

$$
\pi_{k+1} = \arg\max_{\pi}\ \mathbb{E}_{s\sim\rho_{\pi_k}}\Big[\mathbb{E}_{a\sim\pi}[A^{\pi_k}(s,a)] - \frac{1}{\eta_k}\,\mathrm{KL}(\pi(\cdot|s)\,\|\,\pi_k(\cdot|s))\Big]
$$

- $A^{\pi_k}$：当前策略的优势；$\eta_k$：步长，KL 项系数是它的倒数。
- 与 TRPO 的差别：KL 从约束搬进目标（软化）；与 PPO 的差别：邻近项是显式的 KL，不是采样点上的 ratio 裁剪。
- 每次迭代不是解到最优，而是对该目标做 m 步 SGD——论文证明这样仍保留镜像下降的单调改进性质（近似意义下）。
- off-policy 版把 KL 方向反过来用在 soft actor-critic 骨架上，与 SAC 的 energy-based 投影形成对照。

理论贡献：把 TRPO/PPO/SAC 放进同一个镜像下降框架，明确各自对应哪种 Bregman 散度与近似。

## 实验与证据

- MuJoCo 连续控制：on-policy MDPO 与 TRPO 相当、普遍优于 PPO；off-policy MDPO 与 SAC 相当。
- 关键信息不在刷分，在等价性拆解：PPO 的性能优势主要来自实现技巧（多 epoch、advantage 归一化）而非 clip 本身；把这些技巧移植给 MDPO 后 clip 无优势。

## 在谱系中的位置

- 上游：TRPO/PPO（[1707.06347](../1707.06347_ppo/)）、SAC（[1801.01290](../1801.01290_sac/)）、镜像下降理论（Beck & Teboulle）。
- 下游（本仓库内）：[GSB-MDPO](../2603.21621_gsb_mdpo/) 是它在路径空间的直接推广——本仓库收录它的全部理由。

## 与 SB×RL 的关联

MDPO 给 SB×RL 提供了最干净的接口。生成式策略的困境：镜像下降需要 $\mathrm{KL}(\pi\|\pi_k)$，动作层面的 KL 对扩散/流策略不可算。GSB-MDPO 的解法：把邻近项从动作分布搬到路径测度，$\mathrm{KL}(\mathbb{P}\|\mathbb{P}_k)$ 由 Girsanov 化成两个 drift 的 $L^2$ 距离（可算），且 data processing 不等式保证 path-KL ≥ 终端动作 KL——邻近约束依然成立。没有 MDPO 把"KL 邻近项显式化"这一步，path-space 版本无从谈起。这是「经典算法的哪个形式适合被推广」的范例：clip 推广不动，镜像下降可以。

## 局限与批判

- 实验只到 MuJoCo，没有真机、没有高维视觉输入，说服力停留在方法论层面。
- 每状态的 KL 用采样近似，状态分布漂移（$\rho_{\pi_k}$ 变化）带来的误差论文处理得比较宽松。
- 作为算法它没有胜过被它批评的 PPO 多少——它的价值是概念澄清，不是性能。
