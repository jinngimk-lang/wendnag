extends Node3D

const ArenaSimulation = preload("res://scripts/arena_simulation.gd")
const ArenaWorld = preload("res://scripts/arena_world.gd")
const ArenaHUD = preload("res://scripts/arena_hud.gd")

var _simulation = ArenaSimulation.new()
var simulation:
	get:
		return _simulation
var _world: ArenaWorld
var _hud: ArenaHUD
var _playback_timer: Timer
var selected_agent := "value"
var current_view := "arena"
var _status := "SYNTHETIC PAPER MODE  ·  NO BROKER CONNECTION"
var use_imported_models := true

func _ready() -> void:
	_simulation.configure(100000.0, 90, 20261104)
	_world = ArenaWorld.new()
	_world.name = "ArenaWorld"
	_world.use_imported_models = use_imported_models
	add_child(_world)

	_hud = ArenaHUD.new()
	_hud.name = "ArenaHUD"
	add_child(_hud)
	_hud.playback_requested.connect(_on_playback_action)
	_hud.agent_selected.connect(_on_agent_selected)
	_hud.room_requested.connect(_on_room_requested)
	_hud.room_exit_requested.connect(_on_room_exit_requested)
	_hud.day_scrubbed.connect(_on_day_scrubbed)
	_hud.export_requested.connect(_on_export_requested)

	_playback_timer = Timer.new()
	_playback_timer.name = "SimulationPlayback"
	_playback_timer.wait_time = 0.72
	_playback_timer.one_shot = false
	_playback_timer.timeout.connect(_advance_one_day)
	add_child(_playback_timer)
	_refresh()

func _on_playback_action(action: String) -> void:
	match action:
		"play":
			if _simulation.current_day >= _simulation.trading_days:
				_simulation.configure(_simulation.starting_capital, _simulation.trading_days, _simulation.seed_value)
			_playback_timer.start()
			_set_status("SIMULATION RUNNING  ·  PAPER MODE")
		"pause":
			_playback_timer.stop()
			_set_status("SIMULATION PAUSED")
		"next":
			_playback_timer.stop()
			_advance_one_day()
		"next5":
			_playback_timer.stop()
			for _index in range(5):
				if _simulation.current_day < _simulation.trading_days:
					_advance_one_day()
		"finish":
			_playback_timer.stop()
			while _simulation.current_day < _simulation.trading_days:
				_advance_one_day()
			_set_status("SIMULATION SETTLED  ·  %d DAYS" % _simulation.current_day)
		"reset":
			_playback_timer.stop()
			_simulation.configure(_simulation.starting_capital, _simulation.trading_days, _simulation.seed_value)
			_world.return_to_arena()
			current_view = "arena"
			_hud.set_room_mode(false)
			_set_status("RUN RESET  ·  SAME SEED / SAME MARKET PATH")

func _advance_one_day() -> void:
	if _simulation.current_day >= _simulation.trading_days:
		_playback_timer.stop()
		_set_status("SIMULATION SETTLED")
		return
	var operations: Array[Dictionary] = _simulation.advance_day()
	for operation in operations:
		_world.animate_cashflow(str(operation.agent_id), float(operation.delta_equity))
	if _simulation.current_day >= _simulation.trading_days:
		_playback_timer.stop()
		_status = "SIMULATION SETTLED"
	else:
		_status = "DAY %03d  ·  SIX INDEPENDENT DECISIONS" % _simulation.current_day
	_refresh()

func _on_day_scrubbed(day: int) -> void:
	_playback_timer.stop()
	_simulation.set_replay_day(day)
	_set_status("HISTORY REPLAY  ·  DAY %03d" % _simulation.replay_day)

func _on_agent_selected(agent_id: String) -> void:
	selected_agent = agent_id
	_world.select_agent(agent_id)
	_refresh()

func _on_room_requested(agent_id: String) -> void:
	selected_agent = agent_id
	_world.enter_room(agent_id)
	current_view = "room"
	_set_status("RESEARCH ROOM  ·  %s" % agent_id.to_upper())

func _on_room_exit_requested() -> void:
	_world.return_to_arena()
	current_view = "arena"
	_set_status("ARENA OVERVIEW  ·  SIX AGENTS")

func _on_export_requested() -> void:
	var payload: Dictionary = _simulation.export_payload()
	var filename := "user://ai-arena-%s-day-%03d.json" % [str(_simulation.seed_value), _simulation.current_day]
	var file := FileAccess.open(filename, FileAccess.WRITE)
	if file == null:
		_set_status("JSON EXPORT FAILED")
		push_error("Could not open export path: " + filename)
		return
	file.store_string(JSON.stringify(payload, "\t"))
	file.close()
	_set_status("JSON EXPORTED  ·  " + ProjectSettings.globalize_path(filename))

func _set_status(message: String) -> void:
	_status = message
	_refresh()

func _refresh() -> void:
	if _hud != null:
		_hud.update_view(_simulation, _selected_agent, _status)

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		if event.keycode == KEY_ESCAPE and _world.current_view == "room":
			_world.return_to_arena()
			current_view = "arena"
			_hud.set_room_mode(false)
			_set_status("ARENA OVERVIEW")
		elif event.keycode == KEY_TAB:
			_hud.visible = not _hud.visible
	elif event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		_pick_agent(event.position)

func _pick_agent(screen_position: Vector2) -> void:
	var camera := _world.get_camera()
	if camera == null:
		return
	var origin := camera.project_ray_origin(screen_position)
	var end := origin + camera.project_ray_normal(screen_position) * 120.0
	var query := PhysicsRayQueryParameters3D.create(origin, end)
	query.collision_mask = 2
	query.collide_with_areas = true
	query.collide_with_bodies = true
	var hit := get_world_3d().direct_space_state.intersect_ray(query)
	if hit.is_empty():
		return
	var collider: Object = hit.get("collider")
	if collider != null and collider.has_meta("agent_id"):
		_on_agent_selected(str(collider.get_meta("agent_id")))

func apply_responsive_layout(width: float) -> String:
	if _hud == null:
		return ArenaHUD.layout_mode_for(width)
	return _hud.apply_responsive_layout(width)

func advance_one_day() -> void:
	_advance_one_day()

func enter_research_room(agent_id: String) -> void:
	_on_room_requested(agent_id)

func return_to_arena() -> void:
	_on_room_exit_requested()
