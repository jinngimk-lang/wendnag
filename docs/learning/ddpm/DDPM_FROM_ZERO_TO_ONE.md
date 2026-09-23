# DDPM 从 0 到 1：把“扩散模型”学成一句人话

> 目标：不靠背公式，把 DDPM（Denoising Diffusion Probabilistic Models）从“为什么要加噪”一路学到“为什么最后只需要让网络猜噪声”。
>
> 阅读方式：每一节先看 **一句人话**，再看公式。第一次读不要求推导全记住，只要求能回答“这个公式到底在解决什么问题”。

---

## 0. 先把整件事看懂：DDPM 到底在干什么？

先只记两件事。

### 训练时：我们自己把图片弄脏，再让网络猜“我刚才加了什么噪声”

拿一张真实图片：

\[
x_0
\]

随机选一个噪声等级 \(t\)，随机抽一份高斯噪声：

\[
\epsilon\sim\mathcal N(0,I)
\]

直接合成这个噪声等级下的图片：

\[
x_t
=
\sqrt{\bar\alpha_t}x_0
+
\sqrt{1-\bar\alpha_t}\epsilon.
\]

把 \((x_t,t)\) 给网络，让它预测：

\[
\epsilon_\theta(x_t,t).
\]

然后比较：

\[
\boxed{
\|\epsilon-\epsilon_\theta(x_t,t)\|^2
}
\]

网络猜得越准，loss 越小。

### 生成时：从纯噪声出发，反复让网络告诉我们“这里面哪些像噪声”

从：

\[
x_T\sim\mathcal N(0,I)
\]

开始，反复执行：

\[
x_T\to x_{T-1}\to\cdots\to x_1\to x_0.
\]

最后得到一张数据分布里的图片。

所以先把 DDPM 压成一句话：

> **训练时学会识别不同噪声等级里的噪声；生成时利用这种能力，从纯噪声一步一步走回数据分布。**

后面的所有概率论，都是在证明：为什么这样训练是有道理的。

---

# 第一部分：最少预备知识

## 1. 你只需要先认识这些符号

| 符号 | 白话含义 |
|---|---|
| \(x_0\) | 原始干净数据，比如一张真实图片 |
| \(x_t\) | 加噪到第 \(t\) 步的数据 |
| \(x_T\) | 最后一步，理想情况下几乎就是纯高斯噪声 |
| \(T\) | 总噪声步数 |
| \(q\) | 我们人为规定的“前向加噪过程” |
| \(p_\theta\) | 神经网络参数化的“反向生成过程” |
| \(\beta_t\) | 第 \(t\) 步加入的噪声方差 |
| \(\alpha_t=1-\beta_t\) | 第 \(t\) 步保留的信号功率比例 |
| \(\bar\alpha_t=\prod_{s=1}^t\alpha_s\) | 从 0 累积到第 \(t\) 步后还保留多少信号功率 |
| \(\epsilon\) | 标准高斯噪声 |
| \(\epsilon_\theta(x_t,t)\) | 网络预测的噪声 |

特别注意：

\[
\alpha_t=1-\beta_t
\]

是“信号功率比例”，真正乘到数据振幅上的系数是：

\[
\sqrt{\alpha_t}.
\]

同理：

\[
\bar\alpha_t
\]

是累计功率比例，真正乘到 \(x_0\) 上的是：

\[
\sqrt{\bar\alpha_t}.
\]

---

## 2. 高斯分布为什么会不断出现？

一维高斯：

\[
\mathcal N(x;\mu,\sigma^2)
\propto
\exp\left(
-\frac{(x-\mu)^2}{2\sigma^2}
\right).
\]

它有两个关键参数：

- \(\mu\)：中心在哪里；
- \(\sigma^2\)：围绕中心有多大随机波动。

DDPM 故意把前向过程设计成高斯，因为高斯有几个非常省事的性质：

1. 高斯的线性组合还是高斯；
2. 高斯和高斯做条件化，结果仍可解析；
3. 两个高斯之间的 KL 散度有闭式公式。

这三个性质，直接决定了后面“老师答案能算出来”。

---

## 3. KL 散度到底是什么？

\[
D_{\mathrm{KL}}(P\|Q)
=
\sum_iP_i\log\frac{P_i}{Q_i}
=
H(P,Q)-H(P).
\]

可以先理解为：

> 真实世界按照 \(P\) 发生，但你用 \(Q\) 去描述它，多付出了多少信息代价。

几个必须记住的性质：

\[
D_{\mathrm{KL}}(P\|Q)\ge 0
\]

并且分布相同时为 0。

但 KL **不是普通距离**，因为一般：

\[
D_{\mathrm{KL}}(P\|Q)
\neq
D_{\mathrm{KL}}(Q\|P).
\]

