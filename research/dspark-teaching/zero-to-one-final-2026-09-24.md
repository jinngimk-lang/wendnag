# DSpark 从0到1白话学习文档｜终稿节点 2026-09-24

## 终稿产物
- 文件名：DSpark_从0到1_白话高浓缩学习版_终稿.docx
- 页数：14 页
- SHA-256：22b4d0920702fc773ad32962de8467e7e428bb8bc2873fd7b9d949eba494a740
- 生成日期：2026-09-24

## 本轮相对上一版的精炼
1. 从“普通自回归为什么慢”开始，不默认读者懂 speculative decoding。
2. 每章都加入“你现在应该会了”学习检查，形成从直觉到公式再到复述的闭环。
3. 把全文统一成一套类比：
   Parallel=快速打草稿；Sequential=轻量校对；Confidence=估风险；STS=校准；Scheduler=算值不值；Target=最终守门。
4. 关键公式改成更易读的数学表达，减少程序式下划线/花括号。
5. 在 speculative sampling 页新增数值例子：p_d=0.50、p_t=0.20 时接受率为 0.40；p_t>=p_d 时接受率为 1。
6. 保留并强化三组最易混淆概念：
   correctness vs acceptance；c_k vs a_j；Eq.(8) 有 1/2 vs Eq.(10) 无 1/2。
7. 保留 scheduler early-stop 的严格 caveat：全局最优保证依赖 greedy path 上 Θ 近似单峰/硬件 capacity curve 足够平滑。
8. 增加论文定义 vs DeepSpec 工程实现对照页。
9. 最终控制为 14 页，目标是高浓缩但不挤。

## 最终章节
0. 30 秒总览
1. 普通自回归与推测解码
2. suffix decay 与半自回归
3. U_k+B_k 并行后纠错
4. W1/W2 低秩 Markov Head
5. Confidence + STS
6. Prefix Survival
7. Hardware-Aware Scheduler
8. 三个 Loss
9. 位置权重
10. 论文 vs DeepSpec
11. D→G* 全流程脑内动画
12. 8 句话复盘 + 高频误区 + 自测

## 不得回退的事实基线
- speculative sampling 接受率 min(1,p_t/p_d)
- 首次拒绝后 suffix 不能继续作为本轮连续 accepted prefix
- rejection correction 不是直接 Target argmax
- c_k 是条件接受概率，不是 token correctness
- c*_k=1-1/2||p_d-p_t||_1
- a_{r,j}=∏_{i≤j}c_{r,i}
- L_tv 论文 Eq.(10) 是完整加权 L1，没有 1/2
- 论文默认 α_ce=0.1、α_tv=0.9、α_conf=1.0
- 论文 w_k=exp(-(k-1)/γ)；DeepSpec 工程实现是可配置 exp(-position/loss_decay_gamma)
- Markov rank 论文默认 r=256
- Scheduler 优化 Θ=τ·SPS(B)，early-stop 全局最优保证有条件

## QA
- DOCX ZIP 完整性：PASS
- 最终渲染：14 页
- 逐页视觉检查：PASS
- 最终 OOXML 可访问性补丁：为 10 张教学图补充 alt text
- 补丁前后像素级渲染 diff：14/14 页完全一致
- Comments：0
- 公式/关键纠错再次检查：PASS

## 后续恢复规则
用户以后说“继续”时：
1. 先读取本文件；
2. 如终稿 DOCX 当前会话仍可访问，则以终稿继续；
3. 若文件不可访问，则以本节点 + 2026-09-24 refine 节点 + 原《DSpark 教学讲义 · 白话核对版》重建；
4. 不要求用户重新解释前文；
5. 后续新增内容必须继续遵守“高浓缩、白话、论文/代码分层、示意数值明确标注”的原则。
