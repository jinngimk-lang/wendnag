#!/usr/bin/env python3
"""Normalize a Word-native editable BP DOCX for Microsoft Word compatibility.

This is the final compatibility gate for DOCX files containing Word 2010
DrawingML groups (wpg/wps). The source file is opened and re-saved through
LibreOffice's MS Word 2007 XML writer, which adds the AlternateContent/VML
fallback structures that desktop Microsoft Word expects more reliably.

The script then verifies the BP-specific invariants:
- exactly 8 editable Word drawing groups;
- at least 276 native Word shapes;
- exactly 8 VML fallback groups;
- exactly 8 remaining inline product screenshots;
- no legacy InkClaw text.

Usage:
    python tools/normalize_word_native_docx.py input.docx output.docx
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from zipfile import ZipFile

from docx import Document
from lxml import etree

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "wpg": "http://schemas.microsoft.com/office/word/2010/wordprocessingGroup",
    "wps": "http://schemas.microsoft.com/office/word/2010/wordprocessingShape",
    "mc": "http://schemas.openxmlformats.org/markup-compatibility/2006",
    "v": "urn:schemas-microsoft-com:vml",
}


def normalize(src: Path, dst: Path) -> None:
    if not src.exists():
        raise FileNotFoundError(src)
    if shutil.which("soffice") is None:
        raise RuntimeError("LibreOffice/soffice is required for MS Word normalization")

    dst.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="bp-word-normalize-") as td:
        td_path = Path(td)
        profile = td_path / "lo-profile"
        out_dir = td_path / "out"
        out_dir.mkdir()
        cmd = [
            "soffice",
            f"-env:UserInstallation=file://{profile}",
            "--headless",
            "--convert-to",
            "docx",
            "--outdir",
            str(out_dir),
            str(src),
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        if proc.returncode != 0:
            raise RuntimeError(f"LibreOffice normalization failed: {proc.stderr or proc.stdout}")
        generated = out_dir / src.name
        if not generated.exists():
            raise RuntimeError(f"LibreOffice did not generate expected DOCX: {generated}")
        shutil.copy2(generated, dst)


def verify(path: Path) -> dict[str, int]:
    # Package/reader check.
    doc = Document(str(path))
    inline_shapes = len(doc.inline_shapes)

    with ZipFile(path, "r") as zf:
        bad = zf.testzip()
        if bad:
            raise RuntimeError(f"Corrupt ZIP member: {bad}")
        root = etree.fromstring(zf.read("word/document.xml"))

    groups = len(root.xpath("//wpg:wgp", namespaces=NS))
    shapes = len(root.xpath("//wps:wsp", namespaces=NS))
    fallbacks = len(root.xpath("//mc:Fallback", namespaces=NS))
    vml_groups = len(root.xpath("//v:group", namespaces=NS))
    tables = len(root.xpath("//w:tbl", namespaces=NS))
    text = "".join(root.xpath("//w:t/text()", namespaces=NS))

    if groups != 8:
        raise RuntimeError(f"Expected 8 native drawing groups, found {groups}")
    if shapes < 276:
        raise RuntimeError(f"Expected at least 276 native shapes, found {shapes}")
    if fallbacks != 8 or vml_groups != 8:
        raise RuntimeError(
            f"Expected 8 compatibility fallbacks/VML groups, found {fallbacks}/{vml_groups}"
        )
    if inline_shapes != 8:
        raise RuntimeError(f"Expected 8 product screenshots, found {inline_shapes}")
    if "InkClaw" in text:
        raise RuntimeError("Legacy InkClaw name remains in document text")

    return {
        "groups": groups,
        "native_shapes": shapes,
        "fallbacks": fallbacks,
        "vml_groups": vml_groups,
        "product_screenshots": inline_shapes,
        "tables": tables,
    }


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("Usage: normalize_word_native_docx.py INPUT.docx OUTPUT.docx")
    src = Path(sys.argv[1]).resolve()
    dst = Path(sys.argv[2]).resolve()
    normalize(src, dst)
    result = verify(dst)
    print(dst)
    print(result)


if __name__ == "__main__":
    main()
