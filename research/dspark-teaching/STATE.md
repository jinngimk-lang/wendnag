# DSpark 教学文档｜持续上下文存档

> 用途：当聊天上下文过长或换新会话时，先读取本文件，再继续 DSpark 教学文档的制作、核对与改稿。
> 用户指令：用户后续只要说“继续”，优先从本文件恢复任务状态，不让用户重复需求。

## 1. 最终目标

制作一份面向初学者的 **DSpark 教学文档**，要求：

- 把当前对话里已经讲过的 DSpark 信息全部整合成一份完整、连贯的教学材料；
- 必须包含公式、图示/图标、流程图、例子；
- 解释要“白话”，但不能牺牲数学和算法准确性；
- 公式中的每个符号都要解释；
- 对容易混淆的概念给出对比；
- 文档在交付前要进行多轮审核：数学审核、算法逻辑审核、代码/论文一致性审核、排版审核、初学者可读性审核；
- 用户强调：**文档一定不能有问题**，不能把猜测写成事实。

## 2. 当前已有成品

当前会话已经生成过：

- `DSpark_教学讲义_白话核对版.docx`

本地会话路径曾为：

- `/mnt/data/DSpark_教学讲义_白话核对版.docx`

该路径跨会话不保证持续存在，所以以后恢复任务时以本文件和仓库文本状态为准；若需要继续编辑 DOCX，应先检查当前会话附件/工作区是否仍有该文件。

该 DOCX 已经至少做过一轮渲染检查，曾渲染出 18 页页面图并人工检查版式。后续仍需继续做内容核对和最终 QA。

## 3. 用户提供并已讲解的核心内容

### 3.1 并行生成 + logit 修正

核心概率分解：

```text
P(X | x0) = Π_{k=1..γ} p_k(x_k | x0, x_<k)
```

每个位置的修正后分布：

```text
p_k(v | x0, x_<k)
= exp(U_k(v) + B_k(x0, x_<k, v))
  / Σ_{u∈V} exp(U_k(u) + B_k(x0, x_<k, u))
```

白话解释：

- `U_k(v)`：Parallel Block 对候选 token `v` 的原始 logit（原始打分）；
- `B_k(...)`：Sequential Block 根据前文给这个候选 token 的“加分/减分”；
- `U+B`：修正后的最终 logit；
- Softmax：把最终 logit 变成概率。

核心一句话：

> 先并行快速猜多个 token，再用已经确定/前面的 token 对后续位置做轻量顺序修正。

### 3.2 一阶马尔可夫近似

为了让修正模块非常轻量，只考虑前一个 token：

```text
P(X_t | X_{t-1}, X_{t-2}, ..., X_1)
≈ P(X_t | X_{t-1})
```

白话：预测当前位置的修正，只看前一个 token，不重新看完整历史。

### 3.3 V×V 修正矩阵与低秩分解

理论上可以有一个完整 `V×V` 的修正矩阵：

- 行：上一个 token；
- 列：下一个候选 token；
- 元素：前一个 token 出现时，给候选 token 加多少/减多少 logit。

但 `V` 很大，完整矩阵参数量约 `V²`，过大。

所以使用低秩分解：

```text
B(x_{k-1}, ·) = W1[x_{k-1}] W2
W1 ∈ R^{V×r}
W2 ∈ R^{r×V}
r << V
```

白话：

1. `W1[x_{k-1}]`：查表，把前一个 token 映射成一个低维“修正信号”；
2. `W2`：把这个低维修正信号投影回整个词表，得到每个候选 token 的 logit 修正量。

重要澄清：

- `W1` 看起来像 embedding table，但这里更准确的功能是“前一个 token 对下一个位置的修正信号”；
- `W2` 是 logit projection，把修正信号展开成整个词表的加减分。

## 4. DSpark 解码流程（用户给过架构图）

示例 prompt token：`A B C`。

整体流程：

1. **Target Model** 先运行一步，生成 anchor token `D`；
2. 以 `D` 为 anchor，**Parallel Block** 一次为后面多个位置生成 logits；
3. **Sequential Block** 使用轻量顺序修正补回 token 间依赖，形成 draft tokens（示意：`E F G H`）；
4. **Confidence Head** 为每个草稿位置预测“理论上会被 Target Model 接受的概率”；
5. **Hardware-Aware Prefix Scheduler** 根据 confidence、前缀存活概率和真实硬件吞吐曲线，决定每个请求这轮验证多少个 draft token；
6. Target Model 一次验证选中的连续前缀；
7. 例如 `E ✓, F ✓, G ×`，则接受 `E,F`，并由 Target Model 给出修正 token `G*`；
8. `G*` 作为下一轮 anchor，继续循环。

