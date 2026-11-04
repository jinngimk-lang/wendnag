extends SceneTree

const ArenaWorld = preload("res://scripts/arena_world.gd")

func _initialize() -> void:
	call_deferred("_run")

func _run() -> void:
	var world = ArenaWorld.new()
	root.add_child(world)
	await process_frame

	var positions: Dictionary = world.get_station_positions()
	_check(positions.size() == 6, "arena must expose six station anchors")
	for agent_id in ["value", "growth", "trend", "quant", "sentiment", "macro"]:
		_check(positions.has(agent_id), "%s station anchor must exist" % agent_id)
		_check(world.get_node_or_null("ArenaStage/Stations/" + agent_id) != null, "%s 3D station must exist" % agent_id)
		_check(world.get_node_or_null("RoomViews/" + agent_id) != null, "%s research room must exist" % agent_id)

	world.enter_room("quant")
	_check(world.current_view == "room", "enter_room must switch to the room view")
	_check(world.selected_agent == "quant", "room switch must preserve the selected Agent")
	world.return_to_arena()
	_check(world.current_view == "arena", "return_to_arena must restore the arena view")

	_check(world.animate_cashflow("value", 100.0) == "to_agent", "positive equity change must animate toward Agent")
	_check(world.animate_cashflow("value", -100.0) == "to_vault", "negative equity change must animate toward vault")
	_check(world.animate_cashflow("value", 0.0) == "none", "zero equity change must not spawn a note")

	print("AI ARENA WORLD CONTRACT: PASS")
	quit(0)

func _check(condition: bool, message: String) -> void:
	if not condition:
		push_error("WORLD CONTRACT FAILED: " + message)
		quit(1)
