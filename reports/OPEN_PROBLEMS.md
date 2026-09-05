# 开放问题与实验设计

> 把 [DIGEST](DIGEST.md) 里的五个空格展开成可以直接开工的研究方案。每个方案回答五件事：假设是什么、最小实验怎么做、对表谁、什么结果会杀死它、库里哪些论文是零件。窗口估计截至 2026-09。

## P1. One-step SB Policy：桥上的平均漂移场

**假设**：MeanFlow 的「区间平均速度」可以推广为桥上的「区间平均漂移」，配 informative 边界与 $\epsilon$ 旋钮，在 1-NFE 下比 MeanFlow 族多保住多模态覆盖，且在精细任务上精度不退。

**构造**：
- 边界：源 $=$ 上一 chunk 的执行动作（或 BridgePolicy 式的观测潜表示），目标 $=$ 专家动作；参考 $=$ 方差按 $\epsilon$ 缩放的布朗桥（RSBM 的 $\epsilon$-核）。
- 学习对象：$\bar u(a_t,r,t\mid o)=\frac{1}{t-r}\int_r^t b_\tau\,d\tau$，$b$ 是桥的条件漂移。恒等式 $\bar u=b-(t-r)\frac{d}{dt}\bar u$ 形式不变；桥的条件漂移有闭式，目标可算。
- 必须内置两个修补：边界约束（$t=r$ 时 $\bar u=b$，即 MVP 的 IVC）与方向对齐（OMP）——桥在收口段漂移模长趋零，正是梯度饥饿最重的区间。
- 训练可以从零（OFP 式自蒸馏，避开 JVP）。

**最小实验**：RoboMimic（Lift/Can/Square/Transport）+ Adroit，BC 设定。
- 对表：MP1、OFP、DMPO（预训练阶段）、BridgePolicy（NFE=10 与 NFE=1 两档）、Consistency Policy。
- 指标：成功率；推理延迟；**动作熵**（LP-DS 的 KL 估计器）与 PushT 式多模态计数；精细任务（Square/Transport）上的单独成绩。
- 扫 $\epsilon\in\{0.05,0.2,0.5,1\}$：预期 $\epsilon$ 小精度高、$\epsilon$ 大熵高，中间存在使两者同时优于 MeanFlow 基线的区间。

**杀死条件**：若在所有 $\epsilon$ 下动作熵与 MeanFlow 基线无差、或 informative 起点在 1-NFE 下不带来精度收益（起点信息被一步映射「吸收」），则 SB 在一步区间没有位置。

**零件**：[MeanFlow](../papers/2505.13447_meanflow/README.md) · [RSBM](../papers/2604.05673_rsbm/README.md) · [BridgePolicy](../papers/2512.07212_bridge_policy/README.md) · [MVP](../papers/2602.13810_mvp/README.md) · [OMP](../papers/2512.19347_omp/README.md) · [OFP](../papers/2603.12480_ofp/README.md) · [I2SB](../papers/2302.05872_i2sb/README.md)。**窗口 6-12 个月**——BridgePolicy 组或 MeanFlow 族任何一家顺手就能做。

## P2. Few-step SB × Path-space RL 落到操纵

**假设**：path-space 邻近项（GSB-MDPO）或动能正则（FLAC）装进 few-step 桥策略后，在线微调的样本效率与多模态保持优于逐步分解路线（DPPO/DMPO），且在操纵任务上成立——这是 path-space 路线目前完全缺失的证据。

**构造**：
- 骨架：P1 的桥策略（或直接用 RSBM/BridgePolicy 的多步版，$K\in\{3,5\}$）。
- 内核 A（on-policy）：GSB-MDPO 的路径 KL 邻近项，Girsanov 下是新旧漂移的加权 MSE；路径比率用逐步裁剪稳定。
- 内核 B（off-policy）：FLAC 的动能预算 + 拉格朗日温度。
- 对照内核：DPPO 式逐步高斯似然 PPO；FMQ 式一步信赖域（$K=1$ 时的退化形式）。

