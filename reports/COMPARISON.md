# 横向对比表

> 三张表分别回答：一步/少步策略之间怎么选、绕开 log π 的路线各付什么代价、SB 求解器各适合什么场景。数字来自各篇解读（已按原文核对），空格表示原文未报告。

## 表一：一步/少步生成策略

| 方法 | 一步机制 | 需教师 | RL | 基准与关键数字 | 真机/频率 | 多模态评测 |
|---|---|---|---|---|---|---|
| [Consistency Policy](../papers/2405.07503_consistency_policy/README.md) | CTM 自一致性蒸馏 | 是 | 否 | 6 仿真 + 3 真机，比最快替代快一个量级 | 笔记本 GPU 可跑 | 否 |
| [MP1](../papers/2507.10543_mp1/README.md) | MeanFlow 恒等式 + Dispersive Loss | 否 | 否 | Adroit+MetaWorld 超 DP3 10.2pp、FlowPolicy 7.3pp；6.8 ms | Franka 真机 | 否 |
| [OMP](../papers/2512.19347_omp/README.md) | MeanFlow + 方向对齐 + DDE 近似 JVP | 否 | 否 | Adroit+MetaWorld 高精度任务超 MP1 | — | 否 |
| [DMPO](../papers/2601.20701_dmpo/README.md) | MeanFlow + dispersive，微调期展开 K 步做 PPO | 否 | 在线 PPO | RoboMimic Can 100 / Square 83 / Transport 88 | >120 Hz Franka | 否 |
| [MVP](../papers/2602.13810_mvp/README.md) | MeanFlow + IVC 边界约束 + best-of-N | 否 | offline→online | RoboMimic+OGBench 平均 0.88（次优 QC 0.46） | — | 否 |
| [OFP](../papers/2603.12480_ofp/README.md) | EMA 自蒸馏 + 时间收缩课程 + score 自引导 | 否（自举） | 否 | 56 任务 NFE=1 达 68.3% 超 100 步 DP/FM；π0.5 一步超十步 | — | 否 |
| [DBPO](../papers/2604.03540_dbpo/README.md) | 反对称漂移场固定点 + 单步高斯随机接口 | 否 | 在线 PPO | Push-T/RoboMimic 打平多步 DP | 105.2 Hz 双臂 UR5，75% | 定性 |
| [FMQ](../papers/2605.12416_fmq/README.md) | 流映射自蒸馏 + 信赖域闭式 Q 引导 | 否 | offline→online | OGBench+RoboMimic 12 任务，超 MVP 21.3%（相对） | — | 否 |
| [ReactVLA](../papers/2606.14255_reactvla/README.md) | iMF（JVP 修正）+ AttnRes Transformer | 否 | 否 | LIBERO 88.0%（π0 86.0 / SmolVLA 87.3），18.3 ms | <38.6 ms 真机 | 否 |
| [UCA-Flow](../papers/2608.16153_uca_flow/README.md) | 条件-动作统一 token + u/v 双通道监督 | 否 | 否 | 超最强基线 9.3pp，比 MP1 快 2.3× | 真机定性 | 否 |
| [RSBM](../papers/2604.05673_rsbm/README.md)（3 步） | $\epsilon$ 缩放桥方差 + 学习先验 | 否 | 否 | 导航 3 步 92% 成功率、94% 余弦相似度 | — | 定性 |
| [ASBM](../papers/2405.14449_adv_sbm/README.md)（4 NFE） | 离散 IMF + 条件 GAN 转移核 | 否 | 否 | CelebA 翻译 4 NFE 打平 100 NFE 连续 SB | — | 否 |

读法：**「多模态评测」一列几乎全空**——这是 [P3](OPEN_PROBLEMS.md) 的立论依据。MeanFlow 族在 2026 年的分化点是训练目标修补（IVC / 方向对齐 / 双通道 / 免 JVP）与 RL 接法（展开链 PPO / best-of-N / 闭式信赖域 / 单步高斯接口）。

## 表二：绕开 log π 的路线

