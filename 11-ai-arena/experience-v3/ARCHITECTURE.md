# Finance Arena V0.3 — Research-to-Paper-Simulation Contract

## Product loop

`SUBJECT → CONFIGURE → SHARED EVIDENCE SNAPSHOT → INDEPENDENT RESEARCH → CROSS-EXAM → PAPER SIMULATION → DAILY LEDGER → SETTLEMENT / REPLAY`

The user controls simulation length in trading days (20–252), equal starting capital, and a shared portfolio-risk cap. The six factions are:

| Faction | Primary lens | Typical decision drivers |
|---|---|---|
| Value & Quality | valuation, cash-flow quality, balance-sheet resilience | valuation gap, quality, margin of safety |
| Growth | revenue/earnings growth, market expansion, expectation revisions | growth persistence, margin trajectory, estimate revisions |
| Technical / Momentum | price structure, relative strength, trend confirmation | momentum, moving-average regime, volume confirmation |
| Quant | reproducible multi-factor signal and portfolio construction | factor score, volatility targeting, turnover and signal decay |
| Sentiment | attention, news tone, crowding and reflexivity | sentiment level/change, crowding, reversal risk |
| Macro / Regime | liquidity, rates, sector cycle, risk appetite | macro regime, correlation shift, volatility and tail risk |

Each faction exposes three role templates: lead analyst, bear-case challenger, risk officer. In V0.3 these are explanatory templates, **not actual independent LLM workers**.

## Fairness contract

Every faction receives the same:
- company task label and research-scenario seed;
- market path, event sequence and factor snapshots;
- starting capital;
- commission/slippage assumptions and risk cap;
- simulation clock and settlement rules.

Each faction owns an independent cash/share ledger and target-weight policy. Agents propose target weights; the simulator applies orders and computes balances. Agents never directly write authoritative equity.

## Synthetic prototype model

- Price is a deterministic, seeded path with daily idiosyncratic noise plus macro, sector and sentiment components.
- Synthetic events alter one or more environment factors and can create a price shock.
- Environment panel tracks macro liquidity, sentiment temperature, sector momentum and volatility.
- Every faction emits one daily decision (`BUY`, `SELL`, `HOLD`) with target weight, execution notional, fee and concise reason.
- Trading fee and slippage are fixed demonstrative rates; risk cap is shared and selected by the user.
- Equity curves, drawdown, turnover, trade count and score are derived from the same portfolio state.
- Benchmark is a synthetic buy-and-hold path using the same simulated price series.
- JSON export includes input seed, research, daily market snapshots, events, results and full decision ledger.

## Production architecture (not implemented in this static prototype)

1. **Entity Resolver** — canonical issuer, exchange, ticker, share class and corporate-action identity.
2. **Data Gateway** — licensed point-in-time filings, financials, prices, news, sector and macro feeds; source timestamp, fetch timestamp, license and snapshot ID.
3. **Evidence Pack Builder** — immutable, versioned and common to all factions; point-in-time cut-off prevents future-data leakage.
4. **Research Orchestrator** — independent role workers with isolated context and tool budgets; typed outputs include thesis, stance, confidence, evidence refs, counter-thesis, triggers, invalidation conditions and risk limits.
5. **Cross-Exam** — agents challenge claims and cite evidence; it records dissent rather than fabricating consensus.
6. **Paper Simulator** — deterministic order validation, fills, cash/shares, fees, slippage, liquidity, corporate actions, calendar and risk constraints.
7. **Append-only Event Ledger** — immutable event sequence with run ID, actor, event time, input snapshot, action, evidence refs, state hashes and version IDs.
8. **Scoring / Reporting** — total and benchmark-relative return, max drawdown, volatility, Sharpe/Sortino only when statistically valid, turnover, exposure, hit rate and calibration/uncertainty.
9. **Replay / Branch** — rebuild the UI from ledger events; allow controlled what-if branches without altering the original run.

## Required event families

`research_started`, `evidence_added`, `thesis_submitted`, `challenge_raised`, `risk_limit_set`, `market_event`, `sentiment_updated`, `action_proposed`, `order_accepted`, `fill_recorded`, `position_updated`, `risk_triggered`, `day_settled`, `match_settled`.

## Data integrity and safety gates

- No future data in historical decisions; record `published_at` and `available_at`.
- Do not treat news sentiment as fact; store source, text span, model/version, confidence and correction status.
- Keep facts, model inference, scenario assumptions and simulated events visually distinct.
- No live broker execution in MVP. Paper simulation must not share credentials or order endpoints with live trading.
- No “guaranteed profit”, “AI predicts price” or investment-advice claims.
- Validate on held-out periods and against simple baselines; publish costs, missing data and uncertainty.
- Keep all raw reasoning private; expose concise rationale and cited evidence, not hidden chain-of-thought.