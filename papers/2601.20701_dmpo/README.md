# One Step Is Enough: Dispersive MeanFlow Policy Optimization (DMPO)

> Zou, Wang, Wu, Qian, Wang, Li (中山大学), arXiv 2026-01。[arXiv:2601.20701](https://arxiv.org/abs/2601.20701)

## 一句话

MeanFlow 预训练 + dispersive 表征正则 + PPO 微调三件套：一步策略第一次在 RL 微调后达到或超过多步基线，>120 Hz 真机部署——「一步生成 × 在线 RL」闭环的完成形态。

## 问题与动机

一步策略的三个互锁难题：蒸馏路线（CP、1-DP）训练流水线复杂；一步生成没有迭代修正机会，表征塌缩直接砸到动作质量；纯模仿（MP1）无法超越示范。DMPO 逐一对应：MeanFlow 免蒸馏、dispersive 正则防塌缩、PPO 微调破示范上限。

## 方法核心

**阶段一：dispersive MeanFlow 预训练**。标准 MeanFlow 恒等式目标（JVP 实现）+ dispersive 正则（batch 内状态表征互斥，InfoNCE 无正对形式），$\alpha_{\text{disp}}\in\{0.1,0.5,0.9\}$ 均稳定增益——一步生成把表征质量的全部压力压在单次前向上，防塌缩不是锦上添花而是必要件。

**阶段二：PPO 微调**。关键构造是把确定性一步采样临时展开成 $K$ 步随机链做探索：

$$
a_{k+1} \sim \mathcal{N}\big(a_k - \Delta\tau_k\, u_\theta(a_k, \tau_{k+1}, \tau_k, o),\ \sigma^2 I\big)
$$

联合对数似然沿链分解为高斯项之和（同 DPPO 的两层 MDP 思路），PPO clip 直接可用；再加对冻结预训练策略的 BC 正则 $\lambda_{\text{BC}}\|a_\omega(o)-a_\theta(o)\|^2$ 防灾难性遗忘。**部署时收回一步**：微调的是平均速度场本身，推理仍 1-NFE。

## 实验与证据

- RoboMimic 预训练：MeanFlow 变体 1-5 步即近饱和，ReFlow/ShortCut 需要 32-128 步。
- PPO 微调：Can 100%（快于 DPPO 99.3%/ReinFlow-R 99.0%）、Square 83%（DPPO 78.3%）、Transport 88%（打平 ReinFlow-S，NFE=1 vs 4）。
- 推理 5-20 倍加速、>120 Hz；Franka 真机四任务全成，MP1 基线在 Lift/Can 上因抓取不精失败。
- Gym locomotion + Kitchen 长程任务同样有效。

## 在谱系中的位置

- 上游：[MeanFlow](../2505.13447_meanflow/)、[MP1](../2507.10543_mp1/)（dispersive loss 的来源，被超越的纯 BC 版）、[DPPO](../2409.00588_dppo/)（似然分解的方法论模板）。
- 平行：[OFP](../2603.12480_ofp/)（自蒸馏免教师路线）、[DBPO](../2604.03540_dbpo/)（drift 固定点路线）——2026 上半年原生一步竞赛的三驾马车。

## 与 SB×RL 的关联

DMPO 展示了「训练时展开、部署时收回」的通用配方：一步模型在微调期临时借用多步链的可算似然，微调完成后一步部署。这个配方对 SB 策略直接可移植——bridge 的一步化版本（平均漂移场）同样可以展开成短链做 PPO。它也进一步压缩了 SB 策略的生存空间：路径直不直、步数多少、能不能 RL，全部被 MeanFlow 族回答了。SB 剩余的立足点收窄到两处：informative source（DMPO 起点仍是纯噪声，上一 chunk 的信息被丢弃）与显式的多模态-确定性权衡（$\epsilon$ 旋钮）。反过来说，「bridge 起点 + DMPO 配方」就是 one-step SB policy 最现实的实现路径。

## 局限与批判

- 微调期的 $K$ 步展开重新引入了 DPPO 的样本效率税，「一步」在训练阶段并不成立。
- BC 正则锚住冻结策略，改进幅度被 $\lambda_{\text{BC}}$ 钳制——超越示范的幅度与稳定性之间的权衡没有系统分析。
- RoboMimic 四任务 + Gym 是标准但偏窄的评测面，视觉输入任务（像素观测）缺席。
- dispersive 正则「一致增益」的结论来自 3 个 α 值的网格，机制解释仍停留在表征塌缩直觉。
