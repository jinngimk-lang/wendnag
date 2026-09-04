# STATUS — 2026-09-04

## 已完成
- 原始 BP 正文按实际章节拆分为 Markdown 基线，保留原始措辞与数据口径。
- 第一轮内容修改建议已形成 16 项队列；正文投资叙事暂不批量改写。
- 图4-9、图13-14 保持真实产品截图，不做 AI 重绘。
- 正文、图题、表格统一使用 `AegisClaw`，删除“曾用名 InkClaw”说明；产品真实截图像素不修改。
- 已安装并记录两套项目级图形 skill：`.agents/skills/drawio-skill/` 与 `.agents/skills/excalidraw-diagram-generator/`，用于后续图形结构、布局、样式与可编辑性治理。
- 图1、2、3、10、11、12、15、16 已按淡蓝、稳重、咨询风格重构为 **Word 原生 DrawingML 图形组**，不是截图、SVG 或表格模拟。
- 图4-9、图13-14 仍为 8 张真实产品截图。
- 已定位上一版 Microsoft Word 无法打开的根因：直接生成的 Word 2010 DrawingML 图形组未经过 Office DOCX 兼容性规范化，LibreOffice 可渲染但 Microsoft Word 更严格。
- 新增 `tools/normalize_word_native_docx.py`，将原生图形版 DOCX 经 LibreOffice 的 `MS Word 2007 XML` writer 重新保存，并自动校验 DrawingML/VML 兼容结构。
- 兼容版验证结果：8 个 `wpg` 图形组、276 个 `wps` 原生图形、8 个 `mc:Fallback`、8 个 VML fallback group、8 张产品截图、12 个原正文表格，`InkClaw` = 0。
- 兼容版保持 31 页；已使用标准 `render_docx.py` 重新渲染全部页面并逐页检查，无裁切、重叠、图表跨页或图形退化为表格的问题。

## 2026-09-04 — BP 外部对标研究

已在分支 `research/bp-benchmark-20260904` 完成一轮系统性 BP / Pitch Deck benchmark：

- 已创建长期需求锚点 `docs/BP_RESEARCH_REQUIREMENTS.md`，用于长上下文/跨会话恢复。
- 已重新审阅当前 37 页可编辑兼容版 BP 的文字、咨询型图表和真实产品截图。
- 已筛选并核验 10 个主样本：LinkedIn、Figma、Toutiao/ByteDance、Front、Intercom、Agility Robotics、Berkshire Grey、Matterport、Sarcos Robotics、Symbotic。
- 已补充 OpenAI 2019 官方融资叙事和 Anthropic 2022/2023 官方融资叙事；未找到可信官方 OpenAI 早期完整 pitch deck，因此没有使用仿制稿冒充官方材料。
- 已建立 `06-analysis/bp-benchmark/source-index.md`，逐份记录材料类型、来源、可信等级和版权/传播状态。
- 已建立 `06-analysis/bp-benchmark/company-notes/`，10 个主样本均有独立研究档案；英文内容采用 English paraphrase → 中文释义，不大段复制受版权保护原文。
- 已建立 `comparison-matrix.csv`，用 13 个融资表达维度对智瞳安宇和 10 个样本做结构化比较。
- 已形成 `AEGISTON_BP_BENCHMARK_REPORT.md`，包含总览表、逐章节诊断、P0/P1/P2、图表修改建议、商业模式重构、数据/IP 待补清单及 16 页融资主 deck 推荐结构。
- 研究核心结论：当前 BP 最强项是客户 traction，最大缺口是投资命题、单一商业楔子、视觉扫描性、融资里程碑和商业模式聚焦；建议采用“LegalLens 已验证楔子 → 统一企业 Agent 底座 → AragonTeam/AegisClaw 扩张”的叙事。
- 已明确：当前“便携式一体机”是本地算力/模型/软件的部署载体，现有证据不足以把它包装成真正的具身智能硬件；若未来存在真实机器人/具身产品，应另补感知—执行闭环、安全、BOM、制造、客户任务与运营 KPI 后再进入融资主线。
- 已创建 `research/pitch-decks/README.md`，提供 10 个原始/官方访问入口和版权处理规则。多份 SEC investor presentations 明确带 Confidential/Proprietary/禁止复制分发条款，因此仓库只保存合法研究摘要和直接来源，不重新上传受限整份原件。

## 当前研究分支
`research/bp-benchmark-20260904`

## 当前正式 BP 工作分支
`bp/word-native-editable-shapes-v4`

## 当前正式 BP 交付物
`西安智瞳安宇科技有限公司商业计划书-20260903A-Word原生可编辑兼容版.docx`

- 文件大小：2,819,089 bytes
- SHA-256：`c65060e88cec743862760f9bef8502a344b30bce0ca1ce4f040444b9fe7c530b`

## 下一轮正文修改优先级
1. 生成 12–18 页机构融资主 deck，与长版尽调文档分离。
2. 投资命题首页改为“受监管企业的生产级 AI Agent / LegalLens 已验证核心工作流”。
3. 最强客户验证前置到第 2–4 页。
4. 三产品改成“一个底座 + LegalLens 商业楔子 + AragonTeam/AegisClaw 两条扩张路径”。
5. 客户状态统一为：已签约 / 已部署 / 已验收 / 已产生收入 / 已回款 / 已扩容 / 规划测算。
6. 商业模式确认一个真实主收入引擎；一体机退回“部署载体”角色，除非硬件业务事实证明应独立。
7. 融资用途改为“1000 万元 → 12–18 月硬里程碑”，具体数值待公司经营数据核验。
8. Bottom-up 市场、Buyer Map、采购链、Land→Expand→Replicate、单位经济补证据。
9. 技术页改成“客户问题 → 技术能力 → 生产证据 → 商业后果”，并完成公司 IP / 高校成果权属拆分。
10. 实名竞争/替代方案只使用可核验或客户真实采购过程中的对象，不做无证据能力比较。
