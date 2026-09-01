# Score-Based Generative Modeling through Stochastic Differential Equations

> Song, Sohl-Dickstein, Kingma, Kumar, Ermon, Poole, ICLR 2021 (Oral, Outstanding Paper)。[arXiv:2011.13456](https://arxiv.org/abs/2011.13456)

## 一句话

把 DDPM 与 score matching 统一进连续时间 SDE 框架：前向 SDE 加噪、反向 SDE 去噪、还附赠一条同边际分布的确定性 ODE——此后所有扩散理论工作的通用语言。

## 问题与动机

2020 年有两条平行线：DDPM（离散马尔可夫链）和 NCSN（多尺度 score matching + Langevin）。两者形式不同但都在「学噪声下的 score」。这篇论文的问题：有没有一个框架把两者都当成特例，并且解锁只有连续时间才有的能力（精确似然、灵活求解器、可控生成）？

## 方法核心

前向加噪写成 SDE：

$$
dx = f(x,t)\,dt + g(t)\,dW_t
$$

Anderson 1982 的时间反演定理给出反向 SDE：

$$
dx = \big[f(x,t) - g(t)^2\,\nabla_x\log p_t(x)\big]\,dt + g(t)\,d\bar{W}_t
$$

唯一未知量是 score $\nabla\log p_t$，用 denoising score matching 训练。三个关键构造：

- **VE/VP SDE**：NCSN 对应方差爆炸（variance exploding），DDPM 对应方差保持（variance preserving）——两条线正式统一。
- **Probability Flow ODE**：$dx = [f - \frac{1}{2}g^2\nabla\log p_t]\,dt$，与反向 SDE 逐时刻同边际。生成变成解 ODE：可用现成求解器、可精确算似然（instantaneous change of variables）、潜空间可逆。
- **Predictor-Corrector 采样**：数值积分步（predictor）+ Langevin 校正步（corrector），采样质量显著提升。

## 实验与证据

- CIFAR-10：FID 2.20、IS 9.89（NCSN++），刷新当时记录；似然 2.99 bits/dim。
- 首次在 1024×1024 CelebA-HQ 上做高保真扩散生成。
- 零训练成本的可控生成：inpainting、上色、类条件生成都通过修改反向过程实现，不动预训练模型。

## 在谱系中的位置

- 上游：[DDPM](../2006.11239_ddpm/)、NCSN、Anderson 反演定理。
- 下游（本仓库内）：[Flow Matching](../2210.02747_flow_matching/) 直接回归 PF-ODE 一侧的速度场；[DSB](../2106.01357_dsb/) 把「前向固定、反向学」推广为「双向都学、两端都约束」；一切 bridge 方法的 SDE 语言都从这里来。

## 与 SB×RL 的关联

Score-SDE 是 SB 数学的直接前置：SB 的解也是一对互逆的 SDE，只是 drift 由 IPF/IMF 迭代决定而非单次 score matching。PF-ODE 是精确似然的通道——理论上生成式策略的 $\log\pi$ 可以沿 ODE 积分算出来，但每次要解一条 ODE，RL 训练循环里不可承受，这就是 log π 障碍的定量形式。理解 VE/VP 和反向 SDE，是读懂 FLAC 里 Girsanov 动能恒等式（路径 KL = drift 的 L2 能量）的最低数学门槛。

## 局限与批判

- 采样步数问题没有解决（PC 采样甚至更慢），把效率问题留给了后续十几篇工作。
- 连续时间似然训练（likelihood weighting）与样本质量此消彼长，权重选择是未决问题。
- 框架统一的代价是超参空间变大：SDE 形式、噪声表、求解器、corrector 步数，工程调参负担重。
