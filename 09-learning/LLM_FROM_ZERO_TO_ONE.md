# 从 0 到 1 学懂大模型：白话高浓缩学习手册

> 目标：不是背术语，而是建立一张能反复调用的脑内地图。  
> 主线：**文字 → token → 向量 → 概率 → 损失 → Attention → Transformer → 训练 → 推理 → 加速生成**

---

# 先看这一页：整套知识的最短闭环

大多数 decoder-only LLM 可以先压成这一条链：

```text
文本
 ↓ Tokenizer
token id
 ↓ Embedding
向量 X
 ↓ Transformer Block × N
上下文表示 H
 ↓ LM Head
logits z
 ↓ Softmax
下一个 token 概率 q
 ↓
训练：和正确 token 算 Cross Entropy → 反向传播 → 更新参数
推理：采样/选 token → 拼回上下文 → 继续下一步
```

你真正需要掌握的只有 8 个问题：

1. **模型看见什么？** → token 与向量。
2. **模型怎么表示“不确定”？** → logits + softmax。
3. **模型怎么知道错多少？** → cross entropy。
4. **模型怎么从错误中学习？** → gradient + backprop。
5. **token 怎么彼此交换信息？** → attention。
6. **模型怎么知道先后顺序？** → positional information。
7. **为什么 GPT 不能偷看未来？** → causal mask。
8. **为什么生成慢，怎么加速？** → autoregressive decode、KV cache、speculative / block generation。

后面所有公式都服务于这 8 个问题。

---

# 1. Token：模型并不直接读“文字”

## 一句话先懂

**LLM 真正处理的是 token id，不是人类意义上的“字”或“词”。**

概念上：

```text
"我喜欢机器学习"
→ ["我", "喜欢", "机器", "学习"]
→ [125, 8301, 4217, 998]
```

这些整数只是词表索引。8301 > 125 **不代表**“喜欢”比“我”更大。

## 为什么要 token 化？

如果完全按词切：

- 生僻词、新词太多；
- 多语言和代码难统一；
- 词表会变得很大。

如果完全按字符切：

- 序列会更长；
- Attention 成本更高。

所以现代 tokenizer 常做子词/字节级折中：**高频片段尽量合并，低频内容继续拆。**

## 一眼复习

> Tokenizer 做的是“离散化”；Embedding 才开始进入神经网络的连续空间。

---

# 2. Embedding：把编号变成“意义坐标”

token id 本身没有语义，模型会去 embedding 表里查一行向量。

若词表大小是 V，隐藏维度是 d：

$$
E ∈ R^{V×d}
$$

token id = 125 时：

$$
x = E[125]
$$

得到一个 d 维向量。

## 白话直觉

把每个 token 想成被放进一个高维坐标系。

相近语义、相似用法、相似上下文会通过训练形成某些几何结构，但不要把单独某一维硬解释成“动物维”“情绪维”。

真实表示通常是**分布式的**：

> 一个概念靠很多维共同表示，一维也同时参与很多概念。

---

# 3. 为什么神经网络到处都是矩阵乘法

## 一句话先懂

**xW 可以理解成：把同一份信息换一个可学习的观察角度。**

例如：

$$
y = xW
$$

不是“凭空创造事实”，而是对 x 的各维做重新组合。

Attention 里：

$$
Q = XW_Q,quad K = XW_K,quad V = XW_V
$$

就是把同一个 token 的表示分别投影成三种职责：

- Q：我想找什么；
- K：别人该如何匹配我；
- V：别人找到我后，我真正贡献什么。

这就是 QKV 的数学根基。

---

# 4. Logits 与 Softmax：模型如何表达不确定

## 4.1 Logits：先打分

模型最后会对整个词表输出一组实数：

$$
z = [2.1, 0.3, -1.2, ...]
$$

这些叫 logits。

它们：

- 可以为正也可以为负；
- 不要求总和为 1；
- 只是原始偏好分数。

## 4.2 Softmax：把分数变成概率

$$
q_i = e^{z_i} / Σ_j e^{z_j}
$$

