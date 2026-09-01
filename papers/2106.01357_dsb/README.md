# Diffusion Schrödinger Bridge with Applications to Score-Based Generative Modeling

> De Bortoli, Thornton, Heng, Doucet (Oxford), NeurIPS 2021。[arXiv:2106.01357](https://arxiv.org/abs/2106.01357)

## 一句话

用神经网络实现 IPF 迭代（交替拟合前向/反向 drift），第一次把 Schrödinger Bridge 变成可训练的生成模型，并指出 score-based 扩散只是它的第一次迭代。

## 问题与动机

Score-SDE 的前向加噪要跑到 $T$ 足够大才能接近高斯先验，步数因此降不下来；且起点被锁死为无信息噪声。SB 恰好承诺两件事：有限时间内精确到达任意先验、两端都是约束。障碍是 SB 没有可扩展的求解器——经典 IPF/Sinkhorn 在连续高维空间上无法执行。DSB 的贡献就是给 IPF 一个神经实现。

## 方法核心

IPF（Iterative Proportional Fitting）交替解两个半桥（half-bridge）问题：

$$
\mathbb{P}^{2n+1} = \arg\min\big\{\mathrm{KL}(\mathbb{P}\|\mathbb{P}^{2n}) : \mathbb{P}_T = \nu\big\},\qquad
\mathbb{P}^{2n+2} = \arg\min\big\{\mathrm{KL}(\mathbb{P}\|\mathbb{P}^{2n+1}) : \mathbb{P}_0 = \mu\big\}
$$

- 每个半桥只钉住一端边际，解就是「把上一轮过程时间反演后换起点」——反演所需的 score 用类 DSM 的回归学习。具体实现：交替训练两个网络（前向 drift $f_\alpha$、反向 drift $b_\beta$），每轮用上一轮的过程 rollout 出样本对做回归目标（mean-matching 形式）。
- **与扩散的关系**：第一次 IPF 迭代（固定前向为加噪过程、学反向）恰好就是 DDPM/Score-SDE。后续迭代不断修正前向过程，让有限时间 $T$ 内两端边际同时精确成立。
- 理论：给出 IPF 在 KL 意义下的收敛保证（首个 path space 上的定量结果）。

## 实验与证据

- 2D 玩具分布：IPF 迭代次数增加，两端边际误差单调下降，直观验证收敛。
- 图像生成（MNIST、下采样 CelebA）：比同期 score-based 模型用更少的扩散步数达到可比质量——「有限时间精确边际」的直接红利。
- 数据集插值（EMNIST↔MNIST 等）：展示任意两个数据分布之间的桥——这是 DDPM 结构上做不到的能力。

## 在谱系中的位置

- 上游：[Léonard 综述](../1308.0215_leonard_survey/)（IPF 与 SB 理论）、[Score-SDE](../2011.13456_score_sde/)（时间反演与 DSM 工具箱）。
- 下游（本仓库内）：[DSBM](../2303.16852_dsbm/) 指出 DSB 的 IPF 会漂移出联合分布约束并用 IMF 修复；[I2SB](../2302.05872_i2sb/) 在 paired 场景把迭代砍成一次回归；[SB Flow](../2409.09347_sb_flow/) 把迭代在线化；[BDG](../2602.23737_bdg/) 直接用 DSB 做跨域轨迹翻译。

## 与 SB×RL 的关联

DSB 是「SB 可以神经化」的存在性证明，此后一切 SB×具身的算法讨论才有意义。它的算法骨架（交替半桥）对 RL 有一个隐喻式对应：策略评估/策略改进的交替——GSB-MDPO 把这个隐喻做实（每轮 mirror descent 就是一个受 KL 约束的半桥）。它也留下了 SB×RL 要继承的最大工程包袱：迭代拟合需要缓存整条轨迹样本、训练不稳、误差随迭代积累——06 类每篇论文的「训练稳定性」段落都在向这个包袱交税。

## 局限与批判

- 每轮 IPF 都要用当前网络 rollout 采样（simulation-based），训练慢；网络两个、缓存一份，显存贵。
- 误差积累：早期迭代的偏差会被后续迭代放大，实际只跑得起个位数轮次。
- 图像实验分辨率低（CelebA 下采样），与同期 score-based SOTA 有明显规模差距。
- mean-matching 回归目标在离散化步长大时有偏——后续 DSBM 对此有系统分析。
