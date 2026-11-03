# Finance Arena V0.3.1 — Research-to-Paper-Simulation Contract

## Product loop

`SUBJECT → CONFIGURE → SYNTHETIC RESEARCH PACK → INDEPENDENT FACTIONS → CROSS-EXAM → PAPER SIMULATION → DAILY RUN LEDGER → SETTLEMENT / REPLAY`

The production target replaces the synthetic research pack with a common immutable point-in-time evidence pack. The current HTML remains a local deterministic prototype.

## Six independent factions

| Faction | Primary lens | Typical drivers |
|---|---|---|
| Value & Quality | valuation, cash-flow quality, balance-sheet resilience | valuation gap, quality, margin of safety |
| Growth | revenue/earnings growth, market expansion, expectation revisions | growth persistence, margin trajectory, estimate revisions |
| Technical / Momentum | price structure, relative strength, trend confirmation | momentum, moving-average regime, volume confirmation |
| Quant | reproducible multi-factor signal and portfolio construction | factor score, volatility targeting, turnover, signal decay |
| Sentiment | attention, news tone, crowding and reflexivity | sentiment level/change, crowding, reversal risk |
| Macro / Regime | liquidity, rates, sector cycle, risk appetite | macro regime, correlation shift, volatility and tail risk |

Each faction exposes lead analyst, bear-case challenger and risk officer role templates. In V0.3.1 they are explanatory templates, **not actual independent LLM workers**.

## Fairness contract

All factions receive the same:
- company task label and scenario seed;
- market path, event sequence and factor snapshots;
- starting capital;
- commission, slippage assumptions and risk cap;
- simulation clock and settlement rules.

Each faction owns an independent cash/share ledger and target-weight policy. The simulator applies orders and computes balances; strategy functions never write authoritative equity.

## Synthetic model

- Deterministic seeded price path with idiosyncratic noise plus macro, sector and sentiment components.
- Synthetic events alter environment factors and may add a price shock.
- Environment panel tracks macro liquidity, sentiment temperature, sector momentum and volatility.
- Every faction emits one daily `BUY` / `SELL` / `HOLD` record.
- Each operation now carries its own market-context snapshot: market return, macro, raw sentiment, sector, volatility, regime and event metadata.
- Execution rows contain market/fill price, quantity, target weight, notional, fee, slippage, cash, shares and equity.
- Buy-and-hold benchmark deducts the entry fee from invested capital before calculating shares.
- Replay hides future event counts, future event cards, future ledger rows and future chart points.
- JSON export includes a `SYNTHETIC_DEMO_ONLY` evidence-pack declaration, run ID, strategy/simulator versions, benchmark assumptions and full operation context.

## Illustrative score

`totalReturnPct - 0.48 × maxDrawdownPct - 0.20 × dailyReturnVolatilityPct`

This coefficient set is only a prototype fixture, not a validated investment objective. Replay ranking recalculates the same score from observations available up to the selected day.

## Production architecture (not implemented)

1. **Entity Resolver** — canonical issuer, exchange, ticker, share class, CIK and corporate-action identity.
2. **Data Gateway** — licensed point-in-time filings, financials, prices, company/sector news, sentiment and macro feeds.
3. **Evidence Pack Builder** — immutable, versioned, source-attributed and common to all factions; enforce `published_at` / `available_at` cutoffs.
4. **Research Orchestrator** — independent role workers with isolated context/tool budgets; typed outputs include stance, thesis, confidence, evidence refs, counter-thesis, triggers, invalidation and risk limits.
5. **Cross-Exam** — challenge claims against evidence and preserve dissent; do not reveal hidden chain-of-thought.
6. **Policy / Trigger Engine** — agents produce a strategy policy once; re-evaluate on scheduled intervals or material events to avoid one LLM call per faction per day.
7. **Paper Simulator** — deterministic order validation, fills, cash/shares, fees, slippage, liquidity, corporate actions, calendar and risk constraints.
8. **Append-only Event Ledger** — immutable event sequence with run ID, actor, event time, input snapshot, action, evidence refs, state hashes and version IDs.
9. **Scoring / Reporting** — total and benchmark-relative return, max drawdown, volatility, turnover, exposure, hit rate, calibration and uncertainty; Sharpe/Sortino only when statistically valid.
10. **Replay / Branch** — rebuild the UI from ledger events; what-if branches never mutate the original run.

## Required event families

`research_started`, `evidence_added`, `thesis_submitted`, `challenge_raised`, `risk_limit_set`, `market_event`, `sentiment_updated`, `action_proposed`, `order_accepted`, `fill_recorded`, `position_updated`, `risk_triggered`, `day_settled`, `match_settled`.

## Integrity and safety gates

- No future data in historical decisions; persist `published_at`, `available_at`, `retrieved_at` and snapshot ID.
- News sentiment is a model estimate, not fact; store source, text span, model/version, confidence and correction status.
- Visually separate observed facts, model inference, scenario assumptions and simulated events.
- No live broker execution in MVP; paper simulator must not share credentials or order endpoints with live execution.
- Never promise profit or claim that AI predicts a stock price.
- Validate against buy-and-hold / index / simple factor baselines and run look-ahead leakage tests.