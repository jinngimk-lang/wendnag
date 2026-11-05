import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]

class RuntimeContractTests(unittest.TestCase):
    def test_native_scene_is_a_node3d_entrypoint(self):
        scene = (ROOT / "scenes" / "main.tscn").read_text(encoding="utf-8")
        project = (ROOT / "project.godot").read_text(encoding="utf-8")
        self.assertIn('type="Node3D"', scene)
        self.assertIn('res://scripts/main.gd', scene)
        self.assertIn('run/main_scene="res://scenes/main.tscn"', project)

    def test_world_has_six_stations_room_switch_and_signed_cashflow(self):
        source = (ROOT / "scripts" / "arena_world.gd").read_text(encoding="utf-8")
        for token in ("class_name ArenaWorld", "enter_room", "return_to_arena", "animate_cashflow", "get_station_positions"):
            self.assertIn(token, source)
        self.assertIn("res://assets/generated/agents/", source)
        self.assertIn("res://assets/generated/rooms/", source)
        self.assertIn("SharedMarketScreen", source)
        self.assertNotIn("CentralVault", source)
        self.assertIn("target_agent_id", source)

    def test_hud_has_responsive_controls_and_replay(self):
        source = (ROOT / "scripts" / "arena_hud.gd").read_text(encoding="utf-8")
        for token in ("class_name ArenaHUD", "layout_mode_for", "apply_responsive_layout", "ReplaySlider", "export_requested"):
            self.assertIn(token, source)

    def test_main_wires_simulation_world_and_hud(self):
        source = (ROOT / "scripts" / "main.gd").read_text(encoding="utf-8")
        for token in ("ArenaSimulation", "ArenaWorld", "ArenaHUD", "advance_day", "set_replay_day", "export_payload"):
            self.assertIn(token, source)

    def test_godot_project_ignores_local_caches_and_blender_backups(self):
        ignore_file = ROOT / ".gitignore"
        self.assertTrue(ignore_file.is_file(), "Godot project must own a local-artifact ignore file")
        ignore = ignore_file.read_text(encoding="utf-8")
        for pattern in (".godot/", ".venv/", "__pycache__/", "*.py[cod]", "*.blend1", "*.blend2"):
            self.assertIn(pattern, ignore)

    def test_ci_blender_cleanup_uses_shell_safe_find_commands(self):
        candidates = [ROOT.parents[1] / ".github" / "workflows" / "ai-arena-godot.yml", ROOT.parent / ".github" / "workflows" / "ai-arena-godot.yml"]
        workflow = next((path for path in candidates if path.is_file()), None)
        if workflow is None:
            self.skipTest("workflow file is not included in the downloadable Godot project artifact")
        source = workflow.read_text(encoding="utf-8")
        self.assertIn("find assets/source -type f -name '*.blend1' -delete", source)
        self.assertIn("find assets/source -type f -name '*.blend2' -delete", source)

if __name__ == "__main__":
    unittest.main()
