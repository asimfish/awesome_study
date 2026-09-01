# GSB-MDPO: Path-Space Mirror Descent for On-Policy RL under the Generalized Schrödinger Bridge

> Gong, Wang, Chen, Ding, Zhou, Fu (复旦 & 国防科大 & 上科大), arXiv 2026-03 (v2 2026-05)。[arXiv:2603.21621](https://arxiv.org/abs/2603.21621)

## 一句话

把 MDPO 的 KL 邻近项从动作分布搬到生成路径测度：path-KL 上界终端动作 KL 且经 Girsanov 化为 drift 的 MSE（可算），生成式策略第一次拿到有邻近保证的 on-policy 更新——path-space RL 的 mirror descent 支柱。

## 问题与动机

on-policy 邻近更新（TRPO/PPO/MDPO）的稳定性全部建立在动作似然可算之上，生成式策略的终端动作密度不可算——这是结构性错配。DPPO 的答案是把去噪链拆成 MDP 逐步算高斯似然，代价是 credit 均摊与 horizon 膨胀。GSB-MDPO 的答案相反：不拆，把邻近项定义在整条生成路径的测度上，一次算清。

## 方法核心

推导链条（从目标到可训练 loss 的每一步）：

1. **对象升维**：策略视为条件路径测度 $\mathbb{P}_\theta(\tau|s)$，$\tau = a^{(0:N)}$ 是生成链，执行动作是终端 $a^{(N)}$。优化问题写成 GSB 形式的 mirror descent：

$$
\theta_{k+1} = \arg\max_\theta\ \mathbb{E}_{s\sim d_k}\Big[\mathbb{E}_{\mathbb{P}_\theta}[A_k(s, a^{(N)})] - \tfrac{1}{\alpha}\,\mathrm{KL}\big(\mathbb{P}_\theta(\cdot|s)\,\|\,\mathbb{P}_{\theta_k}(\cdot|s)\big)\Big]
$$

回报项作用在终端动作，邻近项作用在全路径。
2. **Proposition 1（合法性）**：$\mathrm{KL}(\mathbb{P}\|\mathbb{Q}) \ge \mathrm{KL}(\pi_P\|\pi_Q)$（KL 链式法则/数据处理不等式）——压路径 KL 就压住了执行动作分布的漂移，邻近更新的语义保住，终端似然一次都不用算。
3. **Girsanov（可算性）**：同先验同扩散系数的两个 SDE 生成器，路径 KL 恰为漂移差的加权 MSE：

$$
\mathrm{KL}(\mathbb{P}_\theta\,\|\,\mathbb{P}_k) = \mathbb{E}_{\tau\sim\mathbb{P}_\theta}\Big[\int_0^1 \frac{\|f_\theta - f_k\|^2}{2\sigma_t^2}\,dt\Big]
$$

离散化后就是逐步 drift-MSE——「MSE 式正则不是拍脑袋惩罚，是路径 KL 的严格离散形式」是本文最干净的一句话。
4. **实用目标**：优势项与路径 KL 都经重要性采样改写到旧策略路径上（复用 rollout），路径比率是逐步似然比的乘积、方差大——实现上对逐步与累积 log-ratio 做裁剪（注意：这是对重要性权重的数值稳定化，不是 PPO 的裁剪代理目标；被裁剪时 drift 正则的梯度仍在）。

## 实验与证据

- 14 个连续控制任务（MuJoCo Playground 8 + Gym-MuJoCo 6，后者 40M 步）：对 Gaussian PPO、DPPO、FPO、GenPO，GSB-MDPO 整体领先或并列第一，高维任务（Ant-v5、Humanoid-v5）与 Finger 系列增益最明显；每套基准内单一超参配置跑全部任务（无逐任务调参），5 seeds。
- 实验设计评价：基线选得对（覆盖高斯、逐步分解、flow on-policy 三类），「单一配置跑全部」加分；但消融只有 2 seeds、无操纵/视觉/真机任务，与 FLAC 互不对比——path-space 两条路线（mirror descent vs max-ent）的内部优劣仍是悬案。

## 在谱系中的位置

- 上游：[MDPO](../2005.09814_mdpo/)（动作空间原型）、[GSBM](../2310.02233_gsbm/)（GSB 语言）、[DSBM](../2303.16852_dsbm/)（path-space 投影词汇）。
- 平行：[FLAC](../2602.12829_flac/)——同一个 path-KL 上界引理，一个用于邻近项（on-policy），一个用于熵正则（off-policy max-ent）。
- 对照：[DPPO](../2409.00588_dppo/)——分解 vs 整体的方法论对立面。

## 与 SB×RL 的关联（对我们选题的启示）

理论位已被占：「path-KL 作 proximal 项」的原创性主张不再可用。留下的空白：(1) 全部实验是 locomotion，操纵/VLA 动作头/真机是空的——把 GSB-MDPO 内核装进 few-step 操纵策略（RSBM/DMPO 的任务面）等于一次占两格；(2) 路径比率的方差问题只用裁剪硬压，理论上更优雅的解（如把重要性采样也搬到路径空间做桥式插值）没人碰；(3) GSB 的 G（路径费用）在本文只是形式存在，任务费用（碰撞、平滑度）真正塞进 $V_t$ 的具身实验为零；(4) 与一步化的关系：$N=1$ 时路径 KL 退化为单步高斯 KL，框架平凡化——一步时代 path-space 邻近项还剩什么价值，是需要正面回答的问题。

## 局限与批判

- 上界松紧同样未量化：路径 KL 可能远大于终端 KL，邻近约束过紧会牺牲改进速度——步长 $\alpha$ 的选择实质上在赌这个松紧。
- 路径重要性比率的高方差是结构性的（逐步比率连乘），裁剪治标；长生成链（$N$ 大）下退化风险论文自己承认。
- 只有 locomotion 仿真；对多模态表达力的收益（生成式策略的立身之本）没有任何直接评测。
- v2 从 GSB-PPO 改名而来，与 PPO 版的差异（clip→显式 KL）的消融没有保留，方法演化的证据链断了一节。
