# 横向对比表

> 三张表分别回答：一步/少步策略之间怎么选、绕开 log π 的路线各付什么代价、SB 求解器各适合什么场景。数字来自各篇解读（已按原文核对），空格表示原文未报告。

## 表一：一步/少步生成策略

| 方法 | 一步机制 | 需教师 | RL | 基准与关键数字 | 真机/频率 | 多模态评测 |
|---|---|---|---|---|---|---|
| [Consistency Policy](../papers/2405.07503_consistency_policy/README.md) | CTM 自一致性蒸馏（1 或 3 步） | 是 | 否 | 6 仿真 + 3 真机，真机对十五步 DDiM 端到端降延迟约九倍 | 笔记本 GPU 可跑 | 定性（Push-T 单侧偏置） |
| [MP1](../papers/2507.10543_mp1/README.md) | MeanFlow 恒等式 + Dispersive Loss | 否 | 否 | Adroit+MetaWorld 超 DP3 10.2pp、FlowPolicy 7.3pp；6.8 ms | ARX R5 双臂真机 | 否 |
| [OMP](../papers/2512.19347_omp/README.md) | MeanFlow + 方向对齐；可选 DDE 近似 JVP | 否 | 否 | Adroit+MetaWorld 平均超 MP1 3.4pp（JVP 版） | 3 项真机任务 | 否 |
| [DMPO](../papers/2601.20701_dmpo/README.md) | MeanFlow + dispersive，微调期用 K 步随机链做 PPO（可 K=1） | 否 | 在线 PPO | RoboMimic 正文 Can 100 / Square 峰值 83 / Transport 88（附录口径不同） | 104.2 Hz Franka | 否 |
| [MVP](../papers/2602.13810_mvp/README.md) | MeanFlow + IVC 边界约束 + best-of-N | 否 | offline→online | RoboMimic+OGBench 平均 0.88（次优 QC 0.86） | — | 否 |
| [OFP](../papers/2603.12480_ofp/README.md) | EMA 自蒸馏 + 时间收缩课程 + score 自引导 | 否（自举） | 否 | 7 个二维任务 NFE=1 达 68.3%；56 个三维任务 71.6%，均超百步基线；π0.5 一步超十步 | — | 否 |
| [DBPO](../papers/2604.03540_dbpo/README.md) | 反对称漂移场固定点 + 单步高斯随机接口 | 否 | 在线 PPO | 六任务族平均 0.83 对多步 DP 0.79；视觉项略降 | DBP：105.2 Hz 双臂 UR5，75%（BC 部署） | 定性 |
| [FMQ](../papers/2605.12416_fmq/README.md) | 流映射自蒸馏 + 信赖域闭式 Q 引导 | 否 | offline→online | OGBench+RoboMimic 12 任务，成功率 IQM 超复现 MVP 21.3%（相对） | — | 否 |
| [ReactVLA](../papers/2606.14255_reactvla/README.md) | iMF（JVP 修正）+ AttnRes Transformer，仿真 2 步 | 否 | 否 | LIBERO 88.0%（π0 86.0 / SmolVLA 87.3），18.3 ms | 38.6 ms 真机（5 步） | 否 |
| [UCA-Flow](../papers/2608.16153_uca_flow/README.md) | 条件-动作统一 token + 同网 u/v 双次前向监督 | 否 | 否 | 原报比 MP1 高 9.3pp（总平均口径不符），比 MP1 快 2.3× | UR5e：拾放 65%、关抽屉 100% | 否 |
| [RSBM](../papers/2604.05673_rsbm/README.md)（3 步） | $\epsilon$ 缩放桥方差 + 学习先验 | 否 | 否 | 室内导航 3 步 92% 成功率、0.945 余弦相似度 | — | 定性 |
| [ASBM](../papers/2405.14449_adv_sbm/README.md)（4 NFE） | 离散 IMF + 条件 GAN 转移核 | 否 | 否 | CelebA 翻译 4 NFE 的 FID 优于 100 NFE DSBM | — | 有（LPIPS 多样性） |

读法：**「多模态评测」一列几乎全空**——这是 [P3](OPEN_PROBLEMS.md) 的立论依据。MeanFlow 族在 2026 年的分化点是训练目标修补（IVC / 方向对齐 / 双次监督 / 免 JVP）与 RL 接法（展开链 PPO / best-of-N / 闭式信赖域 / 单步高斯接口）。

## 表二：绕开 log π 的路线

