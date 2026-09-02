# Flow Q-Learning

> Park, Li, Levine (UC Berkeley), ICML 2025。[arXiv:2502.02538](https://arxiv.org/abs/2502.02538)

## 一句话

不对多步流策略做 RL，而是训一个一步策略同时模仿流 BC 策略（蒸馏项）与最大化 Q（RL 项）：避开穿过迭代生成的递归反传、测试时一步出动作、表达力基本保留——73 个 OGBench/D4RL 任务上 offline 与 offline-to-online 的 flow 版标杆。

## 问题与动机

流/扩散策略进 offline RL 的两条老路都别扭：Diffusion-QL 式把 Q 梯度穿过整条生成链（不稳、贵）；加权 BC 式（AWR/IDQL）只能重加权不能外推。FQL 的想法：表达力交给流 BC 策略，优化交给一个单独的一步策略，两者用蒸馏连接。

## 方法核心

三个网络：流 BC 策略 $\pi^{\text{flow}}$（标准 flow matching 训练，不接 Q）、一步策略 $\mu_\omega(s,z)$（噪声 $z$ 到动作的直接映射）、critic $Q$。一步策略的损失：

$$
\mathcal{L}(\omega)=\underbrace{\mathbb{E}_{s,z}\big[\|\mu_\omega(s,z)-\text{ODE}_{\pi^{\text{flow}}}(s,z)\|^2\big]}_{\text{蒸馏：模仿流策略从同一噪声出发的输出}}\ -\ \alpha\,\mathbb{E}_{s,z}\big[Q(s,\mu_\omega(s,z))\big]
$$

- 蒸馏项把一步策略锚在 BC 分布内（起到行为正则作用），Q 项让它在分布内寻优；$\alpha$ 权衡。
- 关键红利：**Q 梯度只穿过一步网络**，没有递归反传；测试时只用 $\mu_\omega$，一步出动作；流策略的多模态由蒸馏近似保留（从不同 $z$ 出发对应不同模式）。
- critic 用一步策略采样的动作做 TD 目标（标准 double Q）。

## 实验与证据

- OGBench（状态 + 像素）+ D4RL 共 73 任务：offline 与 offline-to-online 两种设定下整体最强或并列最强，对比 IQL/ReBRAC/IDQL/扩散 Q 类方法。
- 消融：去蒸馏项（纯 Q 一步策略）崩溃——行为正则是必需的；直接对流策略做 Q 引导（递归反传版）更不稳且更慢。
- 简洁性本身是证据：实现比 Diffusion-QL 简单，超参少。

## 在谱系中的位置

- 上游：[Diffusion-QL](../2208.06193_diffusion_ql/)（Q+BC 范式）、[Flow Matching](../2210.02747_flow_matching/)、[AWR](../1910.00177_awr/)。
- 下游：[MVP](../2602.13810_mvp/)、[FMQ](../2605.12416_fmq/)（在 OGBench 上超越它的一步策略后继）、QC/BFN。
- 与 [Consistency Policy](../2405.07503_consistency_policy/) 对照：都是「多步教师 → 一步学生」，FQL 的学生同时接 RL。

## 与 SB×RL 的关联

FQL 确立了「表达力与优化解耦」的模板：多步生成模型只当教师，RL 只作用在一步学生上——log π 障碍、credit assignment、推理速度三个问题一次全绕开。这个模板对 SB 策略是零成本可用的：把教师换成桥策略（informative 起点 + 多模态覆盖），学生仍是一步网络，蒸馏项自动把桥的耦合结构传给学生。反过来它也划出了 SB 的必要条件：如果桥教师蒸馏后的一步学生与流教师蒸馏后的没有可测差别（多模态、精度、样本效率任一维），SB 在 offline RL 里就没有位置——这是一个便宜且决定性的对照实验。

## 局限与批判

- 一步学生的表达力上限低于教师，「基本保留」在高度多模态任务上会打折（论文承认）。
- 蒸馏目标要求解教师 ODE 得到目标动作，训练开销转移到了教师采样上。
- $\alpha$ 跨任务要调（与 Diffusion-QL 同样的问题）。
- 无真机；像素任务在 OGBench 内，视觉规模有限。