**最小实验**：RoboMimic 微调（DMPO 的设定，Can/Square/Transport）+ 一个视觉任务（像素 RoboMimic 或 LIBERO 子集）。
- 指标：微调后成功率、样本效率曲线、微调前后动作熵变化（RL 塌模式是已知现象，这是 SB 卖点的试金石）、控制频率。
- 附加分析：路径 KL 上界与实测终端 KL 的比值——量化 GSB-MDPO/FLAC 都没给的「上界松紧」。

**杀死条件**：若 $K\le3$ 时 path-space 内核与逐步分解在所有指标上无差——说明短链下两条路线合流（FMQ 的暗示），path-space 的独立价值仅剩多步长链场景。

**零件**：[GSB-MDPO](../papers/2603.21621_gsb_mdpo/README.md) · [FLAC](../papers/2602.12829_flac/README.md) · [DMPO](../papers/2601.20701_dmpo/README.md) · [DPPO](../papers/2409.00588_dppo/README.md) · [FMQ](../papers/2605.12416_fmq/README.md) · [Soft-SB](../papers/2403.01717_soft_sb/README.md)（几何混合定理给出最优终端分布的精确形式，可作为分析工具）。**窗口 12 个月**。

## P3. Mode Coverage 基准：一步化的多模态代价

**假设**：一步生成策略（MeanFlow 族、蒸馏族）相对多步教师存在系统性的模式丢失，且丢失量随任务多模态程度增加；SB 的 $\epsilon$ 是唯一能连续控制这个代价的旋钮。目前没有任何一篇一步策略论文测过这件事。

**构造**：
- 评测套件：三类任务——合成多峰（可控峰数 2/4/8，如 LP-DS 的四峰玩具）、PushT/Block Pushing（Diffusion Policy 原文的多模态展示）、RoboMimic 多示范风格子集。
- 指标：动作熵（Kozachenko-Leonenko）、峰覆盖率（生成样本落入每个专家模式的比例）、条件多样性（同一观测下 N 次采样的成对距离）、以及成功率——四者并列。
- 被测方法：DP（多步教师）、Consistency Policy、MP1、OFP、DBPO、UCA-Flow、RSBM/P1 的桥策略按 $\epsilon$ 扫描。

**产出**：一张「成功率 vs 模式覆盖」的 Pareto 图 + 每个一步方法的模式丢失量。这是基准工作，价值在定义口径。

**杀死条件**：若所有一步方法的模式覆盖与教师无差——「一步化有多模态代价」的前提不成立，P1 的卖点随之减半。

**零件**：[LP-DS](../papers/2606.01151_lp_ds/README.md)（熵估计先例）· [Diffusion Policy](../papers/2303.04137_diffusion_policy/README.md)（PushT 多模态设定）· [Consistency Policy](../papers/2405.07503_consistency_policy/README.md) · [Rectified Flow](../papers/2209.03003_rectified_flow/README.md)（矫正定理：直化产生确定性耦合，多样性全靠起点噪声——理论上预示模式丢失）。**先做先赢**。

## P4. 像素级 Sim-to-real Schrödinger Bridge

**假设**：SB 做 unpaired 的 sim→real 视觉翻译，比 CycleGAN 类方法更原则、比 domain randomization 更数据高效，且翻译后训练的策略在真机成功率上提升可测。BDGxRL 停在低维状态，该线自 2026-02 起零新对手。

**构造**：
- 翻译器：SB Flow（α-IMF，单网络在线迭代）在 sim 渲染图 ↔ 真机图像上训练，参考过程可按 PRISM 的规则设计（噪声集中在 sim-real 差异大的频段）。
- 训练回路：BDGxRL 的结构——源域（sim）在线交互，观测经 SB 翻译成 real 风格后训练策略；奖励来自 sim。
- 升级项：策略感知的桥（IMF 的 reciprocal 步按当前策略的访问分布加权），让翻译误差不随策略漂移失控。

**最小实验**：一个可 sim-to-real 的操纵任务（如 pick-place，Franka），sim 用 Isaac/MuJoCo 渲染，real 收几百张无标注图。
- 对表：domain randomization、CycleGAN、直接 sim 训练零翻译。
- 指标：真机成功率、翻译 FID/LPIPS、每张真机图的数据效率。

