# Rectified Schrödinger Bridge Matching for Few-Step Visual Navigation (RSBM)

> Luan, Li, Zhao, Zhang, Wu, Ma (吉大 & 利物浦), IEEE TMM（arXiv 2026-04, v3 2026-05）。[arXiv:2604.05673](https://arxiv.org/abs/2604.05673)

## 一句话

给条件桥核装一个熵正则旋钮 $\epsilon$：证明速度场的函数形式在整个 $\epsilon$ 谱上不变（单网络通吃）、方差随 $\epsilon$ 线性下降（粗步 ODE 稳），配上学习的条件先验缩短传输距离，视觉导航 3 步推理拿到 92% 成功率——few-step SB 策略的第一个正经具身实证。

## 问题与动机

单目视觉导航要把图像流变成连续长程动作轨迹，扩散/SB 策略能忠实建模多模态（路口左转右转都合理），但高方差随机传输要几十步积分才收敛，实时性没戏。已有少步方案（蒸馏、多阶段训练）流水线复杂。RSBM 的问题：SB 的熵正则参数 $\epsilon$ 本来就控制「随机-确定」的插值，能不能把它变成一个显式的工程旋钮，直接买到少步稳定性？

## 方法核心

1. **$\epsilon$-矫正桥核**。标准扩散桥（NaviBridger 一系）用布朗桥方差 $\sigma_t^2 = t^2(1-s_t)$，路径高方差纠缠。RSBM 把方差整体缩放：

$$
q_\epsilon(a_t|a_0, a_T) = \mathcal{N}(\mu_t,\ \epsilon\cdot t^2(1-s_t)\,I),\qquad \epsilon\in(0,1]
$$

$\epsilon=1$ 是标准布朗桥（最大熵 SB），$\epsilon\to0$ 塌缩为 Monge-Kantorovich 位移插值（确定性 OT）——一个参数在「多模态多样性」与「路径直度」之间连续换挡。边界条件对任意 $\epsilon$ 都精确钉住两端。
2. **Theorem 1（结构不变性）**：条件速度场 $v_t^* = \frac{d\mu_t}{dt} + \frac{d\log\sigma_{\epsilon,t}}{dt}(a_t-\mu_t)$ 的函数形式跨整个 $\epsilon$ 谱不变——一个网络参数化服务所有正则强度，训练是免仿真的 flow matching 回归。
3. **Proposition 1（方差线性缩减）**：条件速度方差随 $\epsilon$ 线性下降——粗步长 ODE 积分误差的直接控制量，「少步为什么稳」有了定量答案。
4. **学习的条件先验**。变分先验网络 $g_\psi$ 从视觉上下文生成粗轨迹 $a_T$ 作为桥的终端边界（替代各向同性噪声）——informative source 进一步缩短传输距离，与 $\epsilon$ 旋钮叠加。

## 实验与证据

- 导航基准（NoMaD/NaviBridger 一系设定）：3 步积分达 94%+ 余弦相似度、92% 成功率；$k=3$ 时 MSE 比 NaviBridger 低 6.3 倍，用 3.8 倍少的 NFE 打平其 $k=10$ 精度——免蒸馏、免多阶段。
- 定性：$k=2$ 时唯有 RSBM 已贴近 GT，基线要 $k\ge10$。
- 实验设计评价：对比对象选得对（NoMaD 扩散导航、NaviBridger 桥式导航），消融覆盖 $\epsilon$ 与先验两个组件；但任务面窄（纯导航、轨迹相似度导向），没有操纵、没有 RL、多模态保持只有定性展示——「$\epsilon$ 调小是否牺牲 mode coverage」这个关键权衡没有硬指标。

## 在谱系中的位置

- 上游：[I2SB](../2302.05872_i2sb/)（informative 边界）、[DSBM](../2303.16852_dsbm/)（bridge matching 语言）、Rectified Flow（「直化」思想的流侧源头）、NaviBridger（被超越的导航桥基线）。
- 平行：[ASBM](../2405.14449_adv_sbm/)（对抗式少步）、CDBM（蒸馏式少步）——少步 SB 的第三条路线：结构矫正。
- 下游：目前是「few-step SB 具身策略」唯一的正式文献锚点。

## 与 SB×RL 的关联（对我们选题的启示）

RSBM 证明了 06 章选题 memo 里的核心判断：**$\epsilon$ 谱系是 SB 独有的、可操作的 coverage-straightness 旋钮**——MeanFlow 族没有这个自由度（它们只有确定性极限一端）。留下的空白按价值排序：(1) **无 RL**——RSBM 是纯监督（模仿）训练，把 GSB-MDPO/FLAC 的 path-space RL 内核装进 RSBM 的 few-step 骨架，一次占「few-step × path-space RL」两格，是本仓库最明确的出牌点；(2) **1 步极限**——RSBM 停在 3 步，$\epsilon\to0$ + 平均速度场（MeanFlow 恒等式在桥上的版本）能不能做到 1-NFE SB 策略，无文献；(3) **mode coverage 硬指标**——$\epsilon$ 权衡的两端都该量化（借 OMP 谱分析方法），谁先补谁拿定义权；(4) 任务面从导航扩到操纵（RoboMimic/Adroit）即可与 DMPO/DBPO 正面对表。

## 局限与批判

- $\epsilon$ 缩放方差后严格说已不是原 SB 问题的解（参考过程被改了），「rectified SB」在数学上是新插值族而非 SB 的加速——命名有营销成分，理论定位要读者自己校准。
- 成功率/余弦相似度是轨迹贴合度指标，导航语义成功（到达目标、避障）与多模态覆盖的评测缺位。
- 变分先验网络训练期用 GT 轨迹的后验（$q_\psi(z|c,a_0)$），测试期换标准高斯——train-test 的先验分布错配没有讨论。
- 无 RL、无真机、期刊版实验规模有限；作为「SB few-step 可行」的存在性证明合格，作为方法竞争力证据还不够。
