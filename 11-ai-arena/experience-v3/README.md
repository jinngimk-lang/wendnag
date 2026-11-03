# AI Arena — Finance Research Lab V0.3.2

Finance Arena 的 research-to-paper-simulation 原型。它不再只是“输入公司名后看四个固定收益席位”，而是把完整比赛过程拆成：

**公司/代码输入 → 六派系独立投研 → 反方交叉质询 → 用户设置交易周期 → 共同市场环境 → 独立模拟组合 → 每日操作账本 → 回放与复盘。**

## 当前交互能力

1. 输入公司名或股票代码；设置 20–252 个模拟交易日、每派系初始资金和统一风险上限。
2. 六个派系使用不同研究框架：价值与质量、成长、技术趋势、量化、市场情绪、宏观环境。
3. 每个派系有主研、反方挑战、风控三个角色模板；报告显示观点、置信度、驱动信号、风险、触发条件和观点失效条件。
4. 交叉质询动态比较本轮最积极与最谨慎的观点，不伪造单一 AI 共识。
5. 六个派系在相同价格路径、初始资金、费用、滑点、风险上限和模拟时钟下独立管理仓位。
6. 用户可自动运行、暂停、逐日推进、推进五日、直达结算、重置或拖动时间轴回放。
7. 每个派系每天均有 BUY / SELL / HOLD 决策；日志记录市场价、成交价、数量、目标仓位、成交金额、现金、持股、费用、滑点、决策原因、市场涨跌、宏观、情绪、行业动量、波动率和事件。
8. 排名按演示风险分数排序；图表、市场事件、因子面板和日志均随回放时间同步，不展示未来事件或未来净值。
9. 单日推进时，按真实模拟净值变化触发钞票动效：盈利由中央表现池流向派系，亏损由派系回流中央；金额、方向和数量均由当日净值变化决定，不随机播放。聚合盈亏正负同步切换绿/红。
9. 完整 JSON 导出包含 run ID、版本、输入、合成证据包声明、市场路径、事件、基准、结果和逐日决策。

## Run locally

这是无外部 CDN / npm 依赖的单文件 HTML：

```bash
python -m http.server 8000
# open http://127.0.0.1:8000
```

## Browser QA

```bash
python -m venv .venv
.venv/bin/python -m pip install -r requirements-test.txt
.venv/bin/python -m playwright install chromium
.venv/bin/python tests/test_ui.py
```

本工作环境使用系统 Chromium 和预装 Playwright 包运行隔离虚拟环境测试：

```bash
PYTHONPATH=/opt/pyvenv/lib/python3.13/site-packages .venv/bin/python tests/test_ui.py
```

## Backend evidence gateway core (V0.1)

The provider-agnostic standard-library contract lives in `../backend/research_gateway.py`: exact issuer resolution, immutable source-attributed evidence, point-in-time snapshot freezing, evidence-linked typed faction output and a hash-chained in-memory event ledger. The no-network SEC EDGAR submissions/companyfacts parser also maps filing accessions to exact `acceptanceDateTime` availability; license status defaults to `review_required`. It has no live fetcher or persistence yet. Run its tests from `11-ai-arena/` with:

```bash
python -m unittest discover -s backend/tests -v
```

## Truth boundary — must remain visible

**V0.3.2 仍是本地合成演示，不是实际公司投研。** 当前没有从公司输入解析真实发行人，也没有读取真实财报、公告、行情、新闻或社交情绪；没有外部 LLM Agent、券商或真实成交。公司名称仅作为场景标签和确定性随机种子。六个派系由独立本地规则生成；18 个角色是工作流模板，不是 18 次真实模型调用。模拟收益不是历史回测、未来预测或投资建议。

## Real-data integration gate

真正的公司投研必须先完成 `REAL_DATA_BLUEPRINT.md` 中的公司实体解析、许可数据接入、point-in-time 证据快照、独立 Agent worker、确定性模拟器和可审计事件账本。不能用公司名称 seed 出来的合成因子冒充真实公司研究，也不能把 ChatGPT 会话里的 MCP 数据访问误称为网页应用已经接通。

V0.1 控制室和 V0.2 Capital Theater 保留作视觉对照；V0.3.2 是 Finance-first 交互验证版本。