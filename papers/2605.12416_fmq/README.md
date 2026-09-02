# Aligning Flow Map Policies with Optimal Q-Guidance (FMQ)

> Ziakas, Russo, Bose (Imperial & Mila), arXiv 2026-05。[arXiv:2605.12416](https://arxiv.org/abs/2605.12416)

## 一句话

提出「流映射策略」统一所有一步/少步流策略（学任意两时刻间的跳跃算子），并在信赖域下推出 Q 引导的闭式最优学习目标（FMQ）+ Q 引导束搜索采样器：OGBench + RoboMimic 12 任务 offline-to-online SOTA，相对 MVP 平均成功率再提 21.3%。

## 问题与动机

一步流策略族（MeanFlow/MVP/OFP/Shortcut）各自为战，缺统一语言；在线适配阶段大家靠 best-of-N（采 N 个按 Q 选），要 N 次前向 + N 次 Q 评估，且「选」不是「学」——策略本身没被 Q 的方向信息更新。FMQ 问：给一个离线流策略，能不能**闭式**算出在信赖域内让 Q 最大的更新方向？

## 方法核心

1. **流映射策略**：$X_{r,t}(a_r|s)=a_r+(t-r)u_{r,t}(a_r|s)$，$u_{r,t}$ 是区间平均速度（同 MeanFlow），策略 $\pi=[X_{r,1}]_\#p_r$；$r=0,t=1$ 即一步策略。训练 = 对角线 $r=t$ 上的标准 flow matching（切条件）+ 非对角线上的自蒸馏一致性（Lagrange/Euler/Progressive 三种 PINN 式条件，来自 Boffi 等的流映射理论）——MeanFlow/Shortcut/consistency 都是它的特例。
2. **Theorem 3.2（闭式 Q 引导）**：以参考流映射 $u^{\text{ref}}_{r,1}$ 为锚，在 $\|u_{r,1}-u^{\text{ref}}_{r,1}\|\le\eta$ 的信赖域内最大化 $Q$ 的一阶展开，KKT 给出
$$u^*_{r,1}(a_r|s)=u^{\text{ref}}_{r,1}(a_r|s)+\eta\,\frac{\nabla_aQ_\phi(s,a_1)}{\|\nabla_aQ_\phi(s,a_1)\|_2}$$
——沿 Q 梯度的单位方向挪 $\eta$。把它当回归目标训练流映射就是 FMQ：**不需要 best-of-N、不需要似然、不需要 Q 梯度穿过多步链**（只在终端动作处取一次梯度）。
3. **QGBS 采样器**：推理期按 SNR 选 $t'$ 重加噪 $a_{t'}=t'a_1+(1-t')\varepsilon$，束搜索 K 轮（每轮用 eq. 11 的信赖域更新），返回 Q 最高者；K=0 退回一步。

## 实验与证据

- 12 任务（OGBench 长程稀疏 + RoboMimic），offline-to-online：SOTA，相对 MVP 平均成功率 +21.3%（相对提升）。
- 消融：三种自蒸馏条件的对比、信赖域半径 $\eta$、束搜索轮数 K。
- 评价：MVP 是最新最强的一步基线，赢它 21.3% 有分量；但 FMQ 的更新等价于「归一化 Q 梯度上升 + 信赖域」，与 TD3 式确定性策略梯度的差别主要在锚点是生成式策略——「principled」的成色需要与「直接 DPG 微调一步生成器」对比才能坐实，论文未做。

## 在谱系中的位置

- 上游：[MeanFlow](../2505.13447_meanflow/)（平均速度）、Boffi 流映射理论、[FQL](../2502.02538_fql/)（offline-to-online 流基线）、[MVP](../2602.13810_mvp/)（被超越的 best-of-N 路线）。
- 平行：[OFP](../2603.12480_ofp/)（自蒸馏一步）、[DBPO](../2604.03540_dbpo/)。
- 本仓库定位：一步策略 offline RL 的「整合者」——统一框架 + 闭式更新。

## 与 SB×RL 的关联

FMQ 的信赖域闭式解是 [LP-DS](../2606.01151_lp_ds/)（latent 空间）与 [GSB-MDPO](../2603.21621_gsb_mdpo/)（路径空间）的第三个同构：都是「在对参考的距离约束下最大化 Q」，只是距离分别定义在速度场/latent/路径测度上。三者的关系还没人写清——路径 KL 经 Girsanov 就是速度场的 L2，所以 **FMQ 的 $\|u-u^{\text{ref}}\|\le\eta$ 恰好是 GSB-MDPO 路径 KL 邻近项在一步极限下的形式**：一步时代 path-space 邻近项「还剩什么」这个问题（GSB-MDPO 解读里提出的），FMQ 无意中给了答案——剩下的就是平均速度场上的信赖域。对 SB 侧的机会：流映射框架可以原样搬到桥上（两端任意分布的「桥映射」），FMQ 的闭式目标也随之可用，one-step SB policy 的 RL 微调有了现成的更新规则。

## 局限与批判

- 一阶展开 + 归一化梯度：Q 的曲率信息全丢，$\eta$ 固定时在 Q 平坦区与陡峭区行为迥异，自适应 $\eta$ 没讨论。
- 「可行性假设」（最优动作可由扰动到达）在示范覆盖外不成立，与 RECAP/LP-DS 同样受支撑集限制。
- QGBS 的推理成本随 K 与束宽增长，与一步化诉求相悖，且 SNR 选 $t'$ 的规则是经验的。
- 无真机、无视觉输入。
