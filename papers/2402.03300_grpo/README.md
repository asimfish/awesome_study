# DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models (GRPO)

> Shao, Wang, Zhu, Xu et al. (DeepSeek-AI), arXiv 2024。[arXiv:2402.03300](https://arxiv.org/abs/2402.03300)

## 一句话

用组内相对优势替代 critic 网络（GRPO），让 PPO 式 RL 在大模型上便宜一半显存，成为 R1 一系推理 RL 与 VLA RL 微调的算法源头。

## 问题与动机

论文主体是数学推理语言模型（DeepSeekMath 7B），但被后世反复引用的是 §4 的 GRPO 算法。PPO 在 LLM 上的痛点：value 网络和 policy 一样大，训练它既贵又不稳（reward 稀疏、逐 token 的 value 学不准）。GRPO 的观察：对同一个 prompt 采一组回答，组内平均回报本身就是 baseline，不需要学出来。

## 方法核心

对每个问题 $q$ 采样一组 $G$ 个输出 $\{o_1,\dots,o_G\}$，组内标准化的相对优势为

$$
\hat{A}_i = \frac{r_i - \text{mean}(r_1,\dots,r_G)}{\text{std}(r_1,\dots,r_G)}
$$

目标函数保持 PPO-clip 形式，另加一个对参考策略的 KL 正则（写成逐 token 的无偏估计）：

$$
\mathcal{L} = \mathbb{E}\Big[\min\big(r_t\hat{A}_i,\ \text{clip}(r_t,1\pm\epsilon)\hat{A}_i\big)\Big] - \beta\, \mathrm{KL}(\pi_\theta\,\|\,\pi_{\text{ref}})
$$

- 去掉了 critic：优势不来自 $Q-V$，来自组内比较。代价是优势是回合级常数（同一回答内每个 token 共享），credit assignment 更粗。
- $\pi_{\text{ref}}$：SFT 模型，防漂移。

DeepSeekMath 本身的贡献链条：120B 数学 token 预训练 → SFT → GRPO，7B 模型 MATH 达到 51.7%，逼近当时的 GPT-4。

## 实验与证据

- MATH benchmark：GRPO 把 DeepSeekMath-Instruct 7B 从 46.8% 提到 51.7%（top1），GSM8K 82.9%→88.2%。
- 相对 PPO：同等效果下省掉 value 网络的全部显存与训练开销。
- 后续外部证据（非本文）：R1-Zero 证明纯 GRPO 可以从 base 模型直接激发推理能力，SimpleVLA-RL 等把它搬进 VLA。

## 在谱系中的位置

- 上游：[PPO](../1707.06347_ppo/)。
- 下游（本仓库内）：机器人侧的 Flow-GRPO、SimpleVLA-RL 等 R1-style VLA RL（见 [趋势报告](../../reports/TRENDS_2026.md)）；与 [AWR](../1910.00177_awr/) 同属"绕开精确 critic"的路线。

## 与 SB×RL 的关联

GRPO 对生成式策略 RL 的意义在于它把对 $\log\pi$ 的依赖降到最低形态：只需要 ratio（新旧策略的相对似然），且优势不需要 critic。对于扩散/流策略，逐去噪步的 ratio 仍然可算（每步是高斯），所以 GRPO 是 log π 障碍下少数能直接用的 on-policy 算法——Flow-GRPO 就是这么做的。对 SB 策略：组内相对优势 + 路径空间 KL 正则的组合（GRPO 外壳 + GSB-MDPO 内核）是一个还没人做的空格。

## 局限与批判

- 回合级优势没有过程监督，长序列 credit assignment 粗糙；后续工作（PRM、step-level GRPO）都在补这里。
- std 归一化在组内回报全对/全错时退化（除零或优势为零），实际实现要加保护，数学上不优雅。
- KL 正则的无偏估计子在 ratio 大时方差爆炸，这个问题论文没讨论。
- 论文将预训练/SFT/RL 三段混在一起报数，GRPO 单独的贡献量化得不干净。
