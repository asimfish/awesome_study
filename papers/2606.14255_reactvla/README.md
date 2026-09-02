# ReactVLA: Fast and Lightweight Reactive Robot Manipulation via Improved Mean Flow Action Generation

> arXiv 2026-06。[arXiv:2606.14255](https://arxiv.org/abs/2606.14255)

## 一句话

改进版 MeanFlow 动作头（iMF，JVP 修正对齐瞬时速度）+ 注意力残差路由的策略 Transformer：0.39B 参数在 LIBERO 平均 88.0% 超过 4B 的 π0（86.0%）与 0.45B 的 SmolVLA（87.3%），推理延迟 18.3 ms（π0 93.4 ms、SmolVLA 74.1 ms）——一步/少步 MeanFlow 在 VLA 尺度上第一次同时拿到精度与速度。

## 问题与动机

扩散 VLA 多步采样让每个动作 chunk 的延迟落在 70-180 ms，反应式闭环（peg 插孔、动态抓取）不可用。已有 VLA 要么大（π0 4B+），要么快但一步不稳（SmolVLA 在 NFE=1 时轨迹幅度失控）。ReactVLA 的目标：轻量、低延迟、一到少步、精度不退。

## 方法核心

1. **iMF 动作头**：原始 MeanFlow 直接回归平均速度的非线性关系训练不稳，iMF 用 JVP 修正把平均传输预测对齐到瞬时速度场：
$$V_\theta(z_t,r,t) = u_\theta(z_t,r,t) + (t-r)\,\text{JVP}_{\text{sg}}\big[u_\theta;\,v_\theta\big]$$
以此构造的目标与瞬时速度 $v=\epsilon-a$ 匹配，本质是 MeanFlow 恒等式的稳定化参数化（与 [MVP](../2602.13810_mvp/) 的 IVC、[UCA-Flow](../2608.16153_uca_flow/) 的双通道属同一类修补）。
2. **注意力残差（AttnRes）Transformer**：把固定的残差累加换成深度方向的动态特征路由 $h_l=\sum_{j<l}\alpha_{lj}h_j$（各层特征按注意力权重汇聚），保留任务相关的多模态表示不被均匀残差冲淡。
3. 序列由时间、条件、动作 token 拼接，AttnRes 编码多模态观测后条件 iMF 头，一到少步生成 chunk。

## 实验与证据

- LIBERO 四类（Spatial/Object/Goal/Long）：ReactVLA 93.0/95.0/92.0/72.0，平均 88.0%；π0（4.03B）86.0%、SmolVLA（0.45B）87.3%、OpenVLA 76.5%、Diffusion Policy 72.4%。延迟 18.3 ms vs π0 93.4、SmolVLA 74.1、DP 178.8。
- RoboIMI 精密任务（peg 插孔、物体转移）：相对领先 VLA 任务表现最高提升 1.65 倍，推理快 4 倍以上。
- 真机延迟 <38.6 ms，实现反应式闭环控制。
- 评价：同基准同协议对比 π0/SmolVLA 有说服力；但 iMF 与 AttnRes 两个贡献的消融拆分、以及一步 vs 少步的具体 NFE 设置报告不够细。

## 在谱系中的位置

- 上游：[MeanFlow](../2505.13447_meanflow/)、[MF-VLA](../2603.01469_mf_vla/)（更早、更粗糙的 MeanFlow 进 VLA 尝试）、SmolVLA/π0（被超越的 VLA 基线）。
- 平行：[MVP](../2602.13810_mvp/)/[UCA-Flow](../2608.16153_uca_flow/)（对 MeanFlow 训练目标的独立修补）。

## 与 SB×RL 的关联

ReactVLA 把「一步化已是默认」从操纵小模型推进到 VLA 尺度，且以 0.39B 打 4B——说明动作头的建模方式比 backbone 规模更能决定反应式控制的可用性。对 SB 侧的含义：VLA 动作头这个位置目前被 MeanFlow 族占满，SB 策略若要进 VLA，必须以「动作头可替换模块」的形态出现，并在 LIBERO 这类标准基准上拿到同级延迟——桥式起点（上一 chunk 或观测潜表示）能不能在 20 ms 预算内换来精度，是可以直接检验的。另一个空格：ReactVLA 是纯 BC，VLA 尺度的一步动作头 + RL 微调（RECAP 式或 path-space 式）尚无公开工作。

## 局限与批判

- iMF 引自他人工作（[7]），ReactVLA 的原创性主要在架构组合与工程整合。
- LIBERO 是饱和度较高的基准，88.0 vs 87.3 的差距在 seed 方差内的可能性未排除（未报告置信区间）。
- 无 RL、无多模态评测；「反应式」的主张靠延迟数字支撑，缺少动态扰动场景的闭环实验。
