# Finance Arena — Real Company Research Integration Blueprint

**Status:** architecture proposal; not connected to the static HTML demo. Do not describe V0.3.1 as live company research.

## 1. Input resolution

User may enter a company name, ticker or exchange-qualified symbol. Resolve to a canonical issuer record before research:

- legal issuer name, ticker, exchange, share class, CIK and currency;
- active/inactive/tradable state and symbol aliases;
- confidence and ambiguity list when multiple issuers match.

Never silently choose between similarly named companies. The user confirms only when entity resolution is ambiguous.

## 2. Shared evidence pack

Build one immutable snapshot for all six factions. Suggested record schema:

```json
{
  "evidence_id": "ev_...",
  "issuer_id": "CIK-or-provider-id",
  "source_type": "filing|financial_metric|price_bar|news|macro|sentiment",
  "title": "source title",
  "url": "https://...",
  "published_at": "ISO-8601",
  "available_at": "ISO-8601",
  "retrieved_at": "ISO-8601",
  "period_end": "YYYY-MM-DD",
  "value": null,
  "unit": null,
  "provider": "provider-id",
  "license": "terms/version",
  "snapshot_id": "snapshot-...",
  "content_hash": "sha256:..."
}
```

A research run stores a point-in-time cutoff. A document is usable only if it was publicly available by that cutoff; filing period end alone is not enough. All agents receive the same pack and cutoff.

## 3. Candidate data-source adapters

| Domain | First adapter candidates | Required guardrails |
|---|---|---|
| Issuer / filings / financial facts | SEC EDGAR submissions + companyfacts; issuer IR pages as secondary source | User-Agent, rate limits, filing accession, filed/accepted timestamps, amendment lineage, source URL |
| Market bars / quotes | Alpaca market data adapter; optional OpenBB provider abstraction | Explicit feed (IEX/SIP), timestamp, delayed/real-time label, split/dividend adjustment, missing-bar checks, stale/outlier spread checks |
| News / company events | Licensed news provider or official issuer / regulator feeds | Source licensing, published time, duplicate clustering, article corrections, company-entity matching |
| Macro | FRED / official central-bank and statistics releases | Release time, vintage/revision awareness, unit/frequency, geography |
| Social / crowd sentiment | Licensed Stocktwits/Reddit/social provider where terms permit | Never scrape against terms; store sample size, language, bot/noise caveat, model/version and confidence |

A connected Alpaca MCP read-only session was verified during this work for asset metadata, a 21-session NVDA daily-bar sample (2026-10-05 to 2026-11-02) and a snapshot. This proves the ChatGPT session can access that connector; it does **not** mean the website has Alpaca credentials or can call the MCP directly. The returned IEX snapshot also showed a wide bid/ask spread, which is why production ingestion needs stale/outlier and spread-quality guards.

## 4. Agent graph

```text
User input
  ↓
Entity resolver
  ↓
Shared point-in-time evidence pack (immutable)
  ├─ Value & Quality faction: lead → bear challenge → risk review
  ├─ Growth faction: lead → bear challenge → risk review
  ├─ Technical / Momentum faction: lead → bear challenge → risk review
  ├─ Quant faction: lead → model challenge → risk review
  ├─ Sentiment faction: lead → reflexivity challenge → crowding review
  └─ Macro / Regime faction: lead → scenario challenge → tail-risk review
  ↓
Cross-examination (evidence-linked disagreement)
  ↓
Structured strategy policy per faction
  ↓
Deterministic paper simulator + event-driven policy updates
  ↓
Daily ledger / ranking / replay / report
```

Each faction output should be typed and evidence-linked:

- `stance`, `horizon`, `confidence`, `thesis`;
- `evidence_refs[]` with supporting and contradicting evidence;
- `bull_case`, `bear_case`, `key_disagreement`;
- `entry_triggers[]`, `invalidation_conditions[]`;
- `target_weight`, `max_weight`, `stop_or_exit_policy`;
- `uncertainties[]`, `missing_data[]`, `model_version`, `prompt_version`.

Do not expose hidden chain-of-thought. Expose concise conclusions, cited evidence, counterarguments and uncertainty.

## 5. Keep LLM cost and simulator determinism under control

Do not call 18 LLM agents six times per day for a 252-day run. A better design is:

1. Run research roles once in parallel on the shared evidence snapshot.
2. Run a structured cross-examination and risk review.
3. Each faction emits a bounded strategy policy, not an arbitrary order.
4. A deterministic engine applies that policy daily and records `HOLD` when no trigger fires.
5. Re-invoke agents only on scheduled review intervals or material events (earnings, guidance, volatility regime shift, sentiment shock, risk trigger).
6. The simulator remains authoritative for position, cash, fill, fee, slippage and equity calculations.

This preserves a rich daily story and ledger without making the outcome depend on hundreds of unbounded model calls.

## 6. Paper-trading engine requirements

- exchange calendar and timezone;
- point-in-time bar availability and fill timing;
- market/limit order semantics, partial fills and liquidity caps;
- spread, slippage, commission and borrow costs where relevant;
- dividends, splits, mergers, symbol changes and delistings;
- cash, shares, buying power, exposure and risk limits;
- benchmark with matching corporate-action and cost assumptions;
- deterministic replay from seed + data snapshot + policy versions.

## 7. Event ledger and replay

Production ledger should be append-only. Each event includes `run_id`, monotonically increasing sequence, event type, actor/faction, timestamp, input snapshot ID, evidence refs, policy/model versions, payload hash, previous event hash and resulting state hash. Corrections are compensating events; do not rewrite prior fills.

The replay UI should reconstruct the exact state at any sequence/day. A what-if branch creates a new run ID and leaves the original immutable.

## 8. Suggested service boundaries

- `POST /api/research-runs` — create run and resolve issuer.
- `POST /api/research-runs/{id}/evidence` — attach/freeze evidence pack.
- `POST /api/research-runs/{id}/research` — run faction research and cross-exam.
- `POST /api/research-runs/{id}/simulation` — create paper simulation from approved policies.
- `GET /api/research-runs/{id}/events` — event stream / ledger.
- `GET /api/research-runs/{id}/replay?day=N` — state snapshot at a day.
- `GET /api/research-runs/{id}/report` — settled report and score breakdown.
- `POST /api/research-runs/{id}/branches` — fork a what-if scenario.

## 9. Research references reviewed

- `TauricResearch/TradingAgents` (Apache-2.0): specialist analyst team, bull/bear researcher debate, trader and risk manager, portfolio manager approval. Its 2026-10 release notes explicitly call out fixes to filing-date leakage and settlement across market holidays. Reuse the workflow ideas, not its entire runtime by default.
- `AI4Finance-Foundation/FinRobot` (Apache-2.0): current project describes PydanticAI + FastAPI + React/Tauri architecture and a separation between deterministic financial computation and LLM narration. Strongest direct reference for research/report production.
- `microsoft/qlib` (MIT): end-to-end quantitative research pipeline, point-in-time data, factor research, risk modeling and portfolio optimization. Candidate for a later quant-research module, not a mandatory dependency for the first product slice.
- `nautechsystems/nautilus_trader` (LGPL-3.0): deterministic event-driven backtest/live engine with modular adapters and a shared strategy runtime. Technically relevant for a later serious simulator, but its Rust/Python footprint and licensing review make it a later-stage option.
- `mementum/backtrader` (GPL-3.0): mature backtesting concepts, but avoid embedding it in a proprietary product without a deliberate copyleft compliance decision.

No third-party source code was copied or vendored in this milestone. Full license texts were inspected before documenting candidates.