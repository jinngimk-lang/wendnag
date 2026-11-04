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

    def test_hud_has_responsive_controls_and_replay(self):
        source = (ROOT / "scripts" / "arena_hud.gd").read_text(encoding="utf-8")
        for token in ("class_name ArenaHUD", "layout_mode_for", "apply_responsive_layout", "ReplaySlider", "export_requested"):
            self.assertIn(token, source)

    def test_main_wires_simulation_world_and_hud(self):
        source = (ROOT / "scripts" / "main.gd").read_text(encoding="utf-8")
        for token in ("ArenaSimulation", "ArenaWorld", "ArenaHUD", "advance_day", "set_replay_day", "export_payload"):
            self.assertIn(token, source)

if __name__ == "__main__":
    unittest.main()
