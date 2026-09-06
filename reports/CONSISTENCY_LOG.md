# 一致性审校日志

> 2026-09-06。`papers/*/README.md` 经 Codex 二审后成为唯一事实源；以下综合文档、幻灯片与 manifest 中与之冲突的事实陈述已逐条对齐（由 Codex GPT-6 执行修改，配额耗尽后由 Claude 完成 Beamer 编译验证与本日志）。每条为「旧 → 新」。


**合计 181 处修正，涉及 9 个文件。**


## reports/DIGEST.md（17 处）

- 机器人动作是多模态的（同一状态下从左绕或从右绕都对），高斯 actor 把模式平均成无效动作。Diffusion Policy（[2303.04137](../papers/2303.04137_diffusion_policy/README.md)）用条件去噪生成 action chunk 解决了这个问题，12 任务平均提升 46.9%，成为事实标准；π0、RDT-1B 等 VLA 的动作头沿用扩散/流。
  → 机器人动作是多模态的（同一状态下从左绕或从右绕都对），高斯 actor 把模式平均成无效动作。Diffusion Policy（[2303.04137](../papers/2303.04137_diffusion_policy/README.md)）用条件去噪生成 action chunk 解决了这个问题，会议版 12 任务、期刊扩展版 15 任务，仿真平均提升 46.9%，成为事实标准；π0、RDT-1B 等 VLA 的动作头沿用扩
- 代价是 RL 用不上了。策略梯度、SAC 的熵项、PPO 的 ratio 全都需要 $\log\pi(a|s)$，而生成式策略的动作是 SDE/ODE 的终端边际——似然要么只有 ELBO（[DDPM](../papers/2006.11239_ddpm/README.md)），要么要沿 ODE 积分散度（[Score-SDE](../papers/2011.13456_score_sde/README.md)），在线训练里都不可承受。
  → 代价是常规 RL 似然接口用不上了。常规动作层策略梯度、SAC 的熵项、PPO 的 ratio 需要 $\log\pi(a|s)$，而生成式策略的动作是 SDE/ODE 的终端边际——似然要么只有 ELBO（[DDPM](../papers/2006.11239_ddpm/README.md)），要么要沿 ODE 积分散度（[Score-SDE](../papers/2011.13456_score_sde/README.md)），在线
- ## 二、五条绕开 log π 的路线（2026 年全部成型，本库均有代表）
  → ## 二、五条处理 log π 障碍的路线（2026 年全部成型，本库均有代表）
