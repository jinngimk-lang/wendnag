# DDPM 从 0 到 1：一份真正能学懂的白话笔记

> 目标：不靠死背，把 DDPM 从“为什么要加噪”一路学到“为什么最后只训练一个噪声预测 MSE”。
>
> 阅读方法：第一次只看每节开头的白话结论；第二次再看公式。真正需要背的公式只有 4 组，文末有“一屏复习版”。

---

# 0. 先把全局看懂

DDPM 做两件事。

**训练：自己把真实图片弄脏，再让网络猜“我刚才加了什么噪声”。**

\[
x_0
\longrightarrow
x_t
\longrightarrow
\epsilon_\theta(x_t,t)
\]

**生成：从纯高斯噪声出发，反复利用这个网络，一步一步采样回数据空间。**

\[
x_T
\rightarrow
x_{T-1}
\rightarrow
\cdots
\rightarrow
x_1
\rightarrow
x_0
\]

最浓缩的一句话：

\[
\boxed{
\text{DDPM = 用一个完全已知的加噪过程，制造可监督的去噪学习任务。}
}
\]

后面所有概率论，只是在证明这件事为什么成立。

---

# 1. 先建立“三个世界”

这是整篇最重要的认知框架。

## 世界 A：人为规定的前向加噪

\[
q(x_t\mid x_{t-1})
\]

这里的 \(q\) 不需要学习，它是我们自己设计的。

## 世界 B：训练时可计算的“老师答案”

\[
q(x_{t-1}\mid x_t,x_0)
\]

训练时我们知道真实图片 \(x_0\)，所以这个条件后验可以精确算。

## 世界 C：真正生成时使用的模型

\[
p_\theta(x_{t-1}\mid x_t)
\]

生成时没有 \(x_0\)，所以只能让神经网络根据 \(x_t,t\) 学着模仿老师。

整个 DDPM 的训练核心就是：

\[
\boxed{
q(x_{t-1}\mid x_t,x_0)
\quad\longrightarrow\quad
p_\theta(x_{t-1}\mid x_t)
}
\]

左边是老师，右边是学生。

---

# 2. 最少符号表

| 符号 | 白话含义 |
|---|---|
| \(x_0\) | 干净真实数据 |
| \(x_t\) | 第 \(t\) 个噪声等级的数据 |
| \(x_T\) | 最后一步，设计得接近纯高斯噪声 |
| \(T\) | 总步数 |
| \(q\) | 已知的前向扩散分布 |
| \(p_\theta\) | 神经网络参数化的反向生成分布 |
| \(\beta_t\) | 第 \(t\) 步加入的噪声方差 |
| \(\alpha_t=1-\beta_t\) | 第 \(t\) 步保留的信号功率比例 |
| \(\bar\alpha_t=\prod_{s=1}^t\alpha_s\) | 到第 \(t\) 步累计保留的信号功率比例 |
| \(\epsilon\) | 标准高斯噪声 |
| \(\epsilon_\theta(x_t,t)\) | 网络预测的噪声 |

一个很容易混淆的点：

\[
\alpha_t
\]

是**功率/方差比例**，真正乘到信号振幅上的系数是：

\[
\sqrt{\alpha_t}.
\]

同理，累计信号振幅系数是：

\[
\sqrt{\bar\alpha_t}.
\]

---

# 3. 前向扩散：怎么把图片一步一步弄脏

DDPM 规定每一步：

\[
\boxed{
q(x_t\mid x_{t-1})
=
\mathcal N
\left(
x_t;
\sqrt{\alpha_t}x_{t-1},
\beta_t I
\right)
}
\]

等价地：

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

白话：

> 保留大部分旧信号，再加入一点新的高斯噪声。

为什么选高斯？

因为高斯特别容易算：

- 线性组合后还是高斯；
- 条件分布容易解析；
- 两个高斯之间的 KL 有闭式公式。

DDPM 后面能一路简化，几乎都靠这个设计。

---

# 4. 第一条必背公式：直接跳到任意噪声等级

定义：

\[
\alpha_t=1-\beta_t,
\qquad
\bar\alpha_t=\prod_{s=1}^t\alpha_s.
\]

其中 \(s\) 只是乘积的计数下标。

因为连续很多步线性高斯可以合并，所以：

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

对应的采样式：

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

这是整篇最值得背的公式之一。

它就是：

