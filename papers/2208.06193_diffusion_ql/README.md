# Diffusion Policies as an Expressive Policy Class for Offline Reinforcement Learning

> Wang, Hunt, Zhou, ICLR 2023。[arXiv:2208.06193](https://arxiv.org/abs/2208.06193)

## 一句话

用「扩散 BC loss 当行为正则 + Q 值最大化」两项相加训练扩散策略，确立了生成式策略做 offline RL 的 Q+BC 范式，D4RL 全线刷新。

## 问题与动机

Offline RL 的核心矛盾：策略要贴住行为分布（防外推错误）又要往高 Q 区域偏。此前的策略正则（TD3+BC 的 MSE、BEAR 的 MMD）都隐含单模态假设——行为数据本身多模态时，把策略拉向「分布均值」反而拉出分布外。解法：让策略类本身有多模态表达力，正则项自然变成「学得像整个分布」而不是「像均值」。

## 方法核心

策略是一个以状态为条件的小型 DDPM（去噪 5 步左右），训练目标两项相加：

$$
\mathcal{L} = \mathcal{L}_{\text{BC-diffusion}}(\theta) - \alpha\cdot\mathbb{E}_{s\sim\mathcal{D},\,a^0\sim\pi_\theta}\big[Q_\phi(s, a^0)\big]
$$

- 第一项：标准的条件噪声预测 loss——它就是行为克隆，天然覆盖多模态行为分布；
- 第二项：把去噪链末端采出的动作 $a^0$ 喂给 critic，Q 值的梯度**穿过整条去噪链**反传（reparameterized 采样可导）；
- $\alpha$ 按 Q 值尺度归一化，平衡贴数据与提性能；critic 用标准 double Q-learning 训练。

概念要点：BC 项是「支撑集约束」，Q 项是「支撑集内寻优」——扩散策略让这两件事第一次在多模态分布上同时成立。

## 实验与证据

- D4RL 全家桶（Gym locomotion、AntMaze、Adroit、Kitchen）：绝大多数任务超过 CQL/IQL/TD3+BC，AntMaze 提升尤其大（多模态+拼接场景）。
- 2D bandit 多模态实验：直观展示 TD3+BC/CQL 的策略塌到均值（分布外），扩散策略完整覆盖行为模式再由 Q 挑最优模式。
- 消融：去掉 Q 项退化为扩散 BC，去掉扩散（换 MLP）退化为 TD3+BC，两个方向都显著掉分——两项确实互补。

## 在谱系中的位置

- 上游：[DDPM](../2006.11239_ddpm/)、TD3+BC。
- 平行/下游：IDQL（критик换 IQL、推理期重采样）、EDP、QGPO、SRPO；FQL（flow 版）；[Diffusion Policy](../2303.04137_diffusion_policy/)（纯 BC 侧同期工作）；online 侧接力是 [DPPO](../2409.00588_dppo/)。

## 与 SB×RL 的关联

Diffusion-QL 展示了绕开 log π 的第二条路（第一条是 [AWR](../1910.00177_awr/) 的加权 BC）：不算似然，直接让 Q 的梯度穿过采样过程。这条「pathwise 梯度」路线对 SB 策略同样可行——bridge 采样链同样 reparameterized 可导，「bridge matching BC + Q 穿透」是 SB 版 Diffusion-QL 的直接构造，目前无人занял。它也给 06 类立了参照系：任何 SB offline 策略方法必须回答「比 Q+扩散BC 这个朴素组合好在哪」。

## 局限与批判

- Q 梯度穿过多步去噪链，梯度方差大、显存贵，去噪步数被迫压到 5 步——表达力与可训性打架。
- 每次策略评估要跑完整去噪，训练与推理都慢（后续 EDP/IDQL 都在修这个）。
- $\alpha$ 的尺度归一化跨任务仍要调。
- 论文对「为什么 AntMaze 提升最大」的解释停留在直觉层面，多模态收益缺少量化指标（这个空缺到 2026 年仍在——mode coverage 评测是整个领域的短板）。
