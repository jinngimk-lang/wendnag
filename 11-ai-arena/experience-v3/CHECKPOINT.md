# Finance Research Lab checkpoint — 2026-11-03 / V0.3.1

## User's clarified product intent

The Capital Theater screenshot is a visual stage, not the product's complete behavior. The intended Finance Arena loop is:

**company input → independent faction research → cross-examination → user-configured trading days → shared changing market environment → separate paper portfolios → full operation ledger → replay and report.**

A company label alone must never be presented as company-specific research. V0.3.1 is explicitly a synthetic local interaction prototype.

## Current implementation

- Path: `11-ai-arena/experience-v3/index.html`.
- Six strategy factions: Value & Quality, Growth, Technical/Momentum, Quant, Sentiment, Macro/Regime.
- Each faction shows lead analyst, bear-case challenger and risk officer role templates.
- Independent stance, thesis, confidence, synthetic signals, risks, entry triggers, invalidation conditions and target exposure.
- Cross-examination dynamically compares the most positive and cautious synthetic thesis scores and their target-weight difference.
- User chooses 20–252 simulated trading days, equal starting capital ($50k/$100k/$250k/$500k) and a shared risk cap.
- Deterministic seeded synthetic market path; macro, sentiment, sector and volatility evolve daily; event shocks are explicit.
- Six independent portfolios share the same market path, starting capital, transaction-cost model and risk cap.
- Daily BUY / SELL / HOLD decision for each faction.
- Every log row includes market return, raw macro/sentiment/sector/volatility, regime, event kind/title/description/shock, fill price, quantity, target weight, notional, cash, shares, fee and slippage.
- Daily replay, auto-play, pause, next day, next five days, finish, reset and scrub.
- Event count/feed are replay-aware; future event count is not exposed before its date.
- Event feed, four-factor panel, equity curves, dynamic ranking and synthetic buy-and-hold benchmark.
- Benchmark now deducts entry fee from invested capital before calculating shares.
- JSON export includes run ID, strategy/simulator versions, synthetic evidence-pack declaration, assumptions, benchmark and full operation context.
- Files: `README.md`, `ARCHITECTURE.md`, `REAL_DATA_BLUEPRINT.md`, `TEST_REPORT.md`, `CHECKPOINT.md`, `requirements-test.txt`, `tests/test_ui.py`.

## Truth boundary

No live company research, licensed financial data, market news, LLM workers, broker or real orders are connected. Six agents are independent deterministic rule-based strategy functions; 18 role cards are workflow templates, not real LLM calls. Company text is a display label and deterministic demo seed only. Never call this a backtest or forecast.

## QA

- Isolated Python venv + Playwright / Chromium.
- Responsive widths 1440 / 1024 / 768 / 390 / 320.
- 252-day stress test passes with 1,512 daily decisions.
- Dynamic market factors and sentiment change; strategy weights respond to evolving environment.
- Per-operation market context, replay filters, benchmark fee accounting, risk cap, JSON export and deterministic rerun verified.
- No console/page errors or horizontal overflow.

## Research discoveries

- TradingAgents: specialist analysts + bull/bear debate + trader/risk/portfolio manager; latest 2026-10 release notes emphasize filing-date leakage and market-holiday settlement.
- FinRobot: strongest direct architecture reference for typed role workflows, FastAPI service, deterministic computation separated from LLM narration.
- Qlib: point-in-time quantitative data, factor research, risk modeling and portfolio optimization.
- NautilusTrader: event-driven deterministic backtest/live runtime; defer due engineering footprint and LGPL-3.0 review.
- Backtrader is GPL-3.0; do not vendor into a proprietary product without deliberate compliance review.
- Alpaca read-only MCP data access is available in the ChatGPT session, but not callable directly from the static web app. A backend adapter still needs application-owned credentials and provider contract review.

## Next concrete work

1. Implement issuer resolution and a real, licensed point-in-time evidence gateway (SEC filings/facts, price bars, news, sentiment and macro releases).
2. Freeze one shared evidence pack and run six independent faction workflows with typed outputs and evidence references.
3. Use event-triggered Agent policy updates; keep the deterministic simulator authoritative and avoid 18 LLM calls every trading day.
4. Add append-only backend event ledger, state hashes, data/model/prompt versioning and replay.
5. Validate on held-out periods against buy-and-hold / index / simple factor baselines before presenting comparative performance.
6. Keep live brokerage execution out of MVP.

## Recovery

Read `11-ai-arena/PROJECT.md`, `STATUS.md`, `experience-v3/CHECKPOINT.md`, `experience-v3/README.md`, `experience-v3/ARCHITECTURE.md` and `experience-v3/REAL_DATA_BLUEPRINT.md` before continuing. Keep V0.1 and V0.2 unchanged for comparison.