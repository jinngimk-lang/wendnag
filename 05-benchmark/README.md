# 智瞳安宇 BP 对标研究入口

本目录是面向智瞳安宇 BP 改版的**用户交付层**。研究目标不是收集“名气最大的公司”，而是筛选对智瞳安宇在互联网 AI 软件、企业 Agent、具身智能和智能硬件融资表达上最有迁移价值的案例。

## 1. 用户要求对应的 10 家对标

1. 字节跳动 / 今日头条 — 早期互联网算法产品融资叙事
2. Figma — 深技术软件如何用 Demo 消除核心技术风险
3. OpenAI — 官方融资叙事：规模、研究/算力投入与能力跃迁
4. Anthropic — 可靠/安全 AI 如何转化为企业购买理由
5. Scale AI — 用“共同瓶颈”定义基础设施类别
6. Perplexity — 极简 Before / After 产品表达
7. Figure AI — 大愿景 + 窄切入口 + 具身智能规模化路径
8. Anduril — 融资与具体能力跃迁绑定
9. Apptronik — 客户拉动的人形机器人商业化叙事
10. UBTECH 优必选 — AI、软件、硬件、场景与收入之间的资本市场表达

对应研究卡位于 `sources/`。

> 重要：OpenAI 与 Anthropic 未发现可核验的官方早期公开 Pitch Deck，因此本项目明确将其标记为“官方融资叙事/融资公告”，而不是伪称为官方 BP 原件。字节、Figma、Scale AI、Perplexity 的完整历史 deck 主要依赖第三方归档，研究卡已标记可信边界。

## 2. 核心交付文件

- `BENCHMARK_MATRIX.md`：10 家公司横向对比，回答每家公司最值得智瞳安宇借鉴什么。
- `AEGISTON_BP_REWRITE_RECOMMENDATIONS.md`：逐模块、P0/P1/P2 改版建议，包含定位、前 3–5 页、产品、技术、GTM、竞争、融资、视觉等。
- `PACKAGE_MANIFEST.md`：可下载资料包内容与版权边界。
- `sources/`：10 家逐公司研究卡，包含来源、材料性质、结构观察、英文核心表达与中文释义。

## 3. 严谨来源校验层

`../06-analysis/bp-benchmark/` 是更偏“证据审计”的研究层，用于回答：哪些是真实公开 deck、哪些是 SEC Investor Presentation、哪些只是官方融资叙事。

其中：

- `source-index.md`：来源、可信等级、再分发限制。
- `company-notes/`：LinkedIn、Figma、Toutiao、Front、Intercom、Agility Robotics、Berkshire Grey、Matterport、Sarcos、Symbotic 等真实/可交叉验证材料的深入研究。
- `AEGISTON_BP_BENCHMARK_REPORT.md`：更完整的跨软件、AI、机器人/硬件融资表达研究。

这两层不是互相冲突：`05-benchmark/` 优先满足用户点名公司与直接改稿需求；`06-analysis/bp-benchmark/` 负责校验材料真实性和补充高质量真实 deck 样本。

## 4. 当前最重要的对标结论

智瞳安宇当前 BP 的主要问题不是内容不足，而是**投资叙事顺序不对**：最强的客户证据出现太晚，三个产品在前部权重过于接近，宏观市场/政策和架构解释占用了投资人的首屏注意力。

建议融资主线收束为：

> **让企业智能体真正进入生产：用身份、权限、流程、审计与私有化能力把 Agent 带进受监管企业核心流程；先由 LegalLens 的合同审查结果证明商业价值，再把同一底座扩展到组织级工作流。**

前 3–5 页优先回答：

1. 我们是谁；
2. 为什么现在；
3. 已经证明了什么；
4. 为什么我们能赢；
5. 本轮资金买到什么下一阶段的可验证能力。

## 5. 版权与打包规则

公开可访问不等于允许二次分发。对未获明确再分发授权、或材料自身带 confidential / proprietary / 禁止复制条款的完整 deck：

- 不重新上传整套 PDF/PPT；
- 不制作整套逐字中文翻译；
- 保留原始来源 URL、材料身份、页面/结构研究、必要短引文和中文释义；
- 明确允许再分发的材料才进入 `materials/`。

## 6. 长任务恢复

如上下文丢失或任务跨轮次，先读取：

1. `00-project/REQUIREMENTS_BP_BENCHMARK.md`
2. `PROJECT.md`
3. `STATUS.md`
4. 本文件
5. `06-analysis/bp-benchmark/source-index.md`

之后继续推进，不要求用户重复需求。