Softmax 做三件事：

1. 概率全部变成正数；
2. 总和变成 1；
3. 保留排序，并放大较大 logit 的优势。

例如：

$$
z=[2,1,0]
$$

softmax 后约为：

$$
q=[0.665,0.245,0.090]
$$

## 4.3 Temperature：控制“敢不敢冒险”

采样时常把 logits 除以温度 T：

$$
q_i = softmax(z_i/T)
$$

- T 小：分布更尖，模型更保守；
- T 大：分布更平，模型更随机。

注意：**temperature 主要是推理时的采样控制，不是 Attention 公式里的 √dₖ。两者不要混。**

---

# 5. 为什么信息论里总出现 log

这是理解交叉熵最重要的一步。

设事件概率是 p，希望定义信息量 I(p)。

我们希望：

- 概率越小，事件发生时越意外；
- 两个独立事件一起发生，信息量可以相加。

独立事件：

$$
P(A,B)=P(A)P(B)
$$

希望：

$$
I(pq)=I(p)+I(q)
$$

而 log 正好把乘法变成加法：

$$
log(pq)=log p+log q
$$

由于 0 < p ≤ 1 时 log p ≤ 0，所以定义：

$$
I(p)=-log p
$$

于是：

$$
p=1 Rightarrow -log1=0
$$

必然发生，没有惊讶。

而：

$$
p=0.01 Rightarrow -log0.01≈4.605
$$

只给 1% 概率的事情真的发生了，代价很大。

## 一眼复习

> **-log(probability) = “你对真实发生事件有多意外”。**

---

# 6. 熵、交叉熵、KL：三者一次分清

## 6.1 熵 H(p)：真实世界自己有多不确定

$$
H(p)=-Σ_i p_i log p_i
$$

白话：

> 如果现实真的按 p 发生，平均一次事件带来多少“惊讶”。

---

## 6.2 交叉熵 H(p,q)：现实按 p 发生，但你拿 q 去预测

$$
H(p,q)=-Σ_i p_i log q_i
$$

角色一定要分清：

- 外面的 p：**现实出现频率**；
- log 里的 q：**模型押的概率**。

因此：

> 训练时真正被评分的是 q，不是 p。

---

## 6.3 One-hot 为什么只剩 -log qᵧ

假设正确类别是第 2 类：

$$
p=[0,1,0]
$$

模型：

$$
q=[0.1,0.7,0.2]
$$

则：

$$
H(p,q)=-(0log0.1+1log0.7+0log0.2)=-log0.7
$$

因此语言模型训练可以浓缩成：

$$
L=-logP_θ(正确token | 上下文)
$$

一句话：

> **模型给正确 token 的概率越高，loss 越小。**

---

## 6.4 为什么交叉熵正反向不同

通常：

$$
H(p,q)≠H(q,p)
$$

因为交换后：

- 谁代表现实变了；
- 谁接受评分也变了。

又有：

$$
H(p,q)=H(p)+D_{KL}(p||q)
$$

所以可理解成：

> **真实世界本身的不可避免不确定性 + 模型因为预测偏差额外付出的代价。**

KL 一般也不对称：

$$
D_{KL}(p||q)≠D_{KL}(q||p)
$$

---

# 7. 梯度与反向传播：模型究竟怎样“学”

## 一句话先懂

**Loss 只负责说“错多少”；Gradient 才负责说“参数往哪改”。**

对 softmax + cross entropy，有一个非常漂亮的结果：

$$
∂L/∂z_i = q_i-p_i
$$

例如：

$$
p=[0,1,0],quad q=[0.1,0.7,0.2]
$$

则：

$$
q-p=[0.1,-0.3,0.2]
$$

直觉：

- 错误类别概率过高 → 往下压；
- 正确类别概率不够 → 往上推。

然后链式法则把这个误差继续向前传：

```text
Loss
 ↓
logits
 ↓
最后一层
 ↓
Transformer
 ↓
Embedding
 ↓
所有可训练参数
```

优化器再按梯度更新参数。

