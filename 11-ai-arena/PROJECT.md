# PROJECT — AI Arena

## 1. Product definition

AI Arena is a multi-agent competition and simulation platform. A user supplies a compact prompt (company, product, campaign, or life choice), selects or accepts a match preset, presses **Start Arena**, and watches multiple specialist agents reason, act, react to a changing environment, and receive comparable scores.

The emotional promise is “set the match in motion, then watch what happens.” Do not promise effortless wealth, guaranteed virality, or deterministic life outcomes.

## 2. Product architecture at the business level

One platform with three vertical products:
- Finance Arena
- Marketing Arena
- Life Arena

Shared platform capabilities:
- Match setup and presets
- Agent roster, personas, capabilities and budgets
- Round orchestration and event streaming
- Domain simulator and data connectors
- Evidence ledger and provenance
- Scoring, rankings, replay and shareable match reports
- User workspaces, saved matches and comparisons

Domain-specific rules and scoring must remain adapters, not hard-coded into the shared engine.

## 3. Core interaction loop

1. **Prompt** — user enters a natural-language subject.
2. **Configure** — show defaults for timeframe, starting resources, environment, and scoring; keep advanced controls optional.
3. **Reveal** — introduce competitors and their strategies.
4. **Run** — stream meaningful events, not raw chain-of-thought.
5. **React** — competitors can adapt only through explicit, logged actions.
6. **Settle** — calculate results using domain-specific deterministic rules where possible.
7. **Explain** — show winner, score breakdown, uncertainty, evidence and counterfactuals.
8. **Replay / branch** — inspect a decision or alter a variable and rerun.

## 4. Product principles

- **Competition must be fair:** same initial resources, time window, data availability and constraints.
- **Independent agents:** competitors need distinct objectives, evidence paths and strategy priors; avoid superficial persona renaming.
- **Environment before theatrics:** simulations must have a meaningful model of the world. UI animation cannot substitute for causal logic.
- **Evidence over confidence:** separate observed facts, assumptions, model estimates and simulated events.
- **Replayability:** every important decision and state transition is recorded.
- **Bounded autonomy:** agents operate within budgets, tools, permissions and stop conditions.
- **Uncertainty is visible:** use ranges, scenario bands and calibration rather than false precision.
- **No hidden real-world actions:** paper trades, draft posts and scenario actions are clearly distinguished from actual execution.
- **User agency:** users can pause, inspect, branch, compare and stop a match.

## 5. Arena definitions

### 5.1 Finance Arena

Input: company/ticker and optional investment horizon.

Competitors: value, growth, technical, sentiment, macro, contrarian/short, quant. Each produces a thesis, evidence references, confidence, entry/exit policy, sizing and risk limits.

Simulation: historical point-in-time research and paper trading first. All competitors receive the same start capital, benchmark, fees, slippage model, market calendar and information cutoff. No future data may leak into a decision.

Scoring: total return, benchmark-relative return, max drawdown, volatility, Sharpe/Sortino where valid, turnover, exposure and consistency. Use multiple awards; raw return alone is not the winner criterion.

Never enable live brokerage execution in the MVP. If ever added, it is a separate opt-in product requiring explicit authorization, account-level safeguards, suitability/legal review and hard risk controls.

### 5.2 Marketing Arena

Input: product/content, audience, offer, price, geography, campaign budget and objective.

Competitors: emotional storytelling, performance/direct response, expert review, creator/UGC, community/organic, brand-building.

Environment: platform adapters with explicit assumptions about feed ranking, audience segments, content fatigue, social graph, moderation and feedback loops. OASIS is a candidate research engine for social interaction dynamics, not a turnkey predictor of platform reach.

Outputs: platform-specific content concepts and draft assets, scenario-based reach/engagement/click/conversion distributions, audience reactions, risk flags and budget allocation. Clearly label simulated values. Calibrate against actual campaign data before presenting forecasts as empirically calibrated.

Never auto-publish or spend ad budget in the MVP. Real publishing requires per-platform authorization and review.

### 5.3 Life Arena

Input: user-defined starting conditions and choice (career, city, relationship/family, education, entrepreneurship, lifestyle).

Competitors: stability, ambition, financial optimization, wellbeing, freedom, community/family perspectives.

Environment: explicit causal assumptions for income, cost of living, career progression, health/time constraints, social support, relationships and stochastic shocks. Keep personal data optional and minimize collection.

Outputs: parallel scenarios at 1/3/5/10 years, timeline events, trade-offs, sensitivity analysis and branch points. Present ranges and multiple plausible futures, never a single deterministic prophecy or a prescriptive life verdict.

## 6. MVP recommendation

Build the **Finance Arena as the first vertical**, but launch it as a historical/paper-trading research competition. It has comparatively measurable outcomes and clear scoring. In parallel, validate the cross-domain engine with a small marketing simulation demo; defer high-fidelity life simulation until memory, causal state and ethical presentation are stronger.

MVP match:
- one ticker/company;
- 4–6 strategies;
- one fixed historical period and common information cutoffs;
- same notional capital and trading rules;
- event timeline, portfolio curves, leaderboard, score explanation and replay;
- seeded demo data and a transparent “simulation” label.

## 7. Non-goals for first release

- Live financial order execution
- Real social media publishing or paid ad spend
- Claims of accurate individual life prediction
- Unbounded agent-to-agent chat
- Million-agent simulation without a validated need
- User-facing raw chain-of-thought
- A token/points economy before the core match loop proves useful

## 8. Success measures

- Time from prompt to first meaningful event
- Match completion rate
- Replay / branch / compare usage
- Evidence inspection rate
- User ability to correctly distinguish real data from simulation
- Repeat matches and saved match rate
- Scoring stability and calibration against known outcomes
- Cost and latency per completed match

