# AegisTeam（超级团队）竞品调研工作底稿 V0.1

> 日期：2026-09-17  
> 用途：调研分享、持续修改、跨会话恢复上下文。  
> 说明：用户当前指定产品名为 **AegisTeam（超级团队）**；wendnag 现有正式材料仍主要使用 **AragonTeam**。本稿在产品能力事实层引用 AragonTeam 现有材料，但不自动假定所有能力已经在当前生产版本完整上线。最终对外稿前必须确认 AegisTeam/AragonTeam 是否为同一产品的新旧命名，并统一事实源。

## 1. 本轮调研问题

不是做“功能数量清单”，而是回答：monday AI、Genspark GenTeam、hilos 分别把 AI Agent 放在企业工作的什么位置；它们与 AegisTeam 在产品边界、协作方式、治理机制、研发交付闭环与部署方式上有什么不同。

本轮只选 3 个最直接的竞品：

1. **monday AI**：企业工作流 + Agent 治理。
2. **Genspark GenTeam**：Channel/DM/Thread 中的人机混编长期团队。
3. **hilos**：研发聊天室 + 编码 Agent + PR 交付与人工审批。

Codex 仍是重要邻近产品，但更接近个人/工程任务执行器，不纳入本轮 3 个主竞品。

## 2. AegisTeam 当前内部产品基线（基于 wendnag）

wendnag 当前材料把 AragonTeam 定义为面向研发与项目交付的“企业 AI 原生人机协同工作站”：连接员工、智能体、企业知识和业务流程，目标是让智能体以正式数字员工方式进入组织任务、研发和交付链路。

当前仓库材料提出的关键差异轴包括：

- 人与 Agent 使用同一套企业身份体系。
- 权限、成本与风险可进入统一治理。
- Agent 产出进入需求、缺陷、版本、迭代、评审和交付路径。
- 人与 Agent 的操作进入同一条审计链。
- 企业知识库与组织上下文可沉淀为资产。
- 支持私有服务器、便携式一体机、私有云等交付形态。
- 研发流程覆盖 IPD、敏捷、瀑布等模式，并将需求/缺陷/版本/迭代与代码变更关联。

这些是本轮的“内部产品基线”，并不等于已完成独立产品验收。下一版需要用真实界面、权限配置、运行日志、部署文档逐项补证。

## 3. monday AI

### 当前产品位置

monday AI 的核心不是先做一个团队聊天工具，而是把 Agent 放进既有的 board、docs、workflow 与权限体系里。Agent 可由触发器启动，在既定访问边界内读取或编辑数据，并通过 Activity 留下运行记录。

Agent Builder 的当前公开结构包括：Brain（指令、知识/访问范围、工具、skills、模型）、Jobs（独立触发器与工作任务，可并行/定时）、Channels（外部沟通渠道）、Activity（运行状态、应用与 AI credits）。monday vibe 还可以基于自然语言生成 monday 数据上的业务应用。

### 与 AegisTeam 的关键差异

- monday 的原生对象是通用工作管理资产：Board / Doc / Workflow / Dashboard；AegisTeam 内部定位更强调需求、缺陷、版本、迭代、代码、评审与交付等研发对象。
- monday 的权限颗粒度成熟，Agent 可按 board/space/team 及读写范围工作；AegisTeam 如果要形成更强差异，需要证明“Agent 是正式组织成员”的身份、生命周期、成本、审批、移交、审计，而不仅是资源访问权限。
- monday 的 trigger / Jobs / schedule 很成熟；AegisTeam 的流程触发、依赖、重试/重入需要补当前产品证据。
- monday.com 官方为云服务，不提供 on-premises；AegisTeam 当前仓库材料主张整个平台可私有服务器/一体机/私有云交付。这是结构性差异，但必须用真实部署边界证明。

## 4. Genspark GenTeam

### 当前产品位置

GenTeam 与 AegisTeam 的表面交互最接近。它把人和 AI Agent 放在同一批 Channel、DM、Thread 中；Agent 有名字、角色、skills、跨会话记忆，可以读取频道上下文、接任务、与其他 Agent 协作。

任务机制已经超出纯聊天：消息可形成 Task，状态包含 Todo / In Progress / In Review / Done；Agent 认领任务、在 Task Thread 汇报进展并推进 Review。

GenTeam 的权限逻辑更偏“Agent 属于创建者”：credits、连接服务和对外动作受到创建者身份/批准约束。它也支持本地 Claude Code、Codex CLI、Cursor CLI、OpenCode 等 Agent 处理文件/代码，再把结果带回频道。

