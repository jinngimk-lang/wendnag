# DSpark 从0到1白话学习文档｜精炼节点 2026-09-24

## 当前目标
把上一版 14 页《DSpark 从0到1｜白话高浓缩学习文档》继续精炼成“真正能带着初学者从零学会”的版本。

## 不变事实基线
- speculative sampling 单位置接受率：P(accept x_k)=min(1,p_t(x_k)/p_d(x_k))
- 首次拒绝后，后续 draft suffix 本轮不能继续作为连续 accepted prefix
- 拒绝位置走 residual/rejection correction，不是直接 Target argmax
- DSpark 一轮：Target anchor → Parallel Block → Sequential Head → Confidence Head → STS calibration → Hardware-Aware Prefix Scheduler → Target verification
- Eq.(4)：Softmax(U_k+B_k)
- Vanilla Markov：B(x_{k-1},·)=W1[x_{k-1}]W2，W1∈R^{V×r}, W2∈R^{r×V}
- c_k 是条件接受概率，不是 token correctness
- c*_k=1-1/2||p^d_k-p^t_k||_1
- a_{r,j}=∏_{i≤j}c_{r,i}
- B=Σ_r(1+ℓ_r)，τ=Σ_r(1+Σ_{j=1}^{ℓ_r}a_{r,j})，Θ=τ·SPS(B)
- L_ce=-Σw_k log p^d_k(x*_k)
- L_tv=Σw_k||p^d_k-p^t_k||_1，论文 Eq.(10) 没有 1/2
- L_conf 是以 c*_k 为 soft target 的 BCE
- 总损失默认 α_ce=0.1、α_tv=0.9、α_conf=1.0
- 论文位置权重 w_k=exp(-(k-1)/γ)；DeepSpec 实现可配置 exp(-position/loss_decay_gamma)
- 论文默认 Markov rank r=256；官方实现另有 gated/RNN 变体
- scheduler 的“第一次吞吐下降就 break”全局最优保证依赖 greedy path 上 Θ 近似单峰/硬件 capacity curve 足够平滑

## 精炼原则
1. 从“普通自回归为什么慢”开始，不默认读者懂 speculative decoding。
2. 每章固定四层：一句话 → 白话类比 → 公式 → 具体数值。
3. 每章结尾加“你现在应该会什么”，形成学习闭环。
4. 只保留 8 个真正需要记忆的公式，其余用图示/文字解释。
5. 整个文档只保留一套统一类比：
   - Parallel：快速打草稿
   - Sequential：轻量校对
   - Confidence：估计老师会不会通过
   - Calibration：把估计校准
   - Scheduler：算“多验一个值不值”
   - Target：最终守门
6. 所有教学数字必须标注“教学示意”。
7. 重点突出三组最易混淆概念：
   - correctness vs acceptance
   - c_k vs a_j
   - Eq.(8) 的 1/2 vs Eq.(10) 无 1/2
8. 论文定义与 DeepSpec 工程实现分栏，避免把实现细节说成理论必然。
9. 最终控制在约 12–14 页，信息密度高但不挤。
10. 必须做 DOCX render → 逐页视觉检查 → 修复 → 再 render。

## 目标章节
0. 30 秒总览：DSpark 解决什么
1. 普通自回归为什么慢
2. 推测解码为什么能加速
3. 纯并行为什么出现 suffix decay
4. DSpark 一轮六步
5. U_k+B_k：并行后纠错
6. W1/W2：低秩 Markov 小头
7. Confidence + STS：估风险并校准
8. Prefix Survival：c 与 a 的区别
9. Scheduler：Θ=τ·SPS(B)
10. 三个 Loss + 位置权重
11. 论文 vs 代码
12. 8 句话复盘 + 自测

## 交付标准
- 初学者可从头顺读，不需要先看原论文
- 关键公式全部有符号解释
- 至少包含：总流程图、suffix-decay 图、Markov 低秩图、confidence 图、scheduler 图、loss 图
- 无截断、无重叠、无乱码、无公式断行
- 文末给“复习路线”和“常见误区”
