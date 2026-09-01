# MP1: MeanFlow Tames Policy Learning in 1-step for Robotic Manipulation

> Sheng, Wang, Li, Liu (PKU), AAAI 2026（arXiv 2025-07）。[arXiv:2507.10543](https://arxiv.org/abs/2507.10543)

## 一句话

第一个把 MeanFlow 平均速度场搬进机器人操纵的策略：3D 点云输入、1-NFE 生成动作轨迹、6.8 ms 推理，成功率反超多步扩散基线——「一步策略不需要蒸馏」的具身首证。

## 问题与动机

操纵策略的两难：扩散策略（DP3 等）质量好但多步采样慢；已有的快速流方法（FlowPolicy 等）靠显式 consistency 约束换少步，约束本身限制架构并引入调参负担。MeanFlow 恰好承诺「免约束的原生一步」——MP1 验证它在动作生成上是否成立，并补上机器人特有的少样本泛化问题。

## 方法核心

三个组件：

1. **MeanFlow 策略头**：以点云编码为条件，学区间平均速度 $u_\theta(a_t, r, t \mid o)$，训练目标来自 MeanFlow 恒等式 $u = v - (t-r)\frac{d}{dt}u$（JVP 实现），推理一步：$a = a_{\text{noise}} - u_\theta(a_{\text{noise}}, 0, 1 \mid o)$。没有 consistency loss、没有教师蒸馏、没有 ODE 求解误差。
2. **CFG 吸收**：把 classifier-free guidance 折进平均速度场的定义，推理仍是单次前向——可控性不花步数。
3. **Dispersive Loss**：对 batch 内的状态嵌入施加排斥正则（对比学习式、无正样本对），防止少样本场景下相近场景的表征塌在一起——泛化增益零推理开销。

## 实验与证据

- Adroit + Meta-World（共 37 任务）：平均成功率超 DP3 10.2%、超 FlowPolicy 7.3%。
- 推理 6.8 ms：比 DP3 快 19 倍、比 FlowPolicy 快约 2 倍——1-NFE 的直接兑现。
- 真机验证：Franka 上多任务成功率优势保持。
- 消融：Dispersive Loss 在少样本（10 demo）区间贡献最大；CFG 对精细任务的轨迹可控性有可见增益。

## 在谱系中的位置

- 上游：[MeanFlow](../2505.13447_meanflow/)（数学基础）、[Diffusion Policy](../2303.04137_diffusion_policy/)/DP3（被超越的多步范式）。
- 下游（本仓库内）：[DMPO](../2601.20701_dmpo/) 把 dispersive 正则理论化并接上 PPO 在线微调；[OFP](../2603.12480_ofp/) 给出自蒸馏替代路线；[DBPO](../2604.03540_dbpo/) 是 drift 固定点的原生一步竞品。

## 与 SB×RL 的关联

MP1 标志着一步化竞赛进入具身领域，直接改写 SB 策略的立论空间：「SB 理论上能少步」不再是卖点（MeanFlow 族已经把步数打到 1 且免蒸馏），SB 剩下的差异化必须落在 informative source（从上一 chunk/粗规划出发而非纯噪声）与多模态覆盖（$\epsilon$ 旋钮）上。MP1 也留了明显的口子：它是纯 BC（模仿），没有 RL；一步结构让 RL 微调的 credit assignment 问题消失，但也失去了去噪链提供的结构化探索——这个空缺由 DMPO 部分填补，SB 版本（bridge 起点 + 一步平均漂移 + RL）仍是空格。

## 局限与批判

- 纯模仿学习，上限锁死在示范；论文不涉及任何 RL 改进。
- Dispersive Loss 的作用机制停留在直觉（表征防塌缩），与成功率增益之间的因果链没有严格分析。
- 1-NFE 的多模态覆盖没有专门评测——一步生成模式塌缩的风险在动作分布上比图像更隐蔽（成功率看不出模式丢失）。
- 基准以短 horizon 操纵为主，长程任务上一步 chunk 的误差累积未知。