### 与 AegisTeam 的关键差异

- Channel、@Agent、多 Agent、Thread、Task Board 已是成熟基线，不应作为 AegisTeam 独占壁垒。
- GenTeam 更像 AI-native Slack/Discord + 轻任务系统；AegisTeam 若要拉开差距，应证明聊天与结构化研发对象（需求、缺陷、版本、迭代、评审、交付）深度打通。
- GenTeam 的权限主轴是创建者身份与服务权限；AegisTeam 的机会是把 Agent 从“某个人的代理”升级为“企业正式受管身份”，并统一治理成本、风险与审计。
- GenTeam 支持本地 coding Agent，但协作 workspace 仍是 Genspark 服务；这不等于整个平台本体 on-prem 私有化。

## 5. hilos

### 当前产品位置

hilos 非常聚焦研发团队：Agent 是团队聊天室成员，团队在 Channel/Thread 中讨论需求，编码 Agent 对真实代码仓工作，返回 branch/PR、preview、diff、caveats，再由人批准。

hilos 的一个重要方向是“模型/Agent 中立”：支持本地或托管 Agent，并通过 MCP/API 让外部 Agent 以自己的身份接入 workspace。这一开放连接层值得 AegisTeam 正面回答。

在 human-in-the-loop 上，hilos 把 PR 交付和人工批准做成主路径；自动化触发真正的 Agent 工作前，也可以先形成任务/派发建议等待人工批准。

### 旧实测结论更新

用户上传的旧 Channel 调研中记录过 hilos “Agent 工作期间并无进度展示”。这个结论已经过时：hilos 2026-09-11 changelog 显示，当前单一 run card 会实时更新当前步骤、触达文件与耗时，并可展开完整 transcript；更早版本也已支持 live run、PR 状态和 Agent 互评。

### 与 AegisTeam 的关键差异

- hilos 更窄、更深地围绕 `chat -> code -> PR -> review`；AegisTeam 当前定位更宽，目标是研发/项目交付全链路。
- hilos 的单次运行透明度非常完整；AegisTeam 应证明跨需求/缺陷/版本/任务的组织级追溯，而不仅是单次 Agent 日志。
- hilos 已把 MCP/API、外部 Agent 接入、模型中立做成卖点；AegisTeam 当前仓库材料没有把开放 Agent 接入协议作为核心主张。
- hilos 可让本地 Agent 保留 checkout/凭据，但协作 workspace 仍由 hilos 服务；AegisTeam 若能整个平台内网私有化，则面向强监管场景有明显不同。

## 6. 横向结论

| 维度 | AegisTeam（当前内部基线） | monday AI | GenTeam | hilos |
| --- | --- | --- | --- | --- |
| 核心定位 | 企业研发/项目交付的人机协同工作站 | 通用企业工作管理 + AI Agents | 多 Agent 团队协作 workspace | 研发聊天 + 编码 Agent 交付 |
| 核心交互 | 研发对象 + 工作区 + 聊天室/论坛 | Board / Doc / Workflow / Dashboard | Channel / DM / Thread / Task Board | Channel / Thread / Task / PR |
| Agent 身份 | 内部材料定义为正式数字员工 | 工作流执行单元/组织 Agent | 长期 teammate，偏创建者代理 | room member / 外部 Agent 可接入 |
| 任务/状态 | 需求、缺陷、版本、迭代、评审、交付 | 高度可配置 board/workflow/job | 轻量 Task 状态板 | Task + run + PR review |
| 自动化 | 触发/状态机制需补当前实测 | trigger / Jobs / schedule 很强 | 任务驱动，另有 schedules | message / schedule / PR automation |
| 权限/治理 | 企业身份、权限、成本、风险统一治理（需实证） | board/space/team + 读写权限成熟 | 创建者身份 + 服务权限 + Channel/DM | workspace/channel/token/repo + 人工审批 |
| 运行可观测 | 全链路审计（需 UI/日志补证） | Activity | Task Thread/状态 | run card + transcript + audit |
| 外部 Agent | 当前材料未明确标准化协议 | 有 external/BYOA 路径 | Claude/Codex/Cursor/OpenCode 本地接入 | MCP/API，模型/Agent 中立 |
| 平台私有化 | 私有服务器/一体机/私有云（需部署证据） | 无 on-premises | 本地 Agent 可执行，workspace 仍云端 | 本地 Agent 可执行，workspace 仍云端 |

## 7. 分享时最值得强调的 5 个判断

