# Pre-A Deck V2 视觉资产地图

## 方向

V2 不再把“多人商务会议/团队围桌”作为默认背景。背景只做氛围，核心信息由真实产品界面、原生图表、流程图、设备/部署视觉承载。

## AegistonWEB 官网仓库可复用资产

官网仓库：`jinngimk-lang/AegistonWEB`

- `frontend/public/media/product/`：真实产品 WebP。已确认存在 `ara-dashboard.webp`、`ara-dag-orchestration.webp`、`ara-dev-workspace.webp`、`ara-agent-admin.webp`、`ara-agent-chat.webp`、`ara-agent-terminal.webp`、`ara-audit.webp`、`ara-bug-detail.webp`、`ara-bugs-list.webp`、`ara-docs-inproject.webp`、`ara-docs-projects.webp`、`ara-graph-templates.webp` 等 AragonTeam 素材。
- `frontend/public/media/stock/`：官网背景素材。已确认有 `stock-about-*`、`stock-careers-*`、`stock-contact-*`、`stock-deployment-*` 等不同分辨率版本。
- `frontend/public/brand/`：品牌资产。
- `frontend/public/og/`：官网分享/页面视觉，可用于理解当前品牌构图与配色，不应机械搬到 BP。

## 产品介绍 PDF 可复用资产

已从 `智瞳安宇-总体产品介绍-V6-202608(1).pdf` 提取实际产品截图：

- AragonTeam：需求、BUG、版本、运行图、开发工作区、Agent 执行、审计等界面。
- AegisClaw/历史 InkClaw：对话、多 Agent、DAG、网页 IDE、Git、文档、沙箱等界面。正文按当前项目规则统一写 `AegisClaw`；旧截图像素不篡改。
- LegalLens：智能审查、上下游一致性、多智能体校验、合同风险与证据定位等界面。

## 页面视觉建议

- 封面/结尾：官网式深蓝/蓝紫抽象网络、光点、边界/流程结构；不出现人群。
- 市场/痛点/组织 OS：浅色信息图，不用摄影背景。
- LegalLens：合同文档近景可作为弱背景，但以真实产品界面为主。
- AragonTeam：真实产品截图 + 流程箭头，强调研发全生命周期。
- AegisClaw：原生安全边界/沙箱/DAG 图 + 真实界面（如无当前命名截图，宁可不用旧品牌大图）。
- 技术/安全/部署：机柜、服务器、一体机、网络拓扑、抽象数据流；避免人物。
- 客户证据：数字大卡 + 客户流程/复制路径，不用“会议合影”冒充客户现场。
- 团队：只有在来源真实、必要时使用创始人/团队真实照片；不生成陌生人替代团队。

## 真实性规则

- 生成背景绝不标作客户现场、办公现场或团队照片。
- 公司产品截图保持原像素内容，不 AI 重绘 UI。
- 官网现有素材优先于通用图库/生成图。
