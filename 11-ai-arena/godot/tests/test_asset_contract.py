import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
FACTIONS = ("value", "growth", "trend", "quant", "sentiment", "macro")

class AssetContractTests(unittest.TestCase):
    def test_reference_sprite_atlases_are_valid_webp(self):
        for name in ("agents-sprite.webp", "rooms-sprite.webp"):
            path = ROOT / "assets" / name
            self.assertTrue(path.is_file(), f"missing {path}")
            payload = path.read_bytes()
            self.assertGreater(len(payload), 1024, f"{name} is unexpectedly small")
            self.assertEqual(payload[:4], b"RIFF")
            self.assertEqual(payload[8:12], b"WEBP")

    def test_catalog_has_six_stable_faction_ids_and_atlas_coordinates(self):
        source = (ROOT / "scripts" / "agent_catalog.gd").read_text(encoding="utf-8")
        ids = re.findall(r'"id":\s*"([a-z]+)"', source)
        self.assertEqual(tuple(ids), FACTIONS)
        for key in ("sprite_x", "sprite_y", "room_x", "room_y"):
            self.assertGreaterEqual(source.count('"' + key + '"'), 6)

    def test_blender_source_is_kept_out_of_godot_import_scan(self):
        self.assertTrue((ROOT / "assets" / "source" / ".gdignore").is_file())

    def test_blender_builder_and_asset_verifier_are_valid_python(self):
        for relative in ("blender/build_ai_arena_assets.py", "tools/verify_generated_assets.py"):
            path = ROOT / relative
            self.assertTrue(path.is_file(), f"missing {path}")
            compile(path.read_text(encoding="utf-8"), str(path), "exec")

if __name__ == "__main__":
    unittest.main()
