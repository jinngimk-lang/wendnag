# Finance Research Lab V0.3 — 六派系投研与模拟交易

这是 AI Arena Finance Arena 的第三个可审查交互方向。它把原先的「输入公司名 → 看四个固定收益席位」改为完整的研究到复盘流程：

1. 输入公司/代码，设置模拟交易日数、每派系本金与共同风险上限。
2. 六个独立策略派系分别形成观点：价值、成长、趋势、量化、情绪、宏观。
3. 每个派系展示主研、反方挑战、风控三个角色模板；输出不同的研究框架、结论、风险、触发条件与初始仓位倾向。
4. 展示交叉质询，不把不同策略强行合并成一个「AI 共识」。
5. 六个派系使用同一条合成市场路径、同样的本金/费用/滑点/风险上限，独立调整目标仓位。
6. 用户可按日推进、自动运行、暂停、推进五日、直达结算或拖动回放。
7. 每个派系每天均生成 BUY / SELL / HOLD 决策日志；另记录市场情景事件、情绪、宏观流动性、行业动量、波动水平。
8. 操作日志包含市价/成交价、数量、目标仓位、成交金额、现金、持股、费用与滑点，并支持派系/动作/周期筛选。
9. 可导出完整 JSON（研究、市场路径、事件、组合净值与逐日决策）。

## Run

单文件原型，无外部 CDN 或 npm 依赖：

```bash
python -m http.server 8000
# open http://127.0.0.1:8000
```

浏览器也可以直接打开 `index.html`。

## QA

```bash
python -m venv .venv
.venv/bin/python -m pip install -r requirements-test.txt
.venv/bin/python -m playwright install chromium
.venv/bin/python tests/test_ui.py
```

测试脚本优先使用 `/usr/bin/chromium`；若不存在则使用 Playwright 自带浏览器。若本机已有 Chromium，可跳过浏览器安装步骤。

## Truth boundary — read before presenting results

**本版所有数据均为合成演示数据。** 当前没有真实公司公告、财报、行情、新闻、宏观数据、外部 LLM Agent、券商或真实成交。输入公司名只影响可复现的演示场景种子和显示标签，不会抓取或推断该公司的事实。六个派系的研究观点由本地独立规则生成；每派系的三种角色是工作流模板，不是 18 次真实模型调用。收益曲线不是历史回测、未来预测或投资建议。

## Next integration gate

先把本原型作为交互/信息架构验证，不接实盘。真实 Finance vertical slice 必须另行实现：
- 公司实体解析与交易所/证券标识；
- 有许可的数据网关：时点财报/公告、历史行情、公司新闻、行业数据、宏观事件、情绪数据；
- 每条证据记录 URL/来源、发布时点、抓取时点、授权与快照 ID；
- 同一不可变 point-in-time evidence pack 发给各派系，避免信息不公平；
- 独立 Agent worker（主研/挑战/风控）提交结构化研究结论和 evidence refs；
- 由确定性 paper simulator 验证目标仓位、订单、费用、滑点、成交与风险约束；
- append-only event ledger、策略/模型/提示版本、可复现 seed、审计与回放；
- 与 buy-and-hold / 指数 / 简单因子基线比较，做 look-ahead leakage 测试。

V0.3 是 Finance-first prototype，不覆盖 Marketing/Life Arena；V0.1 和 V0.2 保留用于视觉与交互对比。