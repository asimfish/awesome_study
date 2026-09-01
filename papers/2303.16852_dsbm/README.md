# Diffusion Schrödinger Bridge Matching

> Shi, De Bortoli, Campbell, Doucet (Oxford), NeurIPS 2023。[arXiv:2303.16852](https://arxiv.org/abs/2303.16852)

## 一句话

用「SB 解是唯一既 Markov 又 reciprocal 的路径测度」这一刻画，设计出 Markov 投影与 reciprocal 投影交替的 IMF 算法，修复了 DSB 的边际漂移——现代 SB 求解器的主干。

## 问题与动机

DSB 的神经 IPF 有个实践中致命的毛病：每轮半桥拟合都有回归误差，误差让过程慢慢「忘掉」它本该保持的边际，迭代越多漂得越远。诊断：IPF 的投影方向（KL 约束在单端边际）对拟合误差不鲁棒。DSBM 换一组投影：不在「边际」上交替，在「过程类」上交替。

## 方法核心

理论基石（Léonard）：SB 解 $\mathbb{P}^\star$ 是唯一同时满足以下两条的路径测度——(a) Markov；(b) reciprocal（给定两端点，中间路径分布 = 参考桥）。IMF（Iterative Markovian Fitting）据此交替投影：

$$
\text{reciprocal 投影：}\ \Pi_{\mathcal{R}}(\mathbb{P}) = \int \mathbb{Q}^{x_0,x_T}\,d\,\mathbb{P}_{0,T}\qquad
\text{Markov 投影：}\ \Pi_{\mathcal{M}}(\mathbb{P}) = \arg\min_{\mathbb{M}\in\mathcal{M}}\mathrm{KL}(\mathbb{P}\,\|\,\mathbb{M})
$$

- reciprocal 投影：保留当前模型的端点耦合 $\mathbb{P}_{0,T}$，中间用参考桥重填——采样即可实现，无需训练；
- Markov 投影：把「桥的混合」回归成一个 Markov SDE 的 drift——就是标准 bridge matching 回归；
- 两步都**严格保持两端边际不动**（耦合的边际在两类投影下都不变），DSB 的漂移问题从结构上消失。每轮 KL 单调下降、收敛到 SB。
- 实现为交替训练前向/反向两个 drift 网络（IMF 的前后向版本），或看作「先 coupling 后 matching」的循环——与 [OT-CFM](../2302.00482_ot_cfm/) 一族的静态近似的区别是：耦合由模型自己迭代改进而非 minibatch OT 一次拍死。

## 实验与证据

- 高斯基准（SB 有闭式解）：DSBM 收敛到真解，DSB 随迭代漂离——方法论主张的直接验证。
- unpaired 翻译（EMNIST↔MNIST、下采样 CelebA）：质量与边际保持均优于 DSB/Rectified Flow 基线。
- 单细胞动力学插值：与 SF2M 可比，但适用范围更广（不依赖静态 OT 近似）。

## 在谱系中的位置

- 上游：[DSB](../2106.01357_dsb/)（被修复者）、[Léonard](../1308.0215_leonard_survey/)（Markov∩reciprocal 刻画）、bridge matching（Peluchetti）。
- 下游（本仓库内）：[SB Flow](../2409.09347_sb_flow/) 把 IMF 在线化（α-IMF）；[ASBM](../2405.14449_adv_sbm/) 做离散时间对抗版（D-IMF）；06 类的 path-space 语言（GSB-MDPO）直接沿用 IMF 的投影词汇。

## 与 SB×RL 的关联

IMF 是 SB×RL 算法设计的「标准零件库」：reciprocal 投影 = 用当前策略生成端点、参考桥填充路径（纯采样）；Markov 投影 = 把好的路径混合蒸馏回一个可执行策略（纯回归）。这个「采样-蒸馏」循环与 RL 里 planner-distillation、expert iteration 结构同构，嫁接点显然：在 reciprocal 步的端点采样里注入 advantage 加权（好端点多采），就得到一个 RL 化的 IMF——这条构造在 2026-09 没有正式文献。工程警告也从这里来：IMF 每轮要缓存/重生成样本，训练成本是 SB 策略上真机的最大障碍（SB Flow 的在线化正是为此）。

## 局限与批判

- 迭代训练的成本没有消失，只是从「不稳」换成「贵」：每轮 Markov 投影都是一次完整的回归训练。
- 收敛速度对参考过程方差 $\sigma$ 敏感，$\sigma$ 小（接近 OT）时耦合改进极慢。
- 图像实验仍在低分辨率，规模化要等 SB Flow。
