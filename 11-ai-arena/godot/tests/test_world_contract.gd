extends SceneTree

const ARENA_WORLD_PATH := "res://scripts/arena_world.gd"

var _failed := false

func _initialize() -> void:
	var world_script := load(ARENA_WORLD_PATH) as Script
	if world_script == null or not world_script.can_instantiate():
		push_error("ArenaWorld script did not compile")
		quit(1)
		return
	_run(world_script)

func _run(world_script: Script) -> void:
	var world = world_script.new()
	world.use_imported_models = false
	root.add_child(world)
	_check(world.agent_anchors.size() == 6, "the 3D arena must expose six Agent podium anchors")
	_check(world.current_mode == "arena", "the initial 3D mode must be the arena")
	_check(world.select_agent("growth"), "a faction podium must be selectable")
	world.enter_room("growth")
	_check(world.get_node_or_null("RoomViews/growth/AIEnvironmentBackdrop") != null, "selected room must show its generated environment image")
	_check(world.get_node_or_null("RoomViews/growth/RoomTitle") != null, "selected room must show its title")
	_check(world.current_mode == "room", "entering a research room must change the 3D environment")
	_check(world.current_agent == "growth", "the selected Agent must own the room")
	world.return_to_arena()
	_check(world.current_mode == "arena", "return action must restore the shared arena")
	_check(world.animate_cashflow("growth", 200.0) == "to_agent", "positive P&L must route notes toward the Agent")
	_check(world.animate_cashflow("growth", -200.0) == "to_vault", "negative P&L must route notes toward the vault")
	_check(world.animate_cashflow("growth", 0.0) == "none", "zero P&L must not spawn cash notes")
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
