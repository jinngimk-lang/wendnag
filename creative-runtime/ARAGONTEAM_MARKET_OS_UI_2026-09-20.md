# AragonTeam Company Product OS — 市场版交互设计节点

Date: 2026-09-20

## 用户目标
用户希望把 AragonTeam 逐步沉淀为一套“企业产品操作系统 / Company Product OS”的产品语言：未来新增项目管理、市场、销售、法务等模块时，不重新发明交互与 UI；用户熟悉任一模块后约 20 分钟即可迁移使用其它模块。

## 已确认的 Company Product OS 原则
- 公司级一致性优先于单模块局部最优。
- Standardize the solved. Preserve the identity. Maximize the new.
- 人与 Agent 共同维护产品/项目本体；Agent 能提出、分析、执行低风险变更，人可检查、干预、审批、回滚。
- AI Presence / Agent 不只是聊天框，而是贯穿界面的“协作者”：理解意图、打开工具、修改状态、展示执行过程、汇报结果。
- 每个业务模块应复用同一套对象、状态、动作、审批、时间线、证据、复盘语义。

## 当前市场版痛点
现有页面能力很全，但模块过度平铺：市场总览、市场任务、客户作战室、商机管道、行动中心、活动与样机、作战手册、复盘中心、市场战役、市场看板、市场需求等需要用户自己拼接，认知成本过高。

## 已确认的目标交互主线
保留“客户列表与机会总览 → 客户详情与阶段流程 → Agent 建议 → 话术/内容 → 互动记录 → 复盘”的总体逻辑。

将市场版的核心操作收敛为：
1. 选择客户
2. 客户洞察 / 评分 / Why Now
3. 阶段流程
4. 当前阶段 Agent 建议（为什么、重点、风险、下一步）
5. 生成话术/物料或执行动作
6. 记录客户反馈
7. Agent 自动复盘，更新评分、阶段和 Next Best Action

所有线上/线下行为统一进入 Customer Timeline，不让用户在多个模块间跳转拼流程。

## 与未来项目管理界面的统一
参考“项目房间 + 实时动态 + 人与 Agent + 当前任务 + 底部对话输入”的交互：
- 左侧：对象/项目/客户列表
- 中间：当前对象的主要工作面与动态
- 右侧：人 + Agent + 当前关键任务/建议
- 底部或固定区域：自然语言对话，Agent 可把对话转成结构化变更
- 结构化 UI 是真相与可视化；自然语言是低门槛控制面

市场版只替换领域逻辑，不替换交互骨架。

## 客户评分机制方向
不建议只显示一个黑盒 Lead Score，也不直接用所有因子相乘。
建议分为两个独立指标：
A. Opportunity Score（机会分）：商业值得追的程度
- Product Fit
- Company Fit
- Need
- Intent
- Timing
- Trade / external signals
- Relationship strength
- Contactability

B. Evidence Confidence（证据置信度）：我们对上述判断有多确信
- 来源质量
- 来源数量与独立性
- 新鲜度
- 一致性
- 是否有一手互动证据

列表默认显示“机会分 + 置信度”，低置信度高机会客户优先动作是补证据而不是直接重投入。

初始建议权重：
Product Fit 20%
Need 20%
Intent 15%
Timing 15%
Company Fit 10%
Relationship 8%
Contactability 7%
Trade / external signals 5%
Opportunity Score = 加权得分（0-100）。
Evidence Confidence 单独 0-100，不直接混进机会分；若用于排序，可显示“推荐排序分 = Opportunity × (0.7 + 0.3 × Confidence/100)”并允许查看解释。

## 下一步设计交付
需要做成一组具体逐步 UI：
1. 客户选择 / 机会总览
2. 客户总览 / AI 洞察与评分解释
3. 阶段流程 / 当前阶段工作台
4. Agent 协作侧栏或项目房间式互动
5. 话术与内容生成
6. 执行与互动记录
7. 阶段复盘 / 优劣势 / 下一步
8. 可选：未来通用“项目房间”模板，证明市场版与项目管理共用 Company Product OS 骨架

## 视觉约束
- 继承当前 AragonTeam：白 / 暖米底、橙色主强调、克制圆角、细边框、弱阴影。
- 避免把每个能力做成独立大卡片或独立页面。
- 一屏只突出一个当前目标 + 一到两个辅助动作。
- 所有建议必须能落到 Action / Owner / Deadline / Approval / Result。
