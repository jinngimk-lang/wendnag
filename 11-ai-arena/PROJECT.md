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
