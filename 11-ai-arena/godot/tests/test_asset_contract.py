import pathlib
import re
import subprocess
import sys
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

    def test_blender_builder_disables_backup_files_and_source_has_no_backups(self):
        builder = (ROOT / "blender" / "build_ai_arena_assets.py").read_text(encoding="utf-8")
        self.assertIn("bpy.context.preferences.filepaths.save_version = 0", builder)
        source_dir = ROOT / "assets" / "source"
        backups = list(source_dir.glob("*.blend[0-9]")) + list(source_dir.glob("*.blend[0-9][0-9]"))
        self.assertEqual(backups, [], "Blender backup files must not be committed or packaged")

    def test_asset_verifier_rejects_blender_backup_files(self):
        backup = ROOT / "assets" / "source" / "ai_arena_assets.blend1"
        self.assertFalse(backup.exists(), "test fixture must start without a Blender backup")
        backup.write_bytes(b"test backup")
        try:
            verifier = ROOT / "tools" / "verify_generated_assets.py"
            result = subprocess.run([sys.executable, str(verifier), "--require-generated"], capture_output=True, text=True, check=False)
            self.assertNotEqual(result.returncode, 0, "asset verification must reject Blender backup files")
            self.assertIn("backup", (result.stdout + result.stderr).lower())
        finally:
            backup.unlink(missing_ok=True)

    def test_blender_builder_and_asset_verifier_are_valid_python(self):
        for relative in ("blender/build_ai_arena_assets.py", "tools/verify_generated_assets.py"):
            path = ROOT / relative
            self.assertTrue(path.is_file(), f"missing {path}")
            compile(path.read_text(encoding="utf-8"), str(path), "exec")

if __name__ == "__main__":
    unittest.main()
