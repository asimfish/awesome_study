# Consistency Policy: Accelerated Visuomotor Policies via Consistency Distillation

> Prasad, Lin, Wu, Bohg (Stanford), RSS 2024。[arXiv:2405.07503](https://arxiv.org/abs/2405.07503)

## 一句话

用 Consistency Trajectory Model（CTM）的自一致性目标从预训练 Diffusion Policy 蒸馏出一步/三步策略：推理比最快替代方法再快一个量级、成功率相当、笔记本 GPU 可跑——蒸馏路线一步策略的代表作，MeanFlow 族的直接对照。

## 问题与动机

移动操作臂、四旋翼等平台放不下高端 GPU，Diffusion Policy 的多步去噪在这类硬件上延迟不可接受。图像领域的 consistency 蒸馏已证明能把多步扩散压成一步——搬到策略上行不行？

## 方法核心

1. **教师**：标准 Diffusion Policy（EDM 参数化）。
2. **学生目标 = DSM 损失 + CTM 损失**。CTM 的自一致性：同一条 PF-ODE 上的两点 $(x_t,t),(x_u,u)$（$s<u<t$）沿轨迹去噪到同一时刻 $s$ 应重合。实现：教师（stop-grad）从 $t\to u$，学生从 $t\to s$ 与从 $u\to s$（后者 stop-grad），两条路径的终点做一致性损失——学生学的是「任意时刻跳到任意更早时刻」的映射 $g_\theta(x_t,t,s;o)$。
3. **推理**：一步（$T\to0$ 直接跳）或三步（跳-加噪-跳的链式，精度更高）；可配 classifier-free guidance。
4. 附带发现：蒸馏对教师质量鲁棒——教师训得一般，学生仍能接近或超过教师。

## 实验与证据

- 6 个仿真任务 + 3 个真机任务：一步 Consistency Policy 比最快的替代加速方法快一个数量级，成功率与 Diffusion Policy 相当；三步版本进一步逼近教师精度。
- 真机推理在笔记本 GPU 上完成。
- 评价：加速与精度的证据充分；但两阶段训练（先教师再学生）与 CTM 目标的多个时间采样超参，是后来 MeanFlow 族攻击的靶子。

## 在谱系中的位置

- 上游：[Diffusion Policy](../2303.04137_diffusion_policy/)、Consistency Models / CTM。
- 平行：[Rectified Flow](../2209.03003_rectified_flow/)（直化路线）。
- 下游/对手：[MP1](../2507.10543_mp1/)/[DMPO](../2601.20701_dmpo/)/[OFP](../2603.12480_ofp/)/[DBPO](../2604.03540_dbpo/)——原生一步路线以「免教师、免两阶段」为卖点，Consistency Policy 是它们表格里的固定基线。

## 与 SB×RL 的关联

Consistency Policy 是「一步化靠蒸馏」时代的坐标原点：2024 年 SB 策略可以说「我们有理论、他们靠蒸馏」，2025 年后 MeanFlow 族把免蒸馏一步做成了，这句话就失效了——本仓库 06 类选题判断的校准正源于此。CTM 的「任意时刻到任意时刻」映射与 [FMQ](../2605.12416_fmq/) 的流映射、MeanFlow 的区间平均速度是同一对象的三种参数化，桥的版本（任意两时刻间的桥映射）同样可以蒸馏。对 SB 侧还有一个实用提示：蒸馏对教师质量鲁棒——SB 教师即使训练不稳（IMF 的老毛病），蒸馏出的一步学生可能仍然可用，这是绕开 SB 训练稳定性问题的一条现实路径。

## 局限与批判

- 两阶段训练，学生上限受教师锁定；CTM 目标的时间三元组采样与损失权重是敏感超参。
- 一步样本的多模态保持没有评测（consistency 蒸馏在图像上已知会损失多样性）。
- 纯 BC，无 RL；与后续 DPPO/DSRL 的组合留给了他人。
