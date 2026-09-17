# DSpark 教学文档｜LATEST

> 本文件是当前 DSpark 教学文档的最新恢复点；如与 `STATE.md` 冲突，以本文件为准。
> 用户后续说“继续”时，应先读取本文件，再继续，不要求用户重复前文。

## 当前终版产物

- 文件名：`DSpark_教学讲义_最终版.docx`
- 生成/终审日期：2026-09-17
- 页数：20 页
- SHA-256：`25cbf804c60704e8de0cf0b3d5a725a8c1914bf9416cd5ba4b9aedede483492e`
- 生成时本地路径：`/mnt/data/DSpark_教学讲义_最终版.docx`（跨会话可能失效，因此内容状态以本恢复点为准）

## 用户要求

- 面向初学者，解释必须足够白话，但数学/算法不能失真；
- 必须有公式、图示/图标、完整流程、数值例子；
- 每个关键符号都要解释；
- 要区分论文理论公式和官方实现；
- 交付前必须做多轮数学、算法、代码一致性、排版和可读性审核；
- 用户强调“文档一定不能有问题”，不能把猜测写成事实。

## 最终 QA 状态

- DSpark 论文公式核对：PASS，依据 arXiv `2607.05147v1` 的 Eq. 1、Eq. 4–12 与 Algorithm 1；
- 官方 DeepSpec 代码核对：PASS，重点核对 `markov_head.py`、`common.py`、`qwen3/modeling.py`、`loss.py` 与公开 DSpark config；
- 数值例子复算：PASS；
- DOCX 包完整性：PASS（`unzip -t` 无错误）；
- 跟踪修订/批注：无；
- 最终渲染：20 页，逐页检查；
- 真实修复项：此前第 1、3 页重复的 DSpark 流程图下部三个说明框文字有重叠，已重做并重新渲染确认无重叠。

## 已确认的关键正确性结论

### 1. Parallel + Sequential

- Parallel Block 一次生成一整块位置的基础 hidden/logits；
- Sequential Block 用轻量 prefix-dependent bias 左到右修正，不重跑完整大网络；
- Vanilla Markov 头对应：
  `B(x_{k-1}, ·) = W1[x_{k-1}] W2`，其中 `W1∈R^{V×r}`，`W2∈R^{r×V}`；
- 官方 DeepSpec 实现中 `W1` 是 `nn.Embedding(V,r)`，`W2` 是无 bias 的 `nn.Linear(r,V)`；
- 官方代码还提供 gated 与 RNN 版本，RNN 可以携带更长的 block 内前缀状态。

### 2. Confidence Head

论文公式：
`c_k = σ(w^T [h_k ; W1[x_{k-1}]])`。

- `c_k` 表示：在前面的 draft token 已接受条件下，第 k 个 draft token 通过 target verification 的条件存活概率；
- 它不是“token 是语义正确答案的概率”；
- Prefix survival 是 `a_{r,j}=∏_{i≤j} c_{r,i}`，不要与单位置 `c_k` 混淆；
- 官方代码 `AcceptRatePredictor` 是单线性层输出 raw logit，解释为概率时再 sigmoid；
- `confidence_head_with_markov=True` 时，特征是 backbone hidden state 与 Markov previous-token embedding 的拼接。

### 3. Acceptance soft target

`c_k* = 1 - 1/2 ||p_k^d - p_k^t||_1`。

这里的 `1/2` 必须保留，它把 L1 距离转成 Total Variation distance，并对应理论单位置 acceptance probability。

### 4. 三个训练损失

- Eq. 9：`L_ce = -Σ w_k log p_k^d(x_k*)`；
- **关键纠错：论文 Eq. 10 写的是完整加权 L1：**
  `L_tv = Σ w_k ||p_k^d - p_k^t||_1`，**没有 `1/2`**；
- Eq. 11：confidence BCE，soft target 是上面的 `c_k*`；
- Eq. 12：`L = α_ce L_ce + α_tv L_tv + α_conf L_conf`；
- 论文默认权重经核对：`α_ce=0.1`、`α_tv=0.9`、`α_conf=1.0`；
- 官方 DeepSpec `loss.py` 的 `l1_loss` 也是完整 L1，与论文 Eq. 10 一致。

