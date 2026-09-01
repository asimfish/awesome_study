# A Survey of the Schrödinger Problem and Some of Its Connections with Optimal Transport

> Léonard, Discrete and Continuous Dynamical Systems 2014。[arXiv:1308.0215](https://arxiv.org/abs/1308.0215)

## 一句话

现代 SB 文献的数学正典：把 Schrödinger 1931 年的热力学问题严格表述为路径测度上的相对熵最小化，并证明它在小噪声极限下 Γ-收敛到最优传输。

## 问题与动机

Schrödinger 的原始问题：观测到大量独立布朗粒子在 $t=0$ 时刻呈分布 $\mu$、$t=T$ 时刻呈分布 $\nu$（与热扩散预期不符的罕见事件），问最可能的中间演化是什么。Léonard 这篇综述的任务：把散落在概率论、大偏差、最优传输里的相关结果整理成一个自洽的数学框架，说清 SB 与 OT 的确切关系。

## 方法核心

**动态形式**。在路径空间 $\Omega = C([0,T];\mathbb{R}^d)$ 上：

$$
\mathbb{P}^\star = \arg\min\big\{\mathrm{KL}(\mathbb{P}\,\|\,\mathbb{Q})\ :\ \mathbb{P}_0 = \mu,\ \mathbb{P}_T = \nu\big\}
$$

- $\mathbb{Q}$：参考路径测度（布朗运动）。大偏差理论（Sanov 定理）解释「最可能的演化」为什么恰好是 KL 最小化。
- **静态-动态等价**：KL 沿端点分解，$\mathrm{KL}(\mathbb{P}\|\mathbb{Q}) = \mathrm{KL}(\pi\|\pi^{\mathbb{Q}}) + \mathbb{E}_\pi[\mathrm{KL}(\mathbb{P}^{x_0,x_T}\|\mathbb{Q}^{x_0,x_T})]$。第二项取零当且仅当中间路径就是参考桥——所以只需优化端点耦合 $\pi$（静态熵正则 OT），中间用 $\mathbb{Q}$ 的桥填充。
- **Schrödinger 系统（f·g 分解）**：最优耦合密度形如 $\frac{d\pi^\star}{d\pi^{\mathbb{Q}}}(x,y) = f(x)\,g(y)$，$f,g$ 由两个边际条件唯一确定（对应 Sinkhorn 迭代的不动点）。最优过程的 drift 由 $\nabla\log g_t$ 给出（Doob h-变换）。
- **Γ-收敛**：噪声 $\epsilon\to0$ 时，SB 问题收敛到 Monge-Kantorovich OT，动态版收敛到 Benamou-Brenier——SB 是 OT 的熵光滑化这一论断的严格出处。
- **解的结构**：SB 解是既 reciprocal（给定两端、中间与外部条件独立）又 Markov 的唯一路径测度——三十年后 DSBM 的 IMF 算法直接建立在这个刻画上。

## 实验与证据

理论综述，无实验。理论贡献清单：动态/静态形式的等价、存在唯一性条件、f·g 分解与 Schrödinger 系统、与大偏差的联系、$\epsilon\to0$ 的 Γ-收敛、reciprocal 类的刻画。

## 在谱系中的位置

- 上游：Schrödinger 1931/32 原始论文、Föllmer 的随机控制表述、Sinkhorn/IPF 数值传统。
- 下游（本仓库内）：[DSB](../2106.01357_dsb/) 把 IPF 神经化；[DSBM](../2303.16852_dsbm/) 用 reciprocal∩Markov 刻画设计 IMF；[SB Foundations](../2603.18992_sb_foundations/) 是它的 2026 教学化扩写；[GSBM](../2310.02233_gsbm/) 推广到带路径费用的 GSB。

## 与 SB×RL 的关联

三个直接可用的资产：(1) 静态-动态等价意味着 SB 策略的训练可以在「耦合设计」与「路径生成」两层分别做文章；(2) f·g 分解 + h-变换是「奖励塑形 = 改终端势函数」的数学原型（Feynman-Kac 重加权，GSBM/FLAC 的根）；(3) Γ-收敛给出 $\epsilon$ 旋钮的两端语义——$\epsilon\to0$ 得确定性直路径（利于少步），$\epsilon$ 大保多模态覆盖，few-step SB 策略的理论卖点就压在这个权衡上。

## 局限与批判

- 纯数学文本，测度论门槛高，无算法内容——读它是为了拿定义与定理，不是拿方法。
- 只覆盖布朗参考过程的经典设定；带状态费用（GSB）、非马尔可夫参考等现代扩展不在其中。
- 2014 年成文，与神经方法的所有连接都要读者自己搭。