## 不要把“反向传播”理解成模型倒着生成文字

Backpropagation 只是：

> **从 loss 出发，沿计算图反向求导。**

---

# 8. Attention：把“串行记忆”变成“可学习检索”

RNN 可粗略理解为：

```text
x1 → h1 → h2 → h3 → h4 → ...
```

很远的信息要经过很多步传递。

Transformer 的核心变化：

> **每个 token 可以直接检索其他 token。**

核心公式：

$$
Attention(Q,K,V)=softmax(QK^T/√d_k)V
$$

把它拆成三步就不神秘了：

```text
QKᵀ
 ↓
“我该看谁？”
 ↓ softmax
注意力权重
 ↓ × V
“把对方的信息拿回来”
```

---

# 9. Q / K / V 为什么这样设计

最重要的记忆：

$$
Q = 我想找什么
$$

$$
K = 别人怎样找到我
$$

$$
V = 找到我以后，我给什么
$$

例句：

```text
The animal didn't cross the street because it was too tired.
```

处理 it 时，概念上：

- Q_it：我需要找一个可能是我先行词的实体；
- K_animal：我是一个可被指代的实体；
- V_animal：我携带 animal 的实际上下文信息。

先算：

$$
Q_{it} · K_{animal}
$$

如果匹配高，就多读取：

$$
V_{animal}
$$

## 为什么 K 和 V 分开？

因为：

> “是否值得被检索的特征” ≠ “真正需要传递的内容”。

数据库也是：

```text
key      → value
user_123 → 用户完整资料
```

## 为什么 Q 和 K 也分开？

如果直接用同一个空间：

$$
x_i^T x_j = x_j^T x_i
$$

关系天然对称。

但语言很多关系有方向：

- 代词 → 先行词；
- 动词 → 宾语；
- 当前 token → 前文条件。

使用：

$$
Q_i=x_iW_Q,quad K_j=x_jW_K
$$

可以学到更一般的、有方向的匹配关系。

---

# 10. 为什么用点积 QKᵀ，为什么除以 √dₖ

## 10.1 为什么点积好用

点积同时具备：

- 能表达方向/对齐程度；
- 可以一次矩阵乘法算所有 token 两两关系；
- GPU 对大矩阵乘法极其擅长。

设序列长度 n：

$$
Q ∈ R^{n×d_k},quad K ∈ R^{n×d_k}
$$

则：

$$
QK^T ∈ R^{n×n}
$$

一次就得到整张“谁关注谁”的关系矩阵。

## 10.2 为什么除以 √dₖ

如果 Q、K 每维大致独立、方差差不多，那么 dₖ 越大，点积的波动范围通常越大。

结果会导致 softmax 输入过大：

```text
[0.1, 0.2, 12.0]
        ↓ softmax
[≈0, ≈0, ≈1]
```

分布过早饱和，梯度容易变得很小。

除以：

$$
√d_k
$$

是在控制点积的尺度，让 softmax 工作在更稳定的区间。

一句话：

> **√dₖ 不是为了“让概率和为 1”，而是为了防止维度增大后 attention score 过爆。**

---

# 11. Multi-Head Attention：一套检索规则不够

每个 head 都有自己的投影：

$$
W_Q^{(h)},W_K^{(h)},W_V^{(h)}
$$

因此模型可以同时在多个关系子空间里做检索。

可以把它想成：

> 同一段文本，同时交给多名“检索员”，每个人从不同角度找关系。

不要机械地说“第 1 个头一定负责语法”。更准确是：

> **多头给模型多套可学习的关系视角。**

最后各头结果拼接，再经过输出投影整合。

---

# 12. 位置编码：Attention 本身不知道谁先谁后

## 12.1 为什么必须额外加入位置

只看 token 内容时，self-attention 本身不会天然知道：

```text
我 爱 你
你 爱 我
```

谁在第 1 位、谁在第 3 位。

所以必须注入位置信息。

---

## 12.2 原始 Transformer 为什么用 sin / cos

经典正弦位置编码：

