# FLAC: Maximum Entropy RL via Kinetic Energy Regularized Bridge Matching

> Lv, Li, Luo, Sun, Ma (ByteDance Seed & 清华), arXiv 2026-02。[arXiv:2602.12829](https://arxiv.org/abs/2602.12829)

## 一句话

把 max-ent RL 重写成对高熵参考过程的广义 Schrödinger Bridge：用路径动能替代策略熵（动能上界终端 KL），生成式策略第一次拿到免似然的 SAC——SB×RL「路径空间换似然」路线的开山之作之一。

## 问题与动机

SAC 的最大熵框架要算 $\log\pi(a|s)$，生成式策略（流/扩散 actor）的动作是 SDE 终端边际，似然要么解 instantaneous change of variables 要么对全路径边际化——在线训练中既贵又数值不稳。此前的绕法都在动作层打转（展开去噪链、latent RL）。FLAC 换层：熵正则的本体如果不是动作分布而是生成路径，问题还存在吗？

## 方法核心

推导链条完整走一遍：

1. **重写 max-ent**：$\max\ \mathbb{E}[r] + \alpha H(\pi)$ 等价于 $\min\ \mathrm{KL}(\pi\,\|\,\text{Unif})$ 约束下最大化回报——最大熵 = 贴住均匀参考分布。
2. **升维到路径空间**：策略是 state-conditioned SDE $dX_\tau = u_\theta(s,\tau,X_\tau)d\tau + \sigma dW_\tau$（$X_1$=动作）。把「贴住均匀分布」升级为「贴住高熵参考过程」，策略优化变成 GSB 问题：软终端势=Q 值，路径正则=对参考测度的 KL。
3. **Girsanov 变现**：参考取（尺度化）布朗运动时，路径 KL 恰好等于漂移场的动能：

$$
\mathrm{KL}(\mathbb{P}^\theta\,\|\,\mathbb{P}^{\text{ref}}) = \frac{1}{\sigma^2}\,\mathcal{E}(s),\qquad \mathcal{E}(s) = \mathbb{E}\Big[\int_0^1 \tfrac{1}{2}\|u_\theta(s,\tau,X_\tau)\|^2 d\tau\Big]
$$

4. **关键不等式**（data processing）：$\mathrm{KL}(\pi_\theta\,\|\,\mu_1^{\text{ref}}) \le \mathrm{KL}(\mathbb{P}^\theta\|\mathbb{P}^{\text{ref}}) = \mathcal{E}/\sigma^2$——压动能就压住了终端动作分布对高熵参考的偏离，**熵正则不需要似然**。$\sigma\to0$ 极限下动能退化为 Benamou-Brenier 的 W2 传输费用，确定性流也覆盖。
5. **算法**：能量正则的 policy iteration（软策略评估 + 能量约束的策略改进），实用版是带能量预算 $\mathcal{E}_{\text{tgt}}$ 的约束优化，拉格朗日乘子 $\alpha$ 自动调节（结构与 SAC 的自动温度完全对位）：$\min_{\alpha\ge0}\max_\pi\ \mathbb{E}[Q - \alpha(\hat{\mathcal{E}} - \mathcal{E}_{\text{tgt}})]$。off-policy actor-critic 实现。

## 实验与证据

- DMControl + HumanoidBench（Unitree H1）：一致打平或超过强 model-free 基线（TD7、SAC、DIME、SAC-Flow、FlowRL），DMC Dog（状态 223 维/动作 38 维）与接触密集的 H1 任务上稳健；渐近回报接近 model-based 的 TD-MPC2（免世界模型与在线规划）。
- 效率：N=2 的 NFE 即可（生成链极短），DIME 还借了 cross Q-learning 而 FLAC 没用增强。
- 消融：自动拉格朗日调节优于固定正则系数；能量预算是主要超参但敏感性可控。
- 实验设计评价：基线覆盖三类（确定性/高斯/生成式）算充分；但全部是仿真 locomotion/humanoid 控制，无操纵任务、无真机、无视觉输入——「表达力优势来自多模态」的立论在这些单模态倾向的任务上其实没被直接检验。

## 在谱系中的位置

- 上游：[SAC](../1801.01290_sac/)（被重写的对象）、[GSBM](../2310.02233_gsbm/)（GSB 框架）、[Léonard](../1308.0215_leonard_survey/)（Girsanov/路径 KL 的数学）。
- 平行：[GSB-MDPO](../2603.21621_gsb_mdpo/)——同一个「path-KL 上界终端 KL」引理的 mirror-descent 用法；两篇是 path-space RL 坐实的双证据。
- 对照：DPPO/DMPO 的展开分解路线——FLAC 不展开、不分解，整条路径一次正则。

## 与 SB×RL 的关联（对我们选题的启示）

这是预判成真的论文：max-ent RL 与 SB 的形式同构（energy-based 最优策略 vs 指数重加权桥）被做成了可用算法。它占掉了「path-space 熵正则」的理论位，留下的空白很具体：(1) 任务面——只做了 locomotion，操纵/视觉/真机全空；(2) 参考过程设计——只用了布朗/均匀参考，informative reference（预训练 BC 策略的路径测度）会把 GSB 的 reference 自由度真正用起来，这是 FLAC 框架内的直接增量；(3) 与一步化的组合——FLAC 的 N=2 已经很短，但动能正则在 1-NFE 极限下如何退化（平均速度场的动能）没人分析；(4) mode coverage——动能压小会不会把多模态压塌，论文没测，这恰是 SB 卖点的试金石。

## 局限与批判

- 上界的松紧没有量化：动能是终端 KL 的上界，但可能松到过度正则——什么时候上界紧、什么时候浪费探索预算，没有分析。
- 参考过程固定为高熵各向同性过程，「均匀参考=最大熵」在有界动作空间外并不 well-defined（uniform over 无界域不存在），数学细节靠动作空间紧致性兜底。
- 能量预算 $\mathcal{E}_{\text{tgt}}$ 取代了 SAC 的目标熵，跨任务迁移性未知。
- 无操纵/真机/视觉验证；与 GSB-MDPO 互不对比（两篇平行成文），path-space 路线内部的优劣未决。
