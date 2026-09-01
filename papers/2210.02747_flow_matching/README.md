# Flow Matching for Generative Modeling

> Lipman, Chen, Ben-Hamu, Nickel, Le (Meta AI), ICLR 2023。[arXiv:2210.02747](https://arxiv.org/abs/2210.02747)

## 一句话

不学 score、直接回归把噪声运到数据的速度场，配上条件化技巧让这个回归可解，训练比扩散更稳、路径比扩散更直——生成建模从「去噪」语言切换到「传输」语言的分水岭。

## 问题与动机

连续正规化流（CNF）表达力强但训练要反复解 ODE，慢到不可用；扩散模型好训但路径弯（先绕到高斯再回来）、采样步数多。Flow Matching 要的是：CNF 的确定性传输结构 + 扩散式的免仿真回归训练。

## 方法核心

目标是学速度场 $v_\theta$ 使其生成的 ODE 流把 $p_0$（噪声）运到 $p_1$（数据）。直接回归边际速度场 $u_t(x)$ 不可行（没有闭式），核心技巧是条件化：

$$
\mathcal{L}_{\text{CFM}} = \mathbb{E}_{t,\,x_1,\,x\sim p_t(\cdot|x_1)}\big[\|v_\theta(x,t) - u_t(x|x_1)\|^2\big]
$$

- $p_t(\cdot|x_1)$：以单个数据点 $x_1$ 为条件的概率路径（取高斯）；$u_t(x|x_1)$：它对应的条件速度场，有闭式。
- 定理：CFM 与（不可算的）FM 目标梯度相同——回归条件速度场就等于回归边际速度场。
- 路径的选择是自由度：取扩散路径可复现 score-based 模型；取最优传输位移路径（optimal transport displacement）$x_t = (1-t)x_0 + t\,x_1$，直线插值，速度目标就是 $x_1 - x_0$。直路径是后续一切 few-step 工作的几何基础。

## 实验与证据

- ImageNet（32/64/128）：OT 路径的 FM 在 FID 与 NLL 上稳定优于同规模 score-based 基线，且训练收敛更快。
- 采样效率：OT 路径下用低阶 ODE 求解器、更少步数即可达到扩散模型的质量——路径直的直接红利。
- 似然：CNF 的精确似然能力保留。

## 在谱系中的位置

- 上游：CNF（Chen 2018）、[Score-SDE](../2011.13456_score_sde/) 的 PF-ODE。
- 平行：Rectified Flow、Stochastic Interpolants（同期三家给出等价框架）。
- 下游（本仓库内）：[OT-CFM](../2302.00482_ot_cfm/) 把独立采样的端点换成 OT coupling；[MeanFlow](../2505.13447_meanflow/) 回归区间平均速度实现原生一步；π0 等 VLA 用 FM 做动作头；[SF2M](../2307.03672_sf2m/) 证明 FM + score matching 可以拼出 SB。

## 与 SB×RL 的关联

FM 与 SB 的关系：FM 学的是确定性传输，SB 是熵正则的随机传输，$\epsilon\to0$ 时 SB 退化为动态 OT——FM 的 OT 路径正是这个极限的单样本近似。桥匹配（bridge matching）方法在训练形式上就是「带边界的 CFM」。对 RL：FM 策略的 $\log\pi$ 需要沿 ODE 积分散度项，同样不可承受；但 FM 的确定性结构让「一步化」（MeanFlow/Rectified Flow 路线）比扩散容易得多，一步化之后 RL 微调回到普通策略优化——这是 05 类论文的主线逻辑。

## 局限与批判

- 条件路径以单点 $x_1$ 为锚，端点独立采样（$x_0\perp x_1$），边际路径仍然不是真正的 OT——「直」只在条件层面，交叉路径互相打架，这正是 OT-CFM 要修的。
- 高斯路径假设限制了对非欧数据（流形、离散结构）的直接适用性。
- 论文实验集中在图像，似然与 FID 的权衡讨论较浅。
