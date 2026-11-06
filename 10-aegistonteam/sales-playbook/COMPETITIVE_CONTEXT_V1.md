# AegistonTeam 竞争环境与差异化销售假设 V1

研究日期：2026-11-06  
证据性质：厂商公开产品/文档陈述，不等于独立实测或客户侧验证。

## 一、竞争环境给销售带来的变化

企业 AI 软件研发市场已不再只是“代码补全”。客户会比较任务规划、云端执行、测试/PR、Agent 管理、权限治理、数据控制、成本和支持。

因此，以下内容不能单独当作 AegistonTeam 的独特卖点：
- 有多智能体；
- 可以从任务规划到代码修改；
- 可以运行测试或创建 PR；
- 支持人工审核；
- 有企业级权限、审计或成本管理；
- 可以云端长任务运行。

销售不要把 Copilot、Cursor、Devin 等简化成“只会补全代码”的工具。先理解客户已有工具和实际流程，再寻找 AegistonTeam 的增量价值。

## 二、代表性产品的公开能力（需要每次对外引用前复核）

| 产品 | 官方公开能力方向 | 对 AegistonTeam 的销售含义 |
|---|---|---|
| GitHub Copilot | 云端 Agent 可从 Issue/提示启动，研究代码仓、规划、修改文件、运行工具、创建/更新 PR；企业可配置云端 Agent 策略、工具审批、MCP、Web 访问和环境。 | 不要把 Copilot 讲成代码补全工具；需要证明 AegistonTeam 在业务需求入口、项目级人机协作和组织交付上提供的额外价值。 |
| Cursor | Cloud Agents 在独立环境中规划、改代码、运行命令/测试、创建 PR；企业文档涉及 SSO、SCIM、RBAC、隐私/数据治理、网络配置、模型控制、审计日志和用量指标。 | 不要声称云端执行或企业治理是 AegistonTeam 独有；必须展示当前版本真实差异。 |
| Devin | 官方产品资料展示云端/本地执行环境、浏览器测试、并行 Agent、PR、协作入口及企业身份/审计/网络能力。 | “数字员工”“多 Agent 并行”“自动测试”本身不构成差异；要验证数字 FDE 的需求理解和项目组织价值。 |
| OpenHands | 官方资料展示从 signal → plan → execute → validate → ship → monitor 的工作流，以及 issue 分流、PR/CI/QA 自动化、多 Agent/多模型/多运行时和企业部署选项。 | 不能把“从信号到交付”或“Agent 工作流”作为唯一差异；要聚焦业务需求与研发团队之间的组织协作。 |

## 三、客户会怎样比较

1. “如果我已有 GitHub Copilot、Cursor 或 Devin，为什么还需要 AegistonTeam？”
2. “AegistonTeam 是否只是把现有 Coding Agent 放进一个看板？”
3. “数字 FDE 比普通需求分析 Agent 多做了什么？”
4. “多 Agent 的分工、上下文、产物、成本和失败恢复如何统一？”
5. “业务负责人如何参与需求澄清和验收，而不必进入 IDE 或 GitHub？”
6. “项目变更如何从需求追踪到代码、测试和版本？”
7. “现有研发工具是否必须替换，还是能按已验证方式共存？”

## 四、值得验证的差异化假设

### 假设 A：数字 FDE 是业务需求到工程执行的前置桥梁

不是只接收已经写好的 Issue，而是帮助业务人员把模糊目标澄清为：
- 业务目标和成功条件；
- 用户/角色/业务规则；
- 功能范围与非目标；
- 验收标准和边界情况；
- 可执行任务与依赖关系。

**所需证据：** 一份真实业务需求、数字 FDE 的追问、结构化需求、验收标准和客户人工确认记录。

### 假设 B：项目级人机混编协作

让业务负责人、产品、研发、测试和多个 Agent 围绕同一个项目上下文协作，而不只是单个开发者把任务委派给一个 Coding Agent。

**所需证据：** 真实成员/Agent 角色、任务状态、交接记录、共享上下文、人工审批、代码和测试产物之间的关联。

### 假设 C：需求变更跨阶段追踪

一次业务变更不只重新生成代码，还能说明影响哪些需求/任务、哪些 Agent 或人员需重新执行、哪些测试需回归、哪些产物被替换、谁确认最终结果。

**所需证据：** 同一项目中变更前后需求、任务、代码 diff、测试报告、人工评审和版本记录。

### 假设 D：组织知识与交付经验持续沉淀

项目规则、决策、任务、代码/文档产物和验收经验能成为下一次任务可调用的上下文，而不是散落在聊天记录、IDE 和个人账号中。

**所需证据：** 跨任务复用演示、知识/上下文更新记录、权限范围和准确性评估。

以上全部是差异化假设，不是已证实结论。产品未能展示的部分不能作为当前销售承诺。

## 五、客户异议的标准回答

### “我们已经有 Cursor / Copilot / Devin 了。”

> 很好，我们不先要求替换现有工具。先看贵团队的实际问题是个人编码速度，还是业务需求澄清、跨角色分工、任务推进、人工评审和持续变更之间的协作成本。如果只是个人编码，现有工具可能已经够用；如果问题发生在团队级交付，我们可以选同类任务验证是否有增量价值。

### “你们是不是只是把几个 Agent 放到一个项目里？”

> 这个问题应该通过真实任务判断，而不是靠产品名词回答。我们可以一起看需求输入、澄清、任务分工、人工确认、执行产物、测试和一次变更，逐项确认当前版本到底完成了哪些环节。

### “你们能不能比现有工具做得更好？”

> 先定义“更好”是什么：需求澄清质量、人工协调时间、代码/测试质量、返工、总周期还是总成本。用同一任务和同一验收标准比较；没有对照数据前，不承诺全面领先。

## 六、竞争验证方法

选择同一份非敏感软件研发任务，在 AegistonTeam 与 2–3 个客户已使用或可用的工具中做可复现对照：

- 相同输入材料和项目上下文；
- 相同验收标准；
- 记录需求澄清质量、人工补充次数、任务拆解质量；
- 记录代码质量、测试通过、返工、人工复核时间；
- 记录任务总周期、模型/算力成本；
- 记录项目上下文和变更追踪；
- 记录企业控制项（权限、数据流、审计、部署）是否有可复查证据。

不要只比较“谁生成代码快”，应比较客户真实任务从业务输入到可验收交付的完整成本和风险。

## 七、官方来源

- GitHub Copilot — About GitHub Copilot: https://docs.github.com/en/enterprise-cloud@latest/copilot/get-started/about-github-copilot
- GitHub Copilot — Managing Copilot in the cloud for enterprise: https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-for-enterprise/manage-agents/manage-copilot-in-the-cloud
- GitHub Copilot — Agent management: https://docs.github.com/en/copilot/concepts/enterprise/agent-management
- Cursor — Enterprise: https://prod.cursor.com/docs/enterprise
- Cursor — Background agents: https://prod.cursor.com/help/ai-features/background-agents
- Cursor — Security and Privacy Hardening: https://prod.cursor.com/docs/enterprise/security-hardening
- Devin — Official product site: https://app.devin.ai/
- OpenHands — Official product site: https://www.openhands.dev/

注意：厂商页面的能力描述可能随产品和套餐变化；正式客户提案引用前应重新核对日期、适用套餐和限制。