在 DDPM 里，经常是：

\[
\boxed{
\text{老师分布 }q
\quad\text{对比}\quad
\text{模型分布 }p_\theta
}
\]

---

# 第二部分：前向扩散——先学会怎么把图片弄脏

## 4. 一步加噪

DDPM 规定：

\[
\boxed{
q(x_t\mid x_{t-1})
=
\mathcal N
\left(
x_t;
\sqrt{\alpha_t}x_{t-1},
\beta_tI
\right)
}
\]

等价的采样写法是：

\[
\boxed{
x_t
=
\sqrt{\alpha_t}x_{t-1}
+
\sqrt{\beta_t}\epsilon_t,
\qquad
\epsilon_t\sim\mathcal N(0,I).
}
\]

一句人话：

> 每一步保留大部分旧信号，再加入一点新的高斯噪声。

如果 \(\beta_t\) 很小，那么 \(\alpha_t=1-\beta_t\) 很接近 1，一步只会轻微污染。

---

## 5. 为什么定义 \(\bar\alpha_t\)？

\[
\boxed{
\bar\alpha_t
=
\prod_{s=1}^{t}\alpha_s
=
\alpha_1\alpha_2\cdots\alpha_t
}
\]

这里的 \(s\) 没有特殊物理含义，只是乘积的计数下标。

\(\alpha_t\) 说的是：

> **这一小步**保留多少信号。

而 \(\bar\alpha_t\) 说的是：

> 从 \(x_0\) 一路走到 \(x_t\)，**累计**还剩多少原始信号功率。

通常 \(t\) 越大：

\[
\bar\alpha_t\downarrow.
\]

于是原图越来越少，噪声越来越多。

---

## 6. DDPM 第一处关键技巧：不用一步一步加噪，可以直接跳到任意 \(t\)

由于每一步都是线性高斯，很多步可以合并。

最终得到：

\[
\boxed{
q(x_t\mid x_0)
=
\mathcal N
\left(
x_t;
\sqrt{\bar\alpha_t}x_0,
(1-\bar\alpha_t)I
\right)
}
\]

对应采样式：

\[
\boxed{
x_t
=
\sqrt{\bar\alpha_t}x_0
+
\sqrt{1-\bar\alpha_t}\epsilon,
\qquad
\epsilon\sim\mathcal N(0,I).
}
\]

这条公式值得直接背下来，因为训练时每个 batch 都在用。

它可以看成：

\[
\underbrace{\sqrt{\bar\alpha_t}x_0}_{\text{剩余原图}}
+
\underbrace{\sqrt{1-\bar\alpha_t}\epsilon}_{\text{累计噪声}}.
\]

当 \(t\) 很小时：

\[
\bar\alpha_t\approx1
\Rightarrow x_t\approx x_0.
\]

当 \(t\) 很大时：

\[
\bar\alpha_t\approx0
\Rightarrow x_t\approx\epsilon.
\]

### 这对训练为什么重要？

训练时如果随机抽到 \(t=700\)，不用真的计算：

\[
x_1,x_2,\ldots,x_{699}.
\]

直接抽一份 \(\epsilon\)，一次公式就得到 \(x_{700}\)。

---

# 第三部分：反向过程——真正需要网络学习的东西

## 7. 为什么不能直接把前向过程倒着跑？

前向一步：

\[
q(x_t\mid x_{t-1})
\]

是人为规定的，非常简单。

但生成时我们需要：

\[
x_t\to x_{t-1}.
\]

真正的反向条件分布：

\[
q(x_{t-1}\mid x_t)
\]

依赖整个真实数据分布，并不能直接写出来。

所以我们训练一个模型去近似它：

\[
\boxed{
p_\theta(x_{t-1}\mid x_t)
=
\mathcal N
\left(
x_{t-1};
\mu_\theta(x_t,t),
\Sigma_\theta(x_t,t)
\right).
}
\]

为什么网络还要输入 \(t\)？

因为同一个像素值，在：

- \(t=20\)：可能只是轻微噪声；
- \(t=900\)：可能几乎全是噪声。

网络必须知道当前处于哪个噪声尺度。

---

## 8. 生成模型的完整联合分布

从纯噪声开始：

\[
p(x_T)=\mathcal N(0,I)
\]

然后一步一步反向采样：

\[
\boxed{
p_\theta(x_{0:T})
=
p(x_T)
\prod_{t=1}^{T}
p_\theta(x_{t-1}\mid x_t).
}
\]

一句人话：

> 先抽一团纯噪声，再连续做 \(T\) 次“稍微变干净一点”的随机变换。

---

# 第四部分：为什么要绕到 ELBO？

## 9. 真正想做的是最大化真实图片的概率

