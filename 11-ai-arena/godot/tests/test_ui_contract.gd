extends SceneTree

const ArenaHUD = preload("res://scripts/arena_hud.gd")

func _initialize() -> void:
	call_deferred("_run")

func _run() -> void:
	_check(ArenaHUD.layout_mode_for(1600) == "desktop", "wide screens use desktop layout")
	_check(ArenaHUD.layout_mode_for(1024) == "tablet", "medium screens use tablet layout")
	_check(ArenaHUD.layout_mode_for(768) == "tablet", "small tablets keep the compact layout")
	_check(ArenaHUD.layout_mode_for(390) == "mobile", "phones use mobile layout")
	_check(ArenaHUD.layout_mode_for(320) == "mobile", "minimum width remains supported")

	var hud = ArenaHUD.new()
	root.add_child(hud)
	await process_frame
	_check(hud.get_node_or_null("HUDRoot/Header") != null, "HUD header must be built")
	_check(hud.get_node_or_null("HUDRoot/BottomDock/ReplaySlider") != null, "replay slider must be interactive")
	_check(hud.get_node_or_null("HUDRoot/AgentRail") != null, "Agent rail must be present")
	_check(hud.apply_responsive_layout(390) == "mobile", "responsive layout must switch at phone width")
	_check(hud.get_meta("layout_mode") == "mobile", "mobile mode must be recorded")
	hud.apply_responsive_layout(1600)
	_check(hud.get_meta("layout_mode") == "desktop", "desktop mode must be restored")

	print("AI ARENA UI CONTRACT: PASS")
	quit(0)

func _check(condition: bool, message: String) -> void:
	if not condition:
		push_error("UI CONTRACT FAILED: " + message)
		quit(1)