$$
PE(pos,2i)=sin(pos / 10000^{2i/d})
$$

$$
PE(pos,2i+1)=cos(pos / 10000^{2i/d})
$$

白话：

> **给不同维度配不同转速的“钟表”。**

- 高频维度变化快 → 对近距离位置敏感；
- 低频维度变化慢 → 覆盖更长尺度。

很多不同频率组合在一起，就能形成丰富的位置表示。

## 为什么 sin 和 cos 成对？

因为：

$$
sin(a+b)=sin a cos b + cos a sin b
$$

$$
cos(a+b)=cos a cos b - sin a sin b
$$

所以“从位置 a 平移 b”可以由一个只和 b 有关的线性变换表示。

这让相对位移结构很自然。

---

## 12.3 10000 是什么神秘常数吗？

不是物理常数。

它只是原始设计中用于把频率覆盖到很宽范围的尺度基数。

重要思想不是“10000”，而是：

> **用一组从快到慢的频率覆盖不同位置尺度。**

---

## 12.4 RoPE：把“位置”直接变成 Q/K 的旋转

现代 decoder LLM 常用 RoPE 或其变体。

直觉上：

> 不是单独给 token 加一个位置向量，而是根据位置对 Q、K 的不同二维子空间做旋转。

这样点积时能自然带入相对位置信息。

你不需要一开始记复杂公式，只要记：

> **Sin/Cos：用周期函数编码位置；RoPE：进一步把这种旋转结构直接融合进 Q/K。**

---

# 13. Causal Mask：它和位置编码完全不是一回事

这两个经常混。

## 位置编码解决

> **“你在第几个位置？”**

## Causal Mask 解决

> **“你允许看哪些位置？”**

GPT 预测第 t 个 token 时不能偷看未来。

所以 Attention score 会对未来位置加一个极大负数，概念上：

```text
token1: 看 1
token2: 看 1 2
token3: 看 1 2 3
token4: 看 1 2 3 4
```

Softmax 后，被 mask 的未来位置概率接近 0。

一句话：

> **位置编码提供顺序信息；因果 Mask 执行信息访问权限。**

---

# 14. 一个完整 Transformer Block 到底做什么

现代 decoder block 可以先压成：

```text
输入 X
 ↓ Norm
Attention
 ↓
Residual Add
 ↓ Norm
MLP / FFN
 ↓
Residual Add
= 输出
```

## 14.1 Attention：负责“token 之间交流”

它让一个位置读取其他位置的信息。

## 14.2 MLP / FFN：负责“每个位置内部加工”

Attention 之后，每个 token 得到了一份融合上下文的信息。

MLP 再对每个位置独立做非线性变换。

白话：

> Attention 像“开会交换信息”；MLP 像“每个人会后自己消化”。

## 14.3 Residual：为什么要残差

形式近似：

$$
Y = X + F(X)
$$

不是要求新层把旧表示全部重写，而是：

> **在原信息上学习“增量修改”。**

这会让深网络更容易优化，也避免信息每层都被彻底洗掉。

## 14.4 Norm：为什么要归一化

LayerNorm / RMSNorm 的核心作用可以先记为：

> **控制激活尺度，让深层网络训练更稳定。**

不需要把它理解成“让数据服从正态分布”。

---

# 15. 训练时，模型到底看见了什么

假设文本是：

```text
我 喜欢 学习 AI
```

训练样本在概念上是：

```text
输入: 我
目标: 喜欢

输入: 我 喜欢
目标: 学习

输入: 我 喜欢 学习
目标: AI
```

但 Transformer 训练时不会真的一条一条串行跑。

借助 causal mask，可以一次把整段送进去，并行计算所有位置的 loss：

```text
位置1预测位置2
位置2预测位置3
位置3预测位置4
...
```

这就是为什么：

> **训练可以高度并行，但自回归推理仍然串行。**

## Teacher Forcing

训练时，每个位置看到的是数据集里的真实前文，而不是模型刚刚自己生成的前文。

这就是 teacher forcing 的核心直觉。

---

# 16. 预训练、SFT、偏好优化：分别在改变什么