**杀死条件**：若 SB 翻译与 CycleGAN 在下游成功率上无差——「原则性」没有换成性能，该线只剩理论意义。

**零件**：[BDGxRL](../papers/2602.23737_bdg/README.md) · [SB Flow](../papers/2409.09347_sb_flow/README.md) · [DSBM](../papers/2303.16852_dsbm/README.md) · [PRISM](../papers/2608.06893_prism/README.md) · [GSBM](../papers/2310.02233_gsbm/README.md)（把奖励写进路径费用，翻译与奖励对齐一体化）。**竞争最少，工程最重**。

## P5. RL 加权耦合：在 SB 训练循环里做 RL

**假设**：SB 求解器的「耦合」步（IMF 的 reciprocal 投影、OT-CFM 的 minibatch 耦合）是注入 RL 信号的天然位置——按 advantage 加权端点采样，等价于对参考测度做 Feynman-Kac 重加权（GSB 的软终端势），得到一个不需要似然、不需要逐步分解的 SB 策略改进算法。

**构造**：
- 基础循环：SB Flow 的 α-IMF（小步幅在线自更新）。
- 改动一处：reciprocal 步的端点对 $(a_0,a_1)$ 采样权重 $\propto\exp(A(s,a_1)/\lambda)$（AWR 的权重进耦合而非 loss）。
- 收敛分析可借 SB Flow 的框架：驻点从 SB 变为「advantage 重加权后的 SB」，与 Soft-SB 的几何混合定理对接。

**最小实验**：D4RL/OGBench offline 设定 + offline-to-online。
- 对表：FQL、MVP、FMQ（一步族 offline RL 的现役 SOTA）、Diffusion-QL。
- 指标：成功率/回报、训练墙钟、多模态保持。

**杀死条件**：若加权耦合与「AWR 权重进 loss」在性能上无差——耦合层注入没有独立价值，只是换了个位置写同一件事。

**零件**：[SB Flow](../papers/2409.09347_sb_flow/README.md) · [OT-CFM](../papers/2302.00482_ot_cfm/README.md) · [AWR](../papers/1910.00177_awr/README.md) · [Soft-SB](../papers/2403.01717_soft_sb/README.md) · [GSBM](../papers/2310.02233_gsbm/README.md) · [FQL](../papers/2502.02538_fql/README.md)。**纯算法空格**。

## 附：一篇可以先写的短文

**「三个信赖域是同一个」**：GSB-MDPO（路径 KL）、LP-DS（latent 偏移 L2）、FMQ（平均速度场 L2）都在解「对参考的距离约束下最大化 Q」，路径 KL 经 Girsanov 就是速度场 L2，FMQ 恰是 GSB-MDPO 邻近项的一步极限。写清三者的等价条件与各自失效点（长链 vs 一步、冻结 vs 微调解码器），配一组统一实验，是一篇不需要新方法的有分量的分析文。零件：[GSB-MDPO](../papers/2603.21621_gsb_mdpo/README.md) · [LP-DS](../papers/2606.01151_lp_ds/README.md) · [FMQ](../papers/2605.12416_fmq/README.md) · [MDPO](../papers/2005.09814_mdpo/README.md)。

## 风险总表

| 风险 | 影响的问题 | 触发信号 |
|---|---|---|
| UCA-Flow 式架构把一步质量推到与多步无差 | P1、P3 | 一步 vs 多步成功率差 <2 pp 且多模态无差 |
| MeanFlow 族任何一家发 bridge 版 | P1 | 关注 BridgePolicy 组与 MP1/DMPO 组 |
| path-space 两组（FLAC/GSB-MDPO）自己补操纵实验 | P2 | 他们的 v2/v3 |
| 评审不区分 diffusion bridge 与 SB | 全部 | 必须用 $\epsilon$ 谱系实验证明差异，不能只讲理论 |
| 一步化让 $\epsilon$ 旋钮无用 | P1、P3 | $\epsilon$ 扫描曲线平坦 |
