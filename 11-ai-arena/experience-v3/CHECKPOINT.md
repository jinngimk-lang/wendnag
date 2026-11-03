# Finance Research Lab checkpoint — 2026-11-03

## User's clarified product intent

The Capital Theater screenshot is a visual stage, not the product's complete behavior. The intended Finance Arena loop is:

**company input → independent faction research → cross-examination → user-configured trading days → shared changing market environment → separate paper portfolios → full operation ledger → replay and report.**

A company label alone must never be presented as a company-specific research result. Current V0.3 is explicitly a synthetic local interaction prototype.

## Current implementation

- Path: `11-ai-arena/experience-v3/index.html`.
- Six strategy factions: Value & Quality, Growth, Technical/Momentum, Quant, Sentiment, Macro/Regime.
- Each faction shows lead analyst, bear-case challenger and risk officer role templates.
- Independent stance, thesis, confidence, synthetic signals, risks and target exposure.
- Cross-examination view preserves disagreement rather than forcing a false consensus.
- User chooses 20–252 simulated trading days, equal starting capital ($50k/$100k/$250k/$500k) and a shared risk cap.
- Deterministic seeded synthetic market path; macro, sentiment, sector and volatility evolve daily; event shocks are explicit.
- Six independent portfolios share the same market path and transaction-cost model.
- Daily BUY / SELL / HOLD decision for each faction.
- Ledger records market/fill price, quantity, target weight, notional, cash, shares, commission, slippage, reason, event and sentiment.
- Daily replay, auto-play, pause, next day, next five days, finish, reset and scrub.
- Event feed, four-factor panel, equity curves, dynamic ranking and benchmark buy-and-hold fixture.
- JSON export includes inputs, seed, research, market snapshots, events, results and full operations.
- `README.md`, `ARCHITECTURE.md`, `TEST_REPORT.md`, `requirements-test.txt`, `tests/test_ui.py`.

## Truth boundary

No live company research, licensed financial data, market news, LLM workers, broker or real orders are connected. The six agents are independent deterministic rule-based strategy functions; 18 role cards are workflow templates, not real LLM calls. Company text is a display label and deterministic demo seed only. Never call this a backtest or forecast.

## QA

- Isolated Python virtual environment created.
- Playwright / Chromium browser tests pass.
- Responsive widths 1440 / 1024 / 768 / 390 / 320.
- 252-day stress test passes with 1,512 daily decisions.
- Dynamic market factors and sentiment change; strategy weights respond to evolving environment.
- Replay filters future ledger rows and future chart points.
- Export JSON, deterministic rerun, no console/page errors.

## Next concrete work

1. Add a real Research Provider adapter for issuer filings, financial statements, point-in-time prices, company/sector news, macro releases and sentiment. Every record needs source URL, published time, retrieval time, license and snapshot ID.
2. Build an immutable shared evidence pack and give each faction isolated research context; do not let factions receive unequal time windows or future data.
3. Replace the six local strategy functions with separately invoked LLM/agent workers; each must return typed thesis, evidence refs, confidence, counter-thesis, invalidation trigger and risk constraints. Keep deterministic simulator authoritative.
4. Build a real event ledger / paper-execution backend with corporate actions, market calendar, liquidity, fill rules, fees, slippage, cash/positions and state hashes.
5. Validate on held-out point-in-time data against buy-and-hold and simple factor baselines before describing comparative performance.
6. Keep live brokerage execution out of MVP.

## Recovery

Read `11-ai-arena/PROJECT.md`, `STATUS.md`, `ARCHITECTURE.md`, this file, and `experience-v3/README.md` before continuing. Keep V0.1 and V0.2 unchanged for comparison.