### 5. 位置权重：论文 vs 代码必须区分

论文写：
`w_k = exp(-(k-1)/γ)`。

官方代码实现更一般：
`exp(-position / loss_decay_gamma)`。

公开 `dspark_qwen3_4b.py` 配置中：
- `block_size=7`
- `loss_decay_gamma=4.0`

因此当前公开实现中这两个量并不总是相等。教学文档必须明确“论文公式”和“可配置工程实现”是两个层次，不能把它们说成永远数值相同。

### 6. Speculative verification

- 接受的是连续前缀；一旦首次拒绝，后面的 draft suffix 不能继续作为本轮 accepted prefix；
- 标准 speculative decoding 接受概率为 `min(1, p_t(x)/p_d(x))`；
- 被拒绝位置的替代 token 来自 rejection/residual correction 规则，不能写成“直接取 Target argmax”；
- “lossless”是指正确的验证/残差采样保持 Target Model 的目标输出分布，不等于 draft 每个 token 都正确。

### 7. Hardware-Aware Prefix Scheduler

- `a_{r,j}=∏_{i≤j} c_{r,i}`；
- `B = Σ_r (1+ℓ_r)`；
- `τ = Σ_r (1 + Σ_{j=1}^{ℓ_r} a_{r,j})`；
- `Θ = τ · SPS(B)`；
- 所有 `(r,j)` 按 `a_{r,j}` 降序，全局逐个 admission；
- 每加入一个 token，`B←B+1`、`τ←τ+a_{r,j}`，重新计算 `Θ`；
- 第一次吞吐下降就 early stop；
- early stop 与 non-anticipating causality 有关；论文对“获得全局最大值”的保证依赖吞吐目标近似单峰/平滑容量曲线这一条件，工程系统若曲线不平滑需要额外处理，不能无条件说“必然得到全局最优”。

### 8. STS 校准

论文在 Confidence Head 后做 Sequential Temperature Scaling：沿前缀从左到右校准 cumulative survival probability，在 held-out validation data 上用一维搜索最小化 ECE；校准不改变 confidence 排序，只改善概率值的可靠性。

## 文档最终结构（20 页）

1. 封面 + 总流水线 + Eq. 10 关键纠错提示
2. 学习地图 + 标准 speculative decoding / Eq. 1
3. rejection/residual correction + 完整流水线
4. Parallel Block 的 suffix-decay 直觉
5. Eq. 4 + Markov Sequential Head
6. `W1/W2` 低秩图 + 代码映射 + Like/Apple/Banana 数值例子
7. 完整数值过程 + RNN 变体 + Eq. 7
8. Confidence Head 详解 + Eq. 8 + paper/code 对照
9. STS + prefix survival
10. Hardware-Aware Scheduler 核心公式
11. Scheduler 数值例子 + throughput 曲线
12. Algorithm 1 逐行解释 + early-stop 条件与 caveat
13. 三个 loss + 位置权重可视化
14. Eq. 9–12 + Eq. 10 无 `1/2` 的重点纠错
15. 位置权重含义 + 论文/代码 gamma 区别
16. 全流程总复盘表
17. 常见误区 + 符号表
18. 8 句话复习 + 自测题 + 审核说明
19. 审核表 + 论文/代码 cross-check
20. 参考来源 + 推荐复习顺序

## 后续恢复规则

用户以后说“继续”时：

1. 先读本文件；
2. 如当前会话仍可访问 `DSpark_教学讲义_最终版.docx`，从该文件继续；
3. 如文件已不可访问，则用本文件 + `STATE.md` 重建，不要求用户重述；
4. 任何后续修改不得回退本文件列出的关键纠错，尤其是：
   - Eq. 10 **没有** `1/2`；
   - Eq. 8 **有** `1/2`；
   - position weight 的论文写法与代码可配置写法要区分；
   - `c_k` 是条件 acceptance/survival，不是 token correctness；
   - rejected-token correction 不是 Target argmax；
   - scheduler 的 early-stop 最优性有条件。
5. 如继续扩充内容，优先以 DSpark 论文和 `deepseek-ai/DeepSpec` 官方代码作为事实源。
