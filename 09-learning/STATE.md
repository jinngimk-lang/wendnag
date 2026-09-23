# LLM 从 0 到 1 学习项目 — STATE

## 目标
制作一份“白话、高浓缩、从 0 到 1”的 LLM / Transformer 学习主文档。核心不是堆术语，而是让读者能够回答每个核心设计的“为什么”。

## 本学习流与仓库其他工作的隔离
- 仅写入 `09-learning/`。
- 不修改 BP、投资人 Deck、公司事实或既有业务材料。
- 当前工作分支：`docs/llm-zero-to-one-20260923`。

## 用户已重点追问
1. 交叉熵为什么有方向差异，为什么是 `-log q`。
2. Attention 为什么设计 Q / K / V。
3. 位置编码为什么使用 sin / cos；它与 causal mask 的职责差异。
4. 自回归与半自回归 / 块并行 / speculative decoding 各自优势是什么。

## 写作规范
每个核心概念尽量按以下顺序：
1. 一句话先懂
2. 白话直觉
3. 最少必要公式
4. 为什么这样设计
5. 最容易混淆
6. 一眼复习

## 计划主线
文字 → Token → Embedding → Logits/Softmax → 熵/交叉熵/KL → 梯度 → Attention/QKV → 位置/Mask → Transformer Block → 训练 → Prefill/Decode/KV Cache → 自回归/并行/投机解码 → 端到端复盘。

## 进度策略
系统无法提供精确“上下文剩余 30%”遥测，因此按仓库既有规则，用“约完成第一有效三分之一时的保守 checkpoint”替代，不假装知道精确百分比。
- Checkpoint A：完成基础、概率、损失、QKV。
- 写入 Git。
- 重新读取 Checkpoint A。
- 在其基础上继续完整化并压缩。
- Final：保留一份主文档 + 一份状态文件。

## 当前状态
准备写入 Checkpoint A。
