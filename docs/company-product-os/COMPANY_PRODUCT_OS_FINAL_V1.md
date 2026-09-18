# Company Product OS — 最终版 v1.0

> **定义：** Company Product OS 是一家公司的“可执行产品本体”。它把公司本体、价值观、文化、产品哲学、UI/UX、交互、人机协作、技术原则和已验证模式，转化为 **用户与 Agent 可共编、产品可继承、开发前可冻结、上线后可验证并持续进化** 的生产系统。
>
> **原则：已解决的问题标准化，公司的基因被继承，真正新的问题留给创新。**

## 1. 为什么需要它

Agent 让“写出软件”越来越容易，也会放大产品熵增：同一家公司不同 Agent 生成的产品，导航、术语、权限、AI 行为和技术逻辑可能各不相同；用户每个新品都要重新学习，PM/设计师仍需反复纠偏。

Company Product OS 要让所有新品天然具有同一公司的“产品 DNA”，使员工已有经验能迁移到新品，同时保留明确创新空间。

它覆盖完整链路：

**Company Identity → Product Decision → UI/UX → Interaction → Human-Agent Interaction → Technical Pattern → Product → Runtime Evidence → Organizational Learning**

---

## 2. 四个核心系统

### A. Company Genome｜公司基因

回答“我们是谁、通常怎样判断”。

包含：本体、使命愿景、价值观、文化、用户观、产品哲学、人机关系、设计语言、UI/UX、技术、安全隐私、内容语言、Pattern 与反例。

规则分为：

`Principle / Must / Default / Prefer / Pattern / Free / Experimental`

Must 是底线；Default 可解释覆盖；Experimental 是明确创新区。

### B. Collaborative Ontology Graph｜协同本体图

这是 **用户与 Agent 共同工作的核心界面**，不是只给机器读取的后台 YAML。

```text
使命/价值观
   ↓
产品原则 ──→ 用户体验目标
   ↓              ↓
交互原则 ──→ 人机协作原则
   ↓              ↓
Pattern ─────→ UI/UX / Agent Behavior
   ↓              ↓
组件/技术实现 ← 产品/功能
   ↑
会议、文档、Figma、代码、用户研究、运行数据（Evidence）
```

每个节点显示：类型、强度、scope、证据、owner、版本、置信度、引用、影响范围、例外与冲突。

用户可 **增删、连线、改强度/scope、审批 Agent 提议、创建例外、回滚**；Agent 可抽取候选节点、发现冲突、补关系并做影响分析，但不能自行把高影响 Candidate 升级为 Company Must。

知识链路：

`Raw Evidence → Claim → Candidate Node/Rule → Human-Agent Review → Approved Genome`

本体图既是公司的“产品认知地图”，也是所有新品生成的事实源。

### C. Product Design Studio｜协同产品设计空间

回答“在真正写代码前，这个产品到底应该怎样工作”。

新需求进入后，Rule Resolver 只编译当前任务所需的 **Product Context Pack**：适用原则、Must/Default、Pattern、组件、Canonical Examples、Anti-pattern、合法例外，以及 Frozen / Flexible / Experimental Zones。

用户与 Agent 随后联合完成三张互相绑定的图：

**1）UI/UX Design Map**  
信息架构、导航、页面、Token、组件、内容层级，以及 Loading / Empty / Error / Permission / Success、响应式和 Accessibility。

**2）Interaction Logic Graph**  
用户动作 → 系统状态 → 反馈 → 下一状态；覆盖状态机、搜索/表单/审批、异常、恢复、撤销、权限拒绝，并绑定规则、API、数据和审计。

**3）Human-Agent Interaction Map**  
定义人发起 / Agent 建议 / Agent 自动执行的边界；Preview / Confirm / Approve；工具权限；来源与置信度；修改、打断、撤销、重试、接管；高风险操作的控制权。

三张图必须互相引用：一个按钮可追溯到状态机、人机权限、规则、API/数据和本体节点；改一处，Agent 自动检查其他层失配。

用户可直接评论、拖拽、修改、锁定或要求重做；Agent 补全状态、发现遗漏并检查一致性。**产品设计本身就是 Human + Agent 的可视化协同过程。**

### D. Product Compiler + Conformance Engine｜编译与验证

Product Compiler 不从一句 Prompt 直接写代码，而是从已批准设计生成 **Product IR**：

