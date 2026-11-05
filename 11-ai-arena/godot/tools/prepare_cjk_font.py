#!/usr/bin/env python3
"""Build a compact, project-specific Noto Sans SC font subset for Godot."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_FONT = Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc")
LICENSE_SOURCE = Path("/usr/share/doc/fonts-noto-cjk/copyright")
FONT_DIR = ROOT / "assets" / "fonts"
OUTPUT_FONT = FONT_DIR / "NotoSansSC-Subset.otf"
OUTPUT_LICENSE = FONT_DIR / "OFL.txt"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-font", type=Path, default=SOURCE_FONT, help="Noto Sans CJK TTC/OTF source font")
    parser.add_argument("--license-source", type=Path, default=LICENSE_SOURCE, help="Noto CJK OFL/copyright notice")
    parser.add_argument("--font-number", type=int, default=2, help="TTC face index; pass -1 for a standalone OTF")
    args = parser.parse_args()
    if not args.source_font.is_file():
        raise SystemExit(
            "Noto CJK font source is missing. Install fonts-noto-cjk first or pass --source-font: "
            "sudo apt-get install fonts-noto-cjk python3-fonttools"
        )
    FONT_DIR.mkdir(parents=True, exist_ok=True)
    characters = {chr(codepoint) for codepoint in range(32, 127)}
    suffixes = {".gd", ".tscn", ".tres", ".godot", ".md", ".cfg", ".json"}
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in suffixes:
            continue
        if ".godot" in path.parts or ".venv" in path.parts:
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        characters.update(char for char in content if ord(char) >= 32 and char != "\ufeff")

    text_file = FONT_DIR / "font-subset-chars.txt"
    text_file.write_text("".join(sorted(characters)), encoding="utf-8")
    command = [
        sys.executable,
        "-m",
        "fontTools.subset",
        str(args.source_font),
        f"--text-file={text_file}",
        f"--output-file={OUTPUT_FONT}",
        "--unicodes=U+0000-00FF,U+2000-206F,U+3000-30FF,U+3400-4DBF,U+4E00-9FFF,U+F900-FAFF,U+FF00-FFEF",
        "--layout-features=*",
        "--name-IDs=*",
        "--name-languages=*",
        "--glyph-names",
        "--symbol-cmap",
        "--legacy-cmap",
        "--notdef-glyph",
        "--notdef-outline",
        "--recommended-glyphs",
    ]
    if args.font_number >= 0:
        command.insert(3, f"--font-number={args.font_number}")  # SC face in the Noto CJK TTC.
    subprocess.run(command, check=True)
    if args.license_source.is_file():
        OUTPUT_LICENSE.write_text(args.license_source.read_text(encoding="utf-8"), encoding="utf-8")
    text_file.unlink(missing_ok=True)
    print(f"CJK FONT READY: {OUTPUT_FONT.relative_to(ROOT)} ({OUTPUT_FONT.stat().st_size:,} bytes, {len(characters):,} source characters)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
