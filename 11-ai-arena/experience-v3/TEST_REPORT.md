# Browser QA — Finance Research Lab V0.3.2

**Result: PASS** — isolated Python virtual environment + Chromium.

## Environment

- Python 3.13.5.
- Isolated `.venv` created with `python3 -m venv --system-site-packages .venv`.
- Playwright imported from the preinstalled sandbox package path; system Chromium `/usr/bin/chromium`.
- No npm dependencies, external fonts, CDN scripts, API keys or network data required by the UI.

## Coverage

- Research form and user-controlled simulation duration (20–252 trading days).
- Six independent strategy factions; six research reports; 18 visible role templates; three cross-examination columns.
- Each report displays synthetic signals, risk, entry trigger and invalidation conditions.
- Company label, initial capital and shared risk cap.
- Daily paper simulation with a common market path, changing macro/sentiment/sector/volatility factors and synthetic world events.
- BUY / SELL / HOLD for every faction on every simulated day (6 × N decisions).
- Every decision stores its own market return, macro, sentiment, sector, volatility, regime and event context.
- Execution price, market price, quantity, target weight, notional, commission, slippage, cash and share balances.
- Buy-and-hold benchmark applies the entry fee to the actual invested cash before calculating shares.
- Data-linked bill animation tested in both directions: positive equity delta flows vault → Agent; negative delta flows Agent → vault; no rounded zero-dollar chips; animation nodes clean up after completion.
- Aggregate P&L display switches to red on a negative combined result and green on a positive result.
- One-day / five-day advance, auto-play, pause, reset, settlement and timeline scrub.
- Event count, event feed, factor panels and ledger respect the replay cursor; no future event count or future chart points leak into earlier states.
- Agent/action/period filters and complete JSON export with run ID, versions, synthetic evidence declaration and benchmark assumptions.
- Risk cap enforced for all generated target weights.
- Deterministic rerun with identical inputs.
- 252-day stress run: 1,512 decision records.
- Viewport widths 1440, 1024, 768, 390 and 320 px: no horizontal overflow.
- No JavaScript page errors or console errors.

## Exact sandbox test command

```bash
PYTHONPATH=/opt/pyvenv/lib/python3.13/site-packages .venv/bin/python tests/test_ui.py
```

Output:

```text
PASS: 6-faction research, triggers/invalidation, 18 role templates, configurable duration, shared market path, per-decision factor snapshots, bidirectional data-linked cash flow, visible event replay, benchmark fee accounting, 6x daily ledger, filters, export, deterministic rerun, responsive and no browser errors
```

## Limitations

This validates front-end interaction and deterministic local simulation only. It does not validate company-specific research, licensed market data, actual LLM agents, historical backtest quality, exchange execution, legal suitability or investment performance. All current facts, signals, events, prices, fills and returns are synthetic.