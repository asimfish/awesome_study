# Mean-Flow based One-Step Vision-Language-Action

> Chen, Ma, Zhao, arXiv 2026-03。[arXiv:2603.01469](https://arxiv.org/abs/2603.01469)

## 一句话

把 SmolVLA 的流匹配动作专家换成 MeanFlow 平均速度场，真机三任务上动作生成比 SmolVLA 快 8.7 倍、比 Diffusion Policy 快 83.9 倍，成功率相当——MeanFlow 进 VLA 的第一个公开尝试，价值在格局信号而非方法。

## 问题与动机

流匹配 VLA（π0、SmolVLA）的动作专家要多步 Euler 积分，每步一次前向；直接把 NFE 设为 1 会让轨迹幅度失控（论文实测 SmolVLA 在 NFE=1 下不可部署，除非加 consistency 正则）。MeanFlow 天然一步且免 consistency 约束——把它接到 VLA 上是自然的一步。

## 方法核心

- 骨干 SmolVLM-2（SigLIP 视觉编码 + SmolLM-2 语言解码），动作专家预测区间平均速度场 $u(z_t,r,t)$ 而非瞬时速度，训练用 MeanFlow 恒等式目标；推理一次前向从噪声跳到动作 chunk（chunk size 20）。
- 论文声称「解决了动作生成中的噪声引入问题」从而消除 consistency 约束——实质上就是 MeanFlow 恒等式本身的性质，没有额外机制。

## 实验与证据

- 三个真机操纵任务（PickPlace、Stacking、长程 Sorting），每任务 10 轮×10 次：One-Step VLA 动作生成速度比 SmolVLA 快 8.7 倍、比 DP 快 83.9 倍。
- 成功率：PickPlace 与 Sorting 与 SmolVLA 相当；Stacking 略低（高精度任务多步修正仍有优势）。
- 评价：只有真机小样本、无仿真基准、无 seed 统计；SmolVLA 多任务训练而 DP 单任务训练，对比条件不对齐。「相当」的结论证据薄。

## 在谱系中的位置

- 上游：[MeanFlow](../2505.13447_meanflow/)、[MP1](../2507.10543_mp1/)（MeanFlow 进操纵）、SmolVLA。
- 下游：[ReactVLA](../2606.14255_reactvla/)（三个月后在 LIBERO 上给出更完整的 MeanFlow-VLA 证据）。

## 与 SB×RL 的关联

作为格局信号看：2026 年 3 月起 MeanFlow 已在 VLA 动作头位置落地，一步化不再是小模型的专利。它也暴露了一步动作头的真实短板——高精度任务（Stacking）上一步不如多步修正。这个短板恰是 informative source 的用武之地：从上一 chunk / 粗轨迹出发的桥式一步生成，比从纯噪声出发的一步生成更有理由在精度任务上保住优势，可以直接在同样的 Stacking 设置上检验。

## 局限与批判

- 方法贡献几乎为零（MeanFlow 直接替换动作专家），论文的「消除 consistency 约束」是 MeanFlow 原文已有结论的重述。
- 实验条件不对齐、无统计量、无仿真基准，结论「成功率相当」不可靠。
- 无 RL、无多模态评测。收录理由仅为时间线完整性。
