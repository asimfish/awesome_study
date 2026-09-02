# Awesome Study: Schrödinger Bridge × RL × Robot Policy Learning

![papers](https://img.shields.io/badge/papers-51-blue) ![zh--pdf](https://img.shields.io/badge/%E4%B8%AD%E6%96%87PDF-19-red) ![license](https://img.shields.io/badge/license-MIT-green)

围绕 **Schrödinger Bridge（SB）× 强化学习（RL）× 机器人策略学习** 的精读仓库。
每篇论文配：中文详细解读（`papers/*/README.md`）、英文原版 PDF；12 篇前沿论文另配保版式中文翻译 PDF（[SuperTranslate](https://github.com/asimfish/super_translate) 生成）。

**主线问题**：生成式策略（diffusion / flow / bridge）表达能力强，但 `log π` 不可算，经典 RL 的策略梯度/熵正则全部失效。本仓库沿三条线索组织文献：
1. **一步化**（MeanFlow 系）：把多步去噪压成 1-NFE，让 RL 微调回到普通策略优化；
2. **路径空间**（SB 系）：把 KL 正则从动作分布搬到轨迹测度，绕开 log π；
3. **桥式先验**（I2SB 系）：用 informative source 替代高斯先验，天然适配 sim-to-real 与导航。

绕开 `log π` 的五条实用路线在本库均有代表：逐步分解（DPPO/ReinFlow）· 路径空间（FLAC/GSB-MDPO）· 噪声空间（DSRL/LP-DS）· 条件化/加权监督（AWR/RECAP）· 生成-选择（MVP/DF-ExpEnse/FMQ）。

## 目录

- [生成模型基础（score / velocity / one-step）](#生成模型基础score-velocity-one-step)（7 篇）
- [Schrödinger Bridge 理论](#schrödinger-bridge-理论)（4 篇）
- [Bridge 算法（DSB 之后）](#bridge-算法dsb-之后)（7 篇）
- [强化学习基础](#强化学习基础)（5 篇）
- [生成式策略 × RL](#生成式策略-rl)（15 篇）
- [SB × RL 交叉前沿（选题主战场）](#sb-rl-交叉前沿选题主战场)（4 篇）
- [2026 前沿雷达（趋势报告收录的新变量）](#2026-前沿雷达趋势报告收录的新变量)（9 篇）
- [汇总报告](#汇总报告)
- [趋势与 insight](#趋势与-insight)

## 生成模型基础（score / velocity / one-step）

从 DDPM 到 MeanFlow：score → velocity → 平均速度场的一步化路线，外加机器人侧的事实标准 Diffusion Policy。

| 论文 | 作者 | 发表 | 定位 | 链接 |
|---|---|---|---|---|
| Denoising Diffusion Probabilistic Models | Ho, Jain, Abbeel | NeurIPS 2020 | 扩散模型开山：forward 加噪 + reverse 去噪 + ε-prediction | [arXiv](https://arxiv.org/abs/2006.11239) · [解读](papers/2006.11239_ddpm/README.md) · [EN](papers/2006.11239_ddpm/2006.11239.pdf) |
| Score-Based Generative Modeling through Stochastic Differential Equations | Song et al. | ICLR 2021 (Oral) | 连续时间统一框架：forward SDE / reverse SDE / PF-ODE | [arXiv](https://arxiv.org/abs/2011.13456) · [解读](papers/2011.13456_score_sde/README.md) · [EN](papers/2011.13456_score_sde/2011.13456.pdf) |
| Flow Matching for Generative Modeling | Lipman et al. | ICLR 2023 | velocity matching 范式：把生成变成从 0 到 1 的确定性传输 | [arXiv](https://arxiv.org/abs/2210.02747) · [解读](papers/2210.02747_flow_matching/README.md) · [EN](papers/2210.02747_flow_matching/2210.02747.pdf) |
| Improving and Generalizing Flow-Based Generative Models with Minibatch Optimal Transport | Tong et al. | TMLR 2024 | OT-CFM：OT coupling 拉直轨迹，few-step 的前置 | [arXiv](https://arxiv.org/abs/2302.00482) · [解读](papers/2302.00482_ot_cfm/README.md) · [EN](papers/2302.00482_ot_cfm/2302.00482.pdf) |
| Mean Flows for One-step Generative Modeling | Geng et al. | arXiv 2025 | 平均速度场恒等式 → 原生 1-NFE；MP1/DMPO/OFP 的共同基石 | [arXiv](https://arxiv.org/abs/2505.13447) · [解读](papers/2505.13447_meanflow/README.md) · [EN](papers/2505.13447_meanflow/2505.13447.pdf) · [中文](papers/2505.13447_meanflow/2505.13447.zh.pdf) |
| Diffusion Policy: Visuomotor Policy Learning via Action Diffusion | Chi et al. | RSS 2023 / IJRR | action chunk 上做扩散去噪，机器人操纵的事实标准 | [arXiv](https://arxiv.org/abs/2303.04137) · [解读](papers/2303.04137_diffusion_policy/README.md) · [EN](papers/2303.04137_diffusion_policy/2303.04137.pdf) |
| Flow Straight and Fast: Learning to Generate and Transfer Data with Rectified Flow | Liu, Gong, Liu | ICLR 2023 | reflow 迭代拉直耦合，few-step 与 RSBM 矫正思想的流侧源头 | [arXiv](https://arxiv.org/abs/2209.03003) · [解读](papers/2209.03003_rectified_flow/README.md) · [EN](papers/2209.03003_rectified_flow/2209.03003.pdf) |

## Schrödinger Bridge 理论

Schrödinger Bridge 的数学正典与神经化起点：path-space KL、IPF、GSB 推广。

| 论文 | 作者 | 发表 | 定位 | 链接 |
|---|---|---|---|---|
| A Survey of the Schrödinger Problem and Some of Its Connections with Optimal Transport | Léonard | DCDS 2014 | SB 数学正典：path-space KL 投影视角与 OT 联系 | [arXiv](https://arxiv.org/abs/1308.0215) · [解读](papers/1308.0215_leonard_survey/README.md) · [EN](papers/1308.0215_leonard_survey/1308.0215.pdf) |
| Diffusion Schrödinger Bridge with Applications to Score-Based Generative Modeling | De Bortoli et al. | NeurIPS 2021 | 第一个 neural SB（neural IPF），bridge 算法系的起点 | [arXiv](https://arxiv.org/abs/2106.01357) · [解读](papers/2106.01357_dsb/README.md) · [EN](papers/2106.01357_dsb/2106.01357.pdf) · [中文](papers/2106.01357_dsb/2106.01357.zh.pdf) |
| Generalized Schrödinger Bridge Matching | Liu et al. | ICLR 2024 | GSB：边界约束 + 路径 cost，通往 RL 的理论接口 | [arXiv](https://arxiv.org/abs/2310.02233) · [解读](papers/2310.02233_gsbm/README.md) · [EN](papers/2310.02233_gsbm/2310.02233.pdf) · [中文](papers/2310.02233_gsbm/2310.02233.zh.pdf) |
| Foundations of Schrödinger Bridges for Generative Modeling | — | arXiv 2026 | 面向生成建模的系统性综述（2026） | [arXiv](https://arxiv.org/abs/2603.18992) · [解读](papers/2603.18992_sb_foundations/README.md) · [EN](papers/2603.18992_sb_foundations/2603.18992.pdf) |

## Bridge 算法（DSB 之后）

DSB 之后的算法演化主线：IPF → IMF → 免仿真 → 在线 α-IMF → 对抗式少步。

| 论文 | 作者 | 发表 | 定位 | 链接 |
|---|---|---|---|---|
| I2SB: Image-to-Image Schrödinger Bridge | Liu et al. | ICML 2023 | informative source：把退化图像当 boundary 而非 condition | [arXiv](https://arxiv.org/abs/2302.05872) · [解读](papers/2302.05872_i2sb/README.md) · [EN](papers/2302.05872_i2sb/2302.05872.pdf) · [中文](papers/2302.05872_i2sb/2302.05872.zh.pdf) |
| Diffusion Schrödinger Bridge Matching | Shi et al. | NeurIPS 2023 | IMF：交替 Markovian 投影，修复 DSB 的 path-space 漂移 | [arXiv](https://arxiv.org/abs/2303.16852) · [解读](papers/2303.16852_dsbm/README.md) · [EN](papers/2303.16852_dsbm/2303.16852.pdf) · [中文](papers/2303.16852_dsbm/2303.16852.zh.pdf) |
| Simulation-Free Schrödinger Bridges via Score and Flow Matching | Tong et al. | AISTATS 2024 | 免仿真 SDE rollout：SB 变成两个 loss 的回归问题 | [arXiv](https://arxiv.org/abs/2307.03672) · [解读](papers/2307.03672_sf2m/README.md) · [EN](papers/2307.03672_sf2m/2307.03672.pdf) |
| Schrödinger Bridge Flow for Unpaired Data Translation | De Bortoli et al. (DeepMind) | NeurIPS 2024 | α-IMF 在线更新：单网络免重训迭代，规模化最成熟 | [arXiv](https://arxiv.org/abs/2409.09347) · [解读](papers/2409.09347_sb_flow/README.md) · [EN](papers/2409.09347_sb_flow/2409.09347.pdf) · [中文](papers/2409.09347_sb_flow/2409.09347.zh.pdf) |
| Adversarial Schrödinger Bridge Matching | Gushchin et al. | NeurIPS 2024 | 对抗式 D-IMF：SB 采样降到 ~4-5 NFE | [arXiv](https://arxiv.org/abs/2405.14449) · [解读](papers/2405.14449_adv_sbm/README.md) · [EN](papers/2405.14449_adv_sbm/2405.14449.pdf) |
| PRISM: Principled Reference Identification for Schrödinger Bridge Model | — | arXiv 2026 | SB 参考过程设计理论：不可见性原理 + 有限步预算下的最优参考谱 | [arXiv](https://arxiv.org/abs/2608.06893) · [解读](papers/2608.06893_prism/README.md) · [EN](papers/2608.06893_prism/2608.06893.pdf) · [中文](papers/2608.06893_prism/2608.06893.zh.pdf) |
| Soft-constrained Schrödinger Bridge: a Stochastic Control Approach | Garg, Zhang, Baudoin | AISTATS 2024 | 终端约束软化为 KL 惩罚的随机控制解，GSB 的另一条推导路径 | [arXiv](https://arxiv.org/abs/2403.01717) · [解读](papers/2403.01717_soft_sb/README.md) · [EN](papers/2403.01717_soft_sb/2403.01717.pdf) |

## 强化学习基础

为 SB×RL 提供 RL 侧接口的五篇经典：trust region、max-ent、mirror descent、免 critic、advantage-weighted BC。

| 论文 | 作者 | 发表 | 定位 | 链接 |
|---|---|---|---|---|
| Proximal Policy Optimization Algorithms | Schulman et al. | arXiv 2017 | clip = trust region 的工程化，on-policy 的事实标准 | [arXiv](https://arxiv.org/abs/1707.06347) · [解读](papers/1707.06347_ppo/README.md) · [EN](papers/1707.06347_ppo/1707.06347.pdf) |
| Soft Actor-Critic: Off-Policy Maximum Entropy Deep RL with a Stochastic Actor | Haarnoja et al. | ICML 2018 | max-ent RL：最优策略是 energy-based → SB 熵正则的近亲 | [arXiv](https://arxiv.org/abs/1801.01290) · [解读](papers/1801.01290_sac/README.md) · [EN](papers/1801.01290_sac/1801.01290.pdf) |
| Mirror Descent Policy Optimization | Tomar et al. | ICLR 2022 | KL 邻近点迭代视角，GSB-MDPO 的直接前驱 | [arXiv](https://arxiv.org/abs/2005.09814) · [解读](papers/2005.09814_mdpo/README.md) · [EN](papers/2005.09814_mdpo/2005.09814.pdf) |
| DeepSeekMath: Pushing the Limits of Mathematical Reasoning (GRPO) | Shao et al. | arXiv 2024 | group-relative advantage 免 critic，R1-style VLA RL 的源头 | [arXiv](https://arxiv.org/abs/2402.03300) · [解读](papers/2402.03300_grpo/README.md) · [EN](papers/2402.03300_grpo/2402.03300.pdf) |
| Advantage-Weighted Regression: Simple and Scalable Off-Policy RL | Peng et al. | arXiv 2019 | advantage-weighted BC：offline 策略提取绕开 log π 的钥匙 | [arXiv](https://arxiv.org/abs/1910.00177) · [解读](papers/1910.00177_awr/README.md) · [EN](papers/1910.00177_awr/1910.00177.pdf) |

## 生成式策略 × RL

生成式策略 × RL 的两代范式：序列建模/扩散规划 → offline Q+BC → online denoising-as-MDP → 一步策略实时控制。

| 论文 | 作者 | 发表 | 定位 | 链接 |
|---|---|---|---|---|
| Decision Transformer: Reinforcement Learning via Sequence Modeling | Chen et al. | NeurIPS 2021 | 路线 A 起点：trajectory 当 sequence，RL 变条件生成 | [arXiv](https://arxiv.org/abs/2106.01345) · [解读](papers/2106.01345_decision_transformer/README.md) · [EN](papers/2106.01345_decision_transformer/2106.01345.pdf) |
| Planning with Diffusion for Flexible Behavior Synthesis | Janner et al. | ICML 2022 | 路线 B 起点：把 planning 整体变成 diffusion + guidance | [arXiv](https://arxiv.org/abs/2205.09991) · [解读](papers/2205.09991_diffuser/README.md) · [EN](papers/2205.09991_diffuser/2205.09991.pdf) |
| Diffusion Policies as an Expressive Policy Class for Offline RL | Wang et al. | ICLR 2023 | diffusion 进 offline RL 的标杆：Q + BC 双项 | [arXiv](https://arxiv.org/abs/2208.06193) · [解读](papers/2208.06193_diffusion_ql/README.md) · [EN](papers/2208.06193_diffusion_ql/2208.06193.pdf) |
| Diffusion Policy Policy Optimization | Ren et al. | ICLR 2025 | denoising-as-MDP：对去噪链上的 action 做 PPO，在线微调标杆 | [arXiv](https://arxiv.org/abs/2409.00588) · [解读](papers/2409.00588_dppo/README.md) · [EN](papers/2409.00588_dppo/2409.00588.pdf) |
| MP1: MeanFlow Tames Policy Learning in 1-step for Robotic Manipulation | — | arXiv 2025 | MeanFlow 进机器人：1-NFE 策略生成 + Dispersive Loss | [arXiv](https://arxiv.org/abs/2507.10543) · [解读](papers/2507.10543_mp1/README.md) · [EN](papers/2507.10543_mp1/2507.10543.pdf) |
| DMPO: Dispersive MeanFlow Policy Optimization | — | arXiv 2026 | dispersive 表征正则 + PPO 微调，>120 Hz Franka 实机 | [arXiv](https://arxiv.org/abs/2601.20701) · [解读](papers/2601.20701_dmpo/README.md) · [EN](papers/2601.20701_dmpo/2601.20701.pdf) · [中文](papers/2601.20701_dmpo/2601.20701.zh.pdf) |
| One-step Flow Policy (self-distillation from scratch) | — | arXiv 2026 | 从零自蒸馏免教师，训练时间约 0.5 倍 | [arXiv](https://arxiv.org/abs/2603.12480) · [解读](papers/2603.12480_ofp/README.md) · [EN](papers/2603.12480_ofp/2603.12480.pdf) · [中文](papers/2603.12480_ofp/2603.12480.zh.pdf) |
| DBPO: Drift-Based Policy Optimization (v2) | — | arXiv 2026 | native one-step + online RL，105.2 Hz 控制频率 | [arXiv](https://arxiv.org/abs/2604.03540) · [解读](papers/2604.03540_dbpo/README.md) · [EN](papers/2604.03540_dbpo/2604.03540.pdf) |
| Flow Q-Learning | Park, Li, Levine | ICML 2025 | flow BC 策略 + 一步蒸馏 actor 做 Q 最大化，offline RL 的 flow 版标杆 | [arXiv](https://arxiv.org/abs/2502.02538) · [解读](papers/2502.02538_fql/README.md) · [EN](papers/2502.02538_fql/2502.02538.pdf) |
| Consistency Policy: Accelerated Visuomotor Policies via Consistency Distillation | Prasad, Lin, Wu, Bohg | RSS 2024 | 蒸馏路线的一步策略代表，MeanFlow 族要打败的对照 | [arXiv](https://arxiv.org/abs/2405.07503) · [解读](papers/2405.07503_consistency_policy/README.md) · [EN](papers/2405.07503_consistency_policy/2405.07503.pdf) |
| Flow-GRPO: Training Flow Matching Models via Online RL | Liu et al. | NeurIPS 2025 | ODE→SDE 转换让 flow 有逐步似然，GRPO 直接套上；免 critic 的 flow RL 源头 | [arXiv](https://arxiv.org/abs/2505.05470) · [解读](papers/2505.05470_flow_grpo/README.md) · [EN](papers/2505.05470_flow_grpo/2505.05470.pdf) |
| ReinFlow: Fine-tuning Flow Matching Policy with Online Reinforcement Learning | Zhang et al. | NeurIPS 2025 | 流策略注入可学噪声得逐步高斯似然，DPPO 的 flow 对位物 | [arXiv](https://arxiv.org/abs/2505.22094) · [解读](papers/2505.22094_reinflow/README.md) · [EN](papers/2505.22094_reinflow/2505.22094.pdf) |
| Steering Your Diffusion Policy with Latent Space Reinforcement Learning | Wagenmaker et al. | CoRL 2025 | 冻结解码器、RL 只动 latent 噪声：绕 log π 的第三条路线（噪声空间） | [arXiv](https://arxiv.org/abs/2506.15799) · [解读](papers/2506.15799_dsrl/README.md) · [EN](papers/2506.15799_dsrl/2506.15799.pdf) |
| OMP: One-step Meanflow Policy with Directional Alignment | — | arXiv 2025 | 方向对齐正则 + 谱分析评 mode coverage，一步策略多模态评测的先例 | [arXiv](https://arxiv.org/abs/2512.19347) · [解读](papers/2512.19347_omp/README.md) · [EN](papers/2512.19347_omp/2512.19347.pdf) |
| Aligning Flow Map Policies with Optimal Q-Guidance (FMQ) | — | arXiv 2026 | flow map 策略的统一框架 + Q 引导对齐，一步策略 offline RL 的整合者 | [arXiv](https://arxiv.org/abs/2605.12416) · [解读](papers/2605.12416_fmq/README.md) · [EN](papers/2605.12416_fmq/2605.12416.pdf) · [中文](papers/2605.12416_fmq/2605.12416.zh.pdf) |

## SB × RL 交叉前沿（选题主战场）

选题主战场：四条 SB×RL 进路（动能正则、path-space mirror descent、bridge rectification、跨域轨迹翻译）。

| 论文 | 作者 | 发表 | 定位 | 链接 |
|---|---|---|---|---|
| FLAC: Max-Entropy RL via Kinetic Energy Regularized Bridge Matching | ByteDance & Tsinghua | arXiv 2026 | 把 SAC max-ent 的策略熵换成动能正则 GSB，绕开生成式 log π | [arXiv](https://arxiv.org/abs/2602.12829) · [解读](papers/2602.12829_flac/README.md) · [EN](papers/2602.12829_flac/2602.12829.pdf) · [中文](papers/2602.12829_flac/2602.12829.zh.pdf) |
| GSB-MDPO: Path-Space Mirror Descent under the Generalized Schrödinger Bridge | — | arXiv 2026 | path-KL 替代动作 KL：proximal 更新搬进 path space，免 log π | [arXiv](https://arxiv.org/abs/2603.21621) · [解读](papers/2603.21621_gsb_mdpo/README.md) · [EN](papers/2603.21621_gsb_mdpo/2603.21621.pdf) · [中文](papers/2603.21621_gsb_mdpo/2603.21621.zh.pdf) |
| Rectified Schrödinger Bridge Matching for Few-Step Visual Navigation | — | arXiv 2026 | bridge 上做 rectification：3 步导航，few-step SB 策略实证 | [arXiv](https://arxiv.org/abs/2604.05673) · [解读](papers/2604.05673_rsbm/README.md) · [EN](papers/2604.05673_rsbm/2604.05673.pdf) · [中文](papers/2604.05673_rsbm/2604.05673.zh.pdf) |
| Bridging Dynamics Gaps via Diffusion Schrödinger Bridge for Cross-Domain RL | — | arXiv 2026 | sim-to-real 动力学差距：SB 做 unpaired 轨迹翻译 | [arXiv](https://arxiv.org/abs/2602.23737) · [解读](papers/2602.23737_bdg/README.md) · [EN](papers/2602.23737_bdg/2602.23737.pdf) · [中文](papers/2602.23737_bdg/2602.23737.zh.pdf) |

## 2026 前沿雷达（趋势报告收录的新变量）

趋势报告收录的 2026 年新变量：MeanFlow 族扩张（MVP/MFPO/UCA-Flow/ReactVLA）、桥式起点上主会（BridgePolicy）、绕开似然的 RL 微调（RECAP/LP-DS/DF-ExpEnse）。

| 论文 | 作者 | 发表 | 定位 | 链接 |
|---|---|---|---|---|
| Mean Flow Policy with Instantaneous Velocity Constraint for One-step Action Generation | — | ICLR 2026 (Oral) | ICLR 2026 Oral：平均速度策略 + best-of-N 选择做 offline-to-online RL，IVC 边界约束修 MeanFlow 恒等式解不唯一 | [arXiv](https://arxiv.org/abs/2602.13810) · [解读](papers/2602.13810_mvp/README.md) · [EN](papers/2602.13810_mvp/2602.13810.pdf) |
| Mean-Flow based One-Step Vision-Language-Action | — | arXiv 2026 | MeanFlow 动作头进 VLA，真机比 SmolVLA 快 8.7 倍 | [arXiv](https://arxiv.org/abs/2603.01469) · [解读](papers/2603.01469_mf_vla/README.md) · [EN](papers/2603.01469_mf_vla/2603.01469.pdf) |
| Mean Flow Policy Optimization | Dong et al. | ICML 2026 | MeanFlow 策略进 max-ent RL：平均散度网络硬算似然——FLAC 免似然路线的正面对手 | [arXiv](https://arxiv.org/abs/2604.14698) · [解读](papers/2604.14698_mfpo/README.md) · [EN](papers/2604.14698_mfpo/2604.14698.pdf) · [中文](papers/2604.14698_mfpo/2604.14698.zh.pdf) |
| ReactVLA: Fast and Lightweight Reactive Robot Manipulation via Improved Mean Flow Action Generation | — | arXiv 2026 | 改进 MeanFlow（iMF）+ 注意力残差路由，真机延迟 <38.6 ms | [arXiv](https://arxiv.org/abs/2606.14255) · [解读](papers/2606.14255_reactvla/README.md) · [EN](papers/2606.14255_reactvla/2606.14255.pdf) |
| Unified Condition-Action Modeling for Accurate One-Step Action Generation (UCA-Flow) | — | arXiv 2026 | 条件与动作统一 token 序列联合演化，一步生成 +9.3pp，比 MP1 快 2.3 倍 | [arXiv](https://arxiv.org/abs/2608.16153) · [解读](papers/2608.16153_uca_flow/README.md) · [EN](papers/2608.16153_uca_flow/2608.16153.pdf) · [中文](papers/2608.16153_uca_flow/2608.16153.zh.pdf) |
| π*0.6: a VLA That Learns From Experience (RECAP) | Physical Intelligence | arXiv 2025-11 | 优势条件化免策略梯度的真实世界 VLA RL，工业界对 log π 障碍的答案 | [arXiv](https://arxiv.org/abs/2511.14759) · [解读](papers/2511.14759_recap/README.md) · [EN](papers/2511.14759_recap/2511.14759.pdf) · [中文](papers/2511.14759_recap/2511.14759.zh.pdf) |
| Lagrangian Perturbation Diffusion Steering: Latent Reinforcement Learning for Generative Policies | Simsir, Oguz | ICML 2026 | DSRL 的信赖域修正 + 首个动作熵多模态保持评测 | [arXiv](https://arxiv.org/abs/2606.01151) · [解读](papers/2606.01151_lp_ds/README.md) · [EN](papers/2606.01151_lp_ds/2606.01151.pdf) · [中文](papers/2606.01151_lp_ds/2606.01151.zh.pdf) |
| DF-ExpEnse: Diffusion Filtered Exploration for Sample Efficient Finetuning | — | arXiv 2026 | DSRL/ResFiT 的探索增强：batch 候选动作按探索兴趣筛选 | [arXiv](https://arxiv.org/abs/2606.19656) · [解读](papers/2606.19656_df_expense/README.md) · [EN](papers/2606.19656_df_expense/2606.19656.pdf) |
| Sample from What You See: Visuomotor Policy Learning via Diffusion Bridge with Observation-Embedded SDE (BridgePolicy) | Liu et al. (ShanghaiTech) | ICML 2026 | 观测嵌入 SDE 从观测先验起步而非噪声：informative source 策略的顶会锚点 | [arXiv](https://arxiv.org/abs/2512.07212) · [解读](papers/2512.07212_bridge_policy/README.md) · [EN](papers/2512.07212_bridge_policy/2512.07212.pdf) · [中文](papers/2512.07212_bridge_policy/2512.07212.zh.pdf) |

## 汇总报告

| 产物 | 说明 |
|---|---|
| [`slides/overview.html`](slides/overview.html) | HTML PPT：全库综述（浏览器打开，方向键翻页） |
| [`slides/overview.pdf`](slides/overview.pdf) | PDF 版综述报告（Beamer） |
| [`reports/TRENDS_2026.md`](reports/TRENDS_2026.md) | 2026 前沿趋势与 insight 报告 |

## 趋势与 insight

见 [`reports/TRENDS_2026.md`](reports/TRENDS_2026.md)：2026 年 5 月后的新论文雷达、趋势判断、空白与机会、风险。

## 构建工具

| 脚本 | 作用 |
|---|---|
| `tools/download_papers.py` | 按 `data/papers.json` 批量下载 arXiv PDF |
| `tools/translate_batch.sh` | 批量保版式翻译（SuperTranslate + DeepSeek） |
| `tools/gen_readme.py` | 重新生成本 README（链接自动探测产物） |

## 致谢

- 翻译：[SuperTranslate](https://github.com/asimfish/super_translate)
- 排版规范参考：[awesome-ml4co](https://github.com/Thinklab-SJTU/awesome-ml4co)
- PPT：[ppt-master](https://github.com/hugohe3/ppt-master)；PDF 报告：[beamer-skill](https://github.com/Noi1r/beamer-skill)