理想目标：

\[
\max_\theta\log p_\theta(x_0).
\]

等价于最小化：

\[
-\log p_\theta(x_0).
\]

但：

\[
p_\theta(x_0)
=
\int p_\theta(x_{0:T})\,dx_{1:T}
\]

需要把所有中间隐变量：

\[
x_1,\ldots,x_T
\]

积分掉，直接算很困难。

所以引入一个我们完全知道、也很容易采样的前向分布：

\[
q(x_{1:T}\mid x_0).
\]

利用 Jensen 不等式，可以得到一个可优化的变分目标。

最终常写成：

\[
\boxed{
\mathbb E_{q(x_0)}
[-\log p_\theta(x_0)]
\le
L.
}
\]

也就是说：

> 真正的负对数似然不好直接算，就训练一个能算的上界。

从“ELBO”的传统说法看，它是 \(\log p_\theta(x_0)\) 的下界；换成负号以后，就是负对数似然的上界。

---

## 10. ELBO 最重要的分解

DDPM 把损失整理成：

\[
\boxed{
L=
\mathbb E_q
\left[
\underbrace{
D_{\mathrm{KL}}
\left(
q(x_T\mid x_0)
\|p(x_T)
\right)
}_{L_T}
+
\sum_{t=2}^{T}
\underbrace{
D_{\mathrm{KL}}
\left(
q(x_{t-1}\mid x_t,x_0)
\|
p_\theta(x_{t-1}\mid x_t)
\right)
}_{L_{t-1}}
+
\underbrace{
\left(-\log p_\theta(x_0\mid x_1)\right)
}_{L_0}
\right].
}
\]

不要先看细节，先看三个职责：

### \(L_T\)：终点是否对得上

\[
q(x_T\mid x_0)
\quad\text{vs}\quad
p(x_T)=\mathcal N(0,I).
\]

问：

> 前向加噪的终点，是否接近我们生成时规定的标准高斯起点？

### \(L_{t-1}\)：中间每一步有没有学对

\[
q(x_{t-1}\mid x_t,x_0)
\quad\text{vs}\quad
p_\theta(x_{t-1}\mid x_t).
\]

问：

> 网络给出的反向一步，和训练时能够计算出来的“正确反向一步”有多接近？

这是训练的核心。

### \(L_0\)：最后有没有真正落回数据空间

\[
\boxed{
L_0=-\log p_\theta(x_0\mid x_1).
}
\]

宏观上它就是“最后一公里”：

\[
x_1\to x_0.
\]

它让整个潜变量去噪链最终锚定到真实数据。

---

## 11. 关于 \(L_0\) 的一个常见教学类比

有些教程会说：

> 对一条训练样本，真实 \(x_0\) 相当于 one-hot，所以 KL 化成 \(-\log p_\theta(x_0|x_1)\)。

这个类比对理解“给正确答案更高概率”有帮助，但需要知道：

- one-hot 是离散分类的直觉；
- 图像通常不是普通有限类别变量；
- 连续情形更严谨地可以把观测值理解成集中在 \(x_0\) 的点质量 / Dirac delta；
- 原始 DDPM 的 decoder likelihood 对离散图像值还有具体处理。

因此不要把“整张连续图像就是 one-hot”当成严格事实。

---

# 第五部分：DDPM 最聪明的一步——训练时竟然有“老师答案”

## 12. “老师”到底是谁？

中间 KL 里面：

\[
\boxed{
q(x_{t-1}\mid x_t,x_0)
}
\]

可以理解为：

> 已知原图 \(x_0\)，也知道当前噪声图 \(x_t\)，那么正确的上一状态 \(x_{t-1}\) 应该服从什么分布？

训练时 \(x_0\) 是数据集里的真图，所以这件事可以计算。

而模型只有：

\[
\boxed{
p_\theta(x_{t-1}\mid x_t)
}
\]

因为生成时根本看不到 \(x_0\)。

于是：

\[
\text{老师}
=
q(x_{t-1}|x_t,x_0)
\]

教：

\[
\text{学生}
=
p_\theta(x_{t-1}|x_t).
\]

---

## 13. 老师答案为什么能算？从贝叶斯开始

根据贝叶斯：

\[
q(x_{t-1}\mid x_t,x_0)
=
\frac{
q(x_t\mid x_{t-1},x_0)
q(x_{t-1}\mid x_0)
}{
q(x_t\mid x_0)
}.
\]

前向过程是 Markov 链：

\[
x_0\to x_1\to\cdots\to x_{t-1}\to x_t.
\]

已知 \(x_{t-1}\) 后：

\[
q(x_t\mid x_{t-1},x_0)
=
q(x_t\mid x_{t-1}).
\]

于是：