## 预训练

目标通常是海量 next-token prediction。

学到：

- 语言规律；
- 世界模式；
- 代码模式；
- 部分推理模式。

## SFT（监督微调）

继续用“输入 → 目标回答”训练，让模型学会：

- 指令格式；
- 任务风格；
- 特定领域行为。

## 偏好优化

核心不是简单告诉模型“标准答案是哪一个 token”，而是让模型更偏好某些完整行为/回答。

可以先把它理解成：

> 预训练学“会说话和建模世界”，SFT 学“按要求做事”，偏好优化学“哪些行为更符合目标偏好”。

---

# 17. 推理为什么分 Prefill 和 Decode

这是理解 LLM 性能的关键。

## 17.1 Prefill

用户一次输入很长 prompt。

模型可以并行处理整段输入，建立每层的 K/V 状态。

特点：

- 一次处理很多 token；
- 矩阵乘法规模大；
- GPU 通常利用率较高。

## 17.2 Decode

开始生成后：

```text
生成 token1
 ↓
把 token1 加入上下文
 ↓
生成 token2
 ↓
...
```

每一步通常只新增一个 token。

特点：

- 串行；
- 每步计算量相对小；
- 但要访问大量模型权重与历史状态；
- 常更受内存带宽和串行依赖限制。

---

# 18. KV Cache：为什么不用每生成一个 token 就重算整段历史

在第 t 步生成时，过去 token 的 K、V 已经算过。

如果每次重新算：

```text
历史 1..t 全部重算
```

会非常浪费。

所以缓存每层过去 token 的：

```text
K₁...Kₜ
V₁...Vₜ
```

下一步只需为新 token 算新的 Q、K、V，再让新 Q 去和缓存的 K 做匹配。

这就是 KV Cache。

## 它解决了什么？

> **减少重复计算。**

## 它带来了什么新成本？

> **显存占用随序列长度增长。**

所以长上下文推理常常不是只看 FLOPs，还要看 KV Cache 内存与带宽。

---

# 19. 为什么自回归生成慢

自回归概率链：

$$
P(x_1,...,x_T)=Π_t P(x_t|x_{<t})
$$

第 t 个 token 必须依赖已经确定的前文。

于是：

```text
token1 → token2 → token3 → ... → tokenT
```

这条依赖链决定了：

> **即使单步很快，T 个 token 仍然需要大量顺序轮次。**

所以 AR 的核心优势与代价是同一件事：

- 优势：每一步都基于已经确定的全部历史；
- 代价：下一步要等上一步结果。

---

# 20. 自回归 vs 半自回归 / 块生成：谁更有优势

没有绝对赢家，优化目标不同。

## 自回归 AR

每次通常确定 1 个 token。

优势：

- 因果定义直接；
- 条件依赖最自然；
- 训练与推理范式成熟；
- 对代码、长文本、复杂条件生成非常稳健。

代价：

- decode 串行深度约等于生成长度 T。

## 块式 / 半自回归思路

希望一次推进多个 token：

```text
[token1 ... tokenK]
        ↓
[next K tokens]
```

优势：

- 减少串行轮数；
- 更容易发挥 GPU 并行能力。

难点：

- 块内后面的 token 理论上应该依赖块内前面已经确定的 token；
- 如果同时猜，如何保持这种因果依赖？

所以一般存在一个核心张力：

> **并行得越激进，越需要解决“块内依赖”和“质量校验”。**

---

# 21. Speculative Decoding：草稿先猜，目标模型把关

这是非常重要的一类折中。

流程可以理解成：

```text
小/快 Draft 模型
 ↓ 一次猜 K 个 token
候选块
 ↓
大/准 Target 模型一次并行验证
 ↓
能接受的连续前缀直接收下
 ↓
遇到不接受处再纠正
```

例如 draft：

```text
[wooden, chair, near, the, window]
```

target 一次验证：

```text
wooden ✓
chair  ✓
near   ✓
the    ✓
window ✗
```

那一次 target 验证就可能推进多个 token。

