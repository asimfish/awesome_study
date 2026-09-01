# Planning with Diffusion for Flexible Behavior Synthesis

> Janner, Du, Tenenbaum, Levine, ICML 2022。[arXiv:2205.09991](https://arxiv.org/abs/2205.09991)

## 一句话

把整条轨迹（状态+动作拼成二维数组）交给扩散模型一次性生成，规划变成「引导采样」，模型与规划器合二为一——扩散规划路线的开山。

## 问题与动机

基于模型的 RL 的经典困境：学出来的单步动力学模型在规划器的优化压力下被剥削（model exploitation），长 horizon 误差复合。Diffuser 的判断：既然模型终究要为规划服务，不如直接学「好轨迹的分布」，让规划等于从这个分布里条件采样——模型误差与规划器剥削从结构上消失。

## 方法核心

轨迹表示为二维数组（时间 × 状态动作维度），用 U-Net 做非自回归的整条轨迹去噪：

$$
\tau = \begin{bmatrix} s_0 & s_1 & \cdots & s_T \\ a_0 & a_1 & \cdots & a_T \end{bmatrix},\qquad p_\theta(\tau) = \text{DDPM over } \tau
$$

- 整条轨迹同时去噪：时间上的因果性被放弃，换来全局一致性（未来约束可以影响过去的规划）——这是与自回归模型的本质区别。
- 规划 = 引导采样。奖励引导（classifier guidance）：训练一个回报预测器 $\mathcal{J}_\phi(\tau)$，采样时叠加其梯度：

$$
\tilde{\epsilon} = \epsilon_\theta(\tau^k, k) - \omega\,\nabla_{\tau}\mathcal{J}_\phi(\tau^k)
$$

- 目标条件（inpainting）：把起点/终点状态硬钉在数组里，去噪只填中间——goal-reaching 不需要奖励函数。
- warm-start：上一时刻的规划加少量噪声再去噪，摊薄重规划成本。

## 实验与证据

- Maze2D 长 horizon 导航：目标条件 inpainting 拿到 SOTA，远超 TD 类（拼接与长程 credit 都靠全局去噪解决）。
- D4RL locomotion：与 CQL/IQL 可比（不是碾压）；块堆叠（block stacking）等组合任务上明显更好。
- 关键定性证据：同一个模型零改动支持奖励引导、目标条件、约束组合——「一个模型多种规划任务」是它真正的卖点。

## 在谱系中的位置

- 上游：[DDPM](../2006.11239_ddpm/)、[Decision Transformer](../2106.01345_decision_transformer/)（都属「RL 即生成」，DT 自回归、Diffuser 全轨迹）。
- 下游（本仓库内）：Decision Diffuser（classifier-free 化）、[Diffusion Policy](../2303.04137_diffusion_policy/)（把生成对象从轨迹缩到 action chunk，走向实时控制）、MCTD 等 System-2 规划线。

## 与 SB×RL 的关联

Diffuser 是「path-space 思维」在 RL 里的第一次具象化：优化对象不是单步动作分布而是整条轨迹的分布——这正是 SB 的原生语言（路径测度上的 KL）。它的奖励引导 $\nabla\mathcal{J}$ 在 SB 语境里对应 Feynman-Kac 重加权（把奖励写进桥的势函数），GSBM 的 task cost 就是这个思想的严格版。弱点同样有指向性：从纯噪声起点生成整条轨迹既慢又浪费（上一条规划就是天然的 informative source）——「规划修正 = bridge」是一个尚未被充分开采的方向。

## 局限与批判

- 推理极慢：每次重规划都是完整的多步去噪，实时控制不可用，后续所有 diffusion planning 工作都在补这刀。
- 开环执行 chunk 的鲁棒性问题与 Diffusion Policy 相同，但轨迹更长更严重。
- classifier guidance 的引导强度 $\omega$ 与去噪调度耦合，调参黑魔法多。
- locomotion 上不如专门的 offline RL，说明「全轨迹生成」的优势只在长 horizon/组合结构任务上兑现。
