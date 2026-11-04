# AI Investment Arena — Six Factions / Six Independent Portfolios V0.5.0

AI Investment Arena is a local, responsive investment-research workstation built around six distinct investment schools. Each faction has its own Agent persona, research room, challenge roles, paper-trading decisions and independently accounted portfolio.

## Product model

**One shared market path. Six independent research teams. Six independent capital accounts.**

- **Value / 价值派** — quality, intrinsic value, cash-flow durability and margin of safety.
- **Growth / 成长派** — growth quality, market opportunity, margin expansion and estimate revisions.
- **Trend / 趋势派** — price structure, relative strength, momentum and trend invalidation.
- **Quant / 量化派** — factor signals, signal stability, volatility targeting and portfolio constraints.
- **Sentiment / 情绪派** — attention, news sentiment, crowding and reflexivity.
- **Macro / 宏观派** — rates, liquidity, credit, regime shifts and risk appetite.

Each Agent has a lead analyst, an independent challenger and a risk-control role. Every account owns its own cash, shares, equity path, actual/target exposure, fills, fees, slippage and audit log. There is no shared vault and no transfer between Agent accounts.

## V0.5.0 interface

The redesigned experience is organized as:

1. Experiment setup and common market environment.
2. Six faction cards with dedicated research-room scenes and distinct human portraits.
3. Selected-Agent workspace with research thesis, signals, challenge roles, account metrics and trade-decision record.
4. Shared market factors and event timeline.
5. Six-account equity comparison, risk ranking and isolated audit ledger.
6. Replay, pause/resume, step-forward, settle, reset and full JSON export.

The interface is responsive across desktop, laptop, tablet and compact mobile widths. The portrait and room WebP sprite atlases are stored in assets/agents-sprite.webp and assets/rooms-sprite.webp; each card crops only its mapped Agent/room cell, so the sprite sheet itself is never presented as a contact sheet.

## Run locally

No CDN, npm build or remote font is required.

~~~bash
cd 11-ai-arena/experience-v3
python -m http.server 8000
# open http://127.0.0.1:8000
~~~

## Browser QA in an isolated virtual environment

~~~bash
python -m venv .venv
.venv/bin/python -m pip install -r requirements-test.txt
.venv/bin/python -m playwright install chromium
.venv/bin/python tests/test_ui.py
.venv/bin/python tests/visual_qa.py
~~~

The GitHub Actions workflow runs backend contract tests and the full Playwright suite inside an isolated Python virtual environment. It checks the six portrait/room mappings, Agent selection, research roles, decision panels, account isolation, full 252-day simulation, deterministic reruns, export schema, browser errors and horizontal overflow at 1440 / 1024 / 768 / 390 / 320px.

## Truth boundary

**V0.5.0 remains a synthetic local prototype.** Company input is a scenario label and deterministic seed. Research scores, market prices, factors, events, fills and returns are generated locally; no real issuer evidence, live market data, historical backtest, external LLM worker, broker or live trade is connected. Simulated performance is not a forecast, investment advice or a representation of actual trading results.

## Next real-data gates

See REAL_DATA_BLUEPRINT.md for entity resolution, licensed point-in-time evidence, source citations, independent Agent workers, reproducible paper simulation and append-only audit requirements. Do not replace synthetic values with live-looking numbers unless provenance, timestamps, licensing and replayability are implemented.


## V0.5.0 verification

GitHub Actions run #41797576138 passed both isolated-venv jobs: 30 backend contract tests, Playwright functional regression, 252-day / 1,512-operation stress, six portrait and six room asset checks, and visual QA at 1440 / 1024 / 768 / 390 / 320px with zero horizontal overflow and zero browser errors. Screenshot artifact ID: 13305748269.