\[
\underbrace{\sqrt{\bar\alpha_t}x_0}_{\text{还剩多少原图}}
+
\underbrace{\sqrt{1-\bar\alpha_t}\epsilon}_{\text{已经积累多少噪声}}.
\]

当 \(t\) 小：

\[
\bar\alpha_t\approx1
\Rightarrow
x_t\approx x_0.
\]

当 \(t\) 大：

\[
\bar\alpha_t\approx0
\Rightarrow
x_t\approx\epsilon.
\]

## 为什么训练效率突然变高？

如果随机抽到 \(t=700\)，不用真的算：

\[
x_1,x_2,\ldots,x_{699}.
\]

一次公式就直接得到：

\[
x_{700}.
\]

所以训练时可以随机抽任意 \(t\)，独立训练。

---

# 5. 为什么反向过程需要神经网络？

前向：

\[
q(x_t\mid x_{t-1})
\]

是我们自己规定的，所以知道怎么走。

但生成需要反过来：

\[
x_t\rightarrow x_{t-1}.
\]

真正想要的是：

\[
q(x_{t-1}\mid x_t).
\]

问题是：它依赖真实数据分布，通常没法直接写出来。

所以定义模型：

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

网络为什么还要输入 \(t\)？

因为同一个数值状态，在不同噪声尺度下意义不同。网络必须知道：

> 现在到底脏到了什么程度。

---

# 6. DDPM 真正想优化什么？

理想情况当然是：

\[
\max_\theta \log p_\theta(x_0)
\]

也就是让真实数据在模型下概率尽可能高。

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

需要把所有中间变量：

\[
x_1,\ldots,x_T
\]

积分掉，直接算很困难。

于是 DDPM 引入我们完全知道的前向过程 \(q\)，通过变分推断得到一个可计算目标。

你只需要记住：

\[
\boxed{
\text{真正的负对数似然难算}
\;\Rightarrow\;
\text{优化一个可计算的变分上界。}
}
\]

从传统术语看：

- \(\log p_\theta(x_0)\) 有一个 ELBO 下界；
- 加负号后，就变成负对数似然的上界。

---

# 7. ELBO 拆开后，其实只是在管三段路

核心分解：

\[
\boxed{
L=
\mathbb E_q
\left[
L_T
+
\sum_{t=2}^{T}L_{t-1}
+
L_0
\right]
}
\]

其中：

\[
L_T
=
D_{\mathrm{KL}}
\left(
q(x_T\mid x_0)
\|
p(x_T)
\right)
\]

\[
L_{t-1}
=
D_{\mathrm{KL}}
\left(
q(x_{t-1}\mid x_t,x_0)
\|
p_\theta(x_{t-1}\mid x_t)
\right)
\]

\[
L_0
=
-\log p_\theta(x_0\mid x_1).
\]

宏观上：

\[
\boxed{
\underbrace{L_T}_{\text{终点对齐}}
+
\underbrace{\sum L_{t-1}}_{\text{中间每一步学对}}
+
\underbrace{L_0}_{\text{最后落回真实数据}}
}
\]

## \(L_T\)：终点对齐

问：

> 前向加噪走到最后，是否接近生成时的起点 \(p(x_T)=\mathcal N(0,I)\)？

如果噪声 schedule 固定，它不依赖网络参数 \(\theta\)，因此：

\[
\nabla_\theta L_T=0.
\]

所以训练网络时可以不靠它更新参数。

注意：**不参与梯度，不等于建模上不重要。**

## \(L_{t-1}\)：真正的核心

比较：

\[
\underbrace{q(x_{t-1}|x_t,x_0)}_{\text{训练时的老师}}
\]

和：

\[
\underbrace{p_\theta(x_{t-1}|x_t)}_{\text{生成时的学生}}.
\]

## \(L_0\)：最后一公里

\[
-\log p_\theta(x_0|x_1)
\]

作用是把整条潜变量链真正锚回可观测数据 \(x_0\)。

有些教学会把这一项类比成 one-hot 交叉熵。这个类比只能帮助理解“给正确观测更高概率”；连续图像并不是普通有限分类问题，不能把“整张图就是 one-hot”当成严格数学事实。

---

# 8. 第二条必懂公式：训练时为什么有“老师答案”？

老师是：

\[
q(x_{t-1}\mid x_t,x_0).
\]

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

已知 \(x_{t-1}\) 后，\(x_t\) 不需要再直接依赖 \(x_0\)，所以：

\[
q(x_t\mid x_{t-1},x_0)
=
q(x_t\mid x_{t-1}).
\]

于是：

