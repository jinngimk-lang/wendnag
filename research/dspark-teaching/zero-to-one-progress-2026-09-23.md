# DSpark 从 0 到 1 学习文档｜进度节点 2026-09-23

## 用户目标
基于已完成的《DSpark 教学讲义 · 白话核对版》，重新做一份“从 0 到 1 带我学”系列学习文档：
- 初学者友好，白话优先；
- 高浓缩，但不能牺牲数学/算法准确性；
- 每一章都回答“为什么、是什么、怎么算、用来干什么”；
- 必须保留关键公式、图示、数值例子与易错点；
- 不能把教学示意误写成论文/代码真实参数；
- 论文理论与官方 DeepSpec 工程实现要明确区分；
- 需要在上下文压力大时把进度写入本仓库，并从进度点重新读取后继续精炼。

## 事实基线（不得回退）
1. 标准 speculative sampling 单位置接受率：
   P(accept x_k)=min(1,p_t(x_k)/p_d(x_k))。
2. 首次拒绝后，后续 draft suffix 本轮不能继续作为连续 accepted prefix；拒绝位置使用 residual/rejection correction，不是简单 Target argmax。
3. DSpark 一轮：Target anchor → Parallel Block → Sequential Head → Confidence Head → STS calibration → Hardware-Aware Prefix Scheduler → Target verification。
4. Eq.(4)：最终 draft 分布来自 base logit U_k 与 prefix correction B_k 相加后 Softmax。
5. Vanilla Markov Head：
   B(x_{k-1},·)=W1[x_{k-1}]W2，W1∈R^{V×r}, W2∈R^{r×V}；官方代码对应 nn.Embedding(V,r)+nn.Linear(r,V,bias=False)。
6. Confidence c_k 是“前 1..k-1 已通过条件下，第 k 个也通过”的条件接受概率，不是 token correctness。
7. 软标签：c_k*=1-1/2||p_k^d-p_k^t||_1。
8. Prefix survival：a_{r,j}=∏_{i≤j}c_{r,i}。
9. Scheduler：B=Σ_r(1+ℓ_r)，τ=Σ_r(1+Σ_{j=1}^{ℓ_r}a_{r,j})，Θ=τ·SPS(B)；greedy admission 第一次吞吐下降即停止。全局最优保证依赖 Θ 沿 greedy path 近似单峰/硬件 capacity curve 足够平滑。
10. 三个训练损失：
   - L_ce=-Σ w_k log p_k^d(x_k*)
   - L_tv=Σ w_k ||p_k^d-p_k^t||_1（论文 Eq.10 没有 1/2）
   - L_conf 为 soft label c_k* 的 BCE
   - 总损失 α_ce L_ce + α_tv L_tv + α_conf L_conf，论文默认 α_ce=0.1, α_tv=0.9, α_conf=1.0。
11. 位置权重论文写 w_k=exp(-(k-1)/γ)；DeepSpec 代码实现是 exp(-position/loss_decay_gamma)，公开 block7 config 中 loss_decay_gamma=4.0，因此工程实现不必数值等于论文 γ。
12. 论文默认 Markov rank r=256；官方代码另有 gated 与 RNN 变体。

## 新文档拟定结构（高浓缩版）
1. 先不学 DSpark：先懂普通自回归为什么慢
2. 推测解码：小模型先写草稿，大模型一次验一段
3. DSpark 要解决的真正矛盾：纯并行很快，但 suffix decay
4. 一轮 DSpark：6 个模块串起来
5. 核心公式一：U_k + B_k 为什么能“并行后纠错”
6. 核心公式二：Markov 低秩 W1/W2
7. Confidence：它预测的到底是什么
8. Prefix survival：为什么 70% 最后会变 50.4%
9. Scheduler：为什么不是 draft 越长越好
10. 三个 Loss：猜对、猜像、知道自己靠不靠谱
11. 论文 vs 代码：必须分清的 6 个点
12. 终极复盘：一张图 + 8 句话 + 自测题

## 教学表达原则
- 每章固定四层：一句话 → 白话类比 → 公式拆解 → 具体数值例子。
- 术语第一次出现就给中文解释。
- 只保留对理解 DSpark 有用的公式，不堆不必要证明。
- 使用“主干负责快 / 顺序小头负责连贯 / confidence 负责估风险 / scheduler 负责算值不值 / target 负责守门”的统一类比。
- 对所有示意数值标“教学示意”。
- 最终文档要单独放“高频误区纠错框”。

## 后续动作
1. 先从本节点重新读取，确认关键事实未漂移；
2. 生成 0→1 高浓缩 DOCX；
3. 渲染全部页面逐页检查；
4. 修复任何公式、表格、分页、字体、图示问题；
5. 最终交付 DOCX。