| 路线 | 代表 | 需要的似然 | 探索来源 | 改进上限 | 主要代价 | 操纵/真机证据 |
|---|---|---|---|---|---|---|
| 逐步分解 | [DPPO](../papers/2409.00588_dppo/README.md) [ReinFlow](../papers/2505.22094_reinflow/README.md) [Flow-GRPO](../papers/2505.05470_flow_grpo/README.md) [DMPO](../papers/2601.20701_dmpo/README.md) | 逐步高斯转移 | 去噪链噪声（流形上） | 无结构性上限 | horizon ×K、路径比率方差、credit 均摊 | 有（DPPO 真机部署、DMPO 真机） |
| 路径空间 | [FLAC](../papers/2602.12829_flac/README.md) [GSB-MDPO](../papers/2603.21621_gsb_mdpo/README.md) | 无（drift 能量替代） | 动能预算 / 邻近半径 | 无结构性上限 | 上界松紧未量化、路径比率方差 | **无**（全部 locomotion 仿真） |
| 似然近似 | [MFPO](../papers/2604.14698_mfpo/README.md) | 平均散度网络一次前向 | max-ent 温度 | 无结构性上限 | 近似误差无界、Hutchinson 方差随维度涨 | 无 |
| 噪声空间 | [DSRL](../papers/2506.15799_dsrl/README.md) [LP-DS](../papers/2606.01151_lp_ds/README.md) [DF-ExpEnse](../papers/2606.19656_df_expense/README.md) | latent 高斯策略 | 噪声空间 SAC / UCB 候选 | 解码器支撑集内 | 高维噪声空间探索效率、改不了先验形状 | 有（DSRL 真机含 π0；LP-DS Franka） |
| 条件化/加权监督 | [AWR](../papers/1910.00177_awr/README.md) [RECAP](../papers/2511.14759_recap/README.md) [Diffusion-QL](../papers/2208.06193_diffusion_ql/README.md) [FQL](../papers/2502.02538_fql/README.md) | BC 梯度 / 无 | 数据本身 | 数据里最好的行为 | 无外推、依赖价值函数质量 | 有（RECAP 真实家庭部署） |
| 生成-选择 | [MVP](../papers/2602.13810_mvp/README.md) [FMQ](../papers/2605.12416_fmq/README.md) [DF-ExpEnse](../papers/2606.19656_df_expense/README.md) | 无 | 候选多样性 | 受 Q 选择能力限制 | 推理 ×N | 无真机 |

读法：**路径空间是唯一没有操纵/真机证据的路线**——[P2](OPEN_PROBLEMS.md) 的机会。三个信赖域（GSB-MDPO 路径 KL / LP-DS latent L2 / FMQ 速度场 L2）在一步极限下合流。

## 表三：SB 求解器

| 方法 | 数据要求 | 迭代 | 免仿真训练 | 少步推理 | 规模化证据 | 适合场景 |
|---|---|---|---|---|---|---|
| [DSB](../papers/2106.01357_dsb/README.md)（神经 IPF） | unpaired | 是（交替半桥） | 否 | 否 | 低分辩图像 | 概念验证 |
| [I2SB](../papers/2302.05872_i2sb/README.md) | **paired** | 否（解析桥） | 是 | 是（~10-20 NFE） | ImageNet 256 修复 | 有退化算子的修复类任务 |
| [DSBM](../papers/2303.16852_dsbm/README.md)（IMF） | unpaired | 是（Markov/reciprocal 交替） | Markov 投影是回归，reciprocal 步需采样 | 否 | AFHQ 512 | 需要真 SB 耦合的 unpaired 翻译 |
| [SF2M](../papers/2307.03672_sf2m/README.md) | unpaired | 否（minibatch 熵 OT 一次拍死） | 是 | 否 | 中低维科学数据 | 单细胞等中低维 |
| [SB Flow](../papers/2409.09347_sb_flow/README.md)（α-IMF） | unpaired | 是（在线小步幅） | 否（在线自采样） | 否 | 高分辨 unpaired 图像 | 规模化 unpaired 翻译、sim-to-real |
| [ASBM](../papers/2405.14449_adv_sbm/README.md)（D-IMF） | unpaired | 是（离散时刻） | 否 | **是（4 NFE）** | 64-128 人脸 | 少步 unpaired 翻译 |
| [GSBM](../papers/2310.02233_gsbm/README.md) | unpaired + 路径费用 | 是（CondSOC + matching） | 部分 | 否 | 导航/图像翻译 | 带中间约束的任务；RL 接口 |
| [RSBM](../papers/2604.05673_rsbm/README.md) | paired（导航示范） | 否 | 是 | 是（3 步） | 导航 5 数据集 | few-step 具身策略 |

读法：paired 场景（I2SB/RSBM）免迭代、天然少步；unpaired 场景要么迭代（IMF 系）要么接受静态近似偏差（SF2M）；**少步 + unpaired** 只有 ASBM 一家（对抗训练代价），是求解器层面的空格。[PRISM](../papers/2608.06893_prism/README.md) 给出参考过程设计的理论（仅 paired 高斯设定）。
