# Flow Straight and Fast: Learning to Generate and Transfer Data with Rectified Flow

> Liu, Gong, Liu (UT Austin), ICLR 2023。[arXiv:2209.03003](https://arxiv.org/abs/2209.03003)

## 一句话

学一个尽量沿两端点直线走的 ODE，并证明「矫正」（reflow：用自己生成的端点对重新训练）把任意耦合变成传输代价不增的确定性耦合、迭代下路径越来越直——few-step/one-step 生成与「拉直桥」思想的流侧源头。

## 问题与动机

生成模型本质是两个经验分布 $\pi_0,\pi_1$ 之间的传输问题。已有方法要么多步（扩散）、要么训练不稳（GAN）、要么要解 ODE 训练（CNF）。Rectified Flow 的观察：最短路径是直线，直线可以零离散误差地一步模拟——那就直接让 ODE 学直线，学不直就迭代矫正。

## 方法核心

1. **基本目标**：给定耦合 $(X_0,X_1)\sim\gamma$，线性插值 $X_t=tX_1+(1-t)X_0$，回归速度场
$$\min_v\ \mathbb{E}\big[\|(X_1-X_0)-v(X_t,t)\|^2\big]$$
——与 [Flow Matching](../2210.02747_flow_matching/) 的 OT 路径版本、Stochastic Interpolants 同期等价（三家独立提出）。
2. **矫正定理**：由学到的流诱导的新耦合 $(Z_0,Z_1)$（从 $X_0$ 出发解 ODE 到 $Z_1$）满足：边际不变；对所有凸代价 $c$，$\mathbb{E}[c(Z_1-Z_0)]\le\mathbb{E}[c(X_1-X_0)]$（传输代价不增）；且新耦合是确定性的。直觉：ODE 轨迹不能交叉，学到的流把交叉的直线段「重连」成不交叉的，代价只会降。
3. **Reflow**：用 $(Z_0,Z_1)$ 重新训练 → 更直的流；迭代 k 次得 k-rectified flow，路径直度单调改善，可用极粗步长（甚至一步 Euler）采样。代价：每轮 reflow 引入拟合误差，实际 2-3 轮。
4. 同一框架覆盖生成（$\pi_0$ 高斯）与域迁移（两端都是数据），无需配对。

## 实验与证据

- CIFAR-10：1-rectified flow 多步质量与 SOTA 相当；2-rectified flow 单步 Euler 即得可用样本（FID 显著优于其他一步方法），蒸馏后更好。
- 图像翻译（猫↔狗等无配对域迁移）与域适应：直路径带来的少步优势同样成立。
- 评价：理论（代价不增 + 边际保持）干净；reflow 的误差累积与「直度-保真」权衡在论文里主要靠实验体现。

## 在谱系中的位置

- 平行：[Flow Matching](../2210.02747_flow_matching/)、[OT-CFM](../2302.00482_ot_cfm/)（用 minibatch OT 一次性拉直 vs reflow 迭代拉直）。
- 下游：[SB Flow](../2409.09347_sb_flow/) 的 α-IMF 与 reflow 结构相似但收敛到 SB 而非直化耦合；[RSBM](../2604.05673_rsbm/) 的「桥矫正」直接借用 rectification 的名字与动机；[ReinFlow](../2505.22094_reinflow/) 以 Rectified Flow 策略为微调对象；Consistency/MeanFlow 是一步化的后继路线。

## 与 SB×RL 的关联

Rectified Flow 与 SB 的关系是「同一根旋钮的两端」：reflow 把耦合推向确定性 OT（$\epsilon\to0$ 极限），SB 保留熵正则（$\epsilon>0$）。矫正定理告诉我们直化只降传输代价、不保多模态——reflow 后耦合是确定性的，起点到终点一一对应，多样性全靠起点噪声。这正是 SB 在 few-step 区间的立论基础：RSBM 的 $\epsilon$ 谱系本质是「部分矫正」，在直度与覆盖之间取中间点。对 RL：reflow 的「自采样-重训」循环与 policy iteration 同构，[SB Flow](../2409.09347_sb_flow/) 解读里提到的「加权端点采样」在 reflow 框架下同样可做——这是一个尚未有人系统研究的方向。

## 局限与批判

- reflow 每轮都要用当前模型生成整套端点对，训练成本随轮数线性增长，且拟合误差累积限制轮数。
- 直化是耦合层面的，模型容量不足时「直」与「准」冲突（一步样本质量仍明显低于多步）。
- 理论只保证代价不增，不保证收敛到 OT（一般不收敛到 OT）。
