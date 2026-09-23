# LLM 从 0 到 1 学习项目 — STATE

## 目标
制作一份“白话、高浓缩、从 0 到 1”的 LLM / Transformer 学习主文档。核心不是堆术语，而是让读者能够回答每个核心设计的“为什么”。

## 仓库隔离
- 学习流仅写入 `09-learning/`。
- 不修改 BP、投资人 Deck、公司事实或既有业务材料。
- 工作分支：`docs/llm-zero-to-one-20260923`。

## 已确认的用户学习重点
1. 交叉熵正反方向差异，以及为什么是 `-log q`。
2. Q / K / V 为什么拆分。
3. sin/cos 位置编码从何而来，位置编码与 causal mask 的职责差异。
4. 自回归与半自回归 / 块并行 / speculative decoding 的优势与代价。

## 持久化节点
- Checkpoint A 已提交：基础 → 概率 → Cross Entropy/KL → Attention/QKV。
- Checkpoint A 后已按要求从 Git 重新读取 `STATE.md` 与主文档，再继续工作。
- 最终版在重新读取后完成了去重、术语纠偏和高浓缩重构。
- Final QA 已再次检查公式渲染并修复转义问题；主文档当前为可审阅版本。

## 最终主文档
`09-learning/LLM_FROM_ZERO_TO_ONE.md`

覆盖：
- Token / Embedding / Matrix Projection
- Logits / Softmax / Temperature
- log / Entropy / Cross Entropy / KL
- Gradient / Backprop
- Attention / QKV / scaled dot-product / Multi-Head
- Sin/Cos / RoPE / Causal Mask
- Transformer Block / Residual / Norm / MLP
- Next-token training / Teacher Forcing / SFT / preference optimization
- Prefill / Decode / KV Cache
- AR / block / semi-AR / speculative / diffusion-style generation
- 端到端 token 追踪
- 12 组易混概念、9 个核心公式、16 道自测题

## 重要准确性说明
- “半自回归”不是单一统一算法；具体块内依赖、验证机制、是否保持目标 AR 分布，要看具体方法。
- 严格 speculative sampling 可以通过接受/拒绝与修正机制保持 target 分布；普通“多 token 并行预测”不自动具备这一性质。
- DFlash / DSpark 在主文档中只放在“块/扩散草稿 + 验证”的概念抽屉中，不对未核实的具体算法细节做推断。
- 原始 Transformer 的固定 Sin/Cos 位置编码与现代 RoPE 是相关但不同的机制。

## 后续扩展方向
如继续深入，建议顺序：
1. 手算一个 4-token Attention；
2. 手算 softmax + cross entropy 梯度；
3. 展开 RoPE 二维旋转；
4. 推导 KV Cache 的显存量；
5. 对比 MHA / MQA / GQA；
6. 再进入 FlashAttention、量化、MoE、长上下文与推理系统。