## 为什么它可能不牺牲目标分布？

严格的 speculative sampling 会设计接受/拒绝与修正机制，使最终采样分布保持与 target 模型一致。

所以这里要区分：

- **直接并行预测多 token**：可能改变输出分布；
- **带严格验证/修正的 speculative decoding**：可以在理论上保持 target 分布。

## 真正决定加速的是什么？

不是块越大越好，而是综合：

- draft 成本；
- target 验证成本；
- acceptance rate；
- 一次平均接受多少 token。

一句话：

> **投机解码赚的是“用一次昂贵 target 前向，确认多个便宜猜测”。**

---

# 22. Diffusion / 块生成该放在什么知识位置

你可以先把生成范式分成三大类：

```text
A. 自回归
   一个接一个确定

B. 投机/块式半自回归
   一次提出多个候选，再验证/修正

C. 非自回归或扩散式文本生成
   从一组不完整/噪声状态反复迭代整体修正
```

你截图中提到的 DFlash、DSpark，如果课程把它们归在“块扩散草稿 + 投机验证 / 半自回归”附近，那么学习时先抓住这个抽象层：

> **块内尽量并行产生候选，块间或目标模型负责因果约束与验证。**

具体算法的接受规则、训练目标、块大小和是否严格保持目标 AR 分布，要以各自论文/实现为准，不要只凭“半自回归”四个字推断。

---

# 23. 为什么训练能并行，生成却不能直接全并行

这是一个非常容易混淆的问题。

训练时：

> 正确答案整段都已经存在。

所以可以把所有 token 一次送进 GPU，用 causal mask 保证每个位置只看过去。

推理时：

> 后面的真实 token 根本还不存在。

例如要生成第 100 个 token，必须先知道模型到底生成了第 99 个什么。

所以：

```text
训练：答案已知 → 可以并行算每个位置
推理：答案未知 → 默认必须逐步产生
```

这正是 speculative / block / diffusion 方法要突破的系统瓶颈。

---

# 24. 一次完整追踪：从“猫”到下一个 token

假设输入：

```text
这只猫正在
```

## 第一步：Tokenize

```text
["这", "只", "猫", "正在"]
→ token ids
```

## 第二步：Embedding

每个 id 查表，得到向量 X。

## 第三步：加入/注入位置信息

模型知道：

- “猫”是什么；
- 它位于什么相对位置。

## 第四步：进入第 1 个 Transformer Block

先算：

$$
Q=XW_Q,quad K=XW_K,quad V=XW_V
$$

再算：

$$
score=QK^T/√d_k
$$

加 causal mask 后 softmax，得到 attention weights。

再：

$$
context=weights·V
$$

然后 residual、norm、MLP。

## 第五步：重复 N 层

每一层都在重新组织上下文表示。

## 第六步：LM Head

最后位置的 hidden state 映射到词表 logits：

```text
睡觉  8.1
吃饭  6.4
奔跑  4.2
...
```

## 第七步：Softmax + 采样

变成概率，再根据 greedy / temperature / top-p 等策略选出：

```text
睡觉
```

## 第八步：继续 Decode

把“睡觉”加入上下文，利用 KV Cache 继续下一步。

这就是完整的自回归生成循环。

---

# 25. 最容易混淆的 12 组概念

| 容易混淆 | 真正区别 |
|---|---|
| Token vs Embedding | Token 是离散编号；Embedding 是连续向量 |
| Logit vs Probability | Logit 是原始分数；Softmax 后才是概率 |
| Entropy vs Cross Entropy | 前者衡量 p 自己；后者用 q 去描述 p |
| Cross Entropy vs KL | CE = H(p) + KL；训练时 p 固定时最小化 CE 等价于最小化 KL |
| Q vs K | Q 表达“我要找什么”；K 表达“我如何被匹配” |
| K vs V | K 用于寻址；V 是真正被读出的内容 |
| Position vs Mask | Position 告诉顺序；Mask 决定能不能看 |
| Attention vs MLP | Attention 做 token 间通信；MLP 做位置内加工 |
| Training vs Inference | 训练答案已知，可并行；推理答案未知，要生成 |
| Prefill vs Decode | Prefill 并行吃 prompt；Decode 串行产新 token |
| KV Cache vs Parameters | KV Cache 是本次上下文中间状态；Parameters 是长期模型权重 |
| AR vs Speculative | AR 每步确定 1 个；Speculative 一次猜多个再由 target 验证 |