1. **Channel、@Agent、多 Agent 同群不是壁垒。** GenTeam 与 hilos 已经做得成熟。
2. **任务看板 + Agent 执行也已是通用基线。** monday、GenTeam、hilos 都有各自的任务/运行/审批对象。
3. **AegisTeam 真正可能形成结构性差异的是“组织制度化”。** 即独立企业身份、授权/暂停/移交、权限颗粒度、成本预算、审批交付、审计追责是否全部闭环。
4. **整个平台私有化与“本地 Agent”不是一个概念。** 如果 AegisTeam 的模型、向量库、文件、消息、任务、代码、日志、审计均可留在企业内网，这应成为强监管客户的核心证据。
5. **开放 Agent 生态需要明确回答。** GenTeam/hilos 都在降低第三方 Agent 接入门槛；若 AegisTeam 也支持外部 Agent，需要明确身份映射、权限继承、审计边界与成本归属。

## 8. 下一轮必须核验的 AegisTeam 产品事实

- AegisTeam / AragonTeam 命名是否一致；如已改名，仓库事实源同步。
- Agent 是否有独立 ID、组织角色、所属团队、负责人、生命周期状态。
- 权限能否分别落到项目、需求、缺陷、仓库、分支、文件、知识库、工具、外部系统。
- 成本治理是否已有预算、额度、模型消耗、按 Agent/项目/团队归集与告警。
- 多 Agent 是否支持自动拆解、依赖、并行、交接、失败重试/重入、人工接管、循环保护。
- Agent 改代码后，branch、PR/MR、测试、评审、验收、版本发布是否回写同一需求/缺陷。
- 是否存在类似 hilos run card/transcript 或 monday Activity 的逐步运行记录。
- 是否支持 MCP/API/Claude Code/Codex 等第三方 Agent 以独立身份加入；权限/审计如何映射。
- 私有服务器/一体机/私有云是否意味着模型、向量库、文件、日志、消息、任务、代码和审计数据全部可留在内网。

## 9. 10 分钟分享结构

- 1 分钟：AegisTeam 的问题定义——不是多一个 AI 聊天框，而是让 Agent 真正进入企业研发组织。
- 2-4 分钟：monday AI——Agent 已能按触发器在业务流程里持续执行，权限/Activity/应用构建成熟。
- 4-6 分钟：GenTeam——人和 Agent 同频道、同任务，说明“AI 队友”已是产品基线。
- 6-8 分钟：hilos——从一句需求到代码、PR、人工审批，说明研发 Agent 的交付链可以非常短。
- 8-10 分钟：回到 AegisTeam——真正要证明的是统一企业身份、结构化研发流程、全链路审计、组织知识沉淀和整个平台私有化。

## 10. 资料来源登记

### 用户材料

- 《超级团队调研.pdf》：monday AI、Codex 的产品实测与截图整理。
- 《Aragonteam_Channel_AI_频道模块调研模板 (1).pdf》：Genspark GenTeam、hilos 的 Channel/@Agent/多 Agent 协作实测。

### wendnag 内部事实源

- `02-content/04-products.md`
- `02-content/06-competition.md`
- `07-investor-deck/SLIDE_OUTLINE_V2.md`
- `PROJECT.md`
- `STATUS.md`

### 外部公开资料（截至 2026-09-17）

- monday AI Agents: https://support.monday.com/hc/en-us/articles/33347027353746-AI-Agents-on-monday-com
- monday Agent Builder: https://support.monday.com/hc/en-us/articles/38411699315346-Build-and-configure-your-AI-agent
- monday vibe: https://support.monday.com/hc/en-us/articles/28451758349842-Get-started-with-monday-vibe
- monday Security/Privacy FAQ: https://support.monday.com/hc/en-us/articles/31119344104082-Security-and-privacy-on-monday-com-FAQs
- Genspark GenTeam Help Center: https://www.genspark.ai/helpcenter/genteam
- hilos: https://hilos.sh/
- hilos Connect your own agent: https://hilos.sh/docs/connect-your-agent
- hilos Automations: https://hilos.sh/docs/automations
- hilos Changelog: https://hilos.sh/changelog

## 11. 精度规则

- 对 AegisTeam 的内部定位与“已经产品化/已经上线”严格区分。
- 没有截图、配置页、日志或部署文档的能力，不写成确定性“全面领先”。
- 竞品更新频繁，正式分享前再次核对官方帮助中心和 changelog。
- hilos “无进度展示”是旧结论，当前版本不得再作为缺点使用。