\[
\boxed{
q(x_{t-1}\mid x_t,x_0)
=
\frac{
q(x_t\mid x_{t-1})
q(x_{t-1}\mid x_0)
}{
q(x_t\mid x_0)
}.
}
\]

如果只关心它关于 \(x_{t-1}\) 的形状：

\[
q(x_{t-1}\mid x_t,x_0)
\propto
q(x_t\mid x_{t-1})
q(x_{t-1}\mid x_0).
\]

右侧是：

\[
\text{高斯}\times\text{高斯}.
\]

归一化后仍然是高斯。

---

## 14. 老师后验的闭式答案

最终：

\[
\boxed{
q(x_{t-1}\mid x_t,x_0)
=
\mathcal N
\left(
x_{t-1};
\tilde\mu_t(x_t,x_0),
\tilde\beta_tI
\right).
}
\]

其中：

\[
\boxed{
\tilde\beta_t
=
\frac{1-\bar\alpha_{t-1}}
{1-\bar\alpha_t}
\beta_t
}
\]

以及：

\[
\boxed{
\tilde\mu_t(x_t,x_0)
=
\frac{
\sqrt{\bar\alpha_{t-1}}\beta_t
}{
1-\bar\alpha_t
}x_0
+
\frac{
\sqrt{\alpha_t}(1-\bar\alpha_{t-1})
}{
1-\bar\alpha_t
}x_t.
}
\]

这两个式子不建议死背。

真正要理解的是：

\[
\boxed{
\tilde\mu_t
=
A_tx_0+B_tx_t.
}
\]

也就是：

> 知道“原图在哪”和“现在在哪”以后，正确的上一时刻中心位置可以精确算出来。

而：

\[
\tilde\beta_t
\]

告诉我们，即使知道 \(x_0,x_t\)，上一状态仍然有多少剩余随机性。

---

## 15. “闭式计算”和 Rao–Blackwell 化为什么重要？

理论上，我们可以反复随机抽：

\[
x_{t-1}\sim q(x_{t-1}|x_t,x_0)
\]

然后用 Monte Carlo 估计损失。

但现在整个条件后验都能解析写出来，就没必要让这部分随机性继续制造梯度噪声。

可以直接计算高斯与高斯之间的 KL。

这类“把能解析积分掉的随机变量直接积分掉，而不是靠抽样估计”的思路，可以理解为这里 Rao–Blackwell 化的作用：

\[
\boxed{
\text{减少估计方差，让训练更稳定。}
}
\]

最简单的比喻：

> 已经知道公平骰子六个面的概率，就直接算期望 3.5，不必真的掷几万次骰子才估计平均值。

---

# 第六部分：一步一步把复杂 loss 简化成 MSE

## 16. 为什么训练时可以忽略 \(L_T\)？

\[
L_T
=
\mathbb E_{q(x_0)}
D_{\mathrm{KL}}
\left(
q(x_T|x_0)
\|p(x_T)
\right).
\]

如果：

- 前向噪声 schedule \(\beta_1,\ldots,\beta_T\) 已固定；
- \(p(x_T)=\mathcal N(0,I)\) 也固定；

那么 \(L_T\) 里面没有神经网络参数 \(\theta\)。

所以：

\[
\boxed{
\frac{\partial L_T}{\partial\theta}=0.
}
\]

因此它不影响网络参数更新。

注意：

> “训练梯度里可以忽略”不等于“建模上不重要”。

我们仍需要把前向终点设计得足够接近标准高斯，否则生成起点和训练前向终点会错位。

---

## 17. 先把反向方差固定

反向一步写成：

\[
p_\theta(x_{t-1}|x_t)
=
\mathcal N
\left(
x_{t-1};
\mu_\theta(x_t,t),
\sigma_t^2I
\right).
\]

早期 DDPM 的一种简化是：先把 \(\sigma_t^2\) 设好，只让网络学均值。

常见选择包括：

\[
\sigma_t^2=\beta_t
\]

或：

\[
\sigma_t^2=\tilde\beta_t.
\]

这样网络真正需要拟合的核心就变成：

\[
\boxed{\mu_\theta(x_t,t).}
\]

后来的扩散模型也可以学习方差；“固定方差”不是所有扩散模型永远不变的铁律。

---

## 18. 为什么高斯 KL 会变成平方误差？

假设两个一维高斯方差相同：

\[
P=\mathcal N(\mu_1,\sigma^2),
\qquad
Q=\mathcal N(\mu_2,\sigma^2).
\]

则：

\[
D_{\mathrm{KL}}(P\|Q)
=
\frac{1}{2\sigma^2}
(\mu_1-\mu_2)^2.
\]

所以固定方差以后，老师和学生的 KL 中，与网络参数有关的核心就是：