| 路线 | 代表 | 需要的似然 | 探索来源 | 改进上限 | 主要代价 | 操纵/真机证据 |
|---|---|---|---|---|---|---|
| 逐步分解 | [DPPO](../papers/2409.00588_dppo/README.md) [ReinFlow](../papers/2505.22094_reinflow/README.md) [Flow-GRPO](../papers/2505.05470_flow_grpo/README.md) [DMPO](../papers/2601.20701_dmpo/README.md) | 逐步高斯转移 | 去噪/流随机链噪声（可贴近示范） | 无结构性上限 | horizon ×K、路径比率方差、步级信用分配 | 有（DPPO 真机部署、DMPO 真机） |
| 路径空间 | [FLAC](../papers/2602.12829_flac/README.md) [GSB-MDPO](../papers/2603.21621_gsb_mdpo/README.md) | 无终端似然；GSB-MDPO 仍用路径转移比率 | 动能预算 / 邻近半径 | 无结构性上限 | 上界松紧未量化、路径比率方差 | **无视觉操纵/真机**（状态输入控制仿真） |
| 似然近似 | [MFPO](../papers/2604.14698_mfpo/README.md) | 平均散度网络默认两段各一次前向 | max-ent 温度 | 无结构性上限 | 缺统一近似误差界、Hutchinson 迹估计方差 | 无 |
| 噪声空间 | [DSRL](../papers/2506.15799_dsrl/README.md) [LP-DS](../papers/2606.01151_lp_ds/README.md) [DF-ExpEnse](../papers/2606.19656_df_expense/README.md) | DSRL 用 latent 似然；LP-DS 用 latent Q 梯度 | 噪声空间 SAC / UCB 候选 | 解码器支撑集内 | 高维噪声空间探索效率、改不了解码器映射 | 有（DSRL 真机含 π0；LP-DS Franka） |
| 条件化/加权监督/行为正则 | [AWR](../papers/1910.00177_awr/README.md) [RECAP](../papers/2511.14759_recap/README.md) [Diffusion-QL](../papers/2208.06193_diffusion_ql/README.md) [FQL](../papers/2502.02538_fql/README.md) | AWR 需动作似然；其余用监督/重参数化梯度 | 数据与在线交互 | 受数据覆盖与价值估计限制 | 外推偏差、依赖价值函数质量 | 有（RECAP 真实家庭部署） |
| 生成-选择 | [MVP](../papers/2602.13810_mvp/README.md) [FMQ](../papers/2605.12416_fmq/README.md) [DF-ExpEnse](../papers/2606.19656_df_expense/README.md) | 无 | 候选多样性 | 受 Q 选择能力限制 | 候选生成与评分（DF-ExpEnse 仅采集期） | 无真机 |

读法：**路径空间仍没有视觉操纵/真机证据**——[P2](OPEN_PROBLEMS.md) 的机会。三个偏移约束（GSB-MDPO 路径 KL / LP-DS latent L2 / FMQ 速度场 L2）对象不同，一步极限下的等价关系尚未建立。

## 表三：SB 求解器

| 方法 | 数据要求 | 迭代 | 免仿真训练 | 少步推理 | 规模化证据 | 适合场景 |
|---|---|---|---|---|---|---|
| [DSB](../papers/2106.01357_dsb/README.md)（神经 IPF） | unpaired | 是（交替半桥） | 否 | MNIST 有 12 步结果 | 低分辩图像 | 概念验证 |
| [I2SB](../papers/2302.05872_i2sb/README.md) | **paired** | 否（解析桥） | 是 | 是（特定补全 2-10 NFE） | ImageNet 256 修复 | 有配对训练数据的修复类任务 |
| [DSBM](../papers/2303.16852_dsbm/README.md)（IMF） | unpaired | 是（Markov/reciprocal 交替） | Markov 投影是回归，更新端点需模拟模型 | 否 | AFHQ 512 | 需要真 SB 耦合的 unpaired 翻译 |
| [SF2M](../papers/2307.03672_sf2m/README.md) | unpaired | 默认否（静态 OT 耦合；可加外循环） | 是 | 否 | 单细胞（含 1000 基因）与 CIFAR-10 | 单细胞等分布快照 |
| [SB Flow](../papers/2409.09347_sb_flow/README.md)（α-IMF） | unpaired | 是（在线小步幅） | 否（在线自采样） | 否 | 高分辨 unpaired 图像 | 规模化 unpaired 翻译、sim-to-real |
| [ASBM](../papers/2405.14449_adv_sbm/README.md)（D-IMF） | unpaired | 是（离散时刻） | 否 | **是（4 NFE）** | 128×128 人脸 | 少步 unpaired 翻译 |
| [GSBM](../papers/2310.02233_gsbm/README.md) | unpaired + 路径费用 | 是（CondSOC + matching） | 部分 | 否 | 导航/图像翻译 | 带中间约束的任务；RL 接口 |
| [RSBM](../papers/2604.05673_rsbm/README.md) | paired（导航示范） | 否 | 是 | 是（3 积分步，原报 5 NFE） | 2 闭环仿真 + 5 开环真实数据集 | few-step 具身策略 |

读法：paired 场景（I2SB/RSBM）免交替求桥，并有任务相关的少步证据；unpaired 场景要么迭代（IMF 系）要么接受静态近似偏差（SF2M）；**少步 + unpaired** 以本表 ASBM 为代表（对抗训练代价），是求解器层面的空格。[PRISM](../papers/2608.06893_prism/README.md) 给出参考过程设计的理论（仅 paired 高斯设定）。
