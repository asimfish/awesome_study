# Mean Flows for One-step Generative Modeling

> Geng, Deng, Bai, Kolter, He (CMU & MIT), arXiv 2025。[arXiv:2505.13447](https://arxiv.org/abs/2505.13447)

## 一句话

引入「平均速度场」及其与瞬时速度的恒等式，让一步生成不再依赖蒸馏或课程训练，从零训练在 ImageNet 256×256 上做到 1-NFE FID 3.43——原生一步生成的数学基础。

## 问题与动机

Flow Matching 学的是瞬时速度 $v(z_t,t)$，生成必须沿 ODE 多步积分；一步生成此前靠蒸馏（需要教师模型）或 consistency 训练（需要课程与 EMA 技巧，训练脆）。MeanFlow 的问题：有没有一个「天生就是一步」的学习对象？答案：位移本身——平均速度。

## 方法核心

定义 $[r,t]$ 区间的平均速度：

$$
u(z_t, r, t) \triangleq \frac{1}{t-r}\int_r^t v(z_\tau, \tau)\,d\tau
$$

- $u$ 是由 $v$ 诱导的真实场，不依赖网络；$r\to t$ 时退化为瞬时速度。
- 对定义式两边关于 $t$ 求导，得 **MeanFlow 恒等式**：

$$
u(z_t, r, t) = v(z_t, t) - (t-r)\,\frac{d}{dt}u(z_t, r, t)
$$

其中全导数 $\frac{d}{dt}u = \partial_t u + v\,\partial_z u$ 可以用一次 JVP（Jacobian-vector product）计算。训练：把恒等式右侧（用条件速度 $v = x_1 - x_0$ 与网络自身的 JVP 拼出）当作回归目标，损失是标准 L2。不需要教师、不需要蒸馏、不需要两阶段。

- 一步采样：$z_0 = z_1 - u_\theta(z_1, 0, 1)$，直接从噪声跳到数据。
- 天然满足区间可加一致性 $(t-r)u(z_t,r,t) = (s-r)u(z_s,r,s) + (t-s)u(z_t,s,t)$——consistency model 用 loss 逼近的性质，这里是定义的推论。
- CFG 被吸收进场的定义（对带引导的速度场求平均），推理时零额外开销。

## 实验与证据

- ImageNet 256×256 从零训练：1-NFE FID 3.43，比此前最好的一步扩散/流模型（iCT、Shortcut 等）大幅领先（论文图 1 显示相对最强基线降低约 50%~70%）。
- 2-NFE 进一步降到 2.20 附近，逼近多步教师的水平。
- 消融：JVP 目标的 stop-gradient 处理、$(r,t)$ 采样分布是训练稳定的关键。

## 在谱系中的位置

- 上游：[Flow Matching](../2210.02747_flow_matching/)（瞬时速度语言）、Consistency Models（一致性约束思想）。
- 下游（本仓库内）：[MP1](../2507.10543_mp1/) 首先把它搬进机器人操纵；[DMPO](../2601.20701_dmpo/) 加上 dispersive 正则与 PPO 微调；[OFP](../2603.12480_ofp/) 给出免教师自蒸馏的替代路线；[DBPO](../2604.03540_dbpo/) 是 drift 固定点视角的原生一步竞品。

## 与 SB×RL 的关联

MeanFlow 改变了 SB×RL 的竞争格局：此前「SB 有理论、一步靠蒸馏」的说法失效——免蒸馏 1-NFE 已被平均速度场占领。SB 剩余的差异化只在多模态覆盖与耦合结构（熵正则 $\epsilon$ 旋钮），不在步数。同时它也是机会：MeanFlow 恒等式对 bridge（两端任意分布）的推广——「平均漂移场 + SB 边界」——2026-09 尚无文献占位，是 one-step SB policy 这个空格的技术入口。对 RL：一步策略的 $\log\pi$ 虽然仍不可直接算（前向是隐式 pushforward），但单步结构让 DPPO 式逐步分解不再必要，advantage-weighted 或 GRPO 外壳可以直接套。

## 局限与批判

- JVP 使每步训练多一次前向的代价（约 1.5-2 倍计算），大模型上不可忽略。
- 恒等式成立依赖速度场光滑性，理论上对间断分布（低维流形数据）的行为没有分析。
- 只验证了图像；动作分布（多模态、低维、强条件）上的表现要看 MP1/DMPO 的检验。
- 一步生成的多模态覆盖（mode coverage）论文没有专门评测，FID 掩盖模式塌缩的老问题在一步场景更严重。