- | 逐步分解 | 去噪链拆成内层 MDP，每步高斯似然可算 | [DPPO](../papers/2409.00588_dppo/README.md) · [ReinFlow](../papers/2505.22094_reinflow/README.md) · [Flow-GRPO](../papers/2505.05470_flow_grpo/README.md) · [DMPO](../papers/2601.20701_dmpo
  → | 逐步分解 | 去噪链拆成内层 MDP，每步高斯似然可算 | [DPPO](../papers/2409.00588_dppo/README.md) · [ReinFlow](../papers/2505.22094_reinflow/README.md) · [Flow-GRPO](../papers/2505.05470_flow_grpo/README.md) · [DMPO](../papers/2601.20701_dmpo
- | 路径空间 | KL/熵正则从动作分布搬到路径测度，Girsanov 化成 drift 能量 | [FLAC](../papers/2602.12829_flac/README.md) · [GSB-MDPO](../papers/2603.21621_gsb_mdpo/README.md) | 上界松紧未量化；只有 locomotion 仿真证据 |
  → | 路径空间 | KL/熵正则改用路径代价，共享非零扩散下 Girsanov 化成 drift 能量 | [FLAC](../papers/2602.12829_flac/README.md) · [GSB-MDPO](../papers/2603.21621_gsb_mdpo/README.md) | 上界松紧未量化；只有状态输入控制仿真证据 |
- | 条件化/加权监督 | 优势当权重或条件 token，训练变监督 | [AWR](../papers/1910.00177_awr/README.md) · [RECAP](../papers/2511.14759_recap/README.md) · [Diffusion-QL](../papers/2208.06193_diffusion_ql/README.md) | 好不过数据里最好的行为 |
  → | 条件化/加权监督/行为正则 | 优势作权重或条件，或 BC 配合 Q 梯度 | [AWR](../papers/1910.00177_awr/README.md) · [RECAP](../papers/2511.14759_recap/README.md) · [Diffusion-QL](../papers/2208.06193_diffusion_ql/README.md) | 受数据覆盖与价值估计限制 |
- | 生成-选择 | 采 N 个候选按 Q 选，或闭式 Q 引导 | [MVP](../papers/2602.13810_mvp/README.md) · [FMQ](../papers/2605.12416_fmq/README.md) · [DF-ExpEnse](../papers/2606.19656_df_expense/README.md) | 推理成本 ×N |
  → | 生成-选择 | 采候选按 Q 或分歧评分选，或闭式 Q 引导 | [MVP](../papers/2602.13810_mvp/README.md) · [FMQ](../papers/2605.12416_fmq/README.md) · [DF-ExpEnse](../papers/2606.19656_df_expense/README.md) | 多候选与评分开销（DF-ExpEnse 仅采集期） |
- 还有一条正面硬算的路线：[MFPO](../papers/2604.14698_mfpo/README.md) 用平均散度网络一次前向近似似然——它与 FLAC 构成 likelihood-approximation vs likelihood-free 的路线之争，目前互不对比。
  → 还有一条正面硬算的路线：[MFPO](../papers/2604.14698_mfpo/README.md) 用平均散度网络分段近似似然（默认两段各一次前向）——它与 FLAC 构成 likelihood-approximation vs likelihood-free 的路线之争，目前互不对比。
- **线索一：一步化——步数竞赛已结束。** [MeanFlow](../papers/2505.13447_meanflow/README.md) 的平均速度场恒等式给出免蒸馏的原生 1-NFE，半年内 [MP1](../papers/2507.10543_mp1/README.md)（操纵）→ [DMPO](../papers/2601.20701_dmpo/README.md)（+PPO，>120 Hz 真机）→ [OFP](../
  → **线索一：一步化——步数竞赛已结束。** [MeanFlow](../papers/2505.13447_meanflow/README.md) 的平均速度场恒等式给出免蒸馏的原生 1-NFE，此后 [MP1](../papers/2507.10543_mp1/README.md)（操纵）→ [DMPO](../papers/2601.20701_dmpo/README.md)（+PPO，104.2 Hz 真机）→ [OFP](../
- **线索二：路径空间——理论位已被占，落地半场没人打。** 两个恒等式撑起整条线：Girsanov 动能恒等式（路径 KL = drift 能量，不算密度）与数据处理不等式（路径 KL ≥ 终端动作 KL）。FLAC 用前者替代 SAC 的熵，GSB-MDPO 用后者做 mirror descent 的邻近项。两篇全部是 locomotion 仿真——操纵、视觉、真机全空。
  → **线索二：路径空间——理论位已被占，落地半场没人打。** 两个关系撑起整条线：Girsanov 动能恒等式（共享初始分布与非零扩散时，路径 KL = 尺度加权 drift 能量）与数据处理不等式（路径 KL ≥ 终端动作 KL）。FLAC 用动能正则替代显式熵计算（确定性版只给几何约束），GSB-MDPO 用后者做 mirror descent 的邻近项。两篇全部是状态输入控制仿真——视觉操纵、真机全空。
- **线索三：桥式先验——上了顶会，但只做了 BC 半场。** 起点带信息则路径短、少步稳：图像上 [I2SB](../papers/2302.05872_i2sb/README.md) 把 NFE 从几百压到 20；导航上 [RSBM](../papers/2604.05673_rsbm/README.md) 用 $\epsilon$ 旋钮 3 步 92%；操纵上 [BridgePolicy](../papers/2512.07212_
  → **线索三：桥式先验——上了顶会，但只做了 BC 半场。** 起点带信息有望让路径短、少步稳：图像上 [I2SB](../papers/2302.05872_i2sb/README.md) 在特定补全设置以 2-10 NFE 接近最佳，对照至少需 100 NFE；导航上 [RSBM](../papers/2604.05673_rsbm/README.md) 用 $\epsilon$ 旋钮在室内仿真 3 步 92%；操纵上 [Bridge
- 一步化吃掉了「SB 能少步」这个卖点。[PRISM](../papers/2608.06893_prism/README.md) 的不可见性原理进一步说明：无限步下换参考过程毫无意义，参考设计只在有限步预算下有价值。于是 SB 的地盘被精确地钉在 few-step 区间，靶子只剩两个：
  → 一步化吃掉了「SB 能少步」这个卖点。[PRISM](../papers/2608.06893_prism/README.md) 的不可见性原理进一步说明：在线性高斯复原的指定祖先采样器下，精确预测与无限步恢复同一后验，参考噪声设计影响有限步误差。于是这条参考设计线的地盘被钉在 few-step 区间，靶子只剩两个：
- 1. **Informative source（边界即条件）**：从上一 chunk / 观测潜表示 / 粗规划出发，而不是纯噪声。BridgePolicy 证明了红利，PRISM 给了先验噪声该放在哪个维度的第一条可计算规则。
  → 1. **Informative source（边界即条件）**：从上一 chunk / 观测潜表示 / 粗规划出发，而不是纯噪声。BridgePolicy 证明了红利，PRISM 给了高斯复原桥参考噪声该放在哪个维度的可计算规则。
- 2. **$\epsilon$ 谱系（coverage-straightness 同一旋钮）**：$\epsilon\to0$ 是确定性 OT 直路径（利于少步），$\epsilon$ 大保多模态覆盖。MeanFlow 族只有确定性极限这一端。RSBM 的 Theorem 1 说速度场形式跨整个谱不变——一个网络通吃。
  → 2. **$\epsilon$ 谱系（coverage-straightness 同一旋钮）**：$\epsilon\to0$ 使给定端点间的桥核收缩到确定插值（利于少步），$\epsilon$ 大增加桥内随机性，覆盖仍需验证。MeanFlow 族只有确定性极限这一端。RSBM 的 Theorem 1 说条件速度目标形式跨整个谱不变——可沿用同一架构，权重仍需按训练分布学习。
- 一切不落在这两点上的「SB 包装」工作都会贬值——评审已经不区分 diffusion bridge 与严格 SB（BridgePolicy 用的是 Doob h-变换系）。
  → 一切不落在这两点上的「SB 包装」工作都会贬值——评审已经不区分 diffusion bridge 与严格 SB（BridgePolicy 用的是 UniDB 的有限终端惩罚控制框架）。
- **一步时代 path-space 还剩什么？** [FMQ](../papers/2605.12416_fmq/README.md) 的信赖域闭式解 $u^*=u^{\text{ref}}+\eta\,\nabla_aQ/\|\nabla_aQ\|$、LP-DS 的 latent 偏移约束、GSB-MDPO 的路径 KL 是同一优化问题在三个层面的形式；路径 KL 经 Girsanov 就是速度场 L2，所以 FMQ 恰是 GSB-M
  → **一步时代 path-space 还剩什么？** [FMQ](../papers/2605.12416_fmq/README.md) 的局部线性 Q 信赖域闭式解 $u^*=u^{\text{ref}}+\eta\,\nabla_aQ/\|\nabla_aQ\|$、LP-DS 的 latent 偏移约束、GSB-MDPO 的路径 KL 都限制策略偏移，但对象和近似条件不同；共享非零扩散下路径 KL 可化成加权 drift L2，尚不能
- **共性病理。** [OMP](../papers/2512.19347_omp/README.md) 证明回归速度/漂移场的方法在低模长区间梯度饥饿（方向梯度 ∝ 目标模长），[MVP](../papers/2602.13810_mvp/README.md) 证明 MeanFlow 恒等式作为一阶 ODE 缺边界条件解不唯一。桥匹配在收口段同病——one-step SB policy 必须内置方向对齐与边界约束，否则精细操纵先输在这里
  → **共性病理。** [OMP](../papers/2512.19347_omp/README.md) 分析 MSE 速度回归在低模长目标处的方向梯度弱化（方向梯度 ∝ 目标模长），[MVP](../papers/2602.13810_mvp/README.md) 证明 MeanFlow 恒等式作为一阶 ODE 缺边界条件解不唯一。桥匹配在低模长目标处也需检查此病——one-step SB policy 必须内置方向对齐与边界约束，否则

## reports/COMPARISON.md（28 处）

- | [Consistency Policy](../papers/2405.07503_consistency_policy/README.md) | CTM 自一致性蒸馏 | 是 | 否 | 6 仿真 + 3 真机，比最快替代快一个量级 | 笔记本 GPU 可跑 | 否 |
  → | [Consistency Policy](../papers/2405.07503_consistency_policy/README.md) | CTM 自一致性蒸馏（1 或 3 步） | 是 | 否 | 6 仿真 + 3 真机，真机对十五步 DDiM 端到端降延迟约九倍 | 笔记本 GPU 可跑 | 定性（Push-T 单侧偏置） |
- | [MP1](../papers/2507.10543_mp1/README.md) | MeanFlow 恒等式 + Dispersive Loss | 否 | 否 | Adroit+MetaWorld 超 DP3 10.2pp、FlowPolicy 7.3pp；6.8 ms | Franka 真机 | 否 |
  → | [MP1](../papers/2507.10543_mp1/README.md) | MeanFlow 恒等式 + Dispersive Loss | 否 | 否 | Adroit+MetaWorld 超 DP3 10.2pp、FlowPolicy 7.3pp；6.8 ms | ARX R5 双臂真机 | 否 |
- | [OMP](../papers/2512.19347_omp/README.md) | MeanFlow + 方向对齐 + DDE 近似 JVP | 否 | 否 | Adroit+MetaWorld 高精度任务超 MP1 | — | 否 |
  → | [OMP](../papers/2512.19347_omp/README.md) | MeanFlow + 方向对齐；可选 DDE 近似 JVP | 否 | 否 | Adroit+MetaWorld 平均超 MP1 3.4pp（JVP 版） | 3 项真机任务 | 否 |
- | [DMPO](../papers/2601.20701_dmpo/README.md) | MeanFlow + dispersive，微调期展开 K 步做 PPO | 否 | 在线 PPO | RoboMimic Can 100 / Square 83 / Transport 88 | >120 Hz Franka | 否 |
  → | [DMPO](../papers/2601.20701_dmpo/README.md) | MeanFlow + dispersive，微调期用 K 步随机链做 PPO（可 K=1） | 否 | 在线 PPO | RoboMimic 正文 Can 100 / Square 峰值 83 / Transport 88（附录口径不同） | 104.2 Hz Franka | 否 |
- | [MVP](../papers/2602.13810_mvp/README.md) | MeanFlow + IVC 边界约束 + best-of-N | 否 | offline→online | RoboMimic+OGBench 平均 0.88（次优 QC 0.46） | — | 否 |
  → | [MVP](../papers/2602.13810_mvp/README.md) | MeanFlow + IVC 边界约束 + best-of-N | 否 | offline→online | RoboMimic+OGBench 平均 0.88（次优 QC 0.86） | — | 否 |
- | [OFP](../papers/2603.12480_ofp/README.md) | EMA 自蒸馏 + 时间收缩课程 + score 自引导 | 否（自举） | 否 | 56 任务 NFE=1 达 68.3% 超 100 步 DP/FM；π0.5 一步超十步 | — | 否 |
  → | [OFP](../papers/2603.12480_ofp/README.md) | EMA 自蒸馏 + 时间收缩课程 + score 自引导 | 否（自举） | 否 | 7 个二维任务 NFE=1 达 68.3%；56 个三维任务 71.6%，均超百步基线；π0.5 一步超十步 | — | 否 |
- | [DBPO](../papers/2604.03540_dbpo/README.md) | 反对称漂移场固定点 + 单步高斯随机接口 | 否 | 在线 PPO | Push-T/RoboMimic 打平多步 DP | 105.2 Hz 双臂 UR5，75% | 定性 |
  → | [DBPO](../papers/2604.03540_dbpo/README.md) | 反对称漂移场固定点 + 单步高斯随机接口 | 否 | 在线 PPO | 六任务族平均 0.83 对多步 DP 0.79；视觉项略降 | DBP：105.2 Hz 双臂 UR5，75%（BC 部署） | 定性 |
- | [FMQ](../papers/2605.12416_fmq/README.md) | 流映射自蒸馏 + 信赖域闭式 Q 引导 | 否 | offline→online | OGBench+RoboMimic 12 任务，超 MVP 21.3%（相对） | — | 否 |
  → | [FMQ](../papers/2605.12416_fmq/README.md) | 流映射自蒸馏 + 信赖域闭式 Q 引导 | 否 | offline→online | OGBench+RoboMimic 12 任务，成功率 IQM 超复现 MVP 21.3%（相对） | — | 否 |
- | [ReactVLA](../papers/2606.14255_reactvla/README.md) | iMF（JVP 修正）+ AttnRes Transformer | 否 | 否 | LIBERO 88.0%（π0 86.0 / SmolVLA 87.3），18.3 ms | <38.6 ms 真机 | 否 |
  → | [ReactVLA](../papers/2606.14255_reactvla/README.md) | iMF（JVP 修正）+ AttnRes Transformer，仿真 2 步 | 否 | 否 | LIBERO 88.0%（π0 86.0 / SmolVLA 87.3），18.3 ms | 38.6 ms 真机（5 步） | 否 |
- | [UCA-Flow](../papers/2608.16153_uca_flow/README.md) | 条件-动作统一 token + u/v 双通道监督 | 否 | 否 | 超最强基线 9.3pp，比 MP1 快 2.3× | 真机定性 | 否 |
  → | [UCA-Flow](../papers/2608.16153_uca_flow/README.md) | 条件-动作统一 token + 同网 u/v 双次前向监督 | 否 | 否 | 原报比 MP1 高 9.3pp（总平均口径不符），比 MP1 快 2.3× | UR5e：拾放 65%、关抽屉 100% | 否 |
- | [RSBM](../papers/2604.05673_rsbm/README.md)（3 步） | $\epsilon$ 缩放桥方差 + 学习先验 | 否 | 否 | 导航 3 步 92% 成功率、94% 余弦相似度 | — | 定性 |
  → | [RSBM](../papers/2604.05673_rsbm/README.md)（3 步） | $\epsilon$ 缩放桥方差 + 学习先验 | 否 | 否 | 室内导航 3 步 92% 成功率、0.945 余弦相似度 | — | 定性 |
- | [ASBM](../papers/2405.14449_adv_sbm/README.md)（4 NFE） | 离散 IMF + 条件 GAN 转移核 | 否 | 否 | CelebA 翻译 4 NFE 打平 100 NFE 连续 SB | — | 否 |
  → | [ASBM](../papers/2405.14449_adv_sbm/README.md)（4 NFE） | 离散 IMF + 条件 GAN 转移核 | 否 | 否 | CelebA 翻译 4 NFE 的 FID 优于 100 NFE DSBM | — | 有（LPIPS 多样性） |
- 
  → 
- 读法：**「多模态评测」一列几乎全空**——这是 [P3](OPEN_PROBLEMS.md) 的立论依据。MeanFlow 族在 2026 年的分化点是训练目标修补（IVC / 方向对齐 / 双通道 / 免 JVP）与 RL 接法（展开链 PPO / best-of-N / 闭式信赖域 / 单步高斯接口）。
  → 读法：**「多模态评测」一列几乎全空**——这是 [P3](OPEN_PROBLEMS.md) 的立论依据。MeanFlow 族在 2026 年的分化点是训练目标修补（IVC / 方向对齐 / 双次监督 / 免 JVP）与 RL 接法（展开链 PPO / best-of-N / 闭式信赖域 / 单步高斯接口）。
- | 逐步分解 | [DPPO](../papers/2409.00588_dppo/README.md) [ReinFlow](../papers/2505.22094_reinflow/README.md) [Flow-GRPO](../papers/2505.05470_flow_grpo/README.md) [DMPO](../papers/2601.20701_dmpo/README.md) | 逐步高斯转移 | 去噪链噪声（
  → | 逐步分解 | [DPPO](../papers/2409.00588_dppo/README.md) [ReinFlow](../papers/2505.22094_reinflow/README.md) [Flow-GRPO](../papers/2505.05470_flow_grpo/README.md) [DMPO](../papers/2601.20701_dmpo/README.md) | 逐步高斯转移 | 去噪/流随机
- | 路径空间 | [FLAC](../papers/2602.12829_flac/README.md) [GSB-MDPO](../papers/2603.21621_gsb_mdpo/README.md) | 无（drift 能量替代） | 动能预算 / 邻近半径 | 无结构性上限 | 上界松紧未量化、路径比率方差 | **无**（全部 locomotion 仿真） |
  → | 路径空间 | [FLAC](../papers/2602.12829_flac/README.md) [GSB-MDPO](../papers/2603.21621_gsb_mdpo/README.md) | 无终端似然；GSB-MDPO 仍用路径转移比率 | 动能预算 / 邻近半径 | 无结构性上限 | 上界松紧未量化、路径比率方差 | **无视觉操纵/真机**（状态输入控制仿真） |
- | 似然近似 | [MFPO](../papers/2604.14698_mfpo/README.md) | 平均散度网络一次前向 | max-ent 温度 | 无结构性上限 | 近似误差无界、Hutchinson 方差随维度涨 | 无 |
  → | 似然近似 | [MFPO](../papers/2604.14698_mfpo/README.md) | 平均散度网络默认两段各一次前向 | max-ent 温度 | 无结构性上限 | 缺统一近似误差界、Hutchinson 迹估计方差 | 无 |
- | 噪声空间 | [DSRL](../papers/2506.15799_dsrl/README.md) [LP-DS](../papers/2606.01151_lp_ds/README.md) [DF-ExpEnse](../papers/2606.19656_df_expense/README.md) | latent 高斯策略 | 噪声空间 SAC / UCB 候选 | 解码器支撑集内 | 高维噪声空间探索效率、改不了先验形状 
  → | 噪声空间 | [DSRL](../papers/2506.15799_dsrl/README.md) [LP-DS](../papers/2606.01151_lp_ds/README.md) [DF-ExpEnse](../papers/2606.19656_df_expense/README.md) | DSRL 用 latent 似然；LP-DS 用 latent Q 梯度 | 噪声空间 SAC / UCB 候选 | 解码器支
- | 条件化/加权监督 | [AWR](../papers/1910.00177_awr/README.md) [RECAP](../papers/2511.14759_recap/README.md) [Diffusion-QL](../papers/2208.06193_diffusion_ql/README.md) [FQL](../papers/2502.02538_fql/README.md) | BC 梯度 / 无 | 数据本
  → | 条件化/加权监督/行为正则 | [AWR](../papers/1910.00177_awr/README.md) [RECAP](../papers/2511.14759_recap/README.md) [Diffusion-QL](../papers/2208.06193_diffusion_ql/README.md) [FQL](../papers/2502.02538_fql/README.md) | AWR 需动作似然；
- | 生成-选择 | [MVP](../papers/2602.13810_mvp/README.md) [FMQ](../papers/2605.12416_fmq/README.md) [DF-ExpEnse](../papers/2606.19656_df_expense/README.md) | 无 | 候选多样性 | 受 Q 选择能力限制 | 推理 ×N | 无真机 |
  → | 生成-选择 | [MVP](../papers/2602.13810_mvp/README.md) [FMQ](../papers/2605.12416_fmq/README.md) [DF-ExpEnse](../papers/2606.19656_df_expense/README.md) | 无 | 候选多样性 | 受 Q 选择能力限制 | 候选生成与评分（DF-ExpEnse 仅采集期） | 无真机 |
- 读法：**路径空间是唯一没有操纵/真机证据的路线**——[P2](OPEN_PROBLEMS.md) 的机会。三个信赖域（GSB-MDPO 路径 KL / LP-DS latent L2 / FMQ 速度场 L2）在一步极限下合流。
  → 读法：**路径空间仍没有视觉操纵/真机证据**——[P2](OPEN_PROBLEMS.md) 的机会。三个偏移约束（GSB-MDPO 路径 KL / LP-DS latent L2 / FMQ 速度场 L2）对象不同，一步极限下的等价关系尚未建立。
- | [DSB](../papers/2106.01357_dsb/README.md)（神经 IPF） | unpaired | 是（交替半桥） | 否 | 否 | 低分辩图像 | 概念验证 |
  → | [DSB](../papers/2106.01357_dsb/README.md)（神经 IPF） | unpaired | 是（交替半桥） | 否 | MNIST 有 12 步结果 | 低分辩图像 | 概念验证 |
- | [I2SB](../papers/2302.05872_i2sb/README.md) | **paired** | 否（解析桥） | 是 | 是（~10-20 NFE） | ImageNet 256 修复 | 有退化算子的修复类任务 |
  → | [I2SB](../papers/2302.05872_i2sb/README.md) | **paired** | 否（解析桥） | 是 | 是（特定补全 2-10 NFE） | ImageNet 256 修复 | 有配对训练数据的修复类任务 |
- | [DSBM](../papers/2303.16852_dsbm/README.md)（IMF） | unpaired | 是（Markov/reciprocal 交替） | Markov 投影是回归，reciprocal 步需采样 | 否 | AFHQ 512 | 需要真 SB 耦合的 unpaired 翻译 |
  → | [DSBM](../papers/2303.16852_dsbm/README.md)（IMF） | unpaired | 是（Markov/reciprocal 交替） | Markov 投影是回归，更新端点需模拟模型 | 否 | AFHQ 512 | 需要真 SB 耦合的 unpaired 翻译 |
- | [SF2M](../papers/2307.03672_sf2m/README.md) | unpaired | 否（minibatch 熵 OT 一次拍死） | 是 | 否 | 中低维科学数据 | 单细胞等中低维 |
  → | [SF2M](../papers/2307.03672_sf2m/README.md) | unpaired | 默认否（静态 OT 耦合；可加外循环） | 是 | 否 | 单细胞（含 1000 基因）与 CIFAR-10 | 单细胞等分布快照 |
- | [ASBM](../papers/2405.14449_adv_sbm/README.md)（D-IMF） | unpaired | 是（离散时刻） | 否 | **是（4 NFE）** | 64-128 人脸 | 少步 unpaired 翻译 |
  → | [ASBM](../papers/2405.14449_adv_sbm/README.md)（D-IMF） | unpaired | 是（离散时刻） | 否 | **是（4 NFE）** | 128×128 人脸 | 少步 unpaired 翻译 |
- | [RSBM](../papers/2604.05673_rsbm/README.md) | paired（导航示范） | 否 | 是 | 是（3 步） | 导航 5 数据集 | few-step 具身策略 |
  → | [RSBM](../papers/2604.05673_rsbm/README.md) | paired（导航示范） | 否 | 是 | 是（3 积分步，原报 5 NFE） | 2 闭环仿真 + 5 开环真实数据集 | few-step 具身策略 |
- 读法：paired 场景（I2SB/RSBM）免迭代、天然少步；unpaired 场景要么迭代（IMF 系）要么接受静态近似偏差（SF2M）；**少步 + unpaired** 只有 ASBM 一家（对抗训练代价），是求解器层面的空格。[PRISM](../papers/2608.06893_prism/README.md) 给出参考过程设计的理论（仅 paired 高斯设定）。
  → 读法：paired 场景（I2SB/RSBM）免交替求桥，并有任务相关的少步证据；unpaired 场景要么迭代（IMF 系）要么接受静态近似偏差（SF2M）；**少步 + unpaired** 以本表 ASBM 为代表（对抗训练代价），是求解器层面的空格。[PRISM](../papers/2608.06893_prism/README.md) 给出参考过程设计的理论（仅 paired 高斯设定）。

## reports/OPEN_PROBLEMS.md（14 处）

- - 学习对象：$\bar u(a_t,r,t\mid o)=\frac{1}{t-r}\int_r^t b_\tau\,d\tau$，$b$ 是桥的条件漂移。恒等式 $\bar u=b-(t-r)\frac{d}{dt}\bar u$ 形式不变；桥的条件漂移有闭式，目标可算。
  → - 学习对象：$\bar u(a_t,r,t\mid o)=\frac{1}{t-r}\int_r^t b_\tau\,d\tau$，$b$ 是桥的条件漂移。若改学桥对应的确定性概率流，恒等式 $\bar u=b-(t-r)\frac{d}{dt}\bar u$ 形式不变；推广到随机桥漂移需另证，条件桥有闭式不等于边缘目标已知。
- - 必须内置两个修补：边界约束（$t=r$ 时 $\bar u=b$，即 MVP 的 IVC）与方向对齐（OMP）——桥在收口段漂移模长趋零，正是梯度饥饿最重的区间。
  → - 必须内置两个修补：边界约束（$t=r$ 时 $\bar u=b$，即 MVP 的 IVC）与方向对齐（OMP）——需按实际桥回归目标的模长检验方向梯度饥饿，桥在收口段漂移不必趋零。
- **假设**：path-space 邻近项（GSB-MDPO）或动能正则（FLAC）装进 few-step 桥策略后，在线微调的样本效率与多模态保持优于逐步分解路线（DPPO/DMPO），且在操纵任务上成立——这是 path-space 路线目前完全缺失的证据。
  → **假设**：path-space 邻近项（GSB-MDPO）或动能正则（FLAC）装进 few-step 桥策略后，在线微调的样本效率与多模态保持优于逐步分解路线（DPPO/DMPO），且在视觉操纵任务上成立——这是 path-space 路线目前完全缺失的证据。
- - 内核 A（on-policy）：GSB-MDPO 的路径 KL 邻近项，Girsanov 下是新旧漂移的加权 MSE；路径比率用逐步裁剪稳定。
  → - 内核 A（on-policy）：GSB-MDPO 的路径 KL 邻近项，共享初始分布与非退化扩散、满足 Girsanov 条件时是新旧漂移的加权 MSE；路径比率用逐步与累积 log-ratio 裁剪稳定。
- - 对照内核：DPPO 式逐步高斯似然 PPO；FMQ 式一步信赖域（$K=1$ 时的退化形式）。
  → - 对照内核：DPPO 式逐步高斯似然 PPO；FMQ 式平均速度信赖域（$K=1$ 时的对照）。
- **零件**：[GSB-MDPO](../papers/2603.21621_gsb_mdpo/README.md) · [FLAC](../papers/2602.12829_flac/README.md) · [DMPO](../papers/2601.20701_dmpo/README.md) · [DPPO](../papers/2409.00588_dppo/README.md) · [FMQ](../papers/2605.
  → **零件**：[GSB-MDPO](../papers/2603.21621_gsb_mdpo/README.md) · [FLAC](../papers/2602.12829_flac/README.md) · [DMPO](../papers/2601.20701_dmpo/README.md) · [DPPO](../papers/2409.00588_dppo/README.md) · [FMQ](../papers/2605.
- **假设**：一步生成策略（MeanFlow 族、蒸馏族）相对多步教师存在系统性的模式丢失，且丢失量随任务多模态程度增加；SB 的 $\epsilon$ 是唯一能连续控制这个代价的旋钮。目前没有任何一篇一步策略论文测过这件事。
  → **假设**：一步生成策略（MeanFlow 族、蒸馏族）相对多步教师存在系统性的模式丢失，且丢失量随任务多模态程度增加；SB 的 $\epsilon$ 是唯一能连续控制这个代价的旋钮。目前仍缺少一步策略的系统性模式覆盖对照。
- **零件**：[LP-DS](../papers/2606.01151_lp_ds/README.md)（熵估计先例）· [Diffusion Policy](../papers/2303.04137_diffusion_policy/README.md)（PushT 多模态设定）· [Consistency Policy](../papers/2405.07503_consistency_policy/README.md) · [Re
  → **零件**：[LP-DS](../papers/2606.01151_lp_ds/README.md)（熵估计先例）· [Diffusion Policy](../papers/2303.04137_diffusion_policy/README.md)（PushT 多模态设定）· [Consistency Policy](../papers/2405.07503_consistency_policy/README.md) · [Re
- - 翻译器：SB Flow（α-IMF，单网络在线迭代）在 sim 渲染图 ↔ 真机图像上训练，参考过程可按 PRISM 的规则设计（噪声集中在 sim-real 差异大的频段）。
  → - 翻译器：SB Flow（α-IMF，可共享单网络的双向在线迭代）在 sim 渲染图 ↔ 真机图像上训练，参考过程可借 PRISM 的按模态比较思路设计（噪声集中在 sim-real 差异大的频段，作为待验选择）。
- - 训练回路：BDGxRL 的结构——源域（sim）在线交互，观测经 SB 翻译成 real 风格后训练策略；奖励来自 sim。
  → - 训练回路：BDGxRL 的结构向视觉扩展——源域（sim）在线交互，转移经 SB 翻译后训练策略；奖励由源域数据训练的模型在翻译结果上重估。
- - 收敛分析可借 SB Flow 的框架：驻点从 SB 变为「advantage 重加权后的 SB」，与 Soft-SB 的几何混合定理对接。
  → - 收敛分析可借 SB Flow 的框架：加权改变边际后须重证「advantage 重加权后的 SB」驻点，再与 Soft-SB 固定初态下的几何混合定理对接。
- - 对表：FQL、MVP、FMQ（一步族 offline RL 的现役 SOTA）、Diffusion-QL。
  → - 对表：FQL、MVP、FMQ（一步族 offline / offline-to-online RL 的现役 SOTA）、Diffusion-QL。
- **「三个信赖域是同一个」**：GSB-MDPO（路径 KL）、LP-DS（latent 偏移 L2）、FMQ（平均速度场 L2）都在解「对参考的距离约束下最大化 Q」，路径 KL 经 Girsanov 就是速度场 L2，FMQ 恰是 GSB-MDPO 邻近项的一步极限。写清三者的等价条件与各自失效点（长链 vs 一步、冻结 vs 微调解码器），配一组统一实验，是一篇不需要新方法的有分量的分析文。零件：[GSB-MDPO](../pap
  → **「三个信赖域是同一个」**：GSB-MDPO（路径 KL）、LP-DS（latent 偏移 L2）、FMQ（平均速度场 L2）都在解「对参考的距离约束下最大化 Q」，路径 KL 在共享先验与非退化扩散等条件下经 Girsanov 化为漂移差的加权 L2，FMQ 与 GSB-MDPO 邻近项的一步极限是否对应仍需核对。写清三者的等价条件与各自失效点（长链 vs 一步、冻结 vs 微调解码器），配一组统一实验，是一篇不需要新方法的有分量
- | path-space 两组（FLAC/GSB-MDPO）自己补操纵实验 | P2 | 他们的 v2/v3 |
  → | path-space 两组（FLAC/GSB-MDPO）自己补视觉操纵实验 | P2 | 他们的 v2/v3 |

## reports/GLOSSARY.md（27 处）

- **Schrödinger Bridge（SB）**——在所有两端边际分别为 $\mu,\nu$ 的路径测度中，与参考测度 $\mathbb{Q}$ 相对熵最小者：$\min\{\mathrm{KL}(\mathbb{P}\|\mathbb{Q}):\mathbb{P}_0=\mu,\mathbb{P}_T=\nu\}$。直觉：给定起终点分布，最像参考过程（通常是布朗运动）的随机演化。解是一个 Markov 扩散，drift 由参考过程
  → **Schrödinger Bridge（SB）**——在所有两端边际分别为 $\mu,\nu$ 的路径测度中，与参考测度 $\mathbb{Q}$ 相对熵最小者：$\min\{\mathrm{KL}(\mathbb{P}\|\mathbb{Q}):\mathbb{P}_0=\mu,\mathbb{P}_T=\nu\}$。直觉：给定起终点分布，最像参考过程（通常是布朗运动）的随机演化。在相应存在条件和扩散参考下，解是 Markov 扩散
- **静态-动态等价**——路径 KL 沿端点分解为「端点耦合的 KL」+「给定端点后中间路径的 KL」；后者取零当且仅当中间用参考桥填充。于是 SB 只需优化端点耦合（熵正则 OT），中间用参考桥。这是所有「先耦合再匹配」算法（OT-CFM、SF2M、IMF）的依据。
  → **静态-动态等价**——路径 KL 沿端点分解为「端点耦合的 KL」+「给定端点后中间路径的 KL」；后者取零当且仅当中间用参考桥填充。于是 SB 只需优化端点耦合（参考核为相应 Gibbs 形式时对应熵正则 OT），中间用参考桥。这是 SF2M、IMF 及 OT-CFM 中 SB-CFM 构造的依据。
- **熵正则 OT / $\epsilon$**——SB 的静态形式 $\min\int c\,d\pi-\epsilon H(\pi)$。$\epsilon\to0$ 退化为 Monge-Kantorovich OT（确定性直路径），$\epsilon$ 大给噪声桥（多模态覆盖）。**$\epsilon$ 谱系**指把它当显式旋钮，在直度与覆盖间连续换挡——SB 相对 MeanFlow 族的核心差异化资产。→ [RSBM](../pap
  → **熵正则 OT / $\epsilon$**——在相应参考核下，SB 的静态形式为 $\min\int c\,d\pi-\epsilon H(\pi)$。布朗参考下 $\epsilon\to0$ 在适当条件下趋于二次 OT，固定端点间趋于直路径；$\epsilon$ 大增加桥噪声，多模态覆盖仍需验证。**$\epsilon$ 谱系**指把它当显式旋钮，在直度与覆盖间连续换挡——SB 相对 MeanFlow 族的核心差异化资产。→ [R
- **参考过程 $\mathbb{Q}$**——SB 目标里的基准测度，决定「哪条路径便宜」。布朗运动最常见；也可以是预训练模型的路径测度（informed reference）或高熵过程（FLAC）。**不可见性原理**（PRISM）：精确漂移 + 无限步下任何合法参考给同一后验，参考只在有限步预算下有意义。→ [PRISM](../papers/2608.06893_prism/README.md)
  → **参考过程 $\mathbb{Q}$**——SB 目标里的基准测度，决定「哪条路径便宜」。布朗运动最常见；也可以是预训练模型的路径测度（informed reference）或高熵过程（FLAC）。**不可见性原理**（PRISM）：在线性高斯复原模型的指定祖先采样器中，贝叶斯最优预测 + 无限步、正参考噪声恢复同一后验；参考噪声影响有限步误差。→ [PRISM](../papers/2608.06893_prism/README.m
- **广义 SB（GSB）**——在 SB 目标上加路径费用 $\int\mathbb{E}[V_t(x_t)]dt$ 或把硬终端约束换成软势 $-\mathbb{E}[\mathcal{G}(x_T)]$。RL 接口就在这里：$\mathcal{G}=Q$、$V_t=$ 代价。→ [GSBM](../papers/2310.02233_gsbm/README.md)、[Soft-SB](../papers/2403.01717_soft
  → **广义 SB（GSB）**——在 SB 目标上加路径费用 $\int\mathbb{E}[V_t(x_t)]dt$ 或把硬终端约束换成终端 KL 惩罚（Soft-SB）或软势 $-\mathbb{E}[\mathcal{G}(x_T)]$（FLAC）。RL 接口就在软势形式：$\mathcal{G}=Q$、$V_t=$ 代价。→ [GSBM](../papers/2310.02233_gsbm/README.md)、[Soft-SB]
- **Soft-constrained SB 的几何混合定理**——终端约束换成 KL 惩罚后，最优终端分布是目标与参考终端的几何混合 $\propto\mu^{a}\nu^{b}$。翻译到 RL 就是 KL 正则策略改进的闭式解形式。→ [Soft-SB](../papers/2403.01717_soft_sb/README.md)
  → **Soft-constrained SB 的几何混合定理**——固定初态为 Dirac 点、终端约束换成权重 $\beta$ 的 KL 惩罚后，最优终端分布是目标与无控参考终端的几何混合 $\propto\mu^{\beta/(1+\beta)}\nu^{1/(1+\beta)}$。与 KL 正则策略改进形式相关，但一般初态还需联立求势。→ [Soft-SB](../papers/2403.01717_soft_sb/README.m
- **Reciprocal 过程**——给定两端点后中间路径服从参考桥、区间内外条件独立的路径测度。**SB 解是唯一既 reciprocal 又 Markov 的测度**——IMF 算法的理论基础。
  → **Reciprocal 过程**——给定区间两端点后区间内外条件独立的过程；参考 reciprocal 类还要求给定两端点后中间路径服从该参考桥。**在指定两端边际与正则条件下，SB 解是唯一既属该参考 reciprocal 类又 Markov 的测度**——IMF 算法的理论基础。
- **Girsanov 动能恒等式**——参考为（尺度化）布朗运动、受控过程加漂移 $u$ 时，$\mathrm{KL}(\mathbb{P}^u\|\mathbb{Q})=\mathbb{E}\int\frac{\|u\|^2}{2\sigma^2}dt$。路径 KL = 漂移能量，**不算任何密度**。FLAC 用它替代策略熵，GSB-MDPO 用它把邻近项化成 drift-MSE。→ [FLAC](../papers/2602.12
  → **Girsanov 动能恒等式**——共享初始分布与非零扩散、满足绝对连续及可积条件，参考为（尺度化）布朗运动、受控过程加漂移 $u$ 时，$\mathrm{KL}(\mathbb{P}^u\|\mathbb{Q})=\mathbb{E}\int\frac{\|u\|^2}{2\sigma^2}dt$。路径 KL = 漂移能量，**不算任何密度**。FLAC 用相关动能正则替代显式熵计算，确定性版只给 Wasserstein 约束；G
- **Feynman-Kac 重加权**——GSB 的最优解等价于把参考测度按 $\exp(\mathcal{G}(x_T)-\int V\,dt)$ 重加权后再求 SB。「奖励塑形 = 改终端势」的严格版本；RECAP 的优势条件化、AWR 的指数加权都可以看作它的离散实现。
  → **Feynman-Kac 重加权**——在匹配温度与费用尺度、状态费用给定时，可把参考测度按 $\exp(\mathcal{G}(x_T)-\int V\,dt)$ 重加权后求相应约束问题；固定初始边际仍需保留。硬约束终端边际时，终端势期望已固定；RECAP 的优势条件化、AWR 的指数加权与这种重加权相关，但未证明是它的离散实现。
- **IPF（Iterative Proportional Fitting / Sinkhorn）**——交替投影到两个边际约束的经典 SB 数值解法。**神经 IPF** = DSB：交替训练前向/反向 drift 网络。缺点：拟合误差让边际漂移。→ [DSB](../papers/2106.01357_dsb/README.md)
  → **IPF（Iterative Proportional Fitting / Sinkhorn）**——交替投影到两个边际约束的经典 SB 数值解法。**神经 IPF** = DSB：交替训练前向/反向转移均值网络。缺点：拟合误差让边际漂移。→ [DSB](../papers/2106.01357_dsb/README.md)
- **IMF（Iterative Markovian Fitting）**——在 Markov 类与 reciprocal 类之间交替投影：reciprocal 投影保留当前端点耦合、中间用参考桥重填（纯采样）；Markov 投影把桥混合回归成一个 SDE 的 drift（纯回归）。两步都不动边际，修复了 IPF 的漂移。**α-IMF**（SB Flow）是它的小步幅在线离散化，单网络免重训。**D-IMF**（ASBM）是离散时间对抗
  → **IMF（Iterative Markovian Fitting）**——在 Markov 类与 reciprocal 类之间交替投影：reciprocal 投影保留当前端点耦合、中间用参考桥重填（纯采样）；Markov 投影把桥混合回归成一个 SDE 的 drift（纯回归）。精确投影都保持两端边际，只有 Markov 投影保持全部单时刻边际；神经近似仍会漂移。**α-IMF**（SB Flow）是它的小步幅在线离散化，可共享双向网
- **Bridge matching**——给定端点对，在参考桥上采中间点、回归指向端点的 drift。与 DDPM 训练同构；I2SB 在 paired 数据下免迭代，DSBM 把它当 Markov 投影用。
  → **Bridge matching**——给定端点对，在参考桥上采中间点、回归指向端点的 drift。与 DDPM 都用条件回归，但标签和桥核不同；I2SB 在 paired 数据下免交替求桥，DSBM 把它当 Markov 投影用。
- **Simulation-free**——训练不需要 SDE/ODE rollout。SF2M 用 minibatch 熵 OT 耦合 + 布朗桥闭式做到；**只指训练**，与推理少步无关。→ [SF2M](../papers/2307.03672_sf2m/README.md)
  → **Simulation-free**——训练不需要 SDE/ODE rollout。SF2M 用静态 OT 耦合（大量实验为批内无熵正则 OT）+ 布朗桥闭式做到；**只指训练**，与推理少步无关。→ [SF2M](../papers/2307.03672_sf2m/README.md)
- **Rectification / Reflow**——用当前流生成的端点对重训，耦合的传输代价不增且趋于确定性，路径越来越直。RSBM 的「桥矫正」借此名，实质是缩放桥方差（$\epsilon$）。→ [Rectified Flow](../papers/2209.03003_rectified_flow/README.md)
  → **Rectification / Reflow**——用当前流生成的端点对重训，理想拟合下新耦合确定、凸位移代价不增，历史最佳直度误差随迭代下降。RSBM 的「桥矫正」借此名，实质是缩放桥方差（$\epsilon$）。→ [Rectified Flow](../papers/2209.03003_rectified_flow/README.md)
- **Informative source / 边界即条件**——把结构化信息（退化图、上一 chunk、观测潜表示、sim 轨迹）当桥的起点而非网络的条件输入。起点近则路径短、少步稳。→ [I2SB](../papers/2302.05872_i2sb/README.md)、[BridgePolicy](../papers/2512.07212_bridge_policy/README.md)
  → **Informative source / 边界即条件**——把结构化信息（退化图、上一 chunk、观测潜表示、sim 轨迹）当桥的起点，也可保留网络条件输入。起点信息有望减少修正负担，少步收益依任务而定。→ [I2SB](../papers/2302.05872_i2sb/README.md)、[BridgePolicy](../papers/2512.07212_bridge_policy/README.md)
- **梯度饥饿**——MSE 对方向误差的梯度 $\propto\rho\rho^*\sin\alpha$，目标速度模长 $\rho^*$ 小时方向几乎得不到监督，网络宁可压模长也不修方向。精细低速动作首当其冲；桥的收口段同病。→ [OMP](../papers/2512.19347_omp/README.md)
  → **梯度饥饿**——MSE 对方向误差的梯度 $\propto\rho\rho^*\sin\alpha$，目标速度模长 $\rho^*$ 小时方向监督变弱，二维实验中先缩模长、方向纠正滞后。精细动作中的低模长训练目标需重点检查；桥漂移在收口段不一定趋零。→ [OMP](../papers/2512.19347_omp/README.md)
- **Consistency 蒸馏**——沿同一 PF-ODE 的不同点去噪到同一时刻应重合；从多步教师蒸馏一步学生。两阶段、上限受教师锁定。→ [Consistency Policy](../papers/2405.07503_consistency_policy/README.md)
  → **Consistency 蒸馏**——沿同一 PF-ODE 的不同点去噪到同一时刻应重合；从多步教师蒸馏一步或三步学生。两阶段；学生还用示范 DSM 监督，表现并非被教师锁死。→ [Consistency Policy](../papers/2405.07503_consistency_policy/README.md)
- **Dispersive 正则**——batch 内状态表征互斥的对比式损失，防一步生成的表征塌缩。→ [MP1](../papers/2507.10543_mp1/README.md)、[DMPO](../papers/2601.20701_dmpo/README.md)
  → **Dispersive 正则**——鼓励 batch 内隐藏表征分散的正则；MP1 作用于 U-Net 下采样特征，DMPO 作用于观测条件嵌入，不保证无塌缩。→ [MP1](../papers/2507.10543_mp1/README.md)、[DMPO](../papers/2601.20701_dmpo/README.md)
- **NFE**——网络前向次数。真机控制频率的直接决定量；1-NFE 时 Hz 由 backbone 决定，性能锚应改为多模态覆盖等硬指标。
  → **NFE**——网络前向次数。影响生成耗时；真机 Hz 还取决于感知、通信与执行，1-NFE 也需测端到端延迟，性能锚应改为多模态覆盖等硬指标。
- **log π 障碍**——生成式策略的动作是 SDE/ODE 终端边际，$\log\pi(a|s)$ 只有 ELBO 或需解 ODE 积分散度，策略梯度/熵正则/ratio 全部失效。本库主线问题。五条绕法见 [DIGEST](DIGEST.md)。
  → **log π 障碍**——生成式策略的动作是 SDE/ODE 终端边际，$\log\pi(a|s)$ 只有 ELBO 或需解 ODE 积分散度，常规动作似然接口受阻，仍可改用路径似然或其他更新目标。本库主线问题。五条绕法见 [DIGEST](DIGEST.md)。
- **Denoising-as-MDP / 两层 MDP**——去噪链每步当内层动作，逐步高斯似然可算，PPO 直接套。horizon 乘以步数、credit 均摊。→ [DPPO](../papers/2409.00588_dppo/README.md)
  → **Denoising-as-MDP / 两层 MDP**——去噪链每步当内层动作，逐步高斯似然可算，PPO 直接套。horizon 乘以步数，DPPO 用去噪折扣调整各步优势。→ [DPPO](../papers/2409.00588_dppo/README.md)
- **Mirror descent 策略优化**——$\pi_{k+1}=\arg\max\mathbb{E}[A]-\frac{1}{\eta}\mathrm{KL}(\pi\|\pi_k)$，KL 邻近项显式进目标（TRPO 是约束版、PPO clip 是启发式近似）。路径空间版 = GSB-MDPO。→ [MDPO](../papers/2005.09814_mdpo/README.md)
  → **Mirror descent 策略优化**——$\pi_{k+1}=\arg\max\mathbb{E}[A]-\frac{1}{\eta}\mathrm{KL}(\pi\|\pi_k)$，KL 邻近项显式进目标（TRPO 用反向 KL 约束，PPO clip 不与此目标等价）。路径空间版 = GSB-MDPO。→ [MDPO](../papers/2005.09814_mdpo/README.md)
- **Max-ent RL / energy-based 最优策略**——$\pi^*\propto\exp(Q/\alpha)$，Boltzmann 分布；与 SB 解的指数重加权是同一对象在动作/路径两层的投影。FLAC 把它做成严格版。→ [SAC](../papers/1801.01290_sac/README.md)
  → **Max-ent RL / energy-based 最优策略**——不受策略族限制时 $\pi^*\propto\exp(Q/\alpha)$，为 Boltzmann 分布；与 SB 指数重加权的对应还需核对参考与边界。FLAC 用动能正则接入 actor-critic，确定性版不严格等同最大熵目标。→ [SAC](../papers/1801.01290_sac/README.md)
- **Advantage-weighted / 优势条件化**——$\exp(A/\lambda)$ 当 BC 权重（AWR）或二值优势当条件 token（RECAP）。只需 BC 梯度，不需要 ratio；上限是数据里最好的行为。→ [AWR](../papers/1910.00177_awr/README.md)、[RECAP](../papers/2511.14759_recap/README.md)
  → **Advantage-weighted / 优势条件化**——$\exp(A/\lambda)$ 当 BC 权重（AWR）或二值优势当条件 token（RECAP）。不需要 ratio；AWR 仍需动作对数似然，RECAP 连续动作沿用流匹配。数据覆盖限制单次拟合，在线收集可扩展经验。→ [AWR](../papers/1910.00177_awr/README.md)、[RECAP](../papers/2511.14759_rec
- **噪声空间 RL / Diffusion steering**——冻结解码器，RL 学初始噪声。LP-DS 的残差 + 信赖域修正防 latent 漂移与模式坍缩。→ [DSRL](../papers/2506.15799_dsrl/README.md)、[LP-DS](../papers/2606.01151_lp_ds/README.md)
  → **噪声空间 RL / Diffusion steering**——冻结解码器，RL 学初始噪声。LP-DS 的残差 + 平均平方扰动预算抑制 latent 偏移与模式坍缩，但不是精确 KL 信赖域。→ [DSRL](../papers/2506.15799_dsrl/README.md)、[LP-DS](../papers/2606.01151_lp_ds/README.md)
- **生成-选择（best-of-N）**——采 N 个候选按 Q 选，改进靠选择压力，Q 梯度不穿生成器。FMQ 给出信赖域下的闭式替代。→ [MVP](../papers/2602.13810_mvp/README.md)、[DF-ExpEnse](../papers/2606.19656_df_expense/README.md)
  → **生成-选择（best-of-N）**——MVP 采 N 个候选按 Q 选，Q 梯度不穿生成器；DF-ExpEnse 只在采集期按价值与分歧选候选。FMQ 给在线训练目标提供局部闭式替代，推理仍有候选筛选。→ [MVP](../papers/2602.13810_mvp/README.md)、[DF-ExpEnse](../papers/2606.19656_df_expense/README.md)
- **Mode coverage**——策略保持多模态的程度。目前唯一系统评测是 LP-DS 的 Kozachenko-Leonenko 动作熵；本库 [P3](OPEN_PROBLEMS.md) 主张建基准。
  → **Mode coverage**——策略保持多模态的程度。LP-DS 用 Kozachenko-Leonenko 条件动作熵及多目标、绕障覆盖评测；ASBM 也报告 LPIPS 多样性；本库 [P3](OPEN_PROBLEMS.md) 主张建基准。

## reports/READING_PATHS.md（3 处）

- - **半天**：[SAC](../papers/1801.01290_sac/README.md)（energy-based 最优策略）→ [MDPO](../papers/2005.09814_mdpo/README.md)（KL 邻近项）→ [AWR](../papers/1910.00177_awr/README.md)（加权 BC 绕 log π）→ [DPPO](../papers/2409.00588_dppo/READM
  → - **半天**：[SAC](../papers/1801.01290_sac/README.md)（energy-based 最优策略）→ [MDPO](../papers/2005.09814_mdpo/README.md)（KL 邻近项）→ [AWR](../papers/1910.00177_awr/README.md)（加权 BC 绕行为密度与似然比）→ [DPPO](../papers/2409.00588_dppo/REA
- - **加一周**：07 类全部（尤其 [ReactVLA](../papers/2606.14255_reactvla/README.md)、[UCA-Flow](../papers/2608.16153_uca_flow/README.md) 看 VLA 尺度的一步化）+ [OMP](../papers/2512.19347_omp/README.md)/[MVP](../papers/2602.13810_mvp/README.m
  → - **加一周**：07 类全部（尤其 [ReactVLA](../papers/2606.14255_reactvla/README.md) 看 VLA 尺度的少步化、[UCA-Flow](../papers/2608.16153_uca_flow/README.md) 看点云策略的一步化）+ [OMP](../papers/2512.19347_omp/README.md)/[MVP](../papers/2602.13810_mv
- 2. 参考过程是什么（决定几何；多步极限下按 PRISM 不可见）？
  → 2. 参考过程是什么（决定几何；PRISM 的不可见性限于指定线性高斯模型与采样器的多步后验极限）？

## reports/TRENDS_2026.md（21 处）

- 1. **一步生成已成默认前提**：2026 年 2-8 月至少 6 篇新工作（MVP、MF-VLA、ReactVLA、MFPO、UCA-Flow、LP-DS 的 flow 后端）默认一步/少步，「多步 vs 一步」的争论结束了，竞争转入一步内部的表达力与 RL 兼容性。
  → 1. **一步生成已成默认前提**：2026 年 2-8 月至少 6 篇新工作（MVP、MF-VLA、ReactVLA、MFPO、UCA-Flow、OFP）默认一步/少步，「多步 vs 一步」的争论结束了，竞争转入一步内部的表达力与 RL 兼容性。
- 3. **max-ent × 生成式策略赛道开始拥挤**：MFPO（ICML 2026）用平均散度网络硬算 MeanFlow 似然进 SAC 框架，与 FLAC 的免似然动能正则形成正面路线之争；「likelihood-free vs likelihood-approximation」将是 2027 上半年的方法论主战场。
  → 3. **max-ent × 生成式策略赛道开始拥挤**：MFPO（ICML 2026）用平均散度网络近似 MeanFlow 似然进 SAC 框架，与 FLAC 的免似然动能正则形成正面路线之争；「likelihood-free vs likelihood-approximation」将是 2027 上半年的方法论主战场。
- 5. **工业界确认「无策略梯度 RL」路线**：Physical Intelligence 的 π*0.6/RECAP 用优势条件化（advantage conditioning）绕开 log π 做真实世界 VLA 改进——与学术界的 path-space 路线殊途同归，都在回避生成式策略的似然。
  → 5. **工业界确认「无策略梯度 RL」路线**：Physical Intelligence 的 π*0.6/RECAP 用优势条件化（advantage conditioning）绕开连续动作精确 log π 做真实世界 VLA 改进——与学术界的 path-space 路线殊途同归，都在回避连续动作的精确似然。
- - **MVP: Mean Flow Policy with Instantaneous Velocity Constraint**（[arXiv:2602.13810](https://arxiv.org/abs/2602.13810)，ICLR 2026 Oral；[解读](../papers/2602.13810_mvp/README.md)）——给平均速度场加瞬时速度边界约束（IVC），修 MeanFlow 缺边界条件的病；Ro
  → - **MVP: Mean Flow Policy with Instantaneous Velocity Constraint**（[arXiv:2602.13810](https://arxiv.org/abs/2602.13810)，ICLR 2026 Oral；[解读](../papers/2602.13810_mvp/README.md)）——给平均速度场加瞬时速度边界约束（IVC），修仅约束区间内部时的边界欠约束；RoboM
- - **MF-VLA: Mean-Flow based One-Step VLA**（[arXiv:2603.01469](https://arxiv.org/abs/2603.01469)，2026-03；[解读](../papers/2603.01469_mf_vla/README.md)）——MeanFlow 动作头进 VLA，真机比 SmolVLA 快 8.7 倍。证据强度：中弱（成功率仅「相当」）。值得跟：作为格局信号看。
  → - **MF-VLA: Mean-Flow based One-Step VLA**（[arXiv:2603.01469](https://arxiv.org/abs/2603.01469)，2026-03；[解读](../papers/2603.01469_mf_vla/README.md)）——MeanFlow 动作头进 VLA，真机动作生成比 SmolVLA 快 8.7 倍。证据强度：中弱（平均任务分数低 6.5 pp，堆叠低 1
- - **ReactVLA**（[arXiv:2606.14255](https://arxiv.org/abs/2606.14255)，2026-06；[解读](../papers/2606.14255_reactvla/README.md)）——改进版 MeanFlow（iMF）+ 注意力残差路由，LIBERO/真机延迟 <38.6 ms，胜 SmolVLA/π0。证据强度：中。值得跟：iMF 的改动值得读。
  → - **ReactVLA**（[arXiv:2606.14255](https://arxiv.org/abs/2606.14255)，2026-06；[解读](../papers/2606.14255_reactvla/README.md)）——已有改进版 MeanFlow（iMF）+ 注意力残差路由，LIBERO 两步 18.3 ms、真机五步 38.6 ms，LIBERO 平均成功率高于 SmolVLA/π0。证据强度：中。值得跟
- - **UCA-Flow**（[arXiv:2608.16153](https://arxiv.org/abs/2608.16153)，2026-08；[解读](../papers/2608.16153_uca_flow/README.md)）——条件与动作统一进单一 token 序列联合演化，一步生成，平均成功率超最强基线 9.3 pp，比 MP1 快 2.3 倍。证据强度：中强。值得跟：是，条件-动作联合建模可能是一步策略的下一个共
  → - **UCA-Flow**（[arXiv:2608.16153](https://arxiv.org/abs/2608.16153)，2026-08；[解读](../papers/2608.16153_uca_flow/README.md)）——条件与动作统一进单一 token 序列联合演化，一步生成，仿真分组成功率优于 MP1，比 MP1 快约 2.3 倍。证据强度：中强。值得跟：是，条件-动作联合建模可能是一步策略的下一个共识组件
- - **MFPO: Mean Flow Policy Optimization**（[arXiv:2604.14698](https://arxiv.org/abs/2604.14698)，ICML 2026；[解读](../papers/2604.14698_mfpo/README.md)）——MeanFlow 策略进 max-ent RL：平均散度网络近似似然积分 + 自适应瞬时速度估计，MuJoCo/DMC/HumanoidBen
  → - **MFPO: Mean Flow Policy Optimization**（[arXiv:2604.14698](https://arxiv.org/abs/2604.14698)，ICML 2026；[解读](../papers/2604.14698_mfpo/README.md)）——MeanFlow 策略进 max-ent RL：平均散度网络近似似然积分 + 自适应瞬时速度估计，MuJoCo/DMC/HumanoidBen
- - **BridgePolicy: Sample from What You See**（[arXiv:2512.07212](https://arxiv.org/abs/2512.07212)，ICML 2026，ShanghaiTech；[解读](../papers/2512.07212_bridge_policy/README.md)）——观测嵌入 SDE 动力学的 diffusion bridge 策略：从观测先验起步而非噪声，
  → - **BridgePolicy: Sample from What You See**（[arXiv:2512.07212](https://arxiv.org/abs/2512.07212)，ICML 2026，ShanghaiTech；[解读](../papers/2512.07212_bridge_policy/README.md)）——观测嵌入 SDE 动力学的 diffusion bridge 策略：从观测先验起步而非噪声，
- - （对照）**RSBM**（本仓库已收录，IEEE TMM）仍是 few-step SB 具身唯一正式文献；BDGxRL 后 sim-to-real SB×RL 未检索到直接后续——该线竞争格局依旧未恶化。
  → - （对照）**RSBM**（本仓库已收录，IEEE TMM 格式预印本）仍是 few-step SB 具身的文献锚点；BDGxRL 后 sim-to-real SB×RL 未检索到直接后续——该线竞争格局依旧未恶化。
- - **π*0.6 / RECAP**（[arXiv:2511.14759](https://arxiv.org/abs/2511.14759)，Physical Intelligence；[解读](../papers/2511.14759_recap/README.md)）——优势条件化：价值函数打分 → 二值优势 token 条件化 VLA → 推理时永远条件"positive"；免策略梯度、免似然；真实家庭叠衣/装箱/做咖啡，最难
  → - **π*0.6 / RECAP**（[arXiv:2511.14759](https://arxiv.org/abs/2511.14759)，Physical Intelligence；[解读](../papers/2511.14759_recap/README.md)）——优势条件化：价值函数打分 → 二值优势 token 条件化 VLA → 推理时默认条件"positive"；免策略梯度、免连续动作精确似然；真实家庭叠衣/装箱/
- - **LP-DS: Lagrangian Perturbation Diffusion Steering**（[arXiv:2606.01151](https://arxiv.org/abs/2606.01151)，ICML 2026；[解读](../papers/2606.01151_lp_ds/README.md)）——DSRL 的修正：学状态条件的残差噪声扰动 + 拉格朗日信赖域，防 latent 漂出高斯支撑与模式塌缩；Rob
  → - **LP-DS: Lagrangian Perturbation Diffusion Steering**（[arXiv:2606.01151](https://arxiv.org/abs/2606.01151)，ICML 2026；[解读](../papers/2606.01151_lp_ds/README.md)）——DSRL 的修正：学状态与噪声条件的残差扰动 + 拉格朗日扰动预算，抑制 latent 偏离高斯典型区域与模式塌
- - **FMQ: Aligning Flow Map Policies with Optimal Q-Guidance**（[arXiv:2605.12416](https://arxiv.org/abs/2605.12416)，2026-05；[解读](../papers/2605.12416_fmq/README.md)）——流映射策略统一框架 + 信赖域下 Q 引导的闭式更新，超 MVP 21.3%。**它无意中回答了「一步时代 
  → - **FMQ: Aligning Flow Map Policies with Optimal Q-Guidance**（[arXiv:2605.12416](https://arxiv.org/abs/2605.12416)，2026-05；[解读](../papers/2605.12416_fmq/README.md)）——流映射策略统一框架 + 信赖域下线性化 Q 引导的闭式更新，成功率 IQM 相对复现 MVP 提高 21.3
- - **PRISM**（[arXiv:2608.06893](https://arxiv.org/abs/2608.06893)，2026-08；[解读](../papers/2608.06893_prism/README.md)）——SB 参考过程设计理论：不可见性原理（参考只在有限步预算下有意义）+ 有限步最优噪声谱。把 SB 的差异化钉死在 few-step 区间。
  → - **PRISM**（[arXiv:2608.06893](https://arxiv.org/abs/2608.06893)，2026-08；[解读](../papers/2608.06893_prism/README.md)）——线性高斯复原桥的参考设计理论：不可见性原理（指定模型与采样器下的多步后验极限不依赖正噪声尺度）+ 受调度约束的噪声谱优化。把 SB 的差异化钉死在 few-step 区间。
- - **OMP**（[arXiv:2512.19347](https://arxiv.org/abs/2512.19347)，v3 2026-06；[解读](../papers/2512.19347_omp/README.md)）——诊断 MeanFlow 低速区的梯度饥饿，方向对齐修补；对 bridge matching 收口段同样适用。
  → - **OMP**（[arXiv:2512.19347](https://arxiv.org/abs/2512.19347)，v3 2026-06；[解读](../papers/2512.19347_omp/README.md)）——诊断 MeanFlow 低速区的梯度饥饿，方向对齐修补；迁移到 bridge matching 前需检验实际回归目标的模长。
- 1. **一步化完成范式化，竞争焦点转向「一步内部」**。现象：半年 6+ 篇一步策略，MeanFlow 族从操纵（MP1/DMPO）扩到 VLA（MF-VLA/ReactVLA）与 RL（MVP/MFPO）。证据：雷达 A 组。含义：任何 SB 策略工作把「少步」当主卖点都会被拒；SB 必须卖一步化做不到的东西——informative source、ε 旋钮、耦合结构。
  → 1. **一步化完成范式化，竞争焦点转向「一步内部」**。现象：半年 6+ 篇一步/少步策略，MeanFlow 族从操纵（MP1/DMPO）扩到 VLA（MF-VLA/ReactVLA）与 RL（MVP/MFPO）。证据：雷达 A 组。含义：任何 SB 策略工作把「少步」当主卖点都会被拒；SB 必须卖一步化做不到的东西——informative source、ε 旋钮、耦合结构。
- 2. **log π 障碍的四条解法路线成型且开始互相对表**。现象：似然近似（MFPO 的散度网络）、路径空间（FLAC/GSB-MDPO）、噪声空间（DSRL→LP-DS）、条件化监督（RECAP）四条路线各有 2026 年的强代表。证据：雷达 A/C 组。含义：2027 年的评审共识将要求新方法与至少两条既有路线正面对比；path-space 路线目前唯一没有真机与操纵证据，是它的软肋也是补位机会。
  → 2. **log π 障碍的四条解法路线成型且开始互相对表**。现象：似然近似（MFPO 的散度网络）、路径空间（FLAC/GSB-MDPO）、噪声空间（DSRL→LP-DS）、条件化监督（RECAP）四条路线各有近期的强代表。证据：雷达 A/C 组。含义：2027 年的评审共识将要求新方法与至少两条既有路线正面对比；path-space 路线目前唯一没有真机与视觉操纵证据，是它的软肋也是补位机会。
- 3. **informative source 从理念变成主会成果，但只做了 BC 半场**。现象：BridgePolicy 证明观测先验起步在 52 任务上稳定优于噪声起步。证据：雷达 B 组。含义：「bridge 起点 + few-step + RL 微调」的完整技术栈每一环都有文献而组合无人做，竞争窗口预计 6-12 个月。
  → 3. **informative source 从理念变成主会成果，但只做了 BC 半场**。现象：BridgePolicy 在 52 个仿真任务上平均成绩领先噪声起步基线。证据：雷达 B 组。含义：「bridge 起点 + few-step + RL 微调」的完整技术栈每一环都有文献而组合无人做，竞争窗口预计 6-12 个月。
- 2. **Few-step SB × path-space RL**：把 GSB-MDPO/FLAC 内核装进 RSBM/BridgePolicy 的骨架，落到操纵任务对表 DMPO/DBPO。path-space 路线缺操纵与真机证据，这一步同时补位。
  → 2. **Few-step SB × path-space RL**：把 GSB-MDPO/FLAC 内核装进 RSBM/BridgePolicy 的骨架，落到操纵任务对表 DMPO/DBPO。path-space 路线缺视觉操纵与真机证据，这一步同时补位。
- 1. **「SB 帽子」贬值加速**：BridgePolicy 用的是 diffusion bridge（Doob h-变换一系）而非严格 SB，评审已不区分——纯换 loss 的 SB 包装论文死刑，必须有 ε 谱系/耦合结构层面的差异化实验。
  → 1. **「SB 帽子」贬值加速**：BridgePolicy 用的是 diffusion bridge（UniDB 随机最优控制框架）而非严格 SB，评审已不区分——纯换 loss 的 SB 包装论文死刑，必须有 ε 谱系/耦合结构层面的差异化实验。
- 3. **MeanFlow 族的车轮战**：半年 6 篇的速度意味着任何「对表 MeanFlow」的实验节在投稿时就过时，写作策略上应对表「路线」而非单篇。
  → 3. **MeanFlow 族的车轮战**：半年 6 篇一步/少步工作的速度意味着任何「对表 MeanFlow」的实验节在投稿时就过时，写作策略上应对表「路线」而非单篇。

## slides/overview.html（29 处）

- <div class="node"><b>条件化监督</b><br><span class="dim">RECAP / AWR：优势当条件或权重，免梯度</span></div>
  → <div class="node"><b>条件化监督</b><br><span class="dim">RECAP / AWR：优势当条件或权重，监督更新</span></div>
- <div class="node"><b>生成-选择</b><br><span class="dim">MVP / FMQ / DF-ExpEnse：采 N 个按 Q 选或闭式 Q 引导</span></div>
  → <div class="node"><b>生成-选择</b><br><span class="dim">MVP / FMQ / DF-ExpEnse：候选价值筛选 / 探索评分或局部 Q 引导</span></div>
- <div class="node">DDIM / FM 直路径<br><span class="dim">10-50 步</span></div><div class="arr">→</div>
  → <div class="node">DDIM / FM 直路径<br><span class="dim">多步积分</span></div><div class="arr">→</div>
- <div class="node">OT-CFM 拉直耦合<br><span class="dim">5-10 步</span></div><div class="arr">→</div>
  → <div class="node">OT-CFM 拉直耦合<br><span class="dim">少步优势依任务</span></div><div class="arr">→</div>
- <div class="node">Consistency / 蒸馏<br><span class="dim">1-2 步，要教师</span></div><div class="arr">→</div>
  → <div class="node">Consistency Policy / 蒸馏<br><span class="dim">1 或 3 步，要教师</span></div><div class="arr">→</div>
- <h3>进入机器人（半年五连发）</h3>
  → <h3>进入机器人（四篇代表）</h3>
- <li><b>DMPO</b>：+dispersive 正则 +PPO 微调，&gt;120Hz 真机</li>
  → <li><b>DMPO</b>：+dispersive 正则 +PPO 微调，104.2Hz 真机端到端</li>
- <li><b>DBPO</b>：drift 固定点 + 精确似然接口，105.2Hz 双臂</li>
  → <li><b>DBPO</b>：drift 固定点 + 精确条件似然接口，105.2Hz 双臂</li>
- <p class="dim">路径 KL = 漂移场动能。<b>不算任何密度</b>就能正则化对参考过程的偏离。</p>
  → <p class="dim">同初始分布、同非零扩散及 Girsanov 条件下，路径 KL = 相对漂移动能。<b>不算任何密度</b>就能正则化对参考过程的偏离。</p>
- <p style="margin-top:8px"><b>FLAC</b>：把 SAC 的策略熵换成动能预算 + 拉格朗日自动调节 → 生成式策略的免似然 max-ent RL。</p>
  → <p style="margin-top:8px"><b>FLAC</b>：以动能预算 + 拉格朗日自动调节替代显式熵计算 → 免似然能量正则 RL（ODE 只保证几何约束）。</p>
- <p style="margin-top:8px"><b>GSB-MDPO</b>：MDPO 的 KL 邻近项搬进路径空间，drift-MSE 就是路径 KL 的离散形式 → 免终端似然的 on-policy 邻近更新。</p>
  → <p style="margin-top:8px"><b>GSB-MDPO</b>：MDPO 的 KL 邻近项搬进路径空间，加权 drift-MSE 一阶近似路径 KL → 免终端似然的 on-policy 邻近更新。</p>
- <p>「path-KL 换似然」理论位已被 FLAC（off-policy/max-ent）+ GSB-MDPO（on-policy/mirror descent）占满；两篇全是 locomotion 仿真，<b>操纵 / 视觉 / 真机全部空白</b>——path-space 路线的落地半场没人打。新对手 MFPO（ICML 2026）走似然近似路线正面叫板。</p>
  → <p>「path-KL 换似然」理论位已被 FLAC（off-policy/max-ent）+ GSB-MDPO（on-policy/mirror descent）占满；两篇以状态输入仿真为主，<b>视觉操纵 / VLA / 真机全部空白</b>——path-space 路线的落地半场没人打。新对手 MFPO（ICML 2026）走似然近似路线正面叫板。</p>
- <p class="dim">退化图当边界而非条件：ImageNet 修复 4 任务全胜条件扩散，NFE 从几百降到 ~20。<b>起点带信息 → 路径短 → 少步稳</b>。</p>
  → <p class="dim">退化图当边界而非条件：ImageNet 四类修复、九种退化设置，FID 更好但部分 CA 更低；特定补全 2–10 NFE 接近最佳，Palette 至少 100 NFE。<b>起点带信息 → 路径短 → 少步稳</b>。</p>
- <p class="dim">学习先验 + $\epsilon$ 旋钮（布朗桥 ↔ OT 连续换挡）：3 步 92% 成功率，免蒸馏。$\epsilon$ 谱系 = SB 独有的 coverage-straightness 权衡。</p>
  → <p class="dim">学习先验 + $\epsilon$ 旋钮（随机条件桥 ↔ 确定插值）：室内仿真 3 步 92% 成功率，免蒸馏。$\epsilon$ 谱系 = SB 独有的 coverage-straightness 权衡。</p>
- <p class="dim">观测嵌入 SDE 从观测先验起步：52 仿真 + 5 真机任务胜 DP/DP3/FlowPolicy。<b>顶会正面验证桥式起点</b>。</p>
  → <p class="dim">观测嵌入 SDE 从观测先验起步：52 仿真 + 5 真机任务均值领先对应基线，采用 10 NFE（FlowPolicy 为 1 NFE）。<b>顶会正面验证桥式起点</b>。</p>
- <p>DSB 把源域转移在线翻译成目标域风格 + 奖励调制，MuJoCo 跨域基准全胜 DARC 系——但停在低维状态空间，<b>像素级 sim-to-real SB 至今无人做</b>（2026-02 后该线零新对手）。</p>
  → <p>DSB 把源域转移在线翻译成目标域风格 + 奖励调制，MuJoCo 跨域 18 个设置均值均领先 DARC 等基线——但停在低维状态空间，<b>像素级 sim-to-real SB 至今无人做</b>（2026-02 后该线零新对手）。</p>
- <tr><td class="acc">问题定义</td><td>max-ent RL = 对高熵参考的 GSB</td><td>邻近策略更新搬进路径测度</td><td>few-step 部署的桥矫正</td><td>动力学差距 = unpaired 轨迹翻译</td></tr>
  → <tr><td class="acc">问题定义</td><td>以 GSB 动能正则替代显式熵计算</td><td>邻近策略更新搬进路径测度</td><td>few-step 部署的桥矫正</td><td>动力学差距 = unpaired 轨迹翻译</td></tr>
- <tr><td class="acc">log π 处理</td><td>动能上界终端 KL（免似然）</td><td>path-KL 作邻近项（免终端似然）</td><td>不涉及（纯监督）</td><td>不涉及（SAC 在翻译后数据上照常跑）</td></tr>
  → <tr><td class="acc">log π 处理</td><td>SDE 动能上界终端 KL；ODE 控制 W₂ 距离</td><td>path-KL 作邻近项（免终端似然）</td><td>不涉及（纯监督）</td><td>不涉及（SAC 在翻译后数据上照常跑）</td></tr>
- <tr><td class="acc">实验面</td><td>DMC + HumanoidBench（仿真 locomotion）</td><td>14 个 MuJoCo 任务（仿真 locomotion）</td><td>导航 5 数据集，3 步 92%</td><td>MuJoCo 跨域参数扰动</td></tr>
  → <tr><td class="acc">实验面</td><td>DMC + HumanoidBench（仿真 locomotion）</td><td>8 项 Playground + 6 项 Gym-MuJoCo（含手指/到达）</td><td>5 套真实数据开环；室内仿真 3 步 92%</td><td>MuJoCo 跨域参数扰动</td></tr>
- <h2>2026 雷达：半年内的新变量（2-8 月）</h2>
  → <h2>2026 雷达：近期的新变量（2025-11 至 2026-08）</h2>
- <h3>一步族扩张（6 篇）</h3>
  → <h3>少步族扩张（5 篇）</h3>
- <li><b>MF-VLA</b> 2603.01469 / <b>ReactVLA</b> 2606.14255：一步进 VLA</li>
  → <li><b>MF-VLA</b> 2603.01469 / <b>ReactVLA</b> 2606.14255：少步进 VLA（前者 1 步，后者仿真 2 步 / 真机 5 步）</li>
- <li><b>MFPO</b> 2604.14698 (ICML)：MeanFlow+max-ent，散度网络硬算似然——<span class="bad">FLAC 的正面对手</span></li>
  → <li><b>MFPO</b> 2604.14698 (ICML)：两步 MeanFlow+max-ent，平均散度网络近似似然——<span class="bad">FLAC 的正面对手</span></li>
- <li><b>UCA-Flow</b> 2608.16153：条件-动作联合 token，+9.3pp，快 MP1 2.3×</li>
  → <li><b>UCA-Flow</b> 2608.16153：条件-动作联合 token，对 MP1 报称 +9.3pp（总均值口径不符），所报生成延迟快 2.3×</li>
- <li><b>π*0.6/RECAP</b> 2511.14759：优势条件化免策略梯度，真实家庭任务吞吐翻倍</li>
  → <li><b>π*0.6/RECAP</b> 2511.14759：优势条件化免策略梯度，困难叠衣 / 浓缩咖啡任务成功吞吐超两倍</li>
- <li><b>LP-DS</b> 2606.01151 (ICML)：DSRL 修正 + <span class="warn">首个动作熵多模态评测</span></li>
  → <li><b>LP-DS</b> 2606.01151 (ICML)：DSRL 修正 + <span class="warn">动作熵与多目标 / 绕障覆盖评测</span></li>
- <p>三个同构的信赖域：<b>GSB-MDPO</b>（路径 KL）· <b>LP-DS</b>（latent 偏移 L2）· <b>FMQ</b>（平均速度场 L2，闭式解 $u^*=u^{\text{ref}}+\eta\,\nabla_aQ/\|\nabla_aQ\|$）。路径 KL 经 Girsanov 就是速度场 L2——<b>FMQ 的信赖域恰是 GSB-MDPO 邻近项在一步极限下的形式</b>。path-space 的价
  → <p>三个可比较的偏移约束：<b>GSB-MDPO</b>（路径 KL）· <b>LP-DS</b>（latent 偏移 L2）· <b>FMQ</b>（平均速度场 L2，局部线性 Q 目标的解 $u^*=u^{\text{ref}}+\eta\,\nabla_aQ/\|\nabla_aQ\|$）。同初始分布、同非零扩散下，路径 KL 经 Girsanov 对应相对漂移的加权 L2——<b>FMQ 的平均速度约束与 GSB-MDPO 的
- <p><b>不可见性原理</b>：精确漂移 + 无限步下，任何参考过程给出同一后验——换参考（FLAC 的高熵参考、informative reference 的种种设想）只在<b>有限步预算</b>下有意义。这恰好是机器人控制所在的区间。有限步最优噪声谱 ∝ 被摧毁信息谱 → 参考噪声应集中在「观测决定不了的动作维度」——informative source 先验设计的第一条可计算规则。</p>
  → <p><b>不可见性原理</b>：在线性高斯复原模型中，贝叶斯最优预测器 + 满足条件的细化网格下，正噪声参考在无限步恢复同一后验——该模型的参考差异体现于<b>有限步预算</b>，不等于一般 SB 的参考无关。这恰好是机器人控制所在的区间。高斯模型在共享网格、标量最优解唯一等条件下，最优噪声谱 ∝ 后验残差方差谱 → 可尝试在「观测决定不了的动作维度」加噪——informative source 先验设计的候选规则，非高斯动作仍需验证
- <p style="font-size:16.5px">回归速度/漂移场的方法在<b>低模长区间梯度饥饿</b>（方向梯度 ∝ 目标模长），且 MeanFlow 恒等式作为一阶 ODE <b>缺边界条件解不唯一</b>。桥匹配在收口段同病——one-step SB policy 必须内置方向对齐 + 边界约束（IVC 的桥版本），否则精细操纵先输在这里。</p>
  → <p style="font-size:16.5px">回归速度/漂移场的方法在<b>低模长区间梯度饥饿</b>（方向梯度 ∝ 目标模长），且 MeanFlow 恒等式作为一阶 ODE <b>缺边界条件解不唯一</b>。桥匹配是否出现同病需按实际目标模长检查——one-step SB policy 必须内置方向对齐 + 边界约束（IVC 的桥版本），否则精细操纵先输在这里。</p>

## slides/overview.tex（19 处）

- \textbf{步数演化}：DDPM(1000) $\to$ DDIM/FM(10--50) $\to$ OT-CFM(5--10) $\to$ 蒸馏/Consistency(1--2，需教师) $\to$ \textbf{MeanFlow 原生 1-NFE（免蒸馏）}
  → \textbf{步数演化}：DDPM(1000) $\to$ DDIM/FM（多步积分） $\to$ OT-CFM（少步依任务） $\to$ 蒸馏/Consistency Policy（1 或 3，需教师） $\to$ \textbf{MeanFlow 原生 1-NFE（免蒸馏）}
- \textbf{进入机器人（半年五连发）}：MP1（1-NFE 操纵，6.8ms）$\to$ DMPO（+PPO，$>$120Hz 真机）$\to$ OFP（免 JVP 自蒸馏，一步超 $\pi_{0.5}$ 十步）$\to$ DBPO（drift 固定点，105.2Hz 双臂）
  → \textbf{进入机器人（四篇代表）}：MP1（1-NFE 操纵，6.8ms）$\to$ DMPO（+PPO，104.2Hz 真机端到端）$\to$ OFP（免 JVP 自蒸馏，一步超 $\pi_{0.5}$ 十步）$\to$ DBPO（drift 固定点，105.2Hz 双臂）
- \qquad\text{路径 KL = 漂移动能，不算任何密度}
  → \qquad\text{同初态、同非零扩散及 Girsanov 条件下成立}
- FLAC：SAC 的策略熵 $\to$ 动能预算 + 拉格朗日自动调节（免似然 max-ent RL）。
  → FLAC：显式熵计算 $\to$ 动能预算 + 自动调节（ODE 仅有几何约束）。
- GSB-MDPO：MDPO 邻近项搬进路径空间，drift-MSE 即路径 KL 的离散形式。
  → GSB-MDPO：MDPO 邻近项搬进路径空间，加权 drift-MSE 一阶近似路径 KL。
- \alert{格局：理论位已被占满；两篇全是 locomotion 仿真——操纵/视觉/真机全空。MFPO（ICML 2026）走似然近似路线正面叫板。}
  → \alert{格局：理论位已被占满；两篇以状态仿真为主——视觉操纵/VLA/真机全空。MFPO（ICML 2026）走似然近似路线正面叫板。}
- \item \textbf{图像（I$^2$SB）}：退化图当边界而非条件，修复 4 任务全胜，NFE 几百 $\to$ 约 20。起点带信息 $\to$ 路径短 $\to$ 少步稳。
  → \item \textbf{图像（I$^2$SB）}：退化图当边界而非条件，四类修复、九种设置有指标取舍，特定补全 2--10 NFE 接近最佳。起点带信息 $\to$ 路径短 $\to$ 少步稳。
- \item \textbf{导航（RSBM）}：学习先验 + $\epsilon$ 旋钮（布朗桥 $\leftrightarrow$ OT 连续换挡），3 步 92\% 成功率免蒸馏。$\epsilon$ 谱系 = SB 独有的 coverage--straightness 权衡。
  → \item \textbf{导航（RSBM）}：学习先验 + $\epsilon$ 旋钮（随机条件桥 $\leftrightarrow$ 确定插值），室内仿真 3 步 92\% 成功率免蒸馏。$\epsilon$ 谱系 = SB 独有的 coverage--straightness 权衡。
- \item \textbf{操纵（BridgePolicy, ICML 2026）}：观测嵌入 SDE 从观测先验起步，52 仿真 + 5 真机任务胜 DP/DP3/FlowPolicy——顶会正面验证桥式起点（但只做了 BC 半场）。
  → \item \textbf{操纵（BridgePolicy, ICML 2026）}：观测嵌入 SDE 从观测先验起步，52 仿真 + 5 真机任务均值领先对应基线，10 NFE（FlowPolicy 为 1）——顶会正面验证桥式起点（但只做了 BC 半场）。
- \item \textbf{跨域（BDGxRL)}：DSB 在线翻译源域转移 + 奖励调制，MuJoCo 跨域全胜 DARC 系；像素级 sim-to-real SB 至今无人做。
  → \item \textbf{跨域（BDGxRL)}：DSB 在线翻译源域转移 + 奖励调制，MuJoCo 跨域 18 个设置均值均领先 DARC 等基线；像素级 sim-to-real SB 至今无人做。
- 问题定义 & max-ent = 对高熵参考的 GSB & 邻近更新进路径测度 & few-step 桥矫正 & 动力学差距 = unpaired 翻译 \\
  → 问题定义 & GSB 动能正则替代熵计算 & 邻近更新进路径测度 & few-step 桥矫正 & 动力学差距 = unpaired 翻译 \\
- $\log\pi$ 处理 & 动能上界终端 KL & path-KL 作邻近项 & 不涉及（纯监督） & 不涉及（翻译后 SAC） \\
  → $\log\pi$ 处理 & SDE 约束 KL；ODE 约束 $W_2$ & path-KL 作邻近项 & 不涉及（纯监督） & 不涉及（翻译后 SAC） \\
- 实验面 & DMC + HumanoidBench & 14 个 MuJoCo 任务 & 导航 3 步 92\% & MuJoCo 跨域 \\
  → 实验面 & DMC + HumanoidBench & 8 Playground + 6 Gym-MuJoCo & 室内仿真 3 步 92\% & MuJoCo 跨域 \\
- \begin{frame}{2026 雷达（2--8 月，10 篇）}
  → \begin{frame}{2026 雷达（2025-11 至 2026-08，9 篇）}
- \textbf{一步族扩张}：MVP（2602.13810，边界约束）· MF-VLA（2603.01469）· ReactVLA（2606.14255）· \alert{MFPO（2604.14698, ICML：MeanFlow+max-ent，FLAC 正面对手）} · UCA-Flow（2608.16153，+9.3pp）
  → \textbf{少步族扩张}：MVP（2602.13810，边界约束）· MF-VLA（2603.01469）· ReactVLA（2606.14255，仿真 2 步/真机 5 步）· \alert{MFPO（2604.14698, ICML：两步 MeanFlow+max-ent，FLAC 正面对手）} · UCA-Flow（2608.16153，对 MP1 报称 +9.3pp，均值口径不符）
- \textbf{RL 微调路线}：$\pi^*_{0.6}$/RECAP（2511.14759：优势条件化免策略梯度，真实任务吞吐翻倍）· LP-DS（2606.01151, ICML：DSRL 修正 + \textbf{首个动作熵多模态评测}）· DF-ExpEnse（2606.19656）· BridgePolicy（2512.07212, ICML）
  → \textbf{RL 微调路线}：$\pi^*_{0.6}$/RECAP（2511.14759：优势条件化免策略梯度，困难叠衣/浓缩咖啡成功吞吐超两倍）· LP-DS（2606.01151, ICML：DSRL 修正 + \textbf{动作熵与模式覆盖评测}）· DF-ExpEnse（2606.19656）· BridgePolicy（2512.07212, ICML）
- \textbf{(1) 一步时代 path-space 还剩什么}：三个同构信赖域——GSB-MDPO（路径 KL）· LP-DS（latent 偏移）· FMQ（平均速度场，闭式解 $u^*=u^{\mathrm{ref}}+\eta\,\nabla_aQ/\|\nabla_aQ\|$）。路径 KL 经 Girsanov 即速度场 $L^2$，\textbf{FMQ 的信赖域恰是 GSB-MDPO 邻近项的一步极限}。
  → \textbf{(1) 一步时代 path-space 还剩什么}：三个可比较的偏移约束——GSB-MDPO（路径 KL）· LP-DS（latent 偏移）· FMQ（平均速度场，局部线性 Q 解 $u^*=u^{\mathrm{ref}}+\eta\,\nabla_aQ/\|\nabla_aQ\|$）。同初态、同非零扩散下，路径 KL 对应相对漂移的加权 $L^2$，\textbf{与 FMQ 平均速度约束的一步等价性仍需证明}。
- \textbf{(2) PRISM 把 SB 差异化钉死在 few-step 区间}：不可见性原理——精确漂移 + 无限步下任何参考过程给同一后验，换参考只在有限步预算下有意义；有限步最优噪声谱 $\propto$ 被摧毁信息谱 $\to$ informative source 先验设计的第一条可计算规则。
  → \textbf{(2) PRISM 把 SB 差异化钉死在 few-step 区间}：不可见性原理——线性高斯复原模型中，最优预测器与合规细化网格使正噪声参考在无限步恢复同一后验；共享网格及最优解唯一等条件下，最优噪声谱 $\propto$ 后验残差方差谱 $\to$ informative source 的候选规则，动作迁移待验证。
- \textbf{共性病理（OMP / MVP）}：速度/漂移回归在低模长区\textbf{梯度饥饿}；MeanFlow 恒等式缺边界条件\textbf{解不唯一}。桥匹配收口段同病——one-step SB policy 必须内置方向对齐 + 边界约束。
  → \textbf{共性病理（OMP / MVP）}：速度/漂移回归在低模长区\textbf{梯度饥饿}；MeanFlow 恒等式缺边界条件\textbf{解不唯一}。桥匹配是否同病需检查实际目标——one-step SB policy 必须内置方向对齐 + 边界约束。

## data/papers.json（23 处）

- "role": "扩散模型开山：forward 加噪 + reverse 去噪 + ε-prediction"
  → "role": "高质量扩散生成范式：forward 加噪 + reverse 去噪 + ε-prediction"
- "role": "第一个 neural SB（neural IPF），bridge 算法系的起点"
  → "role": "neural SB（neural IPF），bridge 算法系的起点"
- "role": "IMF：交替 Markovian 投影，修复 DSB 的 path-space 漂移"
  → "role": "IMF：交替 Markovian / reciprocal 投影，缓解 DSB 的 path-space 漂移"
- "role": "对抗式 D-IMF：SB 采样降到 ~4-5 NFE"
  → "role": "对抗式 D-IMF：人脸翻译 SB 采样降到 4 NFE"
- "role": "advantage-weighted BC：offline 策略提取绕开 log π 的钥匙"
  → "role": "advantage-weighted BC：offline 策略提取绕开行为策略密度与概率比的钥匙"
- "venue": "arXiv 2025",
  → "venue": "AAAI 2026",
- "role": "dispersive 表征正则 + PPO 微调，>120 Hz Franka 实机"
  → "role": "dispersive 表征正则 + PPO 微调，104.2 Hz Franka 实机"
- "role": "从零自蒸馏免教师，训练时间约 0.5 倍"
  → "role": "从零自蒸馏免独立预训练教师，无需 JVP"
- "role": "sim-to-real 动力学差距：SB 做 unpaired 轨迹翻译"
  → "role": "跨域动力学差距：SB 做 unpaired 转移翻译"
- "role": "SB 参考过程设计理论：不可见性原理 + 有限步预算下的最优参考谱"
  → "role": "高斯复原桥参考过程设计理论：不可见性原理 + 共享调度下有限步预算的最优参考谱"
- "authors": "Garg, Zhang, Baudoin",
  → "authors": "Garg, Zhang, Zhou",
- "role": "终端约束软化为 KL 惩罚的随机控制解，GSB 的另一条推导路径"
  → "role": "终端约束软化为 KL 惩罚的随机控制解，GSB 路径成本的对照"
- "authors": "Prasad, Lin, Wu, Bohg",
  → "authors": "Prasad, Lin, Wu, Zhou, Bohg",
- "venue": "CoRL 2025",
  → "venue": "arXiv 2025",
- "venue": "arXiv 2025",
  → "venue": "ICML 2026",
- "role": "方向对齐正则 + 谱分析评 mode coverage，一步策略多模态评测的先例"
  → "role": "方向对齐正则 + 谱分析评幅度响应，一步策略训练信号分析的先例"
- "role": "flow map 策略的统一框架 + Q 引导对齐，一步策略 offline RL 的整合者"
  → "role": "flow map 策略的统一框架 + Q 引导对齐，一步策略 offline-to-online RL 的整合者"
- "role": "MeanFlow 动作头进 VLA，真机比 SmolVLA 快 8.7 倍"
  → "role": "MeanFlow 动作头进 VLA，真机动作生成比 SmolVLA 快 8.7 倍"
- "role": "MeanFlow 策略进 max-ent RL：平均散度网络硬算似然——FLAC 免似然路线的正面对手"
  → "role": "MeanFlow 策略进 max-ent RL：平均散度网络近似算似然——FLAC 免似然路线的正面对手"
- "role": "改进 MeanFlow（iMF）+ 注意力残差路由，真机延迟 <38.6 ms"
  → "role": "改进 MeanFlow（iMF）+ 注意力残差路由，真机平均延迟 38.6 ms"
- "role": "条件与动作统一 token 序列联合演化，一步生成 +9.3pp，比 MP1 快 2.3 倍"
  → "role": "条件与动作统一 token 序列联合演化，一步生成改善所测任务表现，生成比 MP1 快约 2.3 倍"
- "role": "DSRL 的信赖域修正 + 首个动作熵多模态保持评测"
  → "role": "DSRL 的扰动约束修正 + 动作熵多模态保持评测"
- "venue": "arXiv 2026",
  → "venue": "ICML 2026",