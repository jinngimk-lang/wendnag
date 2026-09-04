# STATUS — 2026-09-04

## 已完成
- 原始 BP 正文按实际章节拆分为 Markdown 基线，保留原始措辞与数据口径。
- 第一轮内容修改建议已形成 16 项队列；图4-9、图13-14 保持真实产品截图，不做 AI 重绘。
- 正文、图题、表格统一使用 `AegisClaw`；产品真实截图像素不篡改。
- 图1、2、3、10、11、12、15、16 已重构为 Word 原生 DrawingML 图形组，并通过 Office 兼容性规范化与逐页渲染检查。
- BP 对标研究层已建立 10 家国际/AI/机器人样本；华擎（武汉）通信科技 22 页 Pre-A BP 作为主 Deck 线性融资流程参考，Notion 2013 仅作为信息层级/单页主结论参考。
- 已完成 V1 16 页 Pre-A 投资人主 Deck，并将结构、背景规则、QA 写入 `07-investor-deck/`。

## 2026-09-04 — V2 源材料重读与主 Deck 重构

用户反馈 V1 存在两个问题：**人物背景过多、内容不足**。本轮按该反馈重新执行源材料阅读与视觉资产审计：

1. 完整解析并阅读用户新上传的长版 BP `BP_EDITABLE_VML_AUTOFIT(1).docx`；
2. 完整解析并阅读 98 页 `智瞳安宇-总体产品介绍-V6-202608(1).pdf`，并重点检查产品、团队、客户章节的页面渲染与嵌入截图；
3. 检查官网仓库 `jinngimk-lang/AegistonWEB`，确认 `frontend/public/media/product/` 已有大量 AragonTeam 等真实产品 WebP，`frontend/public/media/stock/` 已有 about / deployment / contact 等官网背景素材；
4. 检查官网 `search-index.json`，补充 AragonTeam 的“可管理、可执行、可进化”、四重困境、研发协作功能等官网正式表达；同时发现官网搜索索引仍保留 `InkClaw` 历史命名，因此主 Deck 继续按项目规则使用当前正文名 `AegisClaw`，不把旧命名重新带回正文；
5. 在虚拟环境从 98 页 PDF 中提取真实产品界面图，用于 LegalLens / AragonTeam 产品证据页，替代大量通用人物摄影背景；
6. 生成 **21 页 V2 内容增强版主 Deck**：`智瞳安宇_PreA_投资人主Deck_V2_内容增强版.pptx`，并成功导出 21 页 PDF；
7. V2 叙事增加：组织 OS、四重困境、LegalLens 产品证据、AragonTeam 完整研发闭环、AegisClaw 安全运行、私有化/一体机准入、复制飞轮、独立 GTM 等内容；
8. V2 封面/结尾改为品牌化抽象网络视觉，正文以轻背景 + 原生图表 + 真实产品截图为主，**不再使用多人会议/商务合影作为主要背景语言**。

## 当前工作分支
`bp/prea-investor-deck-v2-source-grounded`

## 当前交付物

### 长版尽调 BP
`西安智瞳安宇科技有限公司商业计划书-20260903A-Word原生可编辑兼容版.docx`

### Pre-A 投资人主 Deck V2
- `智瞳安宇_PreA_投资人主Deck_V2_内容增强版.pptx` — 21 页，16:9，内容增强、真实产品证据前置、少人物背景。
- `智瞳安宇_PreA_投资人主Deck_V2_内容增强版.pdf` — 21 页快速审阅版。
- SHA-256 与文件大小写入 `BINARY-MANIFEST.md`。
- 逐页结构写入 `07-investor-deck/SLIDE_OUTLINE_V2.md`。
- 用户补充原始材料登记写入 `01-source/incoming/2026-09-04/README.md`。

## 二进制源文件状态
当前 GitHub 连接器没有“从沙箱文件路径直接上传二进制文件”的接口，因此用户新上传的 DOCX/PDF 原件不能在本轮安全地伪装为已提交到仓库；仓库已保存其文件名、大小、SHA-256、用途和阅读状态。获得认证二进制 Git 上传路径后，应按登记信息原样补入 `01-source/incoming/2026-09-04/`。

## 下一轮主 Deck 优先级
1. 管理层确认当前签约收入、回款、软件/实施收入占比、续费/运维数据；
2. 补 PoC 转化率、销售周期、首单/复制单交付周期与典型实施人天，验证“复制飞轮”；
3. 把 18 个月融资里程碑改成明确数量型 KPI；
4. 从 AegistonWEB 官网正式资产中进一步选择无人物的 deployment / product / abstract 视觉替换通用底纹；
5. 逐家核验具名竞争对手后再进入正式路演版竞争矩阵；
6. 核实一体机 BOM / 售价 / 毛利 / 首批交付目标；
7. 继续区分公司自有 IP 与团队/高校历史专利归属。
