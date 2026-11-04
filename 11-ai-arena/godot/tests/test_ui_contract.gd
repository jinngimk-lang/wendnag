extends SceneTree

const MainScene = preload("res://scenes/main.tscn")

var _failed := false

func _initialize() -> void:
	call_deferred("_run")

func _run() -> void:
	var app = MainScene.instantiate()
	root.add_child(app)
	await process_frame
	_check(app.apply_responsive_layout(1600.0) == "desktop", "wide desktop layout must be selected")
	_check(app.apply_responsive_layout(1024.0) == "tablet", "tablet layout must be selected")
	_check(app.apply_responsive_layout(768.0) == "tablet", "small tablet layout must be selected")
	_check(app.apply_responsive_layout(390.0) == "mobile", "phone layout must be selected")
	_check(app.apply_responsive_layout(320.0) == "mobile", "minimum-width layout must be selected")
	_check(app.simulation.current_day == 0, "the UI must start on the opening market day")
	app.advance_one_day()
	_check(app.simulation.current_day == 1, "the Next Day action must advance the simulator once")
	app.enter_research_room("quant")
	_check(app.current_view == "room", "the Agent room action must change the visible workspace")
	_check(app.selected_agent == "quant", "the Agent room must retain the selected faction")
	app.return_to_arena()
	_check(app.current_view == "arena", "the back action must restore the arena view")
	app.queue_free()
	if _failed:
		quit(1)
	else:
		print("AI ARENA UI CONTRACT: PASS")
		quit(0)

func _check(condition: bool, message: String) -> void:
	if not condition:
		_failed = true
		push_error("UI CONTRACT FAILED: " + message)
