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
