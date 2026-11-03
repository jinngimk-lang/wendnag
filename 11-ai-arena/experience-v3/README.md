# AI Arena — Independent Agent Portfolio Workstation V0.4.0

Finance Arena 已从“六派系围绕中央资金池的竞技场”重构为 **一个 Agent = 一个独立账户** 的投研与模拟交易工作站。

## V0.4.0 产品结构

**实验入口弹窗 → 共同市场环境 → 六个独立 Agent 账户 → 当前 Agent 完整工作区 → 净值比较 / 事件 / 风险 → 逐 Agent 操作账本。**

- 六个 Agent 各自拥有独立现金、股票持仓、净值路径、风险指标和操作记录。
- 六个 Agent 共享同一条市场价格路径、市场因子、事件序列、起始本金、费用、滑点和风险上限，保证横向比较条件公平。
- 不存在中央资金池，不存在 Agent 之间的现金转账；合计盈亏只是六个独立账户的汇总视图。
- 主界面在同一工作台内展示市场数据、六个账户、所选 Agent 研究结论、净值曲线、事件、排名和逐日账本。
- 新建实验、选择公司标签、配置模拟天数、初始本金和风险上限放入独立弹窗。
- 每个 Agent 有独立人物视觉资产槽位。角色设定、色彩和图片规格见 AGENT_VISUAL_SYSTEM.md；生成图片预期路径为 assets/agents/value.webp、growth.webp、trend.webp、quant.webp、sentiment.webp、macro.webp。

## 六个 Agent

| Agent | 研究视角 | 视觉身份 |
|---|---|---|
| 价值派 | 估值、安全边际、现金流质量 | 沉稳的资深价值投资家 |
| 成长派 | 增长质量、利润率、预期修正 | 年轻的科技成长投资人 |
| 趋势派 | 价格结构、相对强弱、动量 | 果断的趋势交易员 |
| 量化派 | 多因子、波动预算、组合约束 | 冷静的算法研究科学家 |
| 情绪派 | 注意力、新闻情绪、拥挤与反身性 | 敏锐的市场心理分析师 |
| 宏观派 | 流动性、利率、周期、风险偏好 | 成熟的全球宏观策略师 |

## 当前交互能力

1. 从“新建实验”弹窗设置研究对象标签、20–252 个模拟交易日、每 Agent 独立初始本金和统一风险上限。
2. 六个 Agent 使用不同的研究框架，生成独立观点、置信度、信号、风险、入场触发和失效条件。
3. 每个 Agent 独立持有现金和股票；模拟器逐日记录独立账户的现金、股数、实际仓位与目标仓位、成交、费用、滑点和净值。
4. 共同市场状态、情绪、宏观、行业动量、波动和事件对所有 Agent 一致。
5. 点击任意 Agent 卡片，查看其独立账户、研究结论、仓位、风险、交易次数和最后决策。
6. 六账户净值曲线、动态排名、事件时间线和操作账本随回放时间同步，不展示未来净值和未来事件。
7. 支持自动运行、暂停、逐日推进、推进五日、直达结算、重置、拖动回放、账本筛选和完整 JSON 导出。

## Run locally

这是无外部 CDN / npm 依赖的单文件 HTML：

~~~bash
python -m http.server 8000
# open http://127.0.0.1:8000
~~~

## Browser QA

~~~bash
python -m venv .venv
.venv/bin/python -m pip install -r requirements-test.txt
.venv/bin/python -m playwright install chromium
.venv/bin/python tests/test_ui.py
.venv/bin/python tests/visual_qa.py
~~~

GitHub Actions 在隔离 Python 虚拟环境中安装 Playwright / Chromium，并运行完整交互回归、252 日压力测试和五种屏幕尺寸视觉检查。

## Truth boundary — must remain visible

**V0.4.0 仍是本地合成演示，不是真实公司投研或历史回测。** 当前没有从公司输入解析真实发行人，也没有读取真实财报、公告、行情、新闻或社交情绪；没有外部 LLM Agent、券商或真实成交。公司名称仅作为场景标签和确定性随机种子。六个 Agent 是独立本地规则策略，不是实际运行的外部 LLM worker。模拟收益不是未来预测或投资建议。

## Real-data integration gate

真实公司投研仍需完成 REAL_DATA_BLUEPRINT.md 中的公司实体解析、许可数据接入、point-in-time 证据快照、独立 Agent worker、确定性模拟器和可审计事件账本。不能用公司名称 seed 出来的合成因子冒充真实公司研究，也不能把 ChatGPT 会话里的 MCP 数据访问误称为网页应用已经接通。
