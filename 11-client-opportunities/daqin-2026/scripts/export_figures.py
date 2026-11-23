#!/usr/bin/env python3
"""Export editable SVG charts to high-resolution PNG, preserving SVG as source."""
from pathlib import Path
try:
    import cairosvg
except ImportError as e:
    raise SystemExit("Install CairoSVG in a Python virtual environment first") from e
p=Path(__file__).resolve().parents[1]/"04-assets"/"figures"
for path in sorted(p.glob("*.svg")):
    target=path.with_suffix(".png")
    cairosvg.svg2png(url=str(path),write_to=str(target),scale=2)
    print(target)