\[
\boxed{
L_{t-1}
=
\mathbb E_q
\left[
\frac{1}{2\sigma_t^2}
\|
\tilde\mu_t(x_t,x_0)
-
\mu_\theta(x_t,t)
\|^2
\right]
+C.
}
\]

其中 \(C\) 与 \(\theta\) 无关。

这一步把：

\[
\text{学习概率分布}
\]

化成了：

\[
\boxed{\text{学习一个回归目标。}}
\]

### 为什么是平方，不是随便选的？

因为高斯密度本身就有：

\[
\exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right).
\]

平方误差是从高斯假设自然推出来的。

而且平方可以避免正负误差互相抵消，并更重地惩罚大偏差。

---

# 第七部分：为什么不直接预测均值，而去预测噪声？

## 19. 从 \(x_t\) 反推出 \(x_0\)

我们已有：

\[
x_t
=
\sqrt{\bar\alpha_t}x_0
+
\sqrt{1-\bar\alpha_t}\epsilon.
\]

移项：

\[
\boxed{
x_0
=
\frac{
x_t-\sqrt{1-\bar\alpha_t}\epsilon
}{
\sqrt{\bar\alpha_t}
}.
}
\]

训练时：

- \(x_t\) 已知；
- \(t\) 已知；
- \(\epsilon\) 是我们自己抽的，也已知。

所以可以用噪声 \(\epsilon\) 来重新表达老师均值。

---

## 20. 老师均值可以改写成“当前图 - 一份噪声”

把上式代入 \(\tilde\mu_t\)，整理得到：

\[
\boxed{
\tilde\mu_t
=
\frac{1}{\sqrt{\alpha_t}}
\left(
x_t
-
\frac{\beta_t}
{\sqrt{1-\bar\alpha_t}}
\epsilon
\right).
}
\]

这里：

- \(x_t\) 已知；
- \(\alpha_t,\beta_t,\bar\alpha_t\) 都由 schedule 决定；
- 唯一具有“要猜”的性质的是 \(\epsilon\)。

因此作者用网络直接预测：

\[
\boxed{
\epsilon_\theta(x_t,t).
}
\]

然后定义模型均值：

\[
\boxed{
\mu_\theta(x_t,t)
=
\frac{1}{\sqrt{\alpha_t}}
\left(
x_t
-
\frac{\beta_t}
{\sqrt{1-\bar\alpha_t}}
\epsilon_\theta(x_t,t)
\right).
}
\]

一句人话：

> 网络不必直接说“上一帧应该长什么样”；它只需要说“我认为当前图里混进来的噪声是什么”，剩下的由确定公式换算。

---

## 21. 均值 MSE 为什么会直接变成噪声 MSE？

老师：

\[
\tilde\mu_t
=
\frac{1}{\sqrt{\alpha_t}}
\left(
x_t
-
\frac{\beta_t}{\sqrt{1-\bar\alpha_t}}
\epsilon
\right)
\]

学生：

\[
\mu_\theta
=
\frac{1}{\sqrt{\alpha_t}}
\left(
x_t
-
\frac{\beta_t}{\sqrt{1-\bar\alpha_t}}
\epsilon_\theta
\right).
\]

两者相减时 \(x_t\) 抵消：

\[
\tilde\mu_t-\mu_\theta
=
-\frac{\beta_t}
{\sqrt{\alpha_t}\sqrt{1-\bar\alpha_t}}
(\epsilon-\epsilon_\theta).
\]

所以：

\[
\boxed{
L_{t-1}-C
=
\mathbb E
\left[
\frac{\beta_t^2}
{2\sigma_t^2\alpha_t(1-\bar\alpha_t)}
\|
\epsilon-\epsilon_\theta(x_t,t)
\|^2
\right].
}
\]

把前面的系数记成 \(w_t\)：

\[
L_{t-1}-C
=
\mathbb E
\left[
w_t
\|
\epsilon-\epsilon_\theta(x_t,t)
\|^2
\right].
\]

所以严格从 ELBO 推出来的是：

\[
\boxed{\text{带时间权重的噪声 MSE。}}
\]

---

## 22. 经典 simplified objective

经典 DDPM 实践中，常直接去掉上面的时间权重，训练：

\[
\boxed{
L_{\mathrm{simple}}
=
\mathbb E_{x_0,t,\epsilon}
\left[
\|
\epsilon-
\epsilon_\theta(x_t,t)
\|^2
\right].
}
\]

这件事要说准确：

> \(L_{\mathrm{simple}}\) 是非常成功的训练简化，但不能把它说成“和完整 ELBO 数学上完全一模一样”。

它改变了不同时间步在优化中的相对权重。

---

# 第八部分：为什么“猜噪声”又和 score matching 有关？