\[
\boxed{
q(x_{t-1}\mid x_t,x_0)
\propto
q(x_t\mid x_{t-1})
q(x_{t-1}\mid x_0).
}
\]

右边是：

\[
\text{高斯}\times\text{高斯}.
\]

归一化以后仍然是高斯：

\[
\boxed{
q(x_{t-1}\mid x_t,x_0)
=
\mathcal N
\left(
x_{t-1};
\tilde\mu_t,
\tilde\beta_t I
\right).
}
\]

这就是为什么训练时存在一个可解析的“老师”。

---

# 9. 老师的均值和方差长什么样？

方差：

\[
\boxed{
\tilde\beta_t
=
\frac{
1-\bar\alpha_{t-1}
}{
1-\bar\alpha_t
}
\beta_t
}
\]

均值：

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

这两个系数**不建议死背**。

真正要懂的是结构：

\[
\boxed{
\tilde\mu_t
=
A_t x_0+B_t x_t.
}
\]

白话：

> 训练时知道原图在哪，也知道现在在哪，所以“正确的上一时刻中心”可以数学上直接算出来。

这也是“闭式计算”的含义。

如果一个随机变量可以解析积分掉，就没必要靠大量 Monte Carlo 抽样去估计它。把这类可解析随机性消掉，可以降低估计方差；这就是这里常提到的 Rao–Blackwell 化直觉。

---

# 10. KL 为什么突然变成 MSE？

基础 DDPM 常先把反向方差设为已知值：

\[
p_\theta(x_{t-1}|x_t)
=
\mathcal N
\left(
x_{t-1};
\mu_\theta(x_t,t),
\sigma_t^2 I
\right).
\]

这样真正需要网络学的主要就是均值。

两个高斯之间的 KL 有闭式解。把与 \(\theta\) 无关的项收进常数 \(C\)，可以写成：

\[
\boxed{
L_{t-1}
=
\mathbb E_q
\left[
\frac{1}{2\sigma_t^2}
\|
\tilde\mu_t-\mu_\theta
\|^2
\right]
+C.
}
\]

所以问题从：

\[
\text{“两个概率分布是否接近？”}
\]

变成：

\[
\boxed{
\text{“两个高斯中心是否接近？”}
}
\]

## 为什么一定是平方？

不是作者随便选的。

高斯密度本身就是：

\[
\mathcal N(x;\mu,\sigma^2)
\propto
\exp
\left(
-\frac{(x-\mu)^2}{2\sigma^2}
\right).
\]

因此固定方差后，负对数密度和高斯 KL 自然都会产生平方项。

所以：

\[
\boxed{
\text{高斯假设}
\Rightarrow
\text{平方误差。}
}
\]

---

# 11. 最关键的一步：为什么最后改成预测噪声？

我们已经有：

\[
x_t
=
\sqrt{\bar\alpha_t}x_0
+
\sqrt{1-\bar\alpha_t}\epsilon.
\]

反解 \(x_0\)：

\[
x_0
=
\frac{
x_t-\sqrt{1-\bar\alpha_t}\epsilon
}{
\sqrt{\bar\alpha_t}
}.
\]

把它代入老师均值，可以整理成：

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

现在观察这个式子：

- \(x_t\)：已知；
- \(t\)：已知；
- \(\alpha_t,\beta_t,\bar\alpha_t\)：schedule 已知；
- 真正需要估计的，只剩 \(\epsilon\)。

所以干脆让网络预测：

\[
\boxed{
\epsilon_\theta(x_t,t).
}
\]

并用它参数化模型均值：

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

这句话一定要说准确：

> 网络预测噪声，不等于“把预测噪声直接从 \(x_t\) 里减掉”。

\(\epsilon_\theta\) 是**反向均值的一种参数化方式**，真正的均值还有时间相关缩放系数。

---

# 12. 第三条必背公式：为什么最终 loss 只是噪声 MSE？

老师均值：

\[
\tilde\mu_t
=
\frac1{\sqrt{\alpha_t}}
\left(
x_t-
\frac{\beta_t}{\sqrt{1-\bar\alpha_t}}
\epsilon
\right)
\]

模型均值：

\[
\mu_\theta
=
\frac1{\sqrt{\alpha_t}}
\left(
x_t-
\frac{\beta_t}{\sqrt{1-\bar\alpha_t}}
\epsilon_\theta
\right).
\]

两者相减，\(x_t\) 消掉：

