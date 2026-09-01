# Diffusion Policy: Visuomotor Policy Learning via Action Diffusion

> Chi, Feng, Du, Xu, Cousineau, Burchfiel, Song (Columbia & TRI & MIT), RSS 2023 / IJRR。[arXiv:2303.04137](https://arxiv.org/abs/2303.04137)

## 一句话

把机器人动作序列当成「图像」用条件扩散模型生成，一举解决模仿学习的多模态动作问题，在 12 个任务上平均提升 46.9%，成为机器人操纵策略的事实标准。

## 问题与动机

行为克隆的老大难：人类示范是多模态的（同一状态下多种合理动作——从左绕或从右绕），高斯 actor 会把模式平均成无效动作，离散化丢精度，EBM 训练不稳（IBC 的痛点）。扩散模型在图像上已证明能表达任意多模态分布——那动作分布为什么不行？

## 方法核心

策略即条件去噪过程。以观测 $O_t$ 为条件，对动作序列（action chunk）$A_t = a_{t:t+H}$ 做 DDPM 式去噪：

$$
A_t^{k-1} = \alpha\big(A_t^k - \gamma\,\epsilon_\theta(O_t,\ A_t^k,\ k)\big) + \mathcal{N}(0, \sigma^2 I)
$$

- $k$：去噪步；$\epsilon_\theta$：以观测为条件的噪声预测网络。梯度场视角：$\epsilon_\theta \propto -\nabla\log p(A_t|O_t)$，去噪就是在动作分布上做条件 Langevin 下降。
- 三个关键设计，缺一不可：
  1. **闭环动作序列**：预测 $H$ 步 chunk、执行前几步就重新规划（receding horizon）——时间一致性与反应性的折中；
  2. **视觉条件化**：观测只编码一次进条件，不参与去噪，推理省一个量级计算；
  3. **位置控制动作空间**：比速度控制对多模态与累积误差更稳。
- 骨干给了 CNN（FiLM 条件）与 Transformer 两版；推理用 DDIM 减步数。

## 实验与证据

- 4 个基准 12 个任务（RoboMimic、PushT、Multimodal Block Pushing、Franka Kitchen）：对 LSTM-GMM、IBC、BET 平均相对提升 46.9%，几乎每个任务都赢。
- PushT 多模态实验：明确展示高斯/EBM 基线塌缩到单模式而扩散策略保持双模式覆盖。
- 真机（UR5/Franka）：6 类操纵任务成功率大幅领先，验证不只是仿真产物。

## 在谱系中的位置

- 上游：[DDPM](../2006.11239_ddpm/)、IBC/EBM 策略、BET。
- 下游（本仓库内）：π0（FM 动作头）、RDT-1B 沿它规模化；[DPPO](../2409.00588_dppo/) 给它加 online RL；[Diffusion-QL](../2208.06193_diffusion_ql/) 是 offline 侧对应物；[MP1](../2507.10543_mp1/)/[DMPO](../2601.20701_dmpo/)/[DBPO](../2604.03540_dbpo/) 把它的多步推理压成一步。

## 与 SB×RL 的关联

Diffusion Policy 定义了 SB×RL 的「宿主生物」：一切 bridge/一步化/path-space RL 方法最终都要落回这个 action-chunk 条件生成的接口上。它也暴露了三个此后被反复攻击的弱点：多步推理限制控制频率（→ 一步化路线）、从纯高斯起点浪费「上一个 chunk」的信息（→ bridge 起点路线，informative source 正是 SB 的地盘）、$\log\pi$ 不可算（→ path-space RL 路线）。本仓库 05/06 两类的每一篇都在打其中至少一个点。

## 局限与批判

- 推理 10-100 次网络前向，控制频率被压到 10 Hz 量级，高动态任务不可用——这是后续一步化竞赛的直接起因。
- 纯模仿学习：性能上限锁死在示范质量，无法超越示范者，须外接 RL 才能改进。
- action chunk + receding horizon 的反应性折中在扰动大的场景失效（chunk 内不闭环）。
- 观测编码一次的设计假设观测在 chunk 内不突变，动态场景存疑。