## 9. Decision log

- 2026-10-30: Adopt one shared Arena Engine with three domain adapters.
- 2026-10-30: Treat “watchable competition” as the core product experience.
- 2026-10-30: Finance MVP is paper/historical simulation only; no live trading.
- 2026-10-30: Marketing reach metrics are simulated unless calibrated by real campaign data.
- 2026-10-30: Life outputs are branching scenarios, not deterministic predictions.
- 2026-10-30: Deliver a dependency-free HTML/CSS/JS prototype as the first reviewable product artifact; keep all demo events and metrics explicitly simulated.

## 2026-11-03 visual experience decision (revisable)

We explicitly declined to continue indefinite surface-level iteration on the V0.1 broadcast dashboard. Created a parallel, independently testable **Capital Theater** under `experience-v2/`: money-flow events become the main visual metaphor, backed by deterministic accounting and an explicit simulation label. Finance is the validation vertical; Marketing and Life remain available in V0.1.

The visual rule is **data-to-effect, never effect-to-data**. Winning cash visuals flow from the central notional pool to the Agent; losing cash visuals flow back. Nothing about particle counts, coin stacks, sound or lighting is allowed to change balances. Ranking remains risk-adjusted, and the sample fixture never becomes a personalized company forecast.

Before investing in large GPU/WebGL animations or photorealistic source assets, compare both directions with actual user tests; retire or redesign the new direction if it increases false confidence. For research and engineering checkpoints see `experience-v2/VISUAL_RESEARCH.md` and `experience-v2/CHECKPOINT.md`.

## 2026-11-03 Finance Arena interaction clarification

The Capital Theater is a visual stage, not the entire product. The Finance Arena's primary user journey is:

**company / ticker → independent faction research → cross-examination → user-configured trading-day window → changing shared market environment → independent paper portfolios → complete operation ledger → replay and report.**

The six factions are Value & Quality, Growth, Technical/Momentum, Quant, Sentiment, and Macro/Regime. Each faction should eventually use a lead researcher, bear-case challenger and risk officer. All factions receive the same immutable point-in-time evidence pack, market path, starting capital, fee/slippage assumptions and risk limits, while maintaining independent theses and portfolio states.

V0.3 at `experience-v3/` is a local deterministic interaction prototype. It uses synthetic company-seeded research signals and synthetic market/event/sentiment data. The six strategy functions are not LLM calls; role cards are workflow templates. Do not present any result as company-specific research, historical backtest or forecast.

The production gate is a licensed point-in-time Research Provider, shared evidence snapshots with provenance, independently invoked structured Agent workers, a deterministic paper-execution engine and an append-only replayable ledger. Live brokerage execution remains out of MVP scope.


## 2026-11-03 Finance Arena V0.3.1 auditability refinement

The local prototype now makes each faction's entry trigger and invalidation condition explicit, dynamically compares the strongest and most cautious synthetic thesis, and attaches the market context (market return, macro, sentiment, sector, volatility, regime and event) to every daily decision. Replay hides future event counts as well as future ledger/chart data. The buy-and-hold benchmark now invests post-entry-fee cash. JSON export records run ID, strategy/simulator versions, synthetic evidence-pack status and benchmark assumptions.

These changes improve traceability but do **not** turn the prototype into real company research. The real-data boundary is specified in experience-v3/REAL_DATA_BLUEPRINT.md: issuer resolution, licensed point-in-time evidence, common immutable snapshots, independent typed faction workers, event-triggered strategy updates, deterministic paper execution and append-only replayable events. Do not copy third-party agent frameworks wholesale; the latest research favors adapting the useful role/evidence patterns while keeping the domain simulator authoritative.


## 2026-11-03 Finance Arena V0.3.2 visual accounting link

The research-to-paper-simulation prototype now carries the earlier Capital Theater money metaphor into the daily simulation. A one-day forward step creates paper-bill movement only from the signed net-value change: gains flow from the central performance vault toward that faction; losses flow from the faction back toward the vault. Amount chips, direction, bill intensity and aggregate red/green color are driven by the same accounting delta. It is explicitly a visual metaphor, not a transfer between separate portfolios. The animation is not triggered by a multi-day jump or arbitrary replay scrub, and reduced-motion cleanup is supported. This joins the V0.2 spectator appeal to V0.3.1's more complete research and operation audit without making animation the source of truth.

## 2026-11-03 backend evidence gateway contract V0.1

The first executable backend contract is now under `backend/research_gateway.py`. It is deliberately provider-agnostic and standard-library-only: exact issuer resolution with explicit ambiguity, immutable source-attributed evidence records, point-in-time snapshot freezing, typed faction outputs validated against the common snapshot, and an append-only in-memory hash chain. The core fails closed on future evidence, foreign issuers, unapproved licenses, invalid references and target weights above the declared cap.

This is not yet a live research service. There are no SEC/Alpaca/news/macro adapters, API credentials, LLM calls, durable database, HTTP API or broker actions. The next production step is to implement and test provider adapters with source-specific availability timestamps and license review, then persist snapshots/events before adding model workers. The deterministic paper simulator remains authoritative for positions, fills, fees and P&L.

## 2026-11-03 SEC EDGAR parser milestone

The backend now includes a no-network parser for SEC submissions and companyfacts JSON. Financial facts are joined to the exact accession and filing `acceptanceDateTime`; reporting period end and date-only filing date are descriptive metadata, never substitutes for public-availability time. Missing acceptance times, unknown accessions and form mismatches are excluded. License status defaults to `review_required`, and the evidence pack refuses to freeze unapproved records.

This parser does not fetch data. A production SEC fetcher must implement the required User-Agent, request pacing, retry/backoff, caching and accession lineage, and must preserve the original point-in-time release timestamps. No terms approval or live SEC connection is implied.
