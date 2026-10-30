# AI Arena — Interactive HTML Prototype

A responsive three-arena product demo. Open `index.html` through a local HTTP server; the bootstrap page inflates the HTML shell, which then loads compressed CSS and JavaScript using the native `DecompressionStream` API.

## Run locally

```bash
cd 11-ai-arena/prototype
python3 -m http.server 4173
```

Open `http://127.0.0.1:4173` in a modern browser with `DecompressionStream` support.

## Editable source

The GitHub text-file workflow stores `shell.html`, `styles.css` and `app.js` as gzip-compressed Base64 text assets. Restore readable source files with:

```bash
python3 unpack.py
```

After editing a source file, regenerate its matching `.gz.b64` asset with deterministic gzip + Base64 encoding:

```python
from pathlib import Path
import base64, gzip
for name in ("shell.html", "styles.css", "app.js"):
    raw = Path(name).read_bytes()
    Path(name + ".gz.b64").write_text(base64.b64encode(gzip.compress(raw, compresslevel=9, mtime=0)).decode("ascii"))
```

## Included flows

- Switch Finance, Marketing and Life arenas.
- Enter a custom subject and start a six-step simulated match.
- Pause, resume, fast-forward and reset.
- Watch the event stream, standings and Agent statuses update.
- Inspect each Agent's objective, evidence and risk.
- Review match rules and the post-match report.

## Data and safety boundary

All values are seeded demonstration data. The prototype does not fetch live filings, market prices, social-platform metrics or personal information. It does not place trades, spend ad budget, publish content or make deterministic predictions about a person's future. Event summaries are public-facing outputs, not private chain-of-thought.

## Files

- `index.html` — small bootstrap loader.
- `shell.html.gz.b64` — compressed page structure and dialogs.
- `styles.css.gz.b64` — compressed CSS source.
- `app.js.gz.b64` — compressed JavaScript source.
- `unpack.py` — restore readable source files.
- `assets/arena-mark.svg` — original favicon.
- `tests/smoke_test.py` — Playwright browser smoke suite.
- `TEST_REPORT.md` — verification results and limits.