`goals / users / IA / screens / states / workflows / actions / permissions / AI behaviors / data / API / components / security / analytics / acceptance tests`

Product IR 再生成代码、测试、文档和部署配置。

Conformance Engine 做四类验证：

- **Deterministic**：Token、组件、API、依赖、权限、安全、审计；
- **Structural**：状态、错误、恢复、权限、AI provenance 是否完整；
- **Semantic**：价值观、术语、交互习惯、认知负担、是否“像公司”；
- **Runtime**：任务成功率、错误、Help、工单和真实使用路径。

原则：**能确定性检查的，不让 LLM 猜。**

---

## 3. 客户会议到产品的流水线

```text
会议录音（经授权）
+ 官网/品牌/文化/产品资料
+ Figma/软件/代码/API/技术规范
+ 用户研究/客服/运行数据
        ↓
Evidence Vault
        ↓
Agent 抽取 FACT / DECISION / PRINCIPLE /
CONSTRAINT / PATTERN / ANTI-PATTERN / CONFLICT
        ↓
Collaborative Ontology Graph
用户 + Agent 校正、补充、批准
        ↓
Company Genome vX
        ↓
Product Intent
        ↓
Product Context Pack
        ↓
Product Design Studio
UI/UX + Interaction + Human-Agent Interaction
        ↓
Development Readiness Gate
        ↓
Frozen Design Baseline + Product IR
        ↓
Agent 开发 / 测试 / 文档
        ↓
Conformance Gate
        ↓
Pilot / Release
        ↓
真实使用证据
        ↺
Ontology / Pattern / Company OS 演进
```

会议只是 Evidence，不直接成为规则；单次陈述先成为 Candidate，再结合制度、现有产品和其他证据判断 scope/authority。

---

## 4. Development Readiness Gate｜开发启动门

**真正启动开发前，必须先形成完善的“设计 + 人机交互”基线。**

至少满足：

1. Product Intent、目标用户、JTBD、成功指标明确；
2. Company Genome / Context Pack 无未解决的高影响冲突；
3. 信息架构和 UI/UX 主流程完成；
4. 关键页面的正常、空、加载、错误、无权限等状态完整；
5. 核心流程已有 Interaction Logic / State Machine；
6. Human-Agent Interaction Map 完成，自动化级别和控制权清楚；
7. 高风险/不可逆/批量动作定义 Preview、Confirm、Undo 或人工审批；
8. 权限、数据、API、审计、安全、Accessibility 已映射到设计；
9. 重要界面/行为可追溯到本体规则或明确 Experimental 决策；
10. 用户与 Agent 联合检查，关键决策由责任人批准。

通过后形成版本化 **Design Baseline**。开发 Agent 不得静默改变关键交互；变更必须回写设计层、显示影响并重新批准。

流程由：

`需求 → 边写代码边想交互`

变为：

`需求 → 本体 → 完整 UI/UX + 交互 + 人机协作设计 → 冻结基线 → 工业化开发`

---

## 5. 一致性与创新如何共存

每个产品主动划分：

- **Frozen Zone**：身份、安全、核心交互语义、基础架构，不重复发明；
- **Flexible Zone**：允许按场景调整；
- **Experimental Zone**：明确要求人和 Agent 创新。

新做法通过真实使用后：

`Experimental → Candidate Pattern → Validated Pattern → Default → Must（极少）`

失败则进入 Anti-pattern，因此它是 **Living Product Operating System**。

---

## 6. 第一版 MVP

第一版只需证明：

> **给定一次客户会议、公司资料和 2–3 个已有产品，系统能否与客户共同建立可编辑本体图，并在写代码前完成 UI/UX + 交互 + 人机协作设计，最终生成一个从未存在过、但员工第一次打开就能认出、能上手的新 Web 产品。**

核心界面：

1. Evidence Inbox  
2. Collaborative Ontology Graph  
3. Conflict / Approval Center  
4. Product Context Pack  
5. Product Design Studio  
6. Human-Agent Interaction Editor  
7. Development Readiness Gate  
8. Conformance Report  
9. Evolution Review  

成功只看三个结果：

- **Recognition**：“这是我们的产品。”
- **Transfer**：“我没学过这个，但我知道怎么用。”
- **Innovation**：“它不是旧产品换皮，而是真正解决了新问题。”

最终分工：**人决定值得创造什么；Company Product OS 保持公司是谁；人 + Agent 共同设计产品如何工作；Agent 将批准的设计工业化为软件。**