## 23. score 是什么？

对一个密度 \(p(x)\)，score 定义为：

\[
\boxed{
\nabla_x\log p(x).
}
\]

直觉：

> 在当前位置，往哪个方向移动，概率密度上升最快？

可以把它想象成概率地形上的“上坡箭头”。

---

## 24. 加噪分布的条件 score

我们知道：

\[
q(x_t|x_0)
=
\mathcal N
\left(
\sqrt{\bar\alpha_t}x_0,
(1-\bar\alpha_t)I
\right).
\]

对 \(x_t\) 求对数密度梯度：

\[
\nabla_{x_t}\log q(x_t|x_0)
=
-
\frac{
x_t-\sqrt{\bar\alpha_t}x_0
}{
1-\bar\alpha_t
}.
\]

而：

\[
x_t-\sqrt{\bar\alpha_t}x_0
=
\sqrt{1-\bar\alpha_t}\epsilon.
\]

所以：

\[
\boxed{
\nabla_{x_t}\log q(x_t|x_0)
=
-\frac{\epsilon}
{\sqrt{1-\bar\alpha_t}}.
}
\]

因此噪声预测与条件 score 只差一个已知比例：

\[
\boxed{
s_\theta(x_t,t)
\approx
-\frac{\epsilon_\theta(x_t,t)}
{\sqrt{1-\bar\alpha_t}}.
}
\]

更严谨地说：训练目标对 \(x_0\) 平均后，最优预测会对应噪声条件期望，从而与时间 \(t\) 下加噪边缘分布 \(q_t(x_t)\) 的 score 联系起来。这正是 denoising score matching 的核心联系。

所以：

> **“猜噪声”不仅是在做图像修复，它也在学习噪声尺度下概率密度的方向场。**

---

# 第九部分：真正写代码时，到底怎么训练？

## 25. DDPM 训练算法

每次迭代：

1. 从训练集采样 \(x_0\)；
2. 均匀随机采样 \(t\in\{1,\ldots,T\}\)；
3. 采样 \(\epsilon\sim\mathcal N(0,I)\)；
4. 构造：
   \[
   x_t
   =
   \sqrt{\bar\alpha_t}x_0
   +
   \sqrt{1-\bar\alpha_t}\epsilon;
   \]
5. 网络计算：
   \[
   \hat\epsilon=\epsilon_\theta(x_t,t);
   \]
6. 计算：
   \[
   \mathcal L=\|\epsilon-\hat\epsilon\|^2;
   \]
7. 反向传播更新 \(\theta\)。

伪代码：

~~~python
x0 = sample_real_data()
t = random_integer(1, T)
eps = randn_like(x0)

xt = sqrt(alpha_bar[t]) * x0 \
   + sqrt(1 - alpha_bar[t]) * eps

eps_hat = model(xt, t)

loss = mse(eps_hat, eps)
loss.backward()
optimizer.step()
~~~

最值得注意的是：

> 训练时不需要真的完整跑一条 \(x_0\to x_1\to\cdots\to x_T\) 链。

每次只随机练一个 \(t\)。

---

# 第十部分：训练好后，到底怎么生成？

## 26. 从纯噪声开始

先采：

\[
\boxed{
x_T\sim\mathcal N(0,I).
}
\]

然后：

\[
t=T,T-1,\ldots,1.
\]

每一步网络先预测：

\[
\epsilon_\theta(x_t,t).
\]

由此计算反向均值：

\[
\boxed{
\mu_\theta(x_t,t)
=
\frac{1}{\sqrt{\alpha_t}}
\left(
x_t
-
\frac{\beta_t}
{\sqrt{1-\bar\alpha_t}}
\epsilon_\theta(x_t,t)
\right).
}
\]

然后从反向高斯采样：

\[
\boxed{
x_{t-1}
=
\mu_\theta(x_t,t)
+
\sigma_tz.
}
\]

其中通常：

\[
z\sim\mathcal N(0,I),\quad t>1
\]

最后一步取：

\[
z=0,\quad t=1.
\]

于是：

\[
x_T\to x_{T-1}\to\cdots\to x_0.
\]

---

## 27. 为什么“去噪”时还要再加 \(\sigma_tz\)？

这是非常常见的疑问。

因为 DDPM 学的不是确定函数：

\[
x_t\mapsto x_{t-1}.
\]

而是条件分布：

\[
p_\theta(x_{t-1}|x_t)
=
\mathcal N(\mu_\theta,\sigma_t^2I).
\]

\(\mu_\theta\) 只是中心。

真正“从一个高斯里采样”本来就应该：

\[
\mu_\theta+\sigma_tz.
\]

所以：

> “反向去噪”不等于“每一步都只做确定性的减法”。

