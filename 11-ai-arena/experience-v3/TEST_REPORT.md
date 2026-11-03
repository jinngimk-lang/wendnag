# Browser QA — Finance Research Lab V0.3

**Result: PASS** — isolated Python virtual environment + Chromium.

## Environment

- Python 3.13.5.
- Isolated `.venv` created with `python3 -m venv --system-site-packages .venv`.
- Playwright imported from the preinstalled sandbox package path; system Chromium `/usr/bin/chromium`.
- No npm dependencies, external fonts, CDN scripts, API keys or network data required by the UI.

## Coverage

- Research form and user-controlled simulation duration (20–252 trading days).
- Six independent strategy factions; six research reports; 18 visible role templates; three cross-examination columns.
- Company label, initial capital and shared risk cap.
- Daily paper simulation with a common market path, changing macro/sentiment/sector/volatility factors, synthetic world events and deterministic seeded replay.
- BUY / SELL / HOLD for every faction on every simulated day (6 × N decisions).
- Execution price, market price, quantity, target weight, notional, commission, slippage, cash and share balances.
- One-day / five-day advance, auto-play, pause, reset, settlement and timeline scrub.
- Event feed and factor panels update with replay time.
- Chart does not reveal future points while the replay cursor is earlier than settlement.
- Agent/action/period filters and complete JSON export.
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
PASS: 6-faction research, 18 role templates, configurable duration, shared market path, dynamic factors, 6x daily ledger, replay, filters, export, deterministic rerun, responsive and no browser errors
```

## Limitations

This validates the front-end interaction and deterministic local simulation only. It does not validate company-specific research, market data, an LLM Agent runtime, historical backtest quality, exchange execution, legal suitability or investment performance. All current facts, signals, events, prices, fills and returns are synthetic.