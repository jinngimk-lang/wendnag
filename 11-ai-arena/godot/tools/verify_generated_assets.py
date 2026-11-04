#!/usr/bin/env python3
"""Verify Blender-generated source and GLB assets for the Godot project."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FACTIONS = ("value", "growth", "trend", "quant", "sentiment", "macro")

def check(path: Path, magic: bytes, minimum: int = 1024) -> None:
    if not path.is_file():
        raise SystemExit(f"Missing generated asset: {path.relative_to(ROOT)}")
    payload = path.read_bytes()
    if len(payload) < minimum:
        raise SystemExit(f"Generated asset is too small: {path.relative_to(ROOT)} ({len(payload)} bytes)")
    if not payload.startswith(magic):
        raise SystemExit(f"Unexpected file signature: {path.relative_to(ROOT)}")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-generated", action="store_true")
    args = parser.parse_args()
    source = ROOT / "assets" / "source" / "ai_arena_assets.blend"
    generated = ROOT / "assets" / "generated"
    if not args.require_generated and not source.exists():
        print("Blender assets not generated yet; procedural fallbacks remain available.")
        return
    check(source, b"BLENDER", 4096)
    for faction in FACTIONS:
        check(generated / "agents" / f"{faction}.glb", b"glTF", 2048)
        check(generated / "rooms" / f"{faction}.glb", b"glTF", 2048)
    check(generated / "banknote.glb", b"glTF", 1024)
    manifest_path = generated / "manifest.json"
    if not manifest_path.is_file():
        raise SystemExit("Missing generated/manifest.json")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if len(manifest.get("agents", [])) != 6 or len(manifest.get("rooms", [])) != 6:
        raise SystemExit("Generated manifest must enumerate six Agents and six rooms")
    print("BLENDER ASSET CONTRACT: PASS (6 Agent GLBs, 6 room GLBs, banknote GLB, editable .blend)")

if __name__ == "__main__":
    main()
