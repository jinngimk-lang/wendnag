# AI Arena Context Checkpoint

Updated: 2026-10-30

## One-sentence goal

Build a premium multi-agent competition platform where a user enters a company, product or life choice and watches distinct AI Agents compete inside a transparent, replayable simulation.

## Three verticals

- Finance: competing research strategies + historical/paper execution + risk-aware scoring.
- Marketing: creative strategies + audience/network simulation + calibrated scenario metrics.
- Life: parallel long-horizon scenarios + editable assumptions + sensitivity analysis.

## Shared engine

Prompt/config → roster → orchestrated rounds → domain simulator → append-only events → scoring → live view → replay/branch.

## Current delivery

- Work branch: `feat/ai-arena-concept-research`.
- Draft PR: https://github.com/jinngimk-lang/wendnag/pull/26.
- Interactive HTML prototype: `prototype/` (`index.html` bootstraps the compressed shell/CSS/JS; run `python3 unpack.py` to restore readable source).
- Implementation and limits: `IMPLEMENTATION.md`.
- Verification: `prototype/TEST_REPORT.md`.
- Visual direction: premium broadcast control room; Finance amber, Marketing cyan, Life violet.

## Current behavior

- Three modes and six distinct Agent profiles per mode.
- Subject prompt and example chips.
- Six-step deterministic demo event stream.
- Live standings, domain visualization, pause/resume, fast-forward, reset, report and agent detail.
- Responsive checks at 1024 / 768 / 390px.
- All demo metrics are seeded and labelled; no real API or real-world action is connected.

## Current decisions and safety boundary

- No live brokerage execution, real ad spend, auto-publishing or personal data collection.
- Finance must use point-in-time data, common initial resources and explicit costs.
- Marketing reach must be calibrated before it is described as a forecast.
- Life outcomes must remain scenario ranges and trade-offs, not deterministic prophecies.
- Render public event summaries, not hidden chain-of-thought.
- Connected Figma plan is View seat; HTML/CSS is current editable design artifact.

## Research snapshots

See `RESEARCH.md` section F for pinned upstream commit SHAs and observed root licenses: TradingAgents, OASIS, Generative Agents, LangGraph, AutoGen, Concordia and AgentSociety.

## Next concrete action

Implement Finance Arena's deterministic historical/paper-trading backend slice and event ledger. Keep the current front-end view-model contract; replace seeded events only after simulator and scoring fixtures are reproducible.

## Recovery order

1. Root `AGENTS.md`.
2. `11-ai-arena/PROJECT.md`.
3. `11-ai-arena/STATUS.md` and this file.
4. `11-ai-arena/IMPLEMENTATION.md`.
5. `11-ai-arena/ARCHITECTURE.md`, `DESIGN.md`, `RESEARCH.md`.
6. `11-ai-arena/prototype/README.md` and `prototype/TEST_REPORT.md`.

## 2026-11-03 V0.2 visual branch checkpoint

The new `experience-v2/` is the **Capital Theater** alternative to the earlier broadcast dashboard. The primary action is now watching physical money flows anchored to explicit per-round P&L rather than reading tables first. Four fixed-demo Agents share $100k simulated capital; all six rounds can be replayed deterministically. The simulator and live Agent integrations are still absent. Read `experience-v2/CHECKPOINT.md`, `README.md`, `VISUAL_RESEARCH.md`, `TEST_REPORT.md`, and `index.html` when working on the next visual iteration.

Do **not** assume V0.2 has won over V0.1 without observed user testing. Judge whether money-flow visuals increase correct comprehension of profit, loss, drawdown, and the simulated nature of outcomes. Figma connected account currently lacks a Design seat, so the HTML source is the actual editable master.

## 2026-11-03 V0.3 Finance Research Lab checkpoint

The user's clarification supersedes the narrower V0.2 demo flow: input a company, let independent factions research it, choose the simulation length, then observe evolving market events/sentiment and inspect every operation. V0.3 is implemented at `experience-v3/index.html`.

Six factions (value, growth, trend, quant, sentiment, macro) each show lead/challenger/risk role templates, independent stance/thesis/confidence/risks and cross-examination. User selects 20–252 trading days, equal starting capital and shared risk cap. Six separate rule-based portfolios share one deterministic synthetic market path; macro, sentiment, sector and volatility change daily and influence strategy weights. Every faction emits one BUY/SELL/HOLD decision per day with execution price, quantity, target weight, notional, cash/shares, fees/slippage, reason and event. Replay, filters and JSON export are implemented.

**Not real research yet:** no company filings, live prices/news, external LLM workers or broker. All V0.3 numbers are synthetic and company text only seeds the demo. Read `experience-v3/README.md`, `ARCHITECTURE.md`, `TEST_REPORT.md` and `CHECKPOINT.md`. QA: isolated venv + Playwright passes; 252-day run creates 1,512 decisions; responsive 1440/1024/768/390/320; no console errors.

Next: licensed point-in-time research/data provider → common immutable evidence pack → isolated LLM role workers → deterministic paper simulator and append-only ledger → held-out baseline/leakage tests. Keep V0.1/V0.2 intact for comparison.

## 2026-11-03 backend evidence gateway contract V0.1

- Executable core: `backend/research_gateway.py` (Python standard library only).
- 12 tests pass for exact/ambiguous issuer resolution, CIK normalization, UTC chronology, point-in-time future exclusion, foreign issuer and license rejection, duplicate IDs, deep immutability, snapshot integrity, evidence-linked faction contracts, weight caps and hash-chain tampering.
- GitHub Actions workflow: `.github/workflows/ai-arena-validation.yml` runs backend contract and Finance Lab browser tests.
- Not implemented: real SEC/Alpaca/news/macro adapters, network access, credentials, LLM calls, HTTP API, durable persistence or broker integration.
- Next: implement one reviewed SEC issuer/filing adapter and one licensed market-data adapter; persist snapshots and ledger before connecting faction workers.
