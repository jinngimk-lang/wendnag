# Capital Theater checkpoint — 2026-11-03

## Goal

Give Finance Arena immediate, believable, **data-tied** visual money feedback. Watch profits arrive and losses leave a four-Agent arena. Do not over-optimize the old broadcast control room without testing a fundamentally different product view.

## Current deliverable

- Path: `11-ai-arena/experience-v2/index.html` (single, self-contained, readable HTML source).
- Four simulated strategies and 6 fixed deterministic rounds, $100,000 notional per strategy.
- Cashflow animation: gain from center vault to Agent pod; loss from Agent pod to vault.
- Risk-adjusted rank, drawdown, benchmark fixture, curve, event ledger and manual replay.
- Reduced-motion setting, keyboard actions and optional sound off by default.
- All imagery is original procedural CSS/SVG, not generated photography.
- The marketing/life versions remain in `11-ai-arena/prototype/`.
- QA: `experience-v2/TEST_REPORT.md`.
- Design research and more daring alternatives: `experience-v2/VISUAL_RESEARCH.md`.

## Product truth

No real market prices, company-specific outcome, actual Agent calls, brokerage or transaction. Ticker input updates the title only; the same sample fixture always applies. **Never present this as a validated backtest or earnings promise.**

## Next decision

Run an A/B usability study between V0.1 dashboard and V0.2 capital theater before investing in heavy WebGL/image generation. Once the money-movement semantics pass comprehension, build finance simulator with point-in-time data and append-only event ledger. If users prefer a different experience, retire or rework V0.2; do not add decorative code merely to preserve sunk cost.

## Recovery order

1. Repository root `AGENTS.md` and both mandatory creative skills.
2. `11-ai-arena/PROJECT.md`, `11-ai-arena/STATUS.md` and `11-ai-arena/CHECKPOINT.md`.
3. This checkpoint, `README.md`, `VISUAL_RESEARCH.md`, `TEST_REPORT.md`.
4. `index.html` and `tests/test_ui.py`.
5. Recheck branch and PR before any write. Keep modifications in `11-ai-arena/`.