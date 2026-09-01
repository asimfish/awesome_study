# Simulation-Free Schrödinger Bridges via Score and Flow Matching

> Tong, Malkin, Fatras, Atanackovic, Zhang, Huguet, Wolf, Bengio (Mila), AISTATS 2024。[arXiv:2307.03672](https://arxiv.org/abs/2307.03672)

## 一句话

用 minibatch 熵正则 OT 近似端点耦合、布朗桥填充中间，把 SB 求解拆成 flow matching + score matching 两个回归——训练全程零 SDE rollout 的 SB 求解器。

## 问题与动机

DSB/DSBM 的迭代范式每轮都要用当前模型仿真采样（simulation-based），慢且误差随迭代传递。[OT-CFM](../2302.00482_ot_cfm/) 已经证明确定性 flow 可以免仿真训练。SF2M 把这个思路补全到随机情形：SB 的解不只有 drift 还有噪声，学它需要同时拿到速度场和 score。

## 方法核心

SB 解的 SDE 可分解为「概率流 + 熵修正」：最优 drift $= v_t(x) + \frac{\sigma^2}{2}\nabla\log p_t(x)$。SF2M 对两个分量各设一个回归：

$$
\mathcal{L}_{\text{SF}^2\text{M}} = \mathbb{E}\big[\|v_\theta(x_t,t) - u_t(x_t|x_0,x_1)\|^2\big] + \lambda\,\mathbb{E}\big[\|s_\theta(x_t,t) - \nabla\log p_t(x_t|x_0,x_1)\|^2\big]
$$

- 端点对 $(x_0,x_1)$ 从 minibatch 熵正则 OT（Sinkhorn）耦合采样——静态 SB 的 minibatch 近似；
- 条件路径取布朗桥（参考过程给定端点的解析桥），其条件速度与条件 score 都有闭式——所以两项 loss 都是免仿真的纯回归；
- 定理：minibatch 熵 OT 收敛于真实静态 SB 耦合时，学到的 SDE 收敛于真 SB。与 DSBM 的关系：SF2M 等价于「一次性用静态近似替代 IMF 的迭代耦合改进」——快，但耦合质量受 minibatch 偏差限制。

## 实验与证据

- 单细胞动力学（CITE-seq、Multiome、胚胎数据）：轨迹推断 SOTA，比 DSB/DSBM 训练快一个量级——免仿真的直接红利；这是 SF2M 的主场景。
- 高斯基准：验证收敛到闭式 SB 解。
- 2D/图像小规模：与迭代法可比；高维图像上 minibatch 熵 OT 的偏差开始显现，不及后来 SB Flow 的在线迭代。

## 在谱系中的位置

- 上游：[OT-CFM](../2302.00482_ot_cfm/)（同组前作，确定性版）、[DSBM](../2303.16852_dsbm/)（迭代范式的参照）。
- 下游（本仓库内）：[SB Flow](../2409.09347_sb_flow/) 用在线 IMF 解决它的耦合偏差；FLAC/GSB-MDPO 的免仿真训练形态师承于此。

## 与 SB×RL 的关联

SF2M 把 SB 的训练成本压到与普通 flow matching 同级——「SB 策略训练太贵」这个反对意见自它之后只对迭代法成立。RL 侧的直接启示：策略学习里端点耦合可以来自 replay buffer 的经验配对（状态-好动作），Sinkhorn 在 batch 内跑一次即可，训练循环与普通 actor 更新一样轻。它也给出了 SB×RL 的一个未开采维度：score 头 $s_\theta$ 学到的是路径上的密度梯度——恰好是探索（往低密度走）与不确定性估计的原料，目前没有工作利用这一点。

## 局限与批判

- minibatch 熵 OT 的偏差在高维急剧放大（batch 内最优 ≠ 全局最优），图像级任务上明显掉队——它的甜点区是中低维科学数据。
- 两个网络头（速度+score）+ Sinkhorn 每 batch 的开销，比纯 CFM 重。
- $\lambda$ 权衡两个回归的尺度，跨任务要调。
- 「免仿真」只指训练；推理仍是常规多步 SDE，与少步化无关。
