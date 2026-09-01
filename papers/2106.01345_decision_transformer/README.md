# Decision Transformer: Reinforcement Learning via Sequence Modeling

> Chen, Lu, Rajeswaran, Lee, Grover, Laskin, Abbeel, Srinivas, Mordatch, NeurIPS 2021。[arXiv:2106.01345](https://arxiv.org/abs/2106.01345)

## 一句话

把轨迹当 token 序列、用 GPT 以目标回报为条件自回归地预测动作，完全不用 Bellman 方程就能打平 offline RL 基线——「RL 即条件生成」路线的起点。

## 问题与动机

Offline RL 的主流做法（TD 学习 + 保守正则）要对付分布外动作的 Q 值外推错误，机制复杂、超参敏感。DT 的赌注：大容量序列模型 + 监督学习的稳定性，能不能干脆绕开 bootstrapping 和动态规划这一整套？

## 方法核心

轨迹重写成三元组序列，回报字段用 **return-to-go**（剩余累计回报）：

$$
\tau = \big(\hat{R}_1, s_1, a_1,\ \hat{R}_2, s_2, a_2,\ \dots\big),\qquad \hat{R}_t = \sum_{t'=t}^{T} r_{t'}
$$

- GPT 架构 + 因果掩码，训练目标就是动作的监督预测（连续动作 MSE）。
- 推理：手工指定期望回报 $\hat{R}_1$（比如数据集最高回报），环境每走一步就把实际获得的奖励从 return-to-go 里扣掉，条件自动更新。
- 没有 critic、没有 policy gradient、没有 bootstrap——「credit assignment」被 self-attention 的长程依赖隐式接管。

## 实验与证据

- D4RL（HalfCheetah/Hopper/Walker + AntMaze）与 Atari offline：与当时最强 offline RL（CQL）整体持平，在长 horizon、稀疏奖励（Key-to-Door）场景显著更好。
- 关键消融：条件回报与实际表现强相关（模型确实学会了「按指定回报行动」），甚至能外推到略高于数据集最高回报的目标。
- 对 %BC（只克隆最好轨迹）的对比：数据低质时 DT 明显更好——它在利用全体数据的信息而非只模仿精英。

## 在谱系中的位置

- 上游：GPT 系列、Upside-Down RL（Schmidhuber）。
- 平行：Trajectory Transformer（同期，token 化更彻底 + beam search）。
- 下游（本仓库内）：[Diffuser](../2205.09991_diffuser/) 把「生成高回报轨迹」从自回归换成扩散；VLA 里的自回归动作头（RT 系、π0-FAST）是它的规模化后裔。

## 与 SB×RL 的关联

DT 是「策略学习 = 分布建模」的第一个纯粹版本：不学值函数，学「以结果为条件的轨迹分布」。这个视角与 SB 的亲缘在于——SB 恰好也是「给定两端（当前分布与目标分布）求最优路径测度」的问题，条件生成与桥式生成是同一个抽象的两种实现。DT 的弱点（拼接能力差、不能超越数据、对随机环境的乐观偏差）标出了纯序列建模路线的天花板，也解释了为什么后续要往回加 RL（值函数/优势）成分——这正是 05/06 类的出发点。

## 局限与批判

- 无法轨迹拼接（stitching）：TD 方法能把两段次优轨迹的好部分拼起来，DT 不能，AntMaze 类任务上是硬伤。
- 随机环境下按回报条件化有系统性乐观偏差（把运气当能力），后续 ESPER 等专门修这个。
- 「指定回报」推理协议在真实部署里别扭：目标回报是人手拍的超参。
- 与 %BC 的差距在高质量数据上消失，说明它主要赢在数据利用率而非算法本质。
