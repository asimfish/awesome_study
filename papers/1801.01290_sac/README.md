# Soft Actor-Critic: Off-Policy Maximum Entropy Deep Reinforcement Learning with a Stochastic Actor

> Haarnoja, Zhou, Abbeel, Levine (UC Berkeley), [ICML 2018](https://proceedings.mlr.press/v80/haarnoja18b.html)。[arXiv:1801.01290](https://arxiv.org/abs/1801.01290)

## 一句话

SAC 把最大熵策略改进写成可直接优化的随机 actor 损失，让经验回放与熵驱动探索同时工作，推进了复杂连续控制中样本效率与训练稳定性的折中。

## 问题与动机

连续控制的瓶颈既是交互昂贵，也是训练脆弱：on-policy 方法依赖当前策略数据，DDPG 能复用经验却容易受探索和价值误差影响，早期 soft Q-learning 又需要复杂的近似采样来表示能量模型。

SAC 要保留最大熵目标的探索收益，同时用显式、可求密度的随机策略简化优化；它学习当前策略的 soft Q，再改进 actor，价值估计与策略更新因此形成闭环。这里的熵进入长期价值递推，不只是给普通策略梯度附加一个鼓励随机性的损失项。

原文把 PPO 与 TRPO 并列描述为每次梯度更新都需新样本，但这一表述不能照搬：PPO 可以在同一批数据上做多轮更新，区别是它没有 SAC 式的长期经验回放。

## 方法核心

有限时域最大熵目标为

$$
J(\pi)=\sum_{t=0}^{T}\mathbb E_{(s_t,a_t)\sim\rho_\pi}
[r(s_t,a_t)+\alpha\mathcal H(\pi(\cdot|s_t))].
$$

$\rho_\pi$ 是策略诱导的状态—动作边缘分布，$\alpha>0$ 控制熵相对奖励的权重；连续动作下 $\mathcal H$ 是微分熵。原文后续公式把温度吸收到奖励缩放中，保留显式温度时，soft Bellman 递推写作

$$
Q^\pi(s,a)=r(s,a)+\gamma\mathbb E_{s'\sim p}[V^\pi(s')],\qquad
V^\pi(s)=\mathbb E_{a\sim\pi}[Q^\pi(s,a)-\alpha\log\pi(a|s)].
$$

$\gamma$ 是折扣因子，$p$ 是环境转移；下一状态的熵会经 $V$ 影响当前动作的价值。策略改进在受限策略族 $\Pi$ 内做反向 KL 投影：

$$
\pi_{\rm new}=\arg\min_{\pi'\in\Pi}
D_{\rm KL}\!\left(\pi'(\cdot|s)\middle\|
\frac{\exp(Q^{\pi_{\rm old}}(s,\cdot)/\alpha)}{Z(s)}\right).
$$

$Z(s)$ 归一化目标分布，与待更新的策略参数无关，因此无需计算它就能优化 actor；只有不受策略族限制时，投影才直接得到 Boltzmann 分布。论文的单调改进与收敛结论要求有限动作、精确评价及精确投影，并不覆盖神经网络训练。

实际算法从回放池取状态，重新从当前 actor 采样动作，最小化 $\mathbb E[\alpha\log\pi_\phi(a|s)-Q_\theta(s,a)]$，通过重参数化把 Q 的动作梯度传给 actor。实现采用 tanh 压缩的高斯，并用变量变换的雅可比修正对数密度。

本篇还训练独立的 $V$ 网络及其目标网络；两套 Q 独立拟合 Bellman 目标，更新 $V$ 与 actor 时取两者较小值。温度通过奖励尺度手调，自动温度调节属于后续的 [SAC Algorithms and Applications](https://arxiv.org/abs/1812.05905)，不能算成本篇贡献。

## 实验与证据

第 5 节比较 Hopper、Walker2d、HalfCheetah、Ant 及 Gym、rllab 两种 Humanoid，基线包括 DDPG、PPO、SQL 和同期 TD3；rllab Humanoid 的动作空间为 21 维。主图使用 5 个随机种子，阴影给出最小—最大回报，不是置信区间。

证据支持“简单任务与基线相当，困难任务的学习速度和最终回报更强”，不支持“所有任务全面超过 TD3”。原文报告 DDPG 在 Ant 与两种 Humanoid 上未取得进展；SAC 学得比 PPO 快，但没有给出统一的样本效率倍数。

随机策略与最大熵训练的联合消融显示，Humanoid 上不同种子的表现更稳定；它没有把随机性和熵目标的贡献完全拆开。第 4.2 节还明确说单 Q 也能学会困难任务，双 Q 的作用是加速，不能写成“缺一不可”。

第 5.2 节显示 reward scale 会改变探索强度，过小或过大都伤害学习；评估常用策略均值动作，曲线统计的是环境奖励，未包含训练目标中的熵。这些证据来自仿真连续控制，原文未报告真机实验。

## 在谱系中的位置

SAC 承接 soft Q-learning 的能量策略视角，把依赖近似采样的最优 Q 学习改成有显式 actor 的 soft policy iteration；双 Q 技巧在文中归于同期 TD3，最大熵框架也不是 SAC 首创。

与 [PPO](../1707.06347_ppo/) 相比，它把历史数据复用和 soft Bellman 递推放到中心；与 [AWR](../1910.00177_awr/) 的加权似然路径相比，它直接用当前 actor 样本与 Q 的动作梯度更新策略。对生成式控制，真正值得继承的是这一策略改进目标及其价值闭环。

## 与 SB×RL 的关联

可以做一个受控替换实验：保留 SAC 的回放、双 Q 和环境步预算，把高斯 actor 换成按状态生成动作的 SB 策略，并与去掉熵项的同结构策略对照；同时记录回报、动作覆盖和采样耗时，检验收益来自表达力还是探索正则。若用生成路径 KL 替代动作熵，要单独检查替代目标与原目标的差距，不能把两条学习曲线的差异全归于策略容量。

理论上应先核对参考过程、扩散系数和端点约束，再讨论路径正则与策略改进的对应关系：SAC 的 Boltzmann 动作目标没有自动指定 SB 所需的两端分布，环境轨迹时间也不同于动作生成时间。SAC 给出可比较的奖励—熵基准；SB 能否在可控成本下实现这个基准，需要由上述实验和目标核对共同判断。

## 局限与批判

- actor 损失要求可计算的动作对数密度，只有隐式采样器的生成策略不能直接接入，流模型能否接入则取决于密度计算成本。
- tanh 高斯限制了可表达的动作分布，反向 KL 投影可能舍弃有效模式，最大熵目标不等于实现了多模态覆盖。
- reward scale 与任务奖励单位耦合，稳定性收益仍建立在逐任务调节该参数之上。
- 有限动作下的精确策略迭代理论，不能保证带回放分布偏移和 Q 近似误差的深度 SAC 收敛。
