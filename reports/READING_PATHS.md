# 阅读路线

> 按背景和时间预算给三条路线。每条先给「为什么按这个顺序」，再给篇目。所有链接指向本库解读；读原文前先读解读的「一句话」与「局限与批判」，能省一半时间。

## 路线一：生成模型背景，要进 RL

**逻辑**：你已经懂 score/flow，缺的是 RL 的语言与「生成式策略为什么卡在 RL 上」。先补 RL 接口，再看生成式策略 RL 的两代范式，最后进 SB×RL。

- **半天**：[SAC](../papers/1801.01290_sac/README.md)（energy-based 最优策略）→ [MDPO](../papers/2005.09814_mdpo/README.md)（KL 邻近项）→ [AWR](../papers/1910.00177_awr/README.md)（加权 BC 绕行为密度与似然比）→ [DPPO](../papers/2409.00588_dppo/README.md)（逐步分解）→ [GSB-MDPO](../papers/2603.21621_gsb_mdpo/README.md)（path-space）
- **加一天**：[Diffusion-QL](../papers/2208.06193_diffusion_ql/README.md) → [FQL](../papers/2502.02538_fql/README.md) → [DSRL](../papers/2506.15799_dsrl/README.md) → [FLAC](../papers/2602.12829_flac/README.md) → [MFPO](../papers/2604.14698_mfpo/README.md)（对比 FLAC）→ [FMQ](../papers/2605.12416_fmq/README.md)
- **加一周**：05 类全部 + [RECAP](../papers/2511.14759_recap/README.md) + [LP-DS](../papers/2606.01151_lp_ds/README.md)，然后读 [OPEN_PROBLEMS](OPEN_PROBLEMS.md) 的 P2/P5。

## 路线二：RL 背景，要懂 SB

**逻辑**：你懂策略优化，缺的是「路径测度」这套语言和 SB 求解器的演化。先建立 SB 的定义与两个恒等式，再看求解器怎么从 IPF 走到在线 IMF，最后看 SB 怎么接到你熟悉的 RL 目标上。

- **半天**：[DDPM](../papers/2006.11239_ddpm/README.md)（起点）→ [Score-SDE](../papers/2011.13456_score_sde/README.md)（SDE 语言）→ [Léonard](../papers/1308.0215_leonard_survey/README.md)（只读「方法核心」节）→ [DSB](../papers/2106.01357_dsb/README.md) → [GSBM](../papers/2310.02233_gsbm/README.md)（RL 接口）
- **加一天**：[Flow Matching](../papers/2210.02747_flow_matching/README.md) → [OT-CFM](../papers/2302.00482_ot_cfm/README.md) → [I2SB](../papers/2302.05872_i2sb/README.md)（informative source）→ [DSBM](../papers/2303.16852_dsbm/README.md)（IMF）→ [SB Flow](../papers/2409.09347_sb_flow/README.md) → [FLAC](../papers/2602.12829_flac/README.md)
- **加一周**：02/03 类全部 + [SB Foundations](../papers/2603.18992_sb_foundations/README.md) 当工具书 + [PRISM](../papers/2608.06893_prism/README.md) + [Soft-SB](../papers/2403.01717_soft_sb/README.md)，然后读 [GLOSSARY](GLOSSARY.md) A 组查漏。

## 路线三：机器人背景，要选题

**逻辑**：你关心的是真机能不能跑、成功率涨不涨。先看策略生成的事实标准与一步化竞赛（这决定你的基线是谁），再看 RL 微调的几条路线（决定你的方法位置），最后看 SB 的具身证据与空格。

- **半天**：[Diffusion Policy](../papers/2303.04137_diffusion_policy/README.md) → [MeanFlow](../papers/2505.13447_meanflow/README.md) → [MP1](../papers/2507.10543_mp1/README.md) → [DMPO](../papers/2601.20701_dmpo/README.md) → [DBPO](../papers/2604.03540_dbpo/README.md) → [COMPARISON](COMPARISON.md) 表一
- **加一天**：[DPPO](../papers/2409.00588_dppo/README.md) → [DSRL](../papers/2506.15799_dsrl/README.md) → [RECAP](../papers/2511.14759_recap/README.md) → [BridgePolicy](../papers/2512.07212_bridge_policy/README.md) → [RSBM](../papers/2604.05673_rsbm/README.md) → [BDGxRL](../papers/2602.23737_bdg/README.md)
- **加一周**：07 类全部（尤其 [ReactVLA](../papers/2606.14255_reactvla/README.md) 看 VLA 尺度的少步化、[UCA-Flow](../papers/2608.16153_uca_flow/README.md) 看点云策略的一步化）+ [OMP](../papers/2512.19347_omp/README.md)/[MVP](../papers/2602.13810_mvp/README.md)（一步策略的病理）→ [OPEN_PROBLEMS](OPEN_PROBLEMS.md) 的 P1/P3/P4。

## 不分背景的两小时版

[DIGEST](DIGEST.md) 全文 → 06 类四篇（[FLAC](../papers/2602.12829_flac/README.md) [GSB-MDPO](../papers/2603.21621_gsb_mdpo/README.md) [RSBM](../papers/2604.05673_rsbm/README.md) [BDGxRL](../papers/2602.23737_bdg/README.md)）只读「一句话」+「与 SB×RL 的关联」+「局限与批判」→ [OPEN_PROBLEMS](OPEN_PROBLEMS.md) 的 P1 全文。

## 读每篇时的固定五问

来自知识库 03 章的 checklist，对本库所有 bridge/策略论文通用：
1. 源分布是什么、目标分布是什么（起点带不带信息）？
2. 参考过程是什么（决定几何；PRISM 的不可见性限于指定线性高斯模型与采样器的多步后验极限）？
3. 训练是 score / flow / bridge matching / 对抗 / 似然中的哪种？
4. 是否免仿真训练；推理 NFE 多少？
5. 相对前作改的是哪一轴：边界 / 参考 / 耦合 / 损失 / 推理步数？——只改损失形式的多半是包装。
