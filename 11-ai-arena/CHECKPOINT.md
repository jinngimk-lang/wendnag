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
