extends SceneTree

const ARENA_WORLD_PATH := "res://scripts/arena_world.gd"

var _failed := false

func _initialize() -> void:
	call_deferred("_run")

func _run() -> void:
	var world_script := load(ARENA_WORLD_PATH) as Script
	if world_script == null or not world_script.can_instantiate():
		push_error("ArenaWorld script did not compile")
		quit(1)
		return

	var world = world_script.new()
	world.use_imported_models = false
	root.add_child(world)
	_check(world.agent_anchors.size() == 6, "the AI roster must expose six Agent podium anchors")
	_check(world.get_station_positions().has("investor"), "the 3D arena must include a separate seventh-investor seat")
	_check(world.find_child("InvestorSeatTitle", true, false) != null, "the seventh seat must be visibly labeled")
	_check(world.current_mode == "arena", "the initial 3D mode must be the arena")
	_check(world.select_agent("growth"), "a faction podium must be selectable")
	world.enter_room("growth")
	_check(world.get_node_or_null("RoomViews/growth/AIEnvironmentBackdrop") != null, "selected room must show its generated environment image")
	_check(world.get_node_or_null("RoomViews/growth/RoomTitle") != null, "selected room must show its title")
	_check(world.current_mode == "room", "entering a research room must change the 3D environment")
	_check(world.current_agent == "growth", "the selected Agent must own the room")
	world.return_to_arena()
	_check(world.current_mode == "arena", "return action must restore the shared arena")
	_check(world.animate_cashflow("growth", 200.0) == "gain", "positive P&L must rise from the Agent’s own account marker")
	_check(world.animate_cashflow("growth", -200.0) == "loss", "negative P&L must return toward the same Agent’s account marker")
	_check(world.animate_cashflow("growth", 0.0) == "none", "zero P&L must not spawn cash notes")
	_check(world.animate_cashflow("investor", 200.0) == "gain", "the seventh investor has a local gain animation")
	var notes: Array = world.get_tree().get_nodes_in_group("cashflow_notes")
	_check(notes.size() == 3, "gain/loss and investor gain each create one local visual note")
	for note in notes:
		_check(str(note.get_meta("source_agent_id", "")) == str(note.get_meta("target_agent_id", "")), "cash note must never cross between independent accounts")
	var investor_note_found := false
	for note in notes:
		if str(note.get_meta("agent_id", "")) == "investor":
			investor_note_found = true
	_check(investor_note_found, "the seventh investor cash note must stay on the personal seat")
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
