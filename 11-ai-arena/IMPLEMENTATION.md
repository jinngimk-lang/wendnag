# IMPLEMENTATION — AI Arena Prototype V0.1

Updated: 2026-10-30

## 1. Delivery scope

The first clickable prototype is implemented in `prototype/`. It proves the spectator-first interaction loop across all three verticals. It is a front-end experience prototype, not a production simulation service.

## 2. Runtime and stack

- Plain HTML5, CSS and vanilla JavaScript.
- No framework, package install, remote font, analytics, API key or external runtime dependency.
- Python's built-in HTTP server is sufficient for local preview.
- Playwright + Chromium are used for interaction and responsive smoke checks.
- HTML, CSS and JavaScript are stored as gzip-compressed Base64 text assets in this branch; `prototype/unpack.py` restores readable source.

## 3. UI architecture

`app.js` contains three domain configurations (`finance`, `marketing`, `life`) behind one presentation shell. Each configuration provides prompt labels, examples, Agent roster, domain-specific stage visualization, summary metrics, six event steps, scoring disclosure and match rules.

Shared controls handle mode switching, subject input, match start, pause/resume, fast-forward, reset, event inspection, Agent detail, report summary and share-copy behavior.

## 4. Prototype event lifecycle

`READY → RUNNING → PAUSED (optional) → SETTLED`

A start action locks the subject and initializes the match. Six seeded milestones update the event ledger, progress indicator, Agent statuses and leaderboard. Fast-forward applies the remaining events synchronously. Reset returns to the ready state.

This is a deterministic UI fixture. It is not a real multi-agent orchestrator and must not be presented as one.

## 5. Domain-specific demo behavior

### Finance
- Six strategies: value, growth, quant, sentiment, macro and risk.
- A sample normalized-portfolio curve, shared simulated capital and fixed 90-day window.
- The illustrative ranking uses a composite score rather than raw return alone.
- No real market data, brokerage connection or order execution.

### Marketing
- Six creative / growth / brand / safety perspectives.
- Four abstract channel cards and a small audience-network visualization.
- Reach ranges are seeded simulated values, not platform predictions.
- No platform API, publishing, paid spend or real audience data.

### Life
- Six decision perspectives and three parallel scenario cards.
- Explicit time horizons and editable assumptions are described in the UI.
- The result is framed as preference-fit, not a universal life ranking.
- No personal profile is collected or uploaded; no deterministic prediction is made.

## 6. Trust and safety presentation

- The environment is labelled as simulation/demo throughout.
- The UI shows concise public event summaries rather than hidden chain-of-thought.
- Agent detail separates thesis, evidence and risk.
- The prototype explicitly discloses that it does not connect to real trading, ad spend, publishing or personal data.
- Future production runs must persist input snapshots, model/prompt versions, data provenance, budgets, simulator version, scoring version, random seed and event history.

## 7. Responsive and accessibility decisions

- Desktop: persistent sidebar and two-column match workspace.
- Tablet: compact icon rail and responsive content grid.
- Mobile: narrow icon rail, stacked stage/leaderboard/event panels and two-column Agent cards.
- Semantic buttons, labelled inputs, dialog elements, visible focus states and reduced-motion support are included.

## 8. Known prototype limitations

- Demo events and scores are pre-seeded fixtures.
- No backend persistence, authentication, streaming API or model invocation.
- No empirical calibration for market, platform or life outcomes.
- The connected Figma account currently reports a View seat, so no editable Figma file was created. The HTML/CSS source is the current design artifact.

## 9. Next engineering slice

Implement Finance Arena as a reproducible historical/paper-trading vertical slice: point-in-time data snapshots, a deterministic execution simulator, four strategies, versioned risk-aware scoring, append-only event ledger, pause/resume, replay and independent benchmark fixtures. Keep live brokerage execution out of scope.

## 10. Finance Research Lab V0.3 interaction prototype

The latest Finance-first UI is in `experience-v3/`. It covers six independent rule-based faction theses, cross-examination, a user-selected 20–252 trading-day window, shared synthetic market factors/events, separate paper portfolios, daily operation records and replay. It is a deterministic front-end fixture—not real company research, LLM invocation, licensed data, historical backtest or broker execution. See its `ARCHITECTURE.md` for the production service boundary and `TEST_REPORT.md` for browser QA.


## 11. Finance Research Lab V0.3.1 auditability refinement

V0.3.1 adds faction-specific trigger/invalidation fields, dynamic thesis comparison, per-operation market-factor/event snapshots, replay-aware event counts, corrected benchmark entry-fee accounting and versioned JSON provenance. The full real-data/agent service boundary is documented in experience-v3/REAL_DATA_BLUEPRINT.md. The prototype remains synthetic; these refinements do not represent actual issuer research or live LLM workers.


## 12. Finance Research Lab V0.3.2 — Capital Flow motion

One-day playback now animates original bill-note elements from the central performance vault to a faction on positive daily equity change, and from a faction back to the vault on negative change. The signed delta determines direction and displayed amount; small changes that would round to zero are suppressed. Aggregate P&L color follows the same sign. Multi-day jumps and arbitrary timeline scrubs do not replay synthetic money transfers. The effect is a spectator visualization only; separate faction portfolios do not actually transfer cash. Both directions and animation cleanup are browser-tested.

## 13. Backend evidence gateway contract V0.1

Added `backend/research_gateway.py` as a standard-library-only foundation for the real-data architecture. The module defines exact issuer-resolution outcomes, immutable evidence records with UTC publication/availability/retrieval timestamps and provider/license metadata, deterministic point-in-time snapshot freezing, typed faction research with snapshot-bound evidence references and weight caps, and an append-only in-memory SHA-256 hash chain. Twelve unit tests cover ambiguity, look-ahead exclusion, provenance/license gates, immutability, evidence-reference validation and tamper detection.

This is a contract layer, not a provider integration or production API. No network fetch, credentials, LLM runtime, database persistence or broker capability is present. GitHub Actions now runs these backend tests and the existing Playwright browser suite for AI Arena changes.

## 14. SEC EDGAR submissions/companyfacts parser V0.1

Added `backend/adapters/sec_edgar.py` as a no-network normalization adapter. It joins companyfacts observations to submissions by accession number and uses the exact filing `acceptanceDateTime` as both publication and availability time. It never substitutes period end or date-only `filingDate` for the information-availability gate. Missing acceptance times, unmatched accessions and form mismatches are excluded; conflicting duplicate accession metadata fails closed, fiscal frame participates in fact identity, and issuer candidates preserve ticker/exchange ambiguity. License status defaults to `review_required`, so the common evidence snapshot fails closed until terms review is explicitly completed. The adapter has nine focused tests in addition to the 12 evidence-contract tests, for 21 total.

The adapter consumes already-fetched JSON only. A compliant SEC HTTP fetcher, network access, persistence, live LLM workers and broker actions remain unimplemented.
