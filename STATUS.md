# STATUS — 2026-09-04

## 已完成
- 原始 BP 正文按实际章节拆分为 Markdown 基线，保留原始措辞与数据口径。
- 第一轮内容修改建议已形成 16 项队列；正文投资叙事暂不批量改写。
- 图4-9、图13-14 保持真实产品截图，不做 AI 重绘。
- 正文、图题、表格统一使用 `AegisClaw`，删除“曾用名 InkClaw”说明；产品真实截图像素不修改。
- 已安装并记录两套项目级图形 skill：`.agents/skills/drawio-skill/` 与 `.agents/skills/excalidraw-diagram-generator/`，用于后续图形结构、布局、样式与可编辑性治理。
- 图1、2、3、10、11、12、15、16 已按淡蓝、稳重、咨询风格重构为 **Word 原生 DrawingML 图形组**，不是截图、SVG 或表格模拟。
- 8 张咨询型图合计保留 8 个 Word 原生图形组、276 个原生子图形对象；圆角卡片、箭头、柱形、阶梯、分层架构、复制路径、资金结构与时间轴造型均保留。
- 图4-9、图13-14 仍为 8 张真实产品截图。
- 已定位上一版 Microsoft Word 无法打开的根因：直接生成的 Word 2010 DrawingML 图形组未经过 Office DOCX 兼容性规范化，LibreOffice 可渲染但 Microsoft Word 更严格。
- 新增 `tools/normalize_word_native_docx.py`，将原生图形版 DOCX 经 LibreOffice 的 `MS Word 2007 XML` writer 重新保存，并自动校验 DrawingML/VML 兼容结构。
- 兼容版验证结果：8 个 `wpg` 图形组、276 个 `wps` 原生图形、8 个 `mc:Fallback`、8 个 VML fallback group、8 张产品截图、12 个原正文表格，`InkClaw` = 0。
- 兼容版保持 31 页；已使用标准 `render_docx.py` 重新渲染全部页面并逐页检查，无裁切、重叠、图表跨页或图形退化为表格的问题。
- BP 对标研究层已建立 10 家国际/AI/机器人样本、严格来源校验层和详细改版建议。
- 新增华擎（武汉）通信科技 22 页 Pre-A BP 作为**主 Deck 内容介绍流程的核心结构参考**；逐页拆解见 `05-benchmark/sources/11-huaengine-2019-prea.md`，原始 PDF 快捷入口见 `05-benchmark/materials/huaengine-2019/`。
- 已将 `Panniantong/Agent-Reach` 的项目级互联网研究 skill 集成到 `.agents/skills/agent-reach/`，保留 MIT License、上游 commit、网页/搜索/GitHub/视频/社交等路由规则和 wendnag 专用安全/版权规则；运行时依赖、Cookie、Token 不进入仓库。
- 已完成第一版 **16 页 Pre-A 投资人主 Deck**：以华擎线性融资结构为骨架、吸收 Notion 2013 的低文字密度与单页单结论表达；LegalLens 作为商业楔子，通信/交通量化证据前置，一个底座连接 AragonTeam / AegisClaw 两条扩张路径。
- V1 摄影背景采用低饱和企业实拍摄影感生成资产；客户事实、产品能力、融资数据全部由文字和原生 PPT 图表承载，生成背景不冒充真实客户现场。
- `智瞳安宇_PreA_投资人主Deck_v1.pptx` 已通过 LibreOffice → PDF 导出与 16 页逐页渲染检查；`slides_test.py` 通过，无检测到文本溢出。PPTX/PDF 二进制在对话中交付，SHA-256 已写入 `BINARY-MANIFEST.md`。
- V1 逐页结构、背景设计规则与后续待补事实写入 `07-investor-deck/`。

## 当前工作分支
`bp/prea-investor-deck-v1`

> 华擎参考与 Agent-Reach 研究集成已经进入 `main`；本轮 Pre-A 主 Deck V1 在独立分支完成并等待最终差异复核。

## 当前交付物

### 长版尽调 BP
`西安智瞳安宇科技有限公司商业计划书-20260903A-Word原生可编辑兼容版.docx`

- 文件大小：2,819,089 bytes
- SHA-256：`c65060e88cec743862760f9bef8502a344b30bce0ca1ce4f040444b9fe7c530b`

### Pre-A 投资人主 Deck V1
- `智瞳安宇_PreA_投资人主Deck_v1.pptx` — 16 页，16:9，PPT 原生可编辑图表 + 摄影背景。
- `智瞳安宇_PreA_投资人主Deck_v1.pdf` — 快速审阅版。
- 哈希与文件大小见 `BINARY-MANIFEST.md`。

## 下一轮主 Deck 优先级
1. 用户实际审阅 V1 的内容顺序与视觉节奏；
2. 将真实产品截图有选择地放入 LegalLens / AragonTeam / AegisClaw 页面，避免“全图表无产品”；
3. 管理层确认当前签约收入、回款、软件/实施收入占比、续费/运维数据；
4. 补 PoC 转化率、销售周期、交付周期与典型实施人天；
5. 把 18 个月里程碑改成明确数量型 KPI；
6. 逐家核验具名竞争对手后替换 V1 类别象限；
7. 核实一体机 BOM / 售价 / 毛利 / 首批交付目标；
8. 继续区分公司自有 IP 与团队/高校历史专利归属。