它是在一个越来越接近数据的条件概率链里采样。

---

## 28. 为什么不能简单写成 \(x_{t-1}=x_t-\epsilon_\theta\)？

因为 \(\epsilon_\theta\) 的尺度不是“直接减掉就得到上一帧”。

不同 \(t\) 的：

- 信号比例不同；
- 噪声方差不同；
- 反向条件分布的均值缩放不同。

真正的均值要经过：

\[
\frac{1}{\sqrt{\alpha_t}}
\left(
x_t
-
\frac{\beta_t}
{\sqrt{1-\bar\alpha_t}}
\epsilon_\theta
\right).
\]

所以“网络预测噪声”只是参数化方式；真正的反向一步仍由概率模型公式决定。

---

# 第十一部分：把整套推导连成一条线

## 29. 从概率模型到噪声 MSE

你真正需要记住的是下面这条链：

\[
\boxed{
\text{希望真实数据概率最大}
}
\]

\[
\Downarrow
\]

\[
-\log p_\theta(x_0)
\]

\[
\Downarrow
\]

\[
\text{用可计算的变分上界 / ELBO}
\]

\[
\Downarrow
\]

\[
D_{\mathrm{KL}}
\left(
q(x_{t-1}|x_t,x_0)
\|
p_\theta(x_{t-1}|x_t)
\right)
\]

\[
\Downarrow
\]

\[
\text{老师和学生都是高斯}
\]

\[
\Downarrow
\]

\[
\|\tilde\mu_t-\mu_\theta\|^2
\]

\[
\Downarrow
\]

\[
\boxed{
\|\epsilon-\epsilon_\theta(x_t,t)\|^2
}
\]

这就是：

> **为什么一个看起来像“噪声回归”的网络，背后其实是在训练一个概率生成模型。**

---

# 第十二部分：最容易混淆的 10 个问题

## 30. \(\beta_t\) 是“噪声本身”吗？

不是。

\(\beta_t\) 是第 \(t\) 步噪声的**方差参数**。

真正随机抽出来的噪声是：

\[
\epsilon_t\sim\mathcal N(0,I).
\]

---

## 31. \(\alpha_t\) 和 \(\bar\alpha_t\) 有什么区别？

\[
\alpha_t
\]

只管一步。

\[
\bar\alpha_t
=
\alpha_1\cdots\alpha_t
\]

管从 0 到 \(t\) 的累计效果。

一句记忆：

> \(\alpha\) 是单步，\(\bar\alpha\) 是累计。

---

## 32. 为什么网络要输入 \(t\)？

同一张 \(x_t\) 在不同噪声尺度下，其统计意义不同。

\(t\) 告诉网络：

> 现在大约脏到了什么程度。

---

## 33. 老师为什么训练时有，生成时没有？

老师是：

\[
q(x_{t-1}|x_t,x_0).
\]

它需要知道 \(x_0\)。

训练时 \(x_0\) 就是数据集里的原图。

生成时 \(x_0\) 正是我们还没有、需要创造出来的东西，所以不能使用老师。

---

## 34. 网络真的在预测 \(x_{t-1}\) 吗？

经典噪声参数化里，网络直接输出的是：

\[
\epsilon_\theta(x_t,t).
\]

然后通过确定公式换算成：

\[
\mu_\theta(x_t,t).
\]

再从：

\[
p_\theta(x_{t-1}|x_t)
\]

采样得到 \(x_{t-1}\)。

---

## 35. 为什么 MSE 是合理的？

不是“因为 MSE 比较常用”。

更根本的原因是：

> 前面假设的是高斯分布，而高斯的负对数密度天然带平方项。

---

## 36. \(L_T\) 被忽略是不是就不重要？

不是。

只是固定 schedule 时它不依赖 \(\theta\)，所以：

\[
\nabla_\theta L_T=0.
\]

它仍然反映前向终点与标准高斯是否对齐。

---

## 37. 预测噪声是不是唯一选择？

不是。

扩散模型常见参数化还包括：

- 预测 \(x_0\)；
- 预测 \(\epsilon\)；
- 预测 \(v\)。

这些参数化之间可以根据 schedule 做换算。

本文聚焦经典 DDPM 的 \(\epsilon\)-prediction，因为它最能看清原始推导。

---

## 38. “预测噪声 = 预测 score”是完全相等吗？

在条件高斯：

\[
q(x_t|x_0)
\]

下，两者确实只差已知比例：

\[
\nabla_{x_t}\log q(x_t|x_0)
=
-\frac{\epsilon}{\sqrt{1-\bar\alpha_t}}.
\]

但实际网络只看到 \(x_t,t\)，没有 \(x_0\)。

对训练分布取期望后，最优噪声预测与边缘 score 联系起来。

