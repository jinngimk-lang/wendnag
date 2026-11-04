from pathlib import Path
import base64
import gzip

ROOT = Path(__file__).resolve().parent
for filename in ("shell.html", "styles.css", "app.js"):
    packed = base64.b64decode((ROOT / f"{filename}.gz.b64").read_text(encoding="ascii"))
    (ROOT / filename).write_bytes(gzip.decompress(packed))
    print(f"Unpacked {filename}")
