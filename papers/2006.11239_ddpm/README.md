# Denoising Diffusion Probabilistic Models

> Ho, Jain, Abbeel (UC Berkeley), NeurIPS 2020。[arXiv:2006.11239](https://arxiv.org/abs/2006.11239)

## 一句话

把「逐步加噪-学习去噪」的马尔可夫链训练目标化简成一个预测噪声的回归 loss，第一次让扩散模型在图像质量上追平 GAN，是整个扩散时代的起点。

## 问题与动机

Sohl-Dickstein 2015 提出的扩散概率模型理论漂亮但生成质量差。DDPM 的问题是：这套框架的变分目标里，哪些项重要、怎么参数化才能训得好？答案出乎意料地简单——把重建目标重写成噪声预测，加权系数干脆丢掉。

## 方法核心

前向过程按固定方差表 $\beta_t$ 逐步加噪，且有闭式跳步：

$$
q(x_t|x_0) = \mathcal{N}\big(\sqrt{\bar\alpha_t}\,x_0,\ (1-\bar\alpha_t)\,I\big),\quad \bar\alpha_t = \prod_{s\le t}(1-\beta_s)
$$

反向过程学一个高斯 $p_\theta(x_{t-1}|x_t)$。关键一步：把 ELBO 里的 KL 项重参数化为噪声预测，得到简化目标

$$
\mathcal{L}_{\text{simple}} = \mathbb{E}_{x_0,\epsilon,t}\big[\|\epsilon - \epsilon_\theta(\sqrt{\bar\alpha_t}x_0 + \sqrt{1-\bar\alpha_t}\,\epsilon,\ t)\|^2\big]
$$

- $\epsilon\sim\mathcal{N}(0,I)$ 是前向加的噪声，$\epsilon_\theta$ 是网络。
- 这个 loss 恰好等价于（加权的）denoising score matching：$\epsilon_\theta \propto -\nabla\log p_t$。扩散与 score 两条线在此汇合。
- 采样即逐步去噪的祖先采样，等价于一种离散化的 Langevin 动力学。

## 实验与证据

- CIFAR-10 无条件生成：FID 3.17、IS 9.46，当时无条件生成的最好成绩，首次正面击败多数 GAN。
- LSUN Church/Bedroom 256×256 质量与 StyleGAN 相当。
- 消融：简化 loss（去掉 ELBO 权重）比完整变分目标的样本质量明显更好——「正确的目标不如好训的目标」，这个经验后来反复出现。

## 在谱系中的位置

- 上游：Sohl-Dickstein 2015（扩散框架）、Song & Ermon 2019（score matching + Langevin）。
- 下游（本仓库内）：[Score-SDE](../2011.13456_score_sde/) 把它连续时间化并统一两条线；[Flow Matching](../2210.02747_flow_matching/) 换成确定性传输语言；[Diffusion Policy](../2303.04137_diffusion_policy/) 把它搬到机器人动作生成；[DSB](../2106.01357_dsb/) 指出 DDPM 是 Schrödinger Bridge 的单边退化情形。

## 与 SB×RL 的关联

DDPM 是 SB 的特例：起点固定为高斯、只学单向 drift。SB 视角下，DDPM 的前向过程是一个「不需要学」的参考过程，全部学习量在反向。理解这一点才能理解 bridge 系方法在改什么——把无信息的高斯起点换成有信息的结构化分布。对 RL：DDPM 的多步采样结构就是后来 log π 障碍的来源（似然只有 ELBO），本仓库 RL 侧一半的论文都在处理这个后果。

## 局限与批判

- 采样需要上千步网络前向，推理成本是 GAN 的三个数量级。
- 似然（bits/dim）不如自回归模型，论文自己承认样本质量与似然脱节。
- 方差表 $\beta_t$ 手工固定，后续（improved DDPM、EDM）证明这里有大量免费性能。
