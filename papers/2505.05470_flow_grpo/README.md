# Flow-GRPO: Training Flow Matching Models via Online RL

> Liu et al., NeurIPS 2025。[arXiv:2505.05470](https://arxiv.org/abs/2505.05470)

## 一句话

两个技巧让 GRPO 能训流匹配模型：ODE→SDE 转换（把确定性流变成逐时刻同边际的随机过程，从而有逐步高斯似然和探索）+ 去噪缩减（训练少步、推理全步）——SD3.5-M 在 GenEval 上 63%→95%，且几乎没有 reward hacking。flow 侧免 critic RL 的源头，R1-style VLA RL 的直接上游。

## 问题与动机

GRPO 在语言模型上证明了「组内相对优势 + PPO clip」可以免 critic 做 RL。流匹配模型是确定性 ODE：给定噪声输出唯一，既没有可算的逐步似然也没有探索的随机性——策略梯度无处下手。此外训练时每个样本要跑完整去噪链，采样成本是瓶颈。

## 方法核心

1. **ODE→SDE 转换**：对流 ODE $dx=v_\theta(x,t)dt$ 构造一个 SDE，其边际分布在所有时刻与 ODE 一致（利用 [Score-SDE](../2011.13456_score_sde/) 里 PF-ODE 与反向 SDE 同边际的关系，score 由速度场换算得到）。离散化后每个去噪步是高斯转移 $p_\theta(x_{t-1}|x_t)=\mathcal{N}(\mu_\theta,\sigma_t^2I)$——**逐步似然闭式、随机性可控**，与 [DPPO](../2409.00588_dppo/) 的两层 MDP 同构。噪声强度是探索旋钮。
2. **GRPO 目标**：同一 prompt 采一组样本，回报组内标准化得优势 $\hat A_i$，沿去噪链的逐步 ratio 做 PPO clip，加对参考模型的 KL。
3. **去噪缩减**：训练时用很少的去噪步（如 10）采样与更新，推理仍用原始步数（如 40）——利用 SDE 边际一致性，少步训练的策略在多步推理下仍有效，采样成本降几倍。

## 实验与证据

- 组合生成（GenEval）：63%→95%，物体计数、空间关系、属性绑定接近完美。
- 视觉文字渲染：59%→92%。
- 人类偏好对齐：显著提升；图像质量与多样性几乎不退——reward hacking 少，归功于 KL 与去噪链上的随机性。
- 评价：文生图上的证据强；机器人侧的意义是方法论移植（Flow-GRPO 本身不做控制）。

## 在谱系中的位置

- 上游：[GRPO](../2402.03300_grpo/)、[Flow Matching](../2210.02747_flow_matching/)、[Score-SDE](../2011.13456_score_sde/)（ODE/SDE 等价）、DDPO（扩散 RLHF）。
- 平行：[ReinFlow](../2505.22094_reinflow/)（同期、面向机器人控制的 flow 在线 RL，注噪方式不同）。
- 下游：SimpleVLA-RL、π-RL 等 R1-style VLA RL；[GSB-MDPO](../2603.21621_gsb_mdpo/) 的基线之一。

## 与 SB×RL 的关联

Flow-GRPO 的 ODE→SDE 转换在 SB 语言里就是「给确定性传输加回熵正则」——它把 flow 临时变成一个带噪的桥，只为拿到似然与探索，训练完再把噪声关掉。SB 策略天生就是这个形态（$\epsilon>0$ 的随机桥），不需要转换：GRPO 外壳可以直接套在 SB 策略的逐步高斯转移上，组内相对优势替代 critic、路径 KL（而非逐 token KL）作参考正则——「GRPO 外壳 + GSB-MDPO 内核」是 [GRPO](../2402.03300_grpo/) 解读里指出的空格，Flow-GRPO 提供了外壳的成熟实现。去噪缩减的思想对 SB 同样成立（IMF 的边际一致性保证少步训练多步推理），能大幅降低 SB 策略 RL 训练的采样成本。

## 局限与批判

- 组内相对优势没有过程监督，credit 沿去噪链均摊（与 DPPO 同病）。
- 噪声强度是新超参，太小探索不足、太大偏离 ODE 边际（离散化误差）。
- 全部文生图实验，控制任务上的样本效率与稳定性要看 ReinFlow/后续 VLA 工作。
- KL 正则用参考模型，微调后策略被锚在预训练分布附近，超越示范的能力有限。
