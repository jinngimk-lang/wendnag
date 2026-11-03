# STATUS — 2026-11-03

## Current phase

**Phase 2 — two competing UI directions tested.** V0.1 three-arena control-room prototype remains available; new V0.2 `experience-v2/index.html` is an independent, finance-first Capital Theater with data-tied physical money flow. Both are front-end demonstrations, not production multi-agent simulators.

## Repository state

- Parent repository: `jinngimk-lang/wendnag`
- Work branch: `feat/ai-arena-concept-research`
- Existing draft PR: [#26](https://github.com/jinngimk-lang/wendnag/pull/26)
- Dedicated folder: `11-ai-arena/`
- BP source and investor-deck workstreams remain untouched.

## New delivery — Capital Theater V0.2 (2026-11-03)

- `experience-v2/index.html` is a standalone, fully editable HTML/CSS/JS experience, not a compressed source package.
- Four agents, common $100k simulated capital, six deterministic rounds; paper-bill gain/loss animation is linked to signed P&L deltas.
- Central aggregate P&L vault, four agent pods, risk-adjusted scoreboard, relative-value chart, six-round replay, event ledger and rule disclosure.
- Start / pause / resume / advance / settle / reset / scrub controls; optional sound off by default; reduced-motion support.
- Browser smoke QA passed for desktop and 1024/768/390/320px viewports, including a caught-and-fixed percentage-formatting error.
- `experience-v2/README.md`, `VISUAL_RESEARCH.md`, `TEST_REPORT.md`, `CHECKPOINT.md` record the visual pivot, open-source research, boundaries and context recovery.
- Figma remains View-seat-only; no editable native Figma design or paid image generation claimed.
- No unvalidated market data, live trading or actual agent service. Entered company name only changes the demonstration label.
- V0.1 is retained to enable usability A/B tests; it is not overwritten.

## Delivered

- `prototype/index.html` — complete responsive application shell and dialogs.
- `prototype/styles.css.gz.b64` — compressed, unpackable premium broadcast-control-room CSS; three domain accents, desktop/tablet/mobile layouts and reduced-motion support.
- `prototype/app.js.gz.b64` — compressed, unpackable JavaScript for three domain adapters, seeded six-step event loop, live ranking, pause/resume, fast-forward, reset, report and Agent detail.
- `prototype/shell.html.gz.b64` — compressed HTML shell loaded by the bootstrap `index.html`.
- `prototype/assets/arena-mark.svg` — original favicon.
- `prototype/tests/smoke_test.py` — Playwright smoke suite.
- `prototype/TEST_REPORT.md` — test coverage and limitations.
- `IMPLEMENTATION.md` — architecture and implementation boundary.
- `RESEARCH.md` — upstream commit and root-license spot-check for seven relevant projects.

## Verification

- Browser smoke test: PASS.
- Finance: custom subject, shared rules, start, pause, resume, fast-forward, result, report and agent detail: PASS.
- Marketing: audience network, four channel cards, six Agent roster and result: PASS.
- Life: three branching paths, six Agent roster and non-deterministic result wording: PASS.
- Responsive viewports 1024px / 768px / 390px: no horizontal overflow.
- No JavaScript page errors or console errors.
- Local Python HTTP server returned HTTP 200.
- Visual review screenshots generated locally under `prototype/screenshots/` during the test run.

## Product decisions preserved

- One shared Arena Engine with three domain adapters.
- Finance MVP remains historical/paper simulation only; no live trades.
- Marketing reach/engagement remain simulated until calibrated against real campaign data.
- Life outputs remain editable branching scenarios, not deterministic predictions.
- The UI shows concise public event summaries, never private hidden chain-of-thought.
- All prototype values are seeded demonstration data and visibly labelled as such.

## Figma status

The connected Figma account reports a View seat. No editable Figma file was created. The HTML/CSS/JS prototype is the current editable visual artifact; Figma handoff can follow when edit access or a suitable target file is available.

## Remaining gaps

- No backend, real LLM Agent runtime, event persistence or SSE/WebSocket stream.
- No licensed point-in-time market-data source or validated backtest engine.
- No actual social-platform ranking model or calibration dataset.
- No validated causal life model or privacy review.
- No production authentication, observability, cost controls or abuse protections.

## Next actions

1. Build the Finance vertical slice: point-in-time data snapshot, deterministic paper execution, costs/slippage, risk-aware scoring and replay.
2. Define a typed Agent action schema and append-only event ledger; keep LLM proposals separate from authoritative simulator state.
3. Benchmark against buy-and-hold and simple factor baselines before showing strategy comparisons as meaningful.
4. Run 5–8 target-user tests on the spectator-versus-steering interaction.
5. Only then calibrate the Marketing audience simulator and expand Life scenarios.

## Context recovery

Before continuing, read root `AGENTS.md`, then `PROJECT.md`, `STATUS.md`, `CHECKPOINT.md`, `IMPLEMENTATION.md`, `DESIGN.md`, `ARCHITECTURE.md` and `prototype/README.md`. Chat memory is not the source of truth.