所以最准确的说法是：

> **噪声预测提供了一个非常方便的 denoising score matching 参数化。**

---

## 39. 生成时每一步都加随机噪声，会不会越加越脏？

不会按前向意义“重新弄脏”。

反向一步整体是在采样：

\[
p_\theta(x_{t-1}|x_t).
\]

其中均值负责把状态推向更干净的区域，随机项负责正确表示该条件分布的剩余不确定性。

---

# 第十三部分：一张符号速查表

| 符号 | 核心含义 | 是否学习 |
|---|---|---|
| \(x_0\) | 真实干净数据 | 否 |
| \(x_t\) | 第 \(t\) 步带噪数据 | 否 |
| \(\beta_t\) | 单步噪声方差 | 经典 DDPM 中通常预设 |
| \(\alpha_t=1-\beta_t\) | 单步信号功率保留率 | 由 \(\beta_t\) 决定 |
| \(\bar\alpha_t\) | 累计信号功率保留率 | 由 schedule 决定 |
| \(\epsilon\) | 训练时真实抽到的高斯噪声 | 否 |
| \(\epsilon_\theta\) | 网络预测的噪声 | 是 |
| \(\tilde\mu_t\) | 训练时老师后验的均值 | 可解析计算 |
| \(\tilde\beta_t\) | 训练时老师后验的方差 | 可解析计算 |
| \(\mu_\theta\) | 模型反向高斯均值 | 由网络输出参数化得到 |
| \(\sigma_t^2\) | 模型反向方差 | 经典基础版可固定 |
| \(q\) | 前向加噪 / 可知分布 | 不学习 |
| \(p_\theta\) | 反向生成模型 | 学习 |

---

# 第十四部分：一屏压缩版

如果一周后你忘了全部细节，只复习这里。

### 前向加噪

\[
\boxed{
x_t
=
\sqrt{\bar\alpha_t}x_0
+
\sqrt{1-\bar\alpha_t}\epsilon
}
\]

### 老师后验

\[
\boxed{
q(x_{t-1}|x_t,x_0)
=
\mathcal N(\tilde\mu_t,\tilde\beta_tI)
}
\]

### 模型反向一步

\[
\boxed{
p_\theta(x_{t-1}|x_t)
=
\mathcal N(\mu_\theta,\sigma_t^2I)
}
\]

### 网络预测噪声

\[
\boxed{
\mu_\theta
=
\frac1{\sqrt{\alpha_t}}
\left(
x_t-
\frac{\beta_t}{\sqrt{1-\bar\alpha_t}}
\epsilon_\theta(x_t,t)
\right)
}
\]

### 实际训练核心

\[
\boxed{
\mathcal L_{\mathrm{simple}}
=
\mathbb E
\|\epsilon-\epsilon_\theta(x_t,t)\|^2
}
\]

### 生成

\[
\boxed{
x_T\sim\mathcal N(0,I)
}
\]

然后：

\[
\boxed{
x_{t-1}
=
\mu_\theta(x_t,t)
+
\sigma_tz
}
\]

从 \(t=T\) 一路走到 1。

---

# 第十五部分：真正学会没有？用这 8 题自测

1. 为什么训练时不用真的从 \(x_0\) 连续加噪到 \(x_t\)？
2. \(\alpha_t\) 与 \(\bar\alpha_t\) 的区别是什么？
3. 为什么真正的 \(q(x_{t-1}|x_t)\) 不好直接算，但 \(q(x_{t-1}|x_t,x_0)\) 却能算？
4. 为什么老师后验仍然是高斯？
5. 为什么固定方差后，高斯 KL 会变成均值 MSE？
6. 为什么预测 \(\epsilon\) 可以换算成预测反向均值？
7. 为什么生成时“去噪”过程还需要 \(\sigma_tz\)？
8. 为什么噪声预测与 score matching 有紧密联系？

如果你能不看答案，用自己的话回答这 8 题，DDPM 的主干已经真正学通了。

---

# 最后一段：你真正应该带走的直觉

DDPM 的厉害之处，不是“把噪声减掉”这么简单。

它做了一件更聪明的事：

1. 先人为设计一个极其容易计算的高斯破坏过程；
2. 因为破坏过程是已知的，训练时就能构造出反向一步的监督信号；
3. 通过变分推导，把概率分布匹配一步步化成普通回归；
4. 最终让网络只做一件非常明确的事——在任意噪声等级下识别噪声；
5. 生成时从标准高斯开始，把这项局部能力连续使用很多次，就得到全新的数据。

所以最浓缩的一句话是：

\[
\boxed{
\text{DDPM = 用已知的加噪过程，制造可监督的去噪学习任务，再把局部去噪能力串成生成过程。}
\]
