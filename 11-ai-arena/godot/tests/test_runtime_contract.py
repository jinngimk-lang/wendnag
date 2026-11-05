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
        for token in ("class_name ArenaHUD", "layout_mode_for", "apply_responsive_layout", "ReplaySlider", "export_requested", "RunSetupDialog", "InvestorTargetWeightSlider", "FollowStrategyButton", "ChallengeStrategyButton", "run_setup_confirmed"):
            self.assertIn(token, source)

    def test_main_wires_simulation_world_and_hud(self):
        source = (ROOT / "scripts" / "main.gd").read_text(encoding="utf-8")
        for token in ("ArenaSimulation", "ArenaWorld", "ArenaHUD", "advance_day", "set_replay_day", "export_payload", "investor_mode_requested", "_on_run_setup_confirmed", "_on_investor_mode_requested"):
            self.assertIn(token, source)

    def test_simulation_keeps_six_agents_and_adds_a_separate_seventh_investor(self):
        source = (ROOT / "scripts" / "arena_simulation.gd").read_text(encoding="utf-8")
        for token in ('const INVESTOR_ID := "investor"', "var investor_account", "set_investor_mode", "set_investor_target_weight", "_advance_investor", "get_investor_snapshot", "challenged_agent_id", "get_rankings"):
            self.assertIn(token, source)
        self.assertIn('"investor": investor_account.duplicate(true)', source)

    def test_world_builds_a_separate_seventh_investor_seat(self):
        source = (ROOT / "scripts" / "arena_world.gd").read_text(encoding="utf-8")
        self.assertIn("_build_investor_seat", source)
        self.assertIn('seat.name = "investor"', source)
        self.assertIn('title.text = "YOU  ·  THE 7TH INVESTOR"', source)

    def test_visual_capture_covers_arena_investor_and_mobile(self):
        source = (ROOT / "tests" / "capture_visual.gd").read_text(encoding="utf-8")
        for token in ("arena-desktop.png", "investor-desktop.png", "investor-mobile.png", "RenderingServer.frame_post_draw"):
            self.assertIn(token, source)

    def test_cjk_font_is_generated_and_applied_to_hud_and_world_labels(self):
        font = ROOT / "assets" / "fonts" / "NotoSansSC-Subset.otf"
        self.assertTrue(font.is_file(), "CI must generate the CJK font before Godot import")
        self.assertTrue((ROOT / "assets" / "fonts" / "OFL.txt").is_file(), "the generated font must include its license")
        hud = (ROOT / "scripts" / "arena_hud.gd").read_text(encoding="utf-8")
        world = (ROOT / "scripts" / "arena_world.gd").read_text(encoding="utf-8")
        self.assertIn("hud_theme.default_font = CJK_FONT", hud)
        self.assertIn("market_label.font = CJK_FONT", world)
        self.assertIn("title.font = CJK_FONT", world)

    def test_cjk_font_builder_is_valid_python(self):
        source = (ROOT / "tools" / "prepare_cjk_font.py").read_text(encoding="utf-8")
        compile(source, "prepare_cjk_font.py", "exec")

    def test_godot_project_ignores_local_caches_and_blender_backups(self):
        ignore_file = ROOT / ".gitignore"
        self.assertTrue(ignore_file.is_file(), "Godot project must own a local-artifact ignore file")
        ignore = ignore_file.read_text(encoding="utf-8")
        for pattern in (".godot/", ".venv/", "__pycache__/", "*.py[cod]", "*.blend1", "*.blend2", "visual-qa/"):
            self.assertIn(pattern, ignore)

    def test_hud_uses_button_theme_constants_for_icon_sizing(self):
        source = (ROOT / "scripts" / "arena_hud.gd").read_text(encoding="utf-8")
        self.assertIn('button.add_theme_constant_override("icon_max_width", 48)', source)
        self.assertIn('button.add_theme_constant_override("icon_max_width", 28)', source)
        self.assertNotIn("button.icon_max_width", source)

    def test_godot_check_runner_fails_on_script_errors(self):
        runner = ROOT / "tools" / "run_godot_check.sh"
        self.assertTrue(runner.is_file(), "CI must use the checked Godot runner")
        source = runner.read_text(encoding="utf-8")
        self.assertIn("SCRIPT ERROR:", source)
        self.assertIn("Parse Error:", source)

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
