# Browser verification — 2026-11-03

**Result: PASS** (interactive UI and layout only).

- Isolated `.venv` created using Python 3.13, Playwright loaded from preinstalled environment via `PYTHONPATH` in this sandbox.
- Tested the *full editable source HTML* and the previous packaging experiment; the GitHub deliverable is the simpler, source-readable HTML.
- Chromium 1440 × 1000 desktop plus responsive widths 1024, 768, 390, and 320 px: no horizontal overflow, console errors or uncaught page exceptions.
- Prompt → title live update, Rules dialog open/close, four Agent pods, zero initial P&L: pass.
- First round: CSS cash notes created; gain pods and loss pods both observed: pass.
- Scrub back to round 0 restores initial balance without compounding a prior run: pass.
- Start → LIVE, pause → PAUSED, resume → LIVE, fast-forward → SETTLED: pass.
- Risk-adjusted standings and champion display: pass.
- **Regression caught and fixed**: score was displayed as `+1059.57%` because cumulativeReturnPct was multiplied twice; corrected to `+10.60%` and added an assertion against the erroneous value.
- No brokerage, real market data, AI model, exchange engine or realistic life/marketing prediction tested.

To reproduce locally with Playwright installed:

```bash
python tests/test_ui.py
```

The visual reference screenshots generated locally during testing are not prerequisites for running the site. The interface was reviewed at 1440px and 390px. A separate user validation session is required before deciding whether to replace V0.1.