---

# 26. 必背公式：只保留真正有用的 9 个

### 1. Softmax

$$
q_i=e^{z_i}/Σ_j e^{z_j}
$$

### 2. 自信息

$$
I(p)=-logp
$$

### 3. 熵

$$
H(p)=-Σ_i p_i logp_i
$$

### 4. 交叉熵

$$
H(p,q)=-Σ_i p_i logq_i
$$

### 5. KL 与交叉熵

$$
H(p,q)=H(p)+D_{KL}(p||q)
$$

### 6. One-hot 语言模型 Loss

$$
L=-logP_θ(x_t|x_{<t})
$$

### 7. QKV

$$
Q=XW_Q,quad K=XW_K,quad V=XW_V
$$

### 8. Attention

$$
softmax(QK^T/√d_k)V
$$

### 9. 自回归分解

$$
P(x_1,...,x_T)=Π_t P(x_t|x_{<t})
$$

如果这 9 个公式都能用白话解释，你就不是“会背 Transformer”，而是真的开始理解它。

---

# 27. 最短学习路线：按这个顺序复习

不要按论文目录硬啃，按因果顺序：

```text
第一遍：只懂直觉
Token → Embedding → Softmax → CE → QKV → Position/Mask → Block

第二遍：补训练
Gradient → Teacher Forcing → Next Token Prediction → SFT

第三遍：补推理
Prefill → Decode → KV Cache → Sampling

第四遍：补加速
AR → Speculative → Block/Semi-AR → Diffusion-style generation

第五遍：回到数学
KL → √dₖ → RoPE → 更细的优化与架构变体
```

---

# 28. 自测：能回答这些，主干就打通了

1. 为什么 token id 不是语义数值？
2. 为什么要 embedding？
3. 为什么 logits 不直接当概率？
4. 为什么信息量用 -log p？
5. 为什么交叉熵是 -Σp log q，而不是 -Σq log p？
6. one-hot 为什么让 CE 退化成 -log qᵧ？
7. Q、K、V 为什么不是一个向量？
8. 为什么 QK 用点积？
9. 为什么除以 √dₖ？
10. 位置编码和 causal mask 的职责分别是什么？
11. Attention 与 MLP 分别解决什么问题？
12. 为什么 residual 重要？
13. 为什么训练能并行而 AR 推理不能？
14. KV Cache 缓存的到底是什么？
15. speculative decoding 为什么可能一次推进多个 token？
16. 为什么“块越大”并不一定“越快”？

如果其中任何一道答不清楚，回到对应章节，而不是继续堆新名词。

---

# 29. 最后一张脑图

```text
                  ┌──────── 概率：Softmax
Token → Embedding ┤
                  └──────── 表示：Transformer
                              │
                    ┌─────────┴─────────┐
                    │                   │
              Attention             MLP / FFN
                    │
           Q / K / V + Position
                    │
              Causal Mask
                    │
              上下文表示 H
                    │
                 LM Head
                    │
                 Logits
                    │
                Softmax
                    │
          ┌─────────┴─────────┐
          │                   │
       Training             Inference
          │                   │
 Cross Entropy        Prefill → Decode
          │                   │
 Backprop              KV Cache
          │                   │
更新参数           AR / Speculative / Block
```

---

# 30. 一句话毕业

**LLM 本质上是在高维向量空间里，用 Attention 动态检索上下文，用 Transformer 层不断重写表示，再把最终表示转成“下一个 token 的概率”；训练靠交叉熵和梯度把正确 token 的概率推高，推理则在因果约束下逐步生成，而现代加速方法的核心就是尽量减少这条逐 token 串行链。**