关键性质：

- speculative verification 接受的是**连续前缀**，不能跳着接受；
- 前面 token 一旦拒绝，后面 draft token 不能作为本轮连续 accepted prefix 继续接受。

## 5. Confidence Head

用户给过公式：

```text
ĉ_k = σ( w^T [ h_k ; W1[x_{k-1}] ] )
```

（注意：不同材料可能把预测 confidence 记成 `c_k` 或 `ĉ_k`；最终文档要统一记号。建议：`ĉ_k` 表示预测值，`c_k*` 表示理论标签。）

白话：

- `h_k`：Parallel Block 在第 k 个位置的隐藏表示，可理解为“模型对当前位置的内部判断”；
- `W1[x_{k-1}]`：前一个 token 产生的低维修正信号；
- `[a;b]`：向量拼接（concatenation），不是乘法；
- `w^T(...)`：很小的线性评分器；
- `σ`：Sigmoid，把任意实数压到 `0~1`；
- 输出 `ĉ_k`：该 draft 位置预计被 Target Model 接受的概率。

它最终服务于 scheduler，不直接决定 token 是谁。

## 6. 三个训练损失

### 6.1 加权交叉熵 `L_ce`

```text
L_ce = - Σ_{k=1..γ} w_k log p_k^d(x_k*)
```

- `x_k*`：训练序列中第 k 个位置的 ground-truth token；
- `p_k^d(x_k*)`：draft model 给正确 token 的概率；
- 目标：让 draft 更会猜正确 token；
- 主要服务：draft quality。

### 6.2 分布匹配损失 `L_tv`

课件/论文写法：

```text
L_tv = Σ_{k=1..γ} w_k · (1/2) || p_k^d - p_k^t ||_1
```

- `p_k^d`：draft distribution；
- `p_k^t`：target distribution；
- `1/2 ||p^d-p^t||_1`：Total Variation distance；
- 目标：让 draft 整个概率分布靠近 target，而不是只让 top-1 猜对；
- 主要服务：acceptance rate。

理论位置接受概率标签：

```text
c_k* = 1 - (1/2) ||p_k^d - p_k^t||_1
```

### 6.3 Confidence loss `L_conf`

```text
L_conf = - Σ_{k=1..γ} w_k [
  c_k* log ĉ_k + (1-c_k*) log(1-ĉ_k)
]
```

- `c_k*`：根据 draft/target 分布差异得到的理论 soft acceptance label；
- `ĉ_k`：Confidence Head 的预测；
- 目标：让 Confidence Head 学会准确预估自己会不会被 target 接受；
- 主要服务：verification scheduling。

### 6.4 总损失

实现中是三者加权：

```text
L = α_ce L_ce + α_tv L_tv + α_conf L_conf
```

最终文档不要擅自写死论文默认权重，除非已从论文/官方配置再次核实。

## 7. 位置权重

用户给过：

```text
w_k = exp(-(k-1)/γ)
```

白话：越靠前的 draft token 越重要，因为 prefix verification 中前面一旦断掉，后面都失去本轮连续验收价值。

示例 `γ=4`：

- `w1 = 1`
- `w2 ≈ 0.779`
- `w3 ≈ 0.607`
- `w4 ≈ 0.472`

重要核对点：官方 DeepSpec 当前代码里的实现更一般：

```python
positions = torch.arange(block_size)
decay_weights = torch.exp(-positions.float() / float(loss_decay_gamma))
```

也就是说代码参数名是 `loss_decay_gamma`，权重形式是 `exp(-position / loss_decay_gamma)`。如果课件把 `loss_decay_gamma` 取为 block size `γ`，就得到 `exp(-(k-1)/γ)`。最终文档要把“论文公式”和“代码实现的可配置形式”区分清楚，不能混为一谈。

## 8. 官方 DeepSpec 代码核对（已完成一部分）

官方仓库：

- `deepseek-ai/DeepSpec`

已核对文件：

- `deepspec/modeling/dspark/loss.py`

已确认实现细节：

1. CE 使用 `F.cross_entropy(..., reduction="none")` 后乘位置权重；
2. draft/target 都先 `softmax`；
3. 理论 acceptance label：
   ```python
   accept_rate_3d = 1.0 - 0.5 * (draft_probs - target_probs).abs().sum(dim=-1)
   ```
   随后 clamp 到 `[0,1]`；