\[
\tilde\mu_t-\mu_\theta
=
-\frac{\beta_t}
{\sqrt{\alpha_t}\sqrt{1-\bar\alpha_t}}
(\epsilon-\epsilon_\theta).
\]

所以严格 ELBO 中对应的核心项变成：

\[
\boxed{
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

也就是：

\[
\boxed{
\text{带时间权重的噪声 MSE。}
}
\]

经典 DDPM 实践常进一步去掉这个时间权重，得到：

\[
\boxed{
L_{\text{simple}}
=
\mathbb E_{x_0,t,\epsilon}
\left[
\|
\epsilon-\epsilon_\theta(x_t,t)
\|^2
\right].
}
\]

这是最终最常见的训练目标。

注意：

> \(L_{\text{simple}}\) 是对严格变分目标的经验简化，不应说成和完整 ELBO 数学上完全相同。

---

# 13. score matching 到底和它有什么关系？

score 定义为：

\[
\boxed{
\nabla_x\log p(x).
}
\]

直觉：

> 在当前位置，概率密度变化最快的方向是什么？

对于：

\[
q(x_t|x_0)
=
\mathcal N
\left(
\sqrt{\bar\alpha_t}x_0,
(1-\bar\alpha_t)I
\right),
\]

条件 score 是：

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
\sqrt{1-\bar\alpha_t}\epsilon,
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

因此，预测 \(\epsilon\) 与预测这个条件 score 只差一个已知比例。

更严谨一点：

网络实际只看到 \(x_t,t\)，看不到 \(x_0\)。MSE 的最优预测是：

\[
\epsilon_\theta^*(x_t,t)
=
\mathbb E[\epsilon\mid x_t].
\]

再对 \(x_0\) 条件平均后，它和时间 \(t\) 下的边缘噪声分布 \(q_t(x_t)\) 的 score 对应。

所以最准确的理解是：

\[
\boxed{
\text{噪声预测，是 denoising score matching 的一种方便参数化。}
}
\]

不要把 sampling 简化成“沿 score 做普通梯度上升”；DDPM 的逆过程是一个有明确均值和方差的概率采样过程。

---

# 14. 真正训练时，代码到底在干什么？

每次迭代只做 7 步：

1. 采一张真实数据 \(x_0\)；
2. 随机采一个 \(t\in\{1,\ldots,T\}\)；
3. 采一份 \(\epsilon\sim\mathcal N(0,I)\)；
4. 一步构造 \(x_t\)；
5. 网络输入 \((x_t,t)\)；
6. 输出 \(\epsilon_\theta(x_t,t)\)；
7. 用 MSE 更新网络。

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

这就是为什么前面几十行概率论，真正落到训练代码时会变得这么短。

---

# 15. 第四条必背公式：训练好以后怎么生成？

先从：

\[
\boxed{
x_T\sim\mathcal N(0,I)
}
\]

开始。

然后：

\[
t=T,T-1,\ldots,1.
\]

网络先预测：

\[
\epsilon_\theta(x_t,t).
\]

再计算：

\[
\boxed{
\mu_\theta(x_t,t)
=
\frac1{\sqrt{\alpha_t}}
\left(
x_t-
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
\sigma_t z.
}
\]

其中通常：

\[
z\sim\mathcal N(0,I),\quad t>1
\]

最后一步：

\[
z=0,\quad t=1.
\]

于是：

\[
x_T
\to
x_{T-1}
\to
\cdots
\to
x_0.
\]

---

# 16. 为什么明明在“去噪”，还要加 \(\sigma_t z\)？

因为模型学的不是确定函数：

\[
x_t\mapsto x_{t-1}.
\]

它学的是：

\[
p_\theta(x_{t-1}|x_t)
=
\mathcal N(\mu_\theta,\sigma_t^2 I).
\]

\(\mu_\theta\) 只是这个高斯的中心。

真正从高斯里采样，本来就是：

\[
\mu_\theta+\sigma_t z.
\]

所以：

\[
\boxed{
\text{去噪}
\neq
\text{每一步都做确定性减法。}
}
\]

DDPM 是一条随机的反向概率链。

---

# 17. 把整篇推导压成一条链

真正应该记住的是：

\[
\boxed{
\text{最大化真实数据似然}
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
\text{变分上界 / ELBO}
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
\text{两个高斯做 KL}
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

所以：

> **一个看起来只是“猜噪声”的回归网络，背后其实是在训练一个概率生成模型。**

---

# 18. 高频误区，一次清掉

| 常见误解 | 正确理解 |
|---|---|
| \(\beta_t\) 就是噪声 | \(\beta_t\) 是噪声方差；真正随机噪声是 \(\epsilon\) |
| \(\alpha_t\) 是累计信号量 | \(\alpha_t\) 只管一步；\(\bar\alpha_t\) 才是累计 |
| 网络输入只有 \(x_t\) | 还必须知道噪声等级 \(t\) |
| 网络直接预测 \(x_{t-1}\) | 经典 \(\epsilon\)-parameterization 直接预测 \(\epsilon\)，再换算 \(\mu_\theta\) |
| 预测噪声就是直接做 \(x_t-\epsilon_\theta\) | 错；中间还有时间相关缩放 |
| \(L_T\) 被忽略说明它没意义 | 错；只是固定 schedule 时它对 \(\theta\) 没梯度 |
| KL 是一种距离 | 不严格；KL 不对称 |
| 图像 \(x_0\) 严格等于 one-hot | 只是某些教程的离散直觉 |
| DDPM 去噪时不应再加随机性 | 错；反向一步本身就是条件高斯采样 |
| 噪声预测是唯一参数化 | 不是；还可以预测 \(x_0\)、\(v\) 等 |
| 所有扩散模型都固定方差 | 不是；基础 DDPM 的常见简化之一 |
| \(L_{\text{simple}}\) 就是原始 ELBO 本身 | 不是；它去掉了时间相关权重 |

---

# 19. 四组公式，一周后只复习这里

## ① 任意噪声等级直接采样

\[
\boxed{
x_t
=
\sqrt{\bar\alpha_t}x_0
+
\sqrt{1-\bar\alpha_t}\epsilon
}
\]

## ② 训练时老师后验

\[
\boxed{
q(x_{t-1}|x_t,x_0)
=
\mathcal N(\tilde\mu_t,\tilde\beta_tI)
}
\]

## ③ 实际训练核心

\[
\boxed{
L_{\text{simple}}
=
\mathbb E
\|\epsilon-\epsilon_\theta(x_t,t)\|^2
}
\]

## ④ 生成时反向采样

\[
\boxed{
x_{t-1}
=
\frac1{\sqrt{\alpha_t}}
\left(
x_t-
\frac{\beta_t}
{\sqrt{1-\bar\alpha_t}}
\epsilon_\theta(x_t,t)
\right)
+
\sigma_t z
}
\]

只要这四组式子的“职责”都能说清楚，DDPM 主干就没有断点。

---

# 20. 最终自测：8 题全会，主干就算真正学通

1. 为什么训练时可以一步直接得到任意 \(x_t\)？
2. \(\alpha_t\) 和 \(\bar\alpha_t\) 分别表示什么？
3. 为什么 \(q(x_{t-1}|x_t)\) 难直接算，而 \(q(x_{t-1}|x_t,x_0)\) 能解析算？
4. 为什么老师后验仍然是高斯？
5. 为什么固定反向方差后，KL 会变成均值的平方误差？
6. 为什么预测噪声可以换算成预测反向均值？
7. 为什么生成时还要保留 \(\sigma_tz\) 这项随机性？
8. 为什么噪声预测与 denoising score matching 有直接联系？

如果能不用公式、只用自己的话回答这 8 题，再回头看公式，你已经不是“会背 DDPM”，而是“知道 DDPM 为什么这么设计”。

---

# 21. 一句话毕业总结

DDPM 的核心不是“神经网络会画图”。

它真正做的是：

\[
\boxed{
\text{先设计一个容易计算的破坏过程}
\rightarrow
\text{用已知破坏制造监督信号}
\rightarrow
\text{学会每个噪声尺度下如何反向恢复}
\rightarrow
\text{把这些局部反向步骤串成生成过程。}
}
\]

而“预测噪声”之所以成为经典训练方式，是因为在线性高斯扩散下：

\[
\boxed{
\text{反向分布匹配}
\;\Longleftrightarrow\;
\text{均值回归}
\;\Longleftrightarrow\;
\text{噪声回归}
}
\]

这就是 DDPM 从概率模型一路落到一行 MSE 的完整逻辑。

---

# 参考

- Jonathan Ho, Ajay Jain, Pieter Abbeel, *Denoising Diffusion Probabilistic Models*, NeurIPS 2020 / arXiv:2006.11239
- 原作者项目页：https://hojonathanho.github.io/diffusion/
- 原始实现：https://github.com/hojonathanho/diffusion
