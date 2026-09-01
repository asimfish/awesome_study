# Generalized Schrödinger Bridge Matching

> Liu, Lipman, Nickel, Karrer, Theodorou, Chen (GaTech & Meta AI), ICLR 2024。[arXiv:2310.02233](https://arxiv.org/abs/2310.02233)

## 一句话

把 SB 推广到带任意路径费用的广义形式（GSB），并给出一个训练中始终满足两端边际的匹配算法——SB 通往最优控制与 RL 的理论接口。

## 问题与动机

标准 SB 只关心两端边际与对参考过程的偏离，路径中间发生什么不管。现实任务偏偏关心中间：人群导航要避开障碍、分子插值要停留在低能量流形、机器人轨迹要平滑。带状态费用的广义 SB（GSB）此前只有 DeepGSB 等基于对偶的解法——训练中边际约束靠惩罚项软保证，高维直接崩。GSBM 要一个「边际永远成立、费用逐步下降」的算法。

## 方法核心

GSB 问题（在 SB 的 KL 目标上加路径费用）：

$$
\min_{\mathbb{P}}\ \mathrm{KL}(\mathbb{P}\,\|\,\mathbb{Q}) + \int_0^T \mathbb{E}_{\mathbb{P}}\big[V_t(x_t)\big]\,dt\qquad \text{s.t. } \mathbb{P}_0=\mu,\ \mathbb{P}_T=\nu
$$

- $V_t$：状态费用（障碍势、拥挤度、几何流形距离等）。$V\equiv0$ 退化为标准 SB。
- 算法是交替投影（匹配版的坐标下降）：
  1. **耦合固定，优化条件路径（CondSOC）**：给定端点对 $(x_0,x_T)$，求两点间最优受控桥 $\min \int(\frac{1}{2}\|u\|^2 + V)\,dt$——低维两点问题，用高斯路径近似或 path integral 数值解；
  2. **路径固定，匹配边际过程（bridge matching）**：把条件桥的混合投影回 Markov 类，回归 drift。
- 关键性质：两步都不动端点耦合的边际——训练全程 $\mathbb{P}_0=\mu,\ \mathbb{P}_T=\nu$ 严格成立（与 DeepGSB 的软约束本质区别），收敛性有局部保证。

## 实验与证据

- 人群导航（障碍势场）：轨迹绕障且到达目标分布，DeepGSB 在同设置下边际漂移明显。
- 意见极化动力学、LiDAR 流形插值：展示 $V_t$ 的表达自由度（费用可以是数据驱动的几何量）。
- 图像翻译（unpaired）：费用取感知距离时质量优于纯 SB 基线——路径费用当正则用。

## 在谱系中的位置

- 上游：[Léonard](../1308.0215_leonard_survey/)（SB 理论）、[DSBM](../2303.16852_dsbm/)（匹配语言与 IMF 骨架）、DeepGSB。
- 下游（本仓库内）：[FLAC](../2602.12829_flac/) 把 max-ent RL 写成 GSB（$V$ 与 $\mathcal{G}$ 来自 Q 函数）；[GSB-MDPO](../2603.21621_gsb_mdpo/) 在 GSB 框架内做 path-space mirror descent。06 类的「G」全部指这里。

## 与 SB×RL 的关联

GSBM 是 SB 与 RL 之间的正式转接头：把 RL 的奖励塞进 $V_t$（或终端势 $\mathcal{G}$），策略优化问题在形式上就是一个 GSB。两个方向的价值：(1) 概念上，Feynman-Kac 告诉我们「加费用 = 对参考测度指数重加权」，奖励塑形获得测度论语义；(2) 算法上，CondSOC+matching 的交替结构就是「规划（两点最优控制）+ 蒸馏（回归到策略）」，与 RL 里 planner-distillation 范式同构。缺口也清楚：GSBM 的 $V_t$ 是给定的静态函数，RL 的奖励要靠 critic 在线估计且随策略变化——把 GSBM 的收敛性搬到「费用本身在动」的设定，是 06 类前沿仍未解决的理论问题。

## 局限与批判

- CondSOC 的高斯路径近似在费用强非凸（窄缝障碍）时不准，path integral 版本又贵——中间步的质量-成本权衡没有好答案。
- 局部收敛保证依赖每步近似解足够好，实际训练对初始化敏感。
- 实验维度仍然有限（图像翻译是最高维场景），没有序列决策/控制回路的验证——它自己不做 RL。