4. confidence target 使用上面的 `accept_rate_3d.detach()`；
5. confidence loss 用 `binary_cross_entropy_with_logits`；
6. confidence 预测概率通过 `.sigmoid()`；
7. 代码里的 L1 loss 计算的是完整 `L1` 距离：
   ```python
   (draft_probs - target_probs).abs().sum(dim=-1)
   ```
   因此如果论文把 `L_tv` 写成 `1/2 * L1`，代码中的 `l1_loss_alpha` 可能吸收了该常数因子。最终文档必须明确“论文 TV 写法”与“代码 L1 实现”差一个常数 `1/2`，不要说成代码直接逐字实现了 TV 公式。
8. 总 loss 由 `ce_loss_alpha`、`l1_loss_alpha`、`confidence_head_alpha` 加权。

## 9. Hardware-Aware Prefix Scheduler

用户给过 Algorithm 1。

### 9.1 前缀存活概率

每个请求 r 的 confidence 序列：

```text
c_{r,1}, ..., c_{r,γ}
```

前缀存活概率：

```text
a_{r,j} = Π_{i≤j} c_{r,i}
```

含义：第 j 个 draft token 真正成为可接受连续前缀的一部分，需要前 1..j 个都成功。

因为 `0≤c≤1`：

```text
a_{r,1} ≥ a_{r,2} ≥ ...
```

所以按 `a` 全局降序排序时，同一请求天然保持 prefix 顺序。

### 9.2 Scheduler 的目标

有 `R` 个活跃请求，初始：

```text
B = R
τ* = R
Θ_best = R · SPS(R)
```

- `B`：Target Model 这轮验证的总 token/batch 工作量；
- `τ`：预计本轮能产出的有效 token 数；
- `SPS(B)`：硬件在 batch size = B 时，实际 profile 得到的 Steps Per Second；
- `Θ = τ · SPS(B)`：预计有效 token throughput。

算法把所有 `(r,j)` 候选按 `a_{r,j}` 从高到低排序，每加入一个额外 draft token：

```text
B ← B + 1
τ ← τ + a_{r,j}
Θ ← τ · SPS(B)
```

若 `Θ` 继续提高，则保存当前每个请求的 prefix 长度；一旦不再提高，就停止扩张。

白话：

> 多验证一个 token 会增加“可能赚到的有效 token”，但也会增大 batch，使 GPU 每秒能跑的 step 下降；调度器寻找两者的甜点位。

## 10. 需要继续核对的重点（下一步）

继续工作时优先做下面这些，不要直接宣布最终完成：

1. 从 DSpark 论文/官方代码再次核对 Parallel Block / Sequential Block 的精确定义；
2. 核对 `B(x_{k-1},·)=W1[x_{k-1}]W2` 的精确记号、维度和是否存在位置/层相关项；
3. 核对 Confidence Head 的精确输入和符号；
4. 核对 Hardware-Aware Prefix Scheduler 的 `B`、`τ`、`SPS(B)` 定义及 early break 的理论/工程假设；
5. 核对论文中的 loss 权重超参数，不要沿用聊天里未经最终确认的数值；
6. 区分论文公式 `TV = 1/2 L1` 与当前 DeepSpec 代码的 `l1_loss`；
7. 对 DOCX 做最终公式显示检查，尤其是上下标、`||·||_1`、`∏`、`Σ`、`σ`、hat/star 记号；
8. 对 18 页排版逐页检查，确认无截断、无字体错乱、表格不跨页破损；
9. 增加/保留足够“白话类比”：校对员、老师/学生、GPU 投资决策器等；
10. 最终文档至少经过：事实核对 → 公式核对 → 数值例子复算 → 排版渲染 → 初学者可读性检查。

## 11. 继续时的推荐动作

用户下次说“继续”时：

1. 读取本文件；
2. 检查当前会话是否仍有 `DSpark_教学讲义_白话核对版.docx`；
3. 若有，按 DOCX skill 继续编辑和渲染 QA；
4. 若没有，从本文件内容恢复，必要时重新生成 DOCX；
5. 优先以 DSpark 论文/官方 `deepseek-ai/DeepSpec` 代码作为事实源；
6. 不要求用户重新解释前面的 DSpark 公式和需求。

## 12. 当前任务状态

**状态：进行中，尚未最终交付。**

已经完成：

- 多轮白话解释；
- DOCX 初版/核对版生成；
- 至少一轮 18 页渲染检查；
- `loss.py` 官方代码核对。

尚未完成：

- 全架构/调度器/置信度头的官方源逐项复核；
- 最终内容纠错；
- 最终 DOCX 二次/三次 QA；
- 正式终版交付。
