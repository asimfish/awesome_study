# Awesome Study: Schrödinger Bridge × RL × Robot Policy Learning

![papers](https://img.shields.io/badge/papers-51-blue) ![notes](https://img.shields.io/badge/%E4%B8%AD%E6%96%87%E8%A7%A3%E8%AF%BB-51-brightgreen) ![zh--pdf](https://img.shields.io/badge/%E4%B8%AD%E6%96%87PDF-19-red) ![code](https://img.shields.io/badge/%E4%BB%A3%E7%A0%81%E9%93%BE%E6%8E%A5-37-orange) ![updated](https://img.shields.io/badge/updated-2026--09--07-lightgrey) ![license](https://img.shields.io/badge/license-MIT-green)

围绕 **Schrödinger Bridge（SB）× 强化学习（RL）× 机器人策略学习** 的精读仓库：51 篇论文，每篇配中文详细解读（`papers/*/README.md`，七节结构：一句话 / 问题与动机 / 方法核心 / 实验与证据 / 谱系位置 / 与 SB×RL 的关联 / 局限与批判）与英文原版 PDF；19 篇前沿论文另配保版式中文翻译 PDF（[SuperTranslate](https://github.com/asimfish/super_translate) 生成）；37 篇附官方代码或项目页。

**主线问题**：生成式策略（diffusion / flow / bridge）表达能力强，但 `log π` 不可算，经典 RL 的策略梯度 / 熵正则 / 概率比全部失效。本仓库沿三条线索组织文献：
1. **一步化**（MeanFlow 系）：把多步去噪压成 1-NFE，让 RL 微调回到普通策略优化；
2. **路径空间**（SB 系）：把 KL 正则从动作分布搬到轨迹测度，绕开 log π；
3. **桥式先验**（I2SB 系）：用 informative source 替代高斯先验，天然适配 sim-to-real 与导航。

处理 `log π` 障碍的五条路线在本库均有代表：逐步分解（DPPO / ReinFlow）· 路径空间（FLAC / GSB-MDPO）· 噪声空间（DSRL / LP-DS）· 条件化 / 加权监督（AWR / RECAP）· 生成-选择（MVP / FMQ / DF-ExpEnse）；另有似然近似路线（MFPO）与之对峙。

> **先读** [十分钟速览](reports/DIGEST.md) · **要选题** [开放问题与实验设计](reports/OPEN_PROBLEMS.md) · **横向比** [三张对比表](reports/COMPARISON.md) · **按背景读** [阅读路线](reports/READING_PATHS.md) · **查词** [术语表](reports/GLOSSARY.md) · **看趋势** [2026 雷达](reports/TRENDS_2026.md)

## 目录

- [生成模型基础（score / velocity / one-step）](#生成模型基础（score--velocity--one-step）)（7 篇）
- [Schrödinger Bridge 理论](#schrödinger-bridge-理论)（4 篇）
- [Bridge 算法（DSB 之后）](#bridge-算法（dsb-之后）)（7 篇）
- [强化学习基础](#强化学习基础)（5 篇）
- [生成式策略 × RL](#生成式策略-×-rl)（15 篇）
- [SB × RL 交叉前沿（选题主战场）](#sb-×-rl-交叉前沿（选题主战场）)（4 篇）
- [2026 前沿雷达（趋势报告收录的新变量）](#2026-前沿雷达（趋势报告收录的新变量）)（9 篇）
- [汇总报告](#汇总报告)
- [仓库结构](#仓库结构)
- [如何扩展](#如何扩展)
- [质量说明](#质量说明)
- [更新日志](#更新日志)
- [引用](#引用)

## 生成模型基础（score / velocity / one-step）

从 DDPM 到 MeanFlow：score → velocity → 平均速度场的一步化路线，外加机器人侧的事实标准 Diffusion Policy。

| 论文 | 作者 | 发表 | 定位 | 链接 |
|---|---|---|---|---|
| Denoising Diffusion Probabilistic Models (DDPM) | Ho, Jain, Abbeel | NeurIPS 2020 | 高质量扩散生成范式：forward 加噪 + reverse 去噪 + ε-prediction | [arXiv](https://arxiv.org/abs/2006.11239) · [解读](papers/2006.11239_ddpm/README.md) · [EN](papers/2006.11239_ddpm/2006.11239.pdf) · [代码](https://github.com/hojonathanho/diffusion) |
| Score-Based Generative Modeling through Stochastic Differential Equations (Score-SDE) | Song, Sohl-Dickstein, Kingma et al. | ICLR 2021 (Oral) | 连续时间统一框架：forward SDE / reverse SDE / PF-ODE | [arXiv](https://arxiv.org/abs/2011.13456) · [解读](papers/2011.13456_score_sde/README.md) · [EN](papers/2011.13456_score_sde/2011.13456.pdf) · [代码](https://github.com/yang-song/score_sde_pytorch) |
| Flow Straight and Fast: Learning to Generate and Transfer Data with Rectified Flow (Rectified Flow) | Liu, Gong, Liu | ICLR 2023 | reflow 迭代拉直耦合，few-step 与 RSBM 矫正思想的流侧源头 | [arXiv](https://arxiv.org/abs/2209.03003) · [解读](papers/2209.03003_rectified_flow/README.md) · [EN](papers/2209.03003_rectified_flow/2209.03003.pdf) · [代码](https://github.com/gnobitab/RectifiedFlow) |
| Flow Matching for Generative Modeling | Lipman, Chen, Ben-Hamu et al. | ICLR 2023 | velocity matching 范式：把生成变成从 0 到 1 的确定性传输 | [arXiv](https://arxiv.org/abs/2210.02747) · [解读](papers/2210.02747_flow_matching/README.md) · [EN](papers/2210.02747_flow_matching/2210.02747.pdf) · [代码](https://github.com/facebookresearch/flow_matching) |
| Improving and generalizing flow-based generative models with minibatch optimal transport (OT-CFM) | Tong, Fatras, Malkin et al. | TMLR 2024 | OT-CFM：OT coupling 拉直轨迹，few-step 的前置 | [arXiv](https://arxiv.org/abs/2302.00482) · [解读](papers/2302.00482_ot_cfm/README.md) · [EN](papers/2302.00482_ot_cfm/2302.00482.pdf) · [代码](https://github.com/atong01/conditional-flow-matching) |
| Diffusion Policy: Visuomotor Policy Learning via Action Diffusion | Chi, Xu, Feng et al. | RSS 2023 / IJRR | action chunk 上做扩散去噪，机器人操纵的事实标准 | [arXiv](https://arxiv.org/abs/2303.04137) · [解读](papers/2303.04137_diffusion_policy/README.md) · [EN](papers/2303.04137_diffusion_policy/2303.04137.pdf) · [代码](https://github.com/real-stanford/diffusion_policy) |
| Mean Flows for One-step Generative Modeling | Geng, Deng, Bai et al. | arXiv 2025 | 平均速度场恒等式 → 原生 1-NFE；MP1/DMPO/OFP 的共同基石 | [arXiv](https://arxiv.org/abs/2505.13447) · [解读](papers/2505.13447_meanflow/README.md) · [EN](papers/2505.13447_meanflow/2505.13447.pdf) · [中文](papers/2505.13447_meanflow/2505.13447.zh.pdf) · [代码](https://github.com/Gsunshine/meanflow) |

## Schrödinger Bridge 理论

Schrödinger Bridge 的数学正典与神经化起点：path-space KL、IPF、GSB 推广。

| 论文 | 作者 | 发表 | 定位 | 链接 |
|---|---|---|---|---|
| A survey of the Schrödinger problem and some of its connections with optimal transport | Léonard | DCDS 2014 | SB 数学正典：path-space KL 投影视角与 OT 联系 | [arXiv](https://arxiv.org/abs/1308.0215) · [解读](papers/1308.0215_leonard_survey/README.md) · [EN](papers/1308.0215_leonard_survey/1308.0215.pdf) |
| Diffusion Schrödinger Bridge with Applications to Score-Based Generative Modeling (DSB) | Bortoli, Thornton, Heng, Doucet | NeurIPS 2021 | neural SB（neural IPF），bridge 算法系的起点 | [arXiv](https://arxiv.org/abs/2106.01357) · [解读](papers/2106.01357_dsb/README.md) · [EN](papers/2106.01357_dsb/2106.01357.pdf) · [中文](papers/2106.01357_dsb/2106.01357.zh.pdf) · [代码](https://github.com/JTT94/diffusion_schrodinger_bridge) |
| Generalized Schrödinger Bridge Matching (GSBM) | Liu, Lipman, Nickel et al. | ICLR 2024 | GSB：边界约束 + 路径 cost，通往 RL 的理论接口 | [arXiv](https://arxiv.org/abs/2310.02233) · [解读](papers/2310.02233_gsbm/README.md) · [EN](papers/2310.02233_gsbm/2310.02233.pdf) · [中文](papers/2310.02233_gsbm/2310.02233.zh.pdf) · [代码](https://github.com/facebookresearch/generalized-schrodinger-bridge-matching) |
| Foundations of Schrödinger Bridges for Generative Modeling | Tang | arXiv 2026 | 面向生成建模的系统性综述（2026） | [arXiv](https://arxiv.org/abs/2603.18992) · [解读](papers/2603.18992_sb_foundations/README.md) · [EN](papers/2603.18992_sb_foundations/2603.18992.pdf) |

## Bridge 算法（DSB 之后）

DSB 之后的算法演化主线：IPF → IMF → 免仿真 → 在线 α-IMF → 对抗式少步；另含软约束与参考过程设计理论。

| 论文 | 作者 | 发表 | 定位 | 链接 |
|---|---|---|---|---|
| I$^2$SB: Image-to-Image Schrödinger Bridge | Liu, Vahdat, Huang et al. | ICML 2023 | informative source：把退化图像当 boundary 而非 condition | [arXiv](https://arxiv.org/abs/2302.05872) · [解读](papers/2302.05872_i2sb/README.md) · [EN](papers/2302.05872_i2sb/2302.05872.pdf) · [中文](papers/2302.05872_i2sb/2302.05872.zh.pdf) · [代码](https://github.com/NVlabs/I2SB) |
| Diffusion Schrödinger Bridge Matching (DSBM) | Shi, Bortoli, Campbell, Doucet | NeurIPS 2023 | IMF：交替 Markovian / reciprocal 投影，缓解 DSB 的 path-space 漂移 | [arXiv](https://arxiv.org/abs/2303.16852) · [解读](papers/2303.16852_dsbm/README.md) · [EN](papers/2303.16852_dsbm/2303.16852.pdf) · [中文](papers/2303.16852_dsbm/2303.16852.zh.pdf) · [代码](https://github.com/yuyang-shi/dsbm-pytorch) |
| Simulation-free Schrödinger bridges via score and flow matching (SF2M) | Tong, Malkin, Fatras et al. | AISTATS 2024 | 免仿真 SDE rollout：SB 变成两个 loss 的回归问题 | [arXiv](https://arxiv.org/abs/2307.03672) · [解读](papers/2307.03672_sf2m/README.md) · [EN](papers/2307.03672_sf2m/2307.03672.pdf) · [代码](https://github.com/atong01/conditional-flow-matching) |
| Soft-constrained Schrodinger Bridge: a Stochastic Control Approach (Soft-SB) | Garg, Zhang, Zhou | AISTATS 2024 | 终端约束软化为 KL 惩罚的随机控制解，GSB 路径成本的对照 | [arXiv](https://arxiv.org/abs/2403.01717) · [解读](papers/2403.01717_soft_sb/README.md) · [EN](papers/2403.01717_soft_sb/2403.01717.pdf) |
| Adversarial Schrödinger Bridge Matching (ASBM) | Gushchin, Selikhanovych, Kholkin et al. | NeurIPS 2024 | 对抗式 D-IMF：人脸翻译 SB 采样降到 4 NFE | [arXiv](https://arxiv.org/abs/2405.14449) · [解读](papers/2405.14449_adv_sbm/README.md) · [EN](papers/2405.14449_adv_sbm/2405.14449.pdf) · [代码](https://github.com/Daniil-Selikhanovych/ASBM) |
| Schrödinger Bridge Flow for Unpaired Data Translation | Bortoli, Korshunova, Mnih, Doucet | NeurIPS 2024 | α-IMF 在线更新：单网络免重训迭代，规模化最成熟 | [arXiv](https://arxiv.org/abs/2409.09347) · [解读](papers/2409.09347_sb_flow/README.md) · [EN](papers/2409.09347_sb_flow/2409.09347.pdf) · [中文](papers/2409.09347_sb_flow/2409.09347.zh.pdf) |
| PRISM: Principled Reference Identification for Schrodinger Bridge Model | Fallah, Yang | arXiv 2026 | 高斯复原桥参考过程设计理论：不可见性原理 + 共享调度下有限步预算的最优参考谱 | [arXiv](https://arxiv.org/abs/2608.06893) · [解读](papers/2608.06893_prism/README.md) · [EN](papers/2608.06893_prism/2608.06893.pdf) · [中文](papers/2608.06893_prism/2608.06893.zh.pdf) |

## 强化学习基础

为 SB×RL 提供 RL 侧接口的五篇经典：trust region、max-ent、mirror descent、免 critic、advantage-weighted BC。

| 论文 | 作者 | 发表 | 定位 | 链接 |
|---|---|---|---|---|
| Proximal Policy Optimization Algorithms (PPO) | Schulman, Wolski, Dhariwal et al. | arXiv 2017 | clip = trust region 的工程化，on-policy 的事实标准 | [arXiv](https://arxiv.org/abs/1707.06347) · [解读](papers/1707.06347_ppo/README.md) · [EN](papers/1707.06347_ppo/1707.06347.pdf) · [代码](https://github.com/openai/baselines) |
| Soft Actor-Critic: Off-Policy Maximum Entropy Deep Reinforcement Learning with a Stochastic Actor (SAC) | Haarnoja, Zhou, Abbeel, Levine | ICML 2018 | max-ent RL：最优策略是 energy-based → SB 熵正则的近亲 | [arXiv](https://arxiv.org/abs/1801.01290) · [解读](papers/1801.01290_sac/README.md) · [EN](papers/1801.01290_sac/1801.01290.pdf) · [代码](https://github.com/haarnoja/sac) |
| Advantage-Weighted Regression: Simple and Scalable Off-Policy Reinforcement Learning (AWR) | Peng, Kumar, Zhang, Levine | arXiv 2019 | advantage-weighted BC：offline 策略提取绕开行为策略密度与概率比的钥匙 | [arXiv](https://arxiv.org/abs/1910.00177) · [解读](papers/1910.00177_awr/README.md) · [EN](papers/1910.00177_awr/1910.00177.pdf) · [代码](https://github.com/xbpeng/awr) |
| Mirror Descent Policy Optimization (MDPO) | Tomar, Shani, Efroni, Ghavamzadeh | ICLR 2022 | KL 邻近点迭代视角，GSB-MDPO 的直接前驱 | [arXiv](https://arxiv.org/abs/2005.09814) · [解读](papers/2005.09814_mdpo/README.md) · [EN](papers/2005.09814_mdpo/2005.09814.pdf) · [代码](https://github.com/manantomar/Mirror-Descent-Policy-Optimization) |
| DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models (GRPO) | Shao, Wang, Zhu et al. | arXiv 2024 | group-relative advantage 免 critic，R1-style VLA RL 的源头 | [arXiv](https://arxiv.org/abs/2402.03300) · [解读](papers/2402.03300_grpo/README.md) · [EN](papers/2402.03300_grpo/2402.03300.pdf) · [代码](https://github.com/deepseek-ai/DeepSeek-Math) |

## 生成式策略 × RL

生成式策略 × RL 的两代范式：序列建模/扩散规划 → offline Q+BC → online 微调（分解 / 噪声空间）→ 原生一步竞赛 → 流映射统一。

| 论文 | 作者 | 发表 | 定位 | 链接 |
|---|---|---|---|---|
| Decision Transformer: Reinforcement Learning via Sequence Modeling | Chen, Lu, Rajeswaran et al. | NeurIPS 2021 | 路线 A 起点：trajectory 当 sequence，RL 变条件生成 | [arXiv](https://arxiv.org/abs/2106.01345) · [解读](papers/2106.01345_decision_transformer/README.md) · [EN](papers/2106.01345_decision_transformer/2106.01345.pdf) · [代码](https://github.com/kzl/decision-transformer) |
| Planning with Diffusion for Flexible Behavior Synthesis (Diffuser) | Janner, Du, Tenenbaum, Levine | ICML 2022 | 路线 B 起点：把 planning 整体变成 diffusion + guidance | [arXiv](https://arxiv.org/abs/2205.09991) · [解读](papers/2205.09991_diffuser/README.md) · [EN](papers/2205.09991_diffuser/2205.09991.pdf) · [代码](https://github.com/jannerm/diffuser) |
| Diffusion Policies as an Expressive Policy Class for Offline Reinforcement Learning (Diffusion-QL) | Wang, Hunt, Zhou | ICLR 2023 | diffusion 进 offline RL 的标杆：Q + BC 双项 | [arXiv](https://arxiv.org/abs/2208.06193) · [解读](papers/2208.06193_diffusion_ql/README.md) · [EN](papers/2208.06193_diffusion_ql/2208.06193.pdf) · [代码](https://github.com/Zhendong-Wang/Diffusion-Policies-for-Offline-RL) |
| Consistency Policy: Accelerated Visuomotor Policies via Consistency Distillation | Prasad, Lin, Wu et al. | RSS 2024 | 蒸馏路线的一步策略代表，MeanFlow 族要打败的对照 | [arXiv](https://arxiv.org/abs/2405.07503) · [解读](papers/2405.07503_consistency_policy/README.md) · [EN](papers/2405.07503_consistency_policy/2405.07503.pdf) · [代码](https://github.com/Aaditya-Prasad/consistency-policy) |
| Diffusion Policy Policy Optimization (DPPO) | Ren, Lidard, Ankile et al. | ICLR 2025 | denoising-as-MDP：对去噪链上的 action 做 PPO，在线微调标杆 | [arXiv](https://arxiv.org/abs/2409.00588) · [解读](papers/2409.00588_dppo/README.md) · [EN](papers/2409.00588_dppo/2409.00588.pdf) · [代码](https://github.com/irom-princeton/dppo) |
| Flow Q-Learning (FQL) | Park, Li, Levine | ICML 2025 | flow BC 策略 + 一步蒸馏 actor 做 Q 最大化，offline RL 的 flow 版标杆 | [arXiv](https://arxiv.org/abs/2502.02538) · [解读](papers/2502.02538_fql/README.md) · [EN](papers/2502.02538_fql/2502.02538.pdf) · [代码](https://github.com/seohongpark/fql) |
| Flow-GRPO: Training Flow Matching Models via Online RL | Liu, Liu, Liang et al. | NeurIPS 2025 | ODE→SDE 转换让 flow 有逐步似然，GRPO 直接套上；免 critic 的 flow RL 源头 | [arXiv](https://arxiv.org/abs/2505.05470) · [解读](papers/2505.05470_flow_grpo/README.md) · [EN](papers/2505.05470_flow_grpo/2505.05470.pdf) · [代码](https://github.com/yifan123/flow_grpo) |
| ReinFlow: Fine-tuning Flow Matching Policy with Online Reinforcement Learning | Zhang, Yu, Su, Wang | NeurIPS 2025 | 流策略注入可学噪声得逐步高斯似然，DPPO 的 flow 对位物 | [arXiv](https://arxiv.org/abs/2505.22094) · [解读](papers/2505.22094_reinflow/README.md) · [EN](papers/2505.22094_reinflow/2505.22094.pdf) · [代码](https://github.com/ReinFlow/ReinFlow) |
| Steering Your Diffusion Policy with Latent Space Reinforcement Learning (DSRL) | Wagenmaker, Nakamoto, Zhang et al. | arXiv 2025 | 冻结解码器、RL 只动 latent 噪声：绕 log π 的第三条路线（噪声空间） | [arXiv](https://arxiv.org/abs/2506.15799) · [解读](papers/2506.15799_dsrl/README.md) · [EN](papers/2506.15799_dsrl/2506.15799.pdf) · [代码](https://diffusion-steering.github.io) |
| MP1: MeanFlow Tames Policy Learning in 1-step for Robotic Manipulation | Sheng, Wang, Li, Liu | AAAI 2026 | MeanFlow 进机器人：1-NFE 策略生成 + Dispersive Loss | [arXiv](https://arxiv.org/abs/2507.10543) · [解读](papers/2507.10543_mp1/README.md) · [EN](papers/2507.10543_mp1/2507.10543.pdf) · [代码](https://github.com/LogSSim/MP1) |
| OMP: One-step Meanflow Policy with Directional Alignment | Fang, Huang, Zhao et al. | ICML 2026 | 方向对齐正则 + 谱分析评幅度响应，一步策略训练信号分析的先例 | [arXiv](https://arxiv.org/abs/2512.19347) · [解读](papers/2512.19347_omp/README.md) · [EN](papers/2512.19347_omp/2512.19347.pdf) |
| One Step Is Enough: Dispersive MeanFlow Policy Optimization (DMPO) | Zou, Wang, Wu et al. | arXiv 2026 | dispersive 表征正则 + PPO 微调，104.2 Hz Franka 实机 | [arXiv](https://arxiv.org/abs/2601.20701) · [解读](papers/2601.20701_dmpo/README.md) · [EN](papers/2601.20701_dmpo/2601.20701.pdf) · [中文](papers/2601.20701_dmpo/2601.20701.zh.pdf) · [代码](https://guowei-zou.github.io/dmpo-page/) |
| One-Step Flow Policy: Self-Distillation for Fast Visuomotor Policies (OFP) | Li, Sun, Chen | arXiv 2026 | 从零自蒸馏免独立预训练教师，无需 JVP | [arXiv](https://arxiv.org/abs/2603.12480) · [解读](papers/2603.12480_ofp/README.md) · [EN](papers/2603.12480_ofp/2603.12480.pdf) · [中文](papers/2603.12480_ofp/2603.12480.zh.pdf) |
| Drift-Based Policy Optimization: Native One-Step Policy Learning for Online Robot Control (DBPO) | Gao, Shen, Zhang et al. | arXiv 2026 | native one-step + online RL，105.2 Hz 控制频率 | [arXiv](https://arxiv.org/abs/2604.03540) · [解读](papers/2604.03540_dbpo/README.md) · [EN](papers/2604.03540_dbpo/2604.03540.pdf) · [代码](https://github.com/YuxuanGao0822/DBPO) |
| Aligning Flow Map Policies with Optimal Q-Guidance (FMQ) | Ziakas, Russo, Bose | arXiv 2026 | flow map 策略的统一框架 + Q 引导对齐，一步策略 offline-to-online RL 的整合者 | [arXiv](https://arxiv.org/abs/2605.12416) · [解读](papers/2605.12416_fmq/README.md) · [EN](papers/2605.12416_fmq/2605.12416.pdf) · [中文](papers/2605.12416_fmq/2605.12416.zh.pdf) |

## SB × RL 交叉前沿（选题主战场）

选题主战场：四条 SB×RL 进路（动能正则、path-space mirror descent、bridge rectification、跨域轨迹翻译）。

| 论文 | 作者 | 发表 | 定位 | 链接 |
|---|---|---|---|---|
| FLAC: Maximum Entropy RL via Kinetic Energy Regularized Bridge Matching | Lv, Li, Luo et al. | arXiv 2026 | 把 SAC max-ent 的策略熵换成动能正则 GSB，绕开生成式 log π | [arXiv](https://arxiv.org/abs/2602.12829) · [解读](papers/2602.12829_flac/README.md) · [EN](papers/2602.12829_flac/2602.12829.pdf) · [中文](papers/2602.12829_flac/2602.12829.zh.pdf) · [代码](https://pinkmoon-io.github.io/flac.github.io/) |
| Bridging Dynamics Gaps via Diffusion Schrödinger Bridge for Cross-Domain Reinforcement Learning (BDGxRL) | Zhang, Guo | arXiv 2026 | 跨域动力学差距：SB 做 unpaired 转移翻译 | [arXiv](https://arxiv.org/abs/2602.23737) · [解读](papers/2602.23737_bdg/README.md) · [EN](papers/2602.23737_bdg/2602.23737.pdf) · [中文](papers/2602.23737_bdg/2602.23737.zh.pdf) |
| Path-Space Mirror Descent for On-Policy Reinforcement Learning under the Generalized Schrödinger Bridge (GSB-MDPO) | Gong, Wang, Chen et al. | arXiv 2026 | path-KL 替代动作 KL：proximal 更新搬进 path space，免 log π | [arXiv](https://arxiv.org/abs/2603.21621) · [解读](papers/2603.21621_gsb_mdpo/README.md) · [EN](papers/2603.21621_gsb_mdpo/2603.21621.pdf) · [中文](papers/2603.21621_gsb_mdpo/2603.21621.zh.pdf) |
| Rectified Schrödinger Bridge Matching for Few-Step Visual Navigation (RSBM) | Luan, Li, Zhao et al. | arXiv 2026 | bridge 上做 rectification：3 步导航，few-step SB 策略实证 | [arXiv](https://arxiv.org/abs/2604.05673) · [解读](papers/2604.05673_rsbm/README.md) · [EN](papers/2604.05673_rsbm/2604.05673.pdf) · [中文](papers/2604.05673_rsbm/2604.05673.zh.pdf) |

## 2026 前沿雷达（趋势报告收录的新变量）

趋势报告收录的 2026 年新变量：MeanFlow 族扩张（MVP/MFPO/UCA-Flow/ReactVLA）、桥式起点上主会（BridgePolicy）、绕开似然的 RL 微调（RECAP/LP-DS/DF-ExpEnse）。

| 论文 | 作者 | 发表 | 定位 | 链接 |
|---|---|---|---|---|
| π*0.6: a VLA That Learns From Experience (RECAP) | Physical Intelligence | arXiv 2025-11 | 优势条件化免策略梯度的真实世界 VLA RL，工业界对 log π 障碍的答案 | [arXiv](https://arxiv.org/abs/2511.14759) · [解读](papers/2511.14759_recap/README.md) · [EN](papers/2511.14759_recap/2511.14759.pdf) · [中文](papers/2511.14759_recap/2511.14759.zh.pdf) · [代码](https://www.pi.website/blog/pistar06) |
| Sample from What You See: Visuomotor Policy Learning via Diffusion Bridge with Observation-Embedded Stochastic Differential Equation (BridgePolicy) | Liu, Pan, Wang et al. | ICML 2026 | 观测嵌入 SDE 从观测先验起步而非噪声：informative source 策略的顶会锚点 | [arXiv](https://arxiv.org/abs/2512.07212) · [解读](papers/2512.07212_bridge_policy/README.md) · [EN](papers/2512.07212_bridge_policy/2512.07212.pdf) · [中文](papers/2512.07212_bridge_policy/2512.07212.zh.pdf) · [代码](https://github.com/jianghcsr/BridgePolicy) |
| Mean Flow Policy with Instantaneous Velocity Constraint for One-step Action Generation (MVP) | Zhan, Tao, Wang et al. | ICLR 2026 (Oral) | 平均速度策略 + best-of-N 选择做 offline-to-online RL，IVC 边界约束修 MeanFlow 恒等式解不唯一 | [arXiv](https://arxiv.org/abs/2602.13810) · [解读](papers/2602.13810_mvp/README.md) · [EN](papers/2602.13810_mvp/2602.13810.pdf) |
| Mean-Flow based One-Step Vision-Language-Action | Chen, Ma, Zhao | arXiv 2026 | MeanFlow 动作头进 VLA，真机动作生成比 SmolVLA 快 8.7 倍 | [arXiv](https://arxiv.org/abs/2603.01469) · [解读](papers/2603.01469_mf_vla/README.md) · [EN](papers/2603.01469_mf_vla/2603.01469.pdf) |
| Mean Flow Policy Optimization (MFPO) | Dong, Zhang, Cheng | ICML 2026 | MeanFlow 策略进 max-ent RL：平均散度网络近似算似然——FLAC 免似然路线的正面对手 | [arXiv](https://arxiv.org/abs/2604.14698) · [解读](papers/2604.14698_mfpo/README.md) · [EN](papers/2604.14698_mfpo/2604.14698.pdf) · [中文](papers/2604.14698_mfpo/2604.14698.zh.pdf) · [代码](https://github.com/dongxiaoyi-xyz/MFPO) |
| Lagrangian Perturbation Diffusion Steering: Latent Reinforcement Learning for Generative Policies (LP-DS) | Simsir, Oguz | ICML 2026 | DSRL 的扰动约束修正 + 动作熵多模态保持评测 | [arXiv](https://arxiv.org/abs/2606.01151) · [解读](papers/2606.01151_lp_ds/README.md) · [EN](papers/2606.01151_lp_ds/2606.01151.pdf) · [中文](papers/2606.01151_lp_ds/2606.01151.zh.pdf) · [代码](https://sites.google.com/view/lp-ds/home) |
| ReactVLA: Fast and Lightweight Reactive Robot Manipulation via Improved Mean Flow Action Generation | Guo, Chen, Zhang | arXiv 2026 | 改进 MeanFlow（iMF）+ 注意力残差路由，真机平均延迟 38.6 ms | [arXiv](https://arxiv.org/abs/2606.14255) · [解读](papers/2606.14255_reactvla/README.md) · [EN](papers/2606.14255_reactvla/2606.14255.pdf) · [代码](https://game-loader.github.io/ReactVLA/) |
| DF-ExpEnse: Diffusion Filtered Exploration for Sample Efficient Finetuning | Luo, Sun, Song | ICML 2026 | DSRL/ResFiT 的探索增强：batch 候选动作按探索兴趣筛选 | [arXiv](https://arxiv.org/abs/2606.19656) · [解读](papers/2606.19656_df_expense/README.md) · [EN](papers/2606.19656_df_expense/2606.19656.pdf) |
| Unified Condition-Action Modeling for Accurate One-Step Action Generation (UCA-Flow) | Zhou, Cai, Zuo et al. | arXiv 2026 | 条件与动作统一 token 序列联合演化，一步生成改善所测任务表现，生成比 MP1 快约 2.3 倍 | [arXiv](https://arxiv.org/abs/2608.16153) · [解读](papers/2608.16153_uca_flow/README.md) · [EN](papers/2608.16153_uca_flow/2608.16153.pdf) · [中文](papers/2608.16153_uca_flow/2608.16153.zh.pdf) · [代码](https://uca-policy.github.io/UCA.github.io/) |

## 汇总报告

| 产物 | 说明 |
|---|---|
| [`reports/DIGEST.md`](reports/DIGEST.md) | **十分钟速览**：核心矛盾、五条路线、三条线索现状、SB 的两个差异化资产、五个空格 |
| [`reports/OPEN_PROBLEMS.md`](reports/OPEN_PROBLEMS.md) | 五个开放问题的实验设计：假设 / 最小实验 / 对表谁 / 杀死条件 / 库内零件 |
| [`reports/COMPARISON.md`](reports/COMPARISON.md) | 横向对比：一步策略 · log π 路线 · SB 求解器 三张表 |
| [`reports/READING_PATHS.md`](reports/READING_PATHS.md) | 生成 / RL / 机器人三种背景 × 半天 / 一天 / 一周的阅读路线 |
| [`reports/GLOSSARY.md`](reports/GLOSSARY.md) | 术语表：SB 家族 · 求解器 · 一步生成 · RL 接口 |
| [`reports/TRENDS_2026.md`](reports/TRENDS_2026.md) | 2026 前沿趋势与 insight 报告（雷达论文已入库为 07 类） |
| [`slides/overview.html`](slides/overview.html) | HTML PPT：全库综述 11 页（浏览器打开，方向键翻页） |
| [`slides/overview.pdf`](slides/overview.pdf) | 同内容的 Beamer PDF |

## 仓库结构

```text
awesome_study/
├── README.md                 # 本文件，由 tools/gen_readme.py 生成
├── data/papers.json          # 唯一 manifest：id / slug / 标题 / 作者 / venue / 类别 / 定位 / 代码链接 / 是否翻译
├── papers/<arxiv_id>_<slug>/
│   ├── README.md             # 中文详细解读（七节结构）
│   ├── <arxiv_id>.pdf        # 英文原版
│   └── <arxiv_id>.zh.pdf     # 保版式中译（前沿篇目）
├── reports/                  # 综合报告（速览 / 开放问题 / 对比表 / 阅读路线 / 术语表 / 趋势）与修订日志
├── slides/                   # HTML PPT 与 Beamer 源码 / PDF
└── tools/                    # 下载、翻译、README 生成、Codex 打磨提示
```

## 如何扩展

1. 在 `data/papers.json` 追加条目（必填 `id` `slug` `title` `category` `translate` `role`；`authors` `venue` `code` 可后补）。
2. `python3 tools/download_papers.py` 下载 PDF（自动跳过已有）。
3. 在 `papers/<id>_<slug>/README.md` 写解读，沿用七节结构；写完可用 `tools/polish/PROMPT_TEMPLATE.md` 交给 Codex CLI 对照原文核对。
4. 需要中译则 `bash tools/translate_batch.sh <slug>`（依赖 SuperTranslate 与 DeepSeek key）。
5. `python3 tools/gen_readme.py` 重新生成本文件，提交。

## 质量说明

51 篇解读经三轮处理：(1) 基于 PDF 原文与知识库笔记撰写；(2) 本地 Codex CLI（GPT-6，reasoning xhigh）逐篇对照原文核对数字、归属、机制并去除套话，修订要点见 [`reports/POLISH_LOG.md`](reports/POLISH_LOG.md)；(3) 「一句话」在只允许使用正文事实的约束下重写为带判断的单句，见 [`reports/ONELINER_LOG.md`](reports/ONELINER_LOG.md)。综合报告、幻灯片与 manifest 中的事实陈述已逐条对齐到核对后的解读，见 [`reports/CONSISTENCY_LOG.md`](reports/CONSISTENCY_LOG.md)。中译 PDF 经视觉 QA，数学密集篇目的公式行保留英文属预期。

## 更新日志

| 日期 | 内容 |
|---|---|
| 2026-09-07 | README 全面更新：官方标题、作者补全、37 个代码 / 项目链接、类别内按时间排序、仓库结构与扩展指南、更新日志、引用 |
| 2026-09-06 | 综合文档 / 幻灯片 / manifest 与核对后解读对齐 181 处；51 篇「一句话」重写 |
| 2026-09-05 | Codex GPT-6 逐篇二审 51 篇解读；新增速览 / 开放问题 / 对比表 / 阅读路线 / 术语表五份综合报告 |
| 2026-09-02 | 扩展至 51 篇：新增 07 类 2026 雷达 9 篇 + 谱系补齐 10 篇；中译 PDF 增至 19 篇 |
| 2026-09-01 | 首发：32 篇解读、英文 PDF、12 篇中译、趋势报告、HTML PPT 与 Beamer PDF |

## 引用

```bibtex
@misc{awesome_study_sbrl_2026,
  title  = {Awesome Study: Schr{\"o}dinger Bridge x RL x Robot Policy Learning},
  author = {asimfish},
  year   = {2026},
  url    = {https://github.com/asimfish/awesome_study}
}
```

## 致谢

- 翻译：[SuperTranslate](https://github.com/asimfish/super_translate)
- 排版规范参考：[awesome-ml4co](https://github.com/Thinklab-SJTU/awesome-ml4co)
- 演示：[ppt-master](https://github.com/hugohe3/ppt-master) · [beamer-skill](https://github.com/Noi1r/beamer-skill)
- 二审：[Codex CLI](https://github.com/openai/codex)
