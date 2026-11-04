extends SceneTree

const ArenaWorld = preload("res://scripts/arena_world.gd")

var _failed := false

func _initialize() -> void:
	_run()

func _run() -> void:
	var world = ArenaWorld.new()
	root.add_child(world)
	_check(world.agent_anchors.size() == 6, "the 3D arena must expose six Agent podium anchors")
	_check(world.current_mode == "arena", "the initial 3D mode must be the arena")
	_check(world.select_agent("growth"), "a faction podium must be selectable")
	world.enter_room("growth")
	_check(world.current_mode == "room", "entering a research room must change the 3D environment")
	_check(world.current_agent == "growth", "the selected Agent must own the room")
	world.return_to_arena()
	_check(world.current_mode == "arena", "return action must restore the shared arena")
	_check(ArenaWorld.cashflow_direction_for(200.0) == "to_agent", "positive P&L must route notes toward the Agent")
	_check(ArenaWorld.cashflow_direction_for(-200.0) == "to_vault", "negative P&L must route notes toward the vault")
	_check(ArenaWorld.cashflow_direction_for(0.0) == "none", "zero P&L must not spawn cash notes")
	world.queue_free()
	if _failed:
		quit(1)
	else:
		print("AI ARENA WORLD CONTRACT: PASS")
		quit(0)

func _check(condition: bool, message: String) -> void:
	if not condition:
		_failed = true
		push_error("WORLD CONTRACT FAILED: " + message)
