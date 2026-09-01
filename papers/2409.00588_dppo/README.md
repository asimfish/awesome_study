# Diffusion Policy Policy Optimization

> Ren, Lidard, Ankile, Simeonov, Agrawal, Majumdar, Burchfiel, Dai, Simchowitz (Princeton & MIT & TRI), ICLR 2025。[arXiv:2409.00588](https://arxiv.org/abs/2409.00588)

## 一句话

把去噪链展开成嵌在环境 MDP 里的内层 MDP，每个去噪步的高斯似然可算，PPO 直接套上去——预训练扩散策略在线 RL 微调的方法论标杆。

## 问题与动机

BC 预训练的扩散策略性能锁死在示范上限，要突破必须在线 RL。但 policy gradient 需要 $\log\pi(a|s)$，扩散策略只有 ELBO——此前社区的共识是 PG 对扩散策略低效（Q 类方法 DIPO/QSM 才是正路）。DPPO 用一组精细的设计决策推翻了这个共识。

## 方法核心

**两层 MDP（Diffusion MDP）**：把 $K$ 步去噪链的每一步当作内层 MDP 的一个动作。内层状态是（环境状态 $s$、去噪步 $k$、当前噪声动作 $a^k$），内层动作是下一个去噪结果 $a^{k-1}$。每个去噪步是条件高斯：

$$
\pi_\theta(a^{k-1}\mid s, a^k) = \mathcal{N}\big(\mu_\theta(s, a^k, k),\ \sigma_k^2 I\big)
$$

- 高斯的 $\log\pi$ 有闭式——log π 障碍被「分解到步」瓦解。环境奖励只在去噪链末端（真实执行）出现，通过内层 $\gamma=1$ 的折扣传播回每一步。
- 在这个扩展 MDP 上跑标准 PPO（clip + GAE）。
- 关键 best practices（消融验证）：只微调去噪链的最后若干步（早期步作为「冻结先验」提供结构化探索）、微调 DDIM 采样器、两层 advantage 的设计、视觉任务只调头部。
- 结构红利：去噪链前段像温度逐降的探索噪声——探索天然「在流形上」，比高斯扰动的 off-manifold 探索样本效率高。

## 实验与证据

- OpenAI Gym + RoboMimic + Furniture-Bench：对其他扩散 RL 方法（DIPO、DQL、IDQL、QSM、DRWR/DAWR）和其他参数化的 PG 微调（高斯、GMM），DPPO 整体最强，长 horizon 任务优势最大。
- 像素观测任务照常工作（此前扩散 RL 方法多数只做状态输入）。
- 真机 zero-shot：Furniture-Bench 仿真训练直接部署 Franka 长程多阶段装配，鲁棒性显著优于 BC——「RL 微调提升的不只是成功率，是抗扰动」。

## 在谱系中的位置

- 上游：[Diffusion Policy](../2303.04137_diffusion_policy/)（被微调对象）、[PPO](../1707.06347_ppo/)（外层算法）、DDPO（文生图 RLHF 的同构做法）。
- 下游（本仓库内）：Flow-GRPO/ReinFlow 是 flow 版；[DMPO](../2601.20701_dmpo/) 在一步策略上重演此范式（去噪链长度=1 时两层 MDP 塌缩）；[GSB-MDPO](../2603.21621_gsb_mdpo/) 是它的 path-space 对位竞品。

## 与 SB×RL 的关联

DPPO 是 SB×RL 必须正面对比的基线：它证明「逐步分解」足以解决扩散策略的 log π 问题，代价是 credit 被均匀摊到每个去噪步、内层 horizon 变长 $K$ 倍（样本效率与方差的税）。path-space 路线（GSB-MDPO/FLAC）的主张恰好相反：不分解，把 KL/熵正则整体搬到路径测度上一次算清。谁对？一步化的出现让问题部分消解（$K=1$ 时两条路线合流），但多步策略仍在（规划、长链生成），这场方法论之争没有完结。

## 局限与批判

- 内层 MDP 让有效 horizon 乘以去噪步数，on-policy 样本量需求大，真机直接在线训练仍不现实（论文是 sim 训练后部署）。
- 「只调后几步」是经验规则，何时失效（分布大迁移时先验反而有害）没有理论刻画。
- 与 Q 类方法的对比在各自超参调优深度上不完全对称，部分基线数字被后续论文质疑偏低。
- 微调后策略的多模态保持度没有评测——RL 微调塌模式是已知现象，恰是 SB 路线主打的差异点。
