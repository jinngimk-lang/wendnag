# STATUS — 2026-11-05

## Current phase

**Phase 3 — Native Godot 4.7.1 3D Finance Arena client**, delivered additively alongside the existing HTML Finance Arena V0.5.0 and earlier research prototypes. The native client has six independent synthetic paper accounts, six Agent stations and research rooms, a shared synthetic market, replay and JSON export. It remains paper-mode only.

## Repository state

- Parent repository: `jinngimk-lang/wendnag`
- Native Godot feature branch: `feat/ai-arena-godot-3d-experience-v01`
- Current review branch: `fix/ai-arena-godot-hud-runtime-errors-20261105`
- Native-client draft PR: [#28](https://github.com/jinngimk-lang/wendnag/pull/28), targeting `feat/ai-arena-independent-agent-workspace-v04`
- Existing HTML V0.5.0 draft PR: [#26](https://github.com/jinngimk-lang/wendnag/pull/26), still open and unmerged; its head branch and contents were not changed by the Godot work.
- Dedicated folder: `11-ai-arena/`
- BP source and investor-deck workstreams remain untouched.

## Latest delivery — Native Godot 3D verification (2026-11-05)

- Forced Blender 4.0.2 rebuild run [#41950047674](https://github.com/jinngimk-lang/wendnag/actions/runs/41950047674) passed asset generation, Godot import/contracts, asset verification, packaging and upload. The run tested `392e616d`, then committed the generated Blender source and GLBs as `a4387d34`.
- Follow-up HUD fix and runtime-error guard passed PR Actions run [#41952957967](https://github.com/jinngimk-lang/wendnag/actions/runs/41952957967) at commit `1b6f7f98`: 14/14 Python tests, Godot import, simulation, 3D world, responsive UI, main-scene smoke test, generated-asset verification and package upload. No `SCRIPT ERROR:` or `Parse Error:` was logged.
- Latest package artifact: [13382140939](https://github.com/jinngimk-lang/wendnag/actions/runs/41952957967). Download inspection confirmed six Agent GLBs, six room GLBs, six room atlases, banknote GLB and the editable 11.23 MB Blender source; no local caches, Python bytecode, virtual environments or Blender backup files were present.
- The Godot UI's icon sizing now uses the Button theme constant. UI contracts assert desktop/mobile sizing, and the shared CI runner fails if Godot logs script or parse errors.
- All finance data, events, prices and fills remain synthetic. No broker, live feed, external LLM workers or real orders are connected.
- Remaining work: user-configurable run setup, seventh-investor follow/challenge interactions and local Godot editor visual QA.


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

## New delivery — Finance Research Lab V0.3 (2026-11-03)

- User flow: company label → six independent faction research reports → cross-examination → configurable 20–252 trading days → paper simulation → daily decision ledger → replay / JSON export.
- Six factions: value & quality, growth, technical/momentum, quant, sentiment, macro/regime.
- Each faction exposes lead analyst, bear-case challenger and risk officer role templates.
- User controls equal starting capital ($50k/$100k/$250k/$500k) and shared risk cap.
- Each faction independently targets exposure while all share one deterministic synthetic market path, starting capital, fee/slippage model and market events.
- Macro liquidity, sentiment temperature, sector momentum and volatility evolve daily and influence both market returns and strategy weights.
- Daily BUY / SELL / HOLD log for every faction, including market/fill price, quantity, target exposure, notional, cash, shares, commission, slippage, reason, event and sentiment.
- Day-by-day replay, auto-play, pause, next-day / five-day advance, settlement, scrub, dynamic ranking, benchmark fixture and JSON export.
- Files: `experience-v3/index.html`, `README.md`, `ARCHITECTURE.md`, `REAL_DATA_BLUEPRINT.md`, `TEST_REPORT.md`, `CHECKPOINT.md`, `requirements-test.txt`, `tests/test_ui.py`.
- Isolated Python venv + Playwright / Chromium QA passed at 1440/1024/768/390/320px; 252-day stress run generated 1,512 daily decisions; no console/page errors or horizontal overflow.
- **Truth boundary:** all V0.3 research signals, prices, events, sentiment, fills and returns are synthetic. The six strategy agents are local deterministic rules, and the 18 role cards are templates—not live LLM calls. No company data, licensed feed, broker or real trade is connected.

## New delivery — Finance Research Lab V0.3.1 (2026-11-03)

- Six faction reports now expose faction-specific entry triggers and thesis-invalidation conditions; cross-examination compares the actual most-positive and most-cautious synthetic signals.
- Every daily operation carries market return, macro, sentiment, sector, volatility, regime and event metadata; the UI exposes this context beside the decision reason.
- Event count and feed are replay-aware, preventing future event-count leakage.
- Corrected buy-and-hold entry-fee accounting by buying shares with post-fee cash.
- Export schema v0.3.1 includes run ID, strategy/simulator versions, explicit synthetic evidence-pack declaration, benchmark assumptions and full operation context.
- Added experience-v3/REAL_DATA_BLUEPRINT.md for issuer resolution, licensed point-in-time evidence, typed faction workers, event-triggered policy updates, deterministic simulation and append-only ledger.
- Added GitHub research on TradingAgents (Apache-2.0), FinRobot (Apache-2.0), Qlib (MIT), NautilusTrader (LGPL-3.0) and Backtrader (GPL-3.0); no code copied or vendored.
- Browser QA rerun: PASS at 1440/1024/768/390/320px; 252-day stress run = 1,512 decisions; no page/console errors or horizontal overflow.

## New delivery — Finance Research Lab V0.3.2 (2026-11-03)

- Single-day forward playback now animates original paper-bill notes between the central performance vault and each faction pod, with direction determined by that faction's signed daily equity delta.
- Amount labels and bill count derive from the same net-value change; profit flows vault → faction, loss flows faction → vault. This is a visual metaphor, not a real inter-faction cash transfer.
- Aggregate P&L and return switch green/red with the sign; no rounded $0 animation labels.
- Browser tests cover both directions, exact sign-to-direction mapping, cleanup of animation nodes, responsive layouts and the 252-day / 1,512-decision stress case.
- V0.3.2 export and simulator version IDs updated.

## New delivery — Backend evidence gateway core V0.1 (2026-11-03)

- Added `backend/research_gateway.py` and 12 standard-library unit tests.
- Exact issuer resolution with explicit ambiguous/not-found states; no silent ticker guessing.
- Deeply immutable, source-attributed evidence records with UTC publication, availability and retrieval timestamps, provider/license metadata and SHA-256 hashes.
- Deterministic point-in-time evidence-pack freezing; excludes evidence not available at `as_of`, rejects foreign issuers, unapproved licenses, invalid chronology and conflicting IDs.
- Typed faction research contract validates all evidence references against the same frozen snapshot and enforces the target-weight cap.
- Append-only in-memory ledger uses payload hashes and previous-event hashes; corruption and time reversal are detected.
- Added a no-network SEC EDGAR submissions/companyfacts parser. It anchors facts to accession `acceptanceDateTime`, rejects unmatched accessions/form mismatches and conflicting accession metadata, includes fiscal frame in fact identity, and defaults license status to `review_required`.
- Added GitHub Actions validation for backend contracts and browser regression.
- Thirty standard-library backend tests pass. Added an opt-in read-only SEC client with required contact-email User-Agent, SEC HTTPS host allowlist, 4/sec default pacing, Retry-After handling, bounded retries, response-size cap and short in-memory cache. HTTP tests use a fake transport; no live SEC request or external data fetch was performed. No market-data provider, external LLM, database persistence or broker integration is connected.

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

- No production API service, real LLM Agent runtime, durable event persistence or SSE/WebSocket stream; only a standard-library contract core exists.
- No licensed point-in-time market-data source or validated backtest engine.
- No actual social-platform ranking model or calibration dataset.
- No validated causal life model or privacy review.
- No production authentication, observability, cost controls or abuse protections.

## Next actions

1. Configure an explicitly monitored `SEC_USER_AGENT` and perform a controlled read-only SEC smoke test; verify live response shape, access policy and rate behavior before enabling ingestion. Keep license status blocked until terms review.
2. Add a licensed market-data adapter with explicit feed, bar availability time, stale/outlier and spread-quality checks.
3. Persist frozen evidence snapshots and the append-only ledger; add replay-by-event-sequence and state hashes.
4. Connect structured faction workers to the shared evidence pack, with evidence/counter-evidence references and event-triggered refreshes.
5. Validate the deterministic paper simulator against buy-and-hold / index / factor baselines and held-out periods before presenting performance comparisons.
6. Keep live brokerage execution out of MVP; continue user tests on spectator-versus-steering interaction.

## Context recovery

Before continuing, read root `AGENTS.md`, then `PROJECT.md`, `STATUS.md`, `CHECKPOINT.md`, `IMPLEMENTATION.md`, `DESIGN.md`, `ARCHITECTURE.md`, `experience-v3/CHECKPOINT.md`, `experience-v3/REAL_DATA_BLUEPRINT.md` and `prototype/README.md`. Chat memory is not the source of truth.


## New delivery — Finance Research Lab V0.3.3 visual redesign (2026-11-03)

- Reworked the complete experience-v3 UI with a MotionSites-calibrated dark finance-console design system while preserving the existing simulator and accounting behavior.
- Added a central P&L vault stage, six faction portfolio pods, more legible research cards, setup controls, market analytics and audit ledger styling.
- Added MOTIONSITES_REDESIGN_SPEC.md and VISUAL_QA_REPORT.md; no remote fonts, CDN, npm dependency or decorative stock imagery.
- Local isolated .venv Playwright regression and 30 backend unit tests passed. Visual snapshots cover 1440 / 1024 / 768 / 390 / 320px with no horizontal overflow or browser errors.
- GitHub Actions now captures and uploads the responsive visual QA screenshot artifact. All financial values and research remain synthetic; no live data or broker integration is claimed.


## CI closure — Finance Research Lab V0.3.3 (2026-11-03)

- GitHub Actions run #98 passed both backend evidence contracts and Finance Lab browser regression after the screenshot framing refinement.
- Visual artifact ID 13201641803 was downloaded and reviewed. Five responsive widths report zero horizontal overflow; six factions, 18 role templates and zero page errors.
- Draft PR #26 remains open and unmerged; no production or live-finance integration is implied.

- Final documentation-closure workflow run #100 also passed; the responsive visual artifact was uploaded successfully.


## 2026-11-04 — AI Investment Arena V0.5.0 faction-first reframe

- Continued the existing independent-Agent workstation branch and kept its simulation/accounting engine unchanged.
- Rebuilt the visible experience around six investment factions, individual Agent portraits, dedicated research-room scenes, three-role adversarial research teams, and per-Agent paper-trade decision panels.
- Added compact WebP portrait/room atlases and mapped each faction to its own visual cell.
- Updated export identifiers and responsive browser-QA assertions. Isolated-venv GitHub Actions run #41797576138 passed: backend contracts 30/30, full browser regression, 252-day / 1,512-operation simulation, portrait/room loading, and 1440 / 1024 / 768 / 390 / 320px visual QA with no horizontal overflow or browser errors. Screenshot artifact 13305748269.


- Draft PR #26 now carries the V0.5.0 faction-first implementation and CI evidence; it remains open and unmerged. Work branch: feat/ai-arena-independent-agent-workspace-v04.


## 2026-11-04 — Native Godot 4.7.1 3D client

- Added an additive native Godot client at `godot/`; the existing HTML V0.5.0 Finance Arena remains unchanged.
- Six independent paper accounts share one synthetic market path and common fee/slippage assumptions.
- Six Agent podiums and six lazily loaded faction research rooms use committed Blender source/GLB assets plus the supplied portrait and room reference atlases.
- The arena center is a shared-market information display, not a central capital vault. Signed-P&L notes remain local to the same Agent account marker; there is no shared cash pool or inter-Agent transfer.
- Godot 4.7.1 CI run #41810429080 passed project import, simulation, 3D world, responsive UI, main-scene smoke, generated-asset integrity and packaging.
- Local isolated Python `.venv` passed 8/8 asset/runtime contract tests and `verify_generated_assets.py --require-generated`.
- CI artifact: `ai-investment-arena-godot`, artifact ID `13311522692` from run #41810429080.
- Current feature branch: `feat/ai-arena-godot-3d-experience-v01`; intended stacked PR base: `feat/ai-arena-independent-agent-workspace-v04`.
- Scope remains synthetic paper mode only. No broker, live market feed, external LLM worker or real order execution is connected. No new paid GPT image-generation call is claimed.
- Follow-on gaps: a run-setup modal (scenario label, trading days, capital and risk cap), seventh-investor follow/challenge interactions, and local visual QA in the Godot editor.


## 2026-11-05 — Godot client verification and artifact hygiene

- Latest Godot 4.7.1 CI run #41949187541 passed at commit `4f2e7e286704ac758b602021b561a25982b557d4`: Python asset contract, project import, simulation, 3D world, responsive UI, main-scene smoke, generated-asset verification, packaging and upload.
- A fresh isolated Python 3.13.5 `.venv` run passed 11/11 unit tests and `verify_generated_assets.py --require-generated`.
- Downloaded artifact #13379977035 was inspected: no `.venv`, `.godot`, `__pycache__`, `.pyc`, `.blend1` or `.blend2` files are packaged.
- Removed the accidentally committed 11.2 MB Blender `.blend1` backup; added project ignore rules, deterministic Blender save-version settings, verifier rejection, CI cleanup and package exclusions.
- The latest CI run skipped the Blender rebuild because the GLBs were already present. A forced rebuild is still required to verify the new save-version suppression in Blender itself.
- Work remains on `feat/ai-arena-godot-3d-experience-v01`, stacked on `feat/ai-arena-independent-agent-workspace-v04`; draft PR creation follows the forced rebuild and whole-branch review.
