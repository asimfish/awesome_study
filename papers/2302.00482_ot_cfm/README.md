# Improving and Generalizing Flow-Based Generative Models with Minibatch Optimal Transport

> Tong, Fatras, Malkin, Huguet, Zhang, Rector-Brooks, Wolf, Bengio (Mila), TMLR 2024。[arXiv:2302.00482](https://arxiv.org/abs/2302.00482)

## 一句话

把 CFM 训练里独立采样的两端点换成 minibatch 最优传输配对，训练目标方差骤降、生成路径真正拉直，并顺手把框架推广到任意源分布——few-step 生成与 SB 近似的共同前置。

## 问题与动机

Flow Matching 的条件路径虽然逐条是直线，但端点 $(x_0, x_1)$ 独立采样，导致不同条件路径大量交叉：网络学到的边际速度场被迫在交叉处折中，实际生成轨迹是弯的。弯路径 = 粗步长误差大 = 少步采样质量差。修法：让端点配对本身接近 OT plan，路径不再交叉。

## 方法核心

广义 CFM 框架：任选端点耦合 $q(x_0, x_1)$，条件路径 $x_t = (1-t)x_0 + t\,x_1$（可加方差 $\sigma$），loss 不变：

$$
\mathcal{L} = \mathbb{E}_{t,\,(x_0,x_1)\sim q,\ x\sim p_t(\cdot|x_0,x_1)}\big[\|v_\theta(x,t) - (x_1 - x_0)\|^2\big]
$$

三个实例对应三种耦合：

- **I-CFM**：$q = p_0\otimes p_1$（独立），即原始 FM。
- **OT-CFM**：$q$ 取 minibatch 上解出的精确 OT plan（每个 batch 跑一次匈牙利/Sinkhorn）。定理：batch 足够大时逼近动态 OT（Benamou-Brenier），路径为直线且互不交叉。
- **SB-CFM**：$q$ 取 minibatch 熵正则 OT plan、路径加布朗桥方差，逼近 Schrödinger Bridge——SB 第一次被写成一个纯回归 loss 的近似（完整版是 [SF2M](../2307.03672_sf2m/)）。

关键收益：源分布不再要求高斯——任意两个可采样分布之间都能训 flow，unpaired 分布翻译从此进入 FM 工具箱。

## 实验与证据

- 2D 合成分布 + CIFAR-10：OT-CFM 同等步数下 FID 一致优于 I-CFM，少步（NFE < 20）区间优势拉大；训练目标方差显著更小、收敛更快。
- 单细胞轨迹推断（CITE-seq / Multiome）：利用「任意源分布」能力做时间点间的分布插值，优于此前 SOTA（TrajectoryNet 等）。
- minibatch OT 的偏差：batch 内 OT ≠ 全局 OT，论文承认这是近似并给出实证上可接受的证据。

## 在谱系中的位置

- 上游：[Flow Matching](../2210.02747_flow_matching/)。
- 下游（本仓库内）：[SF2M](../2307.03672_sf2m/)（同组，把 SB-CFM 补上 score 一侧做成完整 SB 求解器）；[MeanFlow](../2505.13447_meanflow/) 等 one-step 路线受益于直路径几何；[RSBM](../2604.05673_rsbm/) 的 bridge rectification 与本文的动机同构（拉直路径以支持少步）。

## 与 SB×RL 的关联

这篇是「SB 可以廉价近似」的转折点：SB-CFM 证明不需要 IPF 迭代、不需要 SDE rollout，一个加权回归就能得到 SB 的可用近似。对机器人策略：端点耦合设计是被低估的自由度——把「当前策略输出 ↔ 高回报动作」按 advantage 加权做耦合，等于在 coupling 层面注入 RL 信号，这条路线在 2026-09 仍是空格。路径直 = 少步稳的几何逻辑，也是 06 类 few-step SB 策略的立论基础。

## 局限与批判

- minibatch OT 的偏差没有非渐近界，batch 小、维度高时逼近质量未知——图像实验 batch 只有几百，理论与实践之间有缝。
- 每 batch 解 OT 的开销在高维大 batch 下不可忽略（尽管论文说占比小）。
- SB-CFM 只在小规模上验证，高维 SB 近似的质量要到 SF2M 才有认真评估。
