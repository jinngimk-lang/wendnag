extends Node3D
class_name ArenaWorld

const AgentCatalog = preload("res://scripts/agent_catalog.gd")
const ArenaSimulation = preload("res://scripts/arena_simulation.gd")
const AGENT_IDS := ["value", "growth", "trend", "quant", "sentiment", "macro"]

var current_view := "arena"
var current_mode := "arena"
var selected_agent := "value"
var current_agent := "value"
var agent_anchors: Dictionary = {}
var use_imported_models := true
var _arena_stage: Node3D
var _room_views: Dictionary = {}
var _station_positions: Dictionary = {}
var _station_nodes: Dictionary = {}
var _camera: Camera3D
var _vault_position := Vector3.ZERO

func _ready() -> void:
	_build_environment()
	_build_arena_stage()
	_build_room_views()
	_build_camera()
	select_agent(selected_agent)

func _build_environment() -> void:
	var world_environment := WorldEnvironment.new()
	world_environment.name = "ArenaEnvironment"
	var environment := Environment.new()
	environment.background_mode = Environment.BG_SKY
	var sky := Sky.new()
	var sky_material := ProceduralSkyMaterial.new()
	sky_material.sky_top_color = Color("#07111d")
	sky_material.sky_horizon_color = Color("#1a2b3b")
	sky_material.ground_bottom_color = Color("#05080e")
	sky_material.ground_horizon_color = Color("#0c1722")
	sky.sky_material = sky_material
	environment.sky = sky
	environment.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	environment.ambient_light_color = Color("#8a9baa")
	environment.ambient_light_energy = 0.52
	environment.tonemap_mode = Environment.TONE_MAPPER_FILMIC
	environment.glow_enabled = true
	environment.glow_intensity = 0.28
	world_environment.environment = environment
	add_child(world_environment)

	var key := DirectionalLight3D.new()
	key.name = "WarmKeyLight"
	key.rotation_degrees = Vector3(-48, -28, 0)
	key.light_color = Color("#ffe0b0")
	key.light_energy = 1.25
	key.shadow_enabled = true
	add_child(key)

	var fill := OmniLight3D.new()
	fill.name = "CoolFillLight"
	fill.position = Vector3(6.0, 7.0, 7.0)
	fill.light_color = Color("#70aee4")
	fill.light_energy = 520.0
	fill.omni_range = 22.0
	add_child(fill)

func _build_arena_stage() -> void:
	_arena_stage = Node3D.new()
	_arena_stage.name = "ArenaStage"
	add_child(_arena_stage)

	_box(_arena_stage, "ArenaFloor", Vector3(0, -0.25, 0), Vector3(23, 0.5, 17), Color("#111c27"), 0.82, 0.36)
	_box(_arena_stage, "RearArchitecture", Vector3(0, 2.3, -8.0), Vector3(22, 5.2, 0.35), Color("#172633"), 0.65, 0.46)
	_box(_arena_stage, "LeftArchitecture", Vector3(-11.2, 2.1, 0), Vector3(0.35, 4.8, 16), Color("#14222f"), 0.58, 0.48)
	_box(_arena_stage, "RightArchitecture", Vector3(11.2, 2.1, 0), Vector3(0.35, 4.8, 16), Color("#14222f"), 0.58, 0.48)

	_cylinder(_arena_stage, "CentralVaultBase", Vector3(0, 0.12, 0), 2.1, 0.32, Color("#8f7048"), 0.72)
	_cylinder(_arena_stage, "CentralVaultGlass", Vector3(0, 0.78, 0), 1.15, 1.05, Color("#263f50"), 0.42)
	_cylinder(_arena_stage, "CentralVaultCap", Vector3(0, 1.36, 0), 1.42, 0.16, Color("#c5a16b"), 0.72)
	_box(_arena_stage, "VaultFrontPlate", Vector3(0, 0.88, 1.10), Vector3(0.9, 0.34, 0.08), Color("#142431"), 0.55, 0.28, Color("#e8c98e"), 0.75)
	var vault_label := Label3D.new()
	vault_label.name = "VaultLabel"
	vault_label.text = "AI  ·  CAPITAL VAULT"
	vault_label.font_size = 30
	vault_label.pixel_size = 0.006
	vault_label.position = Vector3(0, 1.75, 0)
	vault_label.modulate = Color("#f1d9ac")
	_arena_stage.add_child(vault_label)

	var ring := _cylinder(_arena_stage, "ArenaInnerRing", Vector3(0, -0.01, 0), 8.3, 0.055, Color("#263d4c"), 0.7)
	ring.scale = Vector3(1.0, 1.0, 0.72)
	var stations := Node3D.new()
	stations.name = "Stations"
	_arena_stage.add_child(stations)

	for index in range(AGENT_IDS.size()):
		var agent_id: String = str(AGENT_IDS[index])
		var angle := -PI * 0.5 + float(index) * TAU / 6.0
		var station_position := Vector3(cos(angle) * 7.1, 0.0, sin(angle) * 5.15)
		_station_positions[agent_id] = station_position
		var station := _build_station(agent_id, station_position)
		stations.add_child(station)
		_station_nodes[agent_id] = station
	agent_anchors = _station_positions.duplicate(true)

func _build_station(agent_id: String, station_position: Vector3) -> Node3D:
	var faction := AgentCatalog.get_faction(agent_id)
	var accent := AgentCatalog.color_for(agent_id)
	var station := Node3D.new()
	station.name = agent_id
	station.position = station_position
	station.set_meta("agent_id", agent_id)

	_cylinder(station, "PodiumBase", Vector3(0, 0.18, 0), 1.38, 0.34, Color("#1a2b38"), 0.62)
	_cylinder(station, "PodiumAccent", Vector3(0, 0.39, 0), 1.18, 0.075, accent, 0.68)
	_cylinder(station, "PodiumTop", Vector3(0, 0.49, 0), 1.08, 0.10, Color("#233744"), 0.44)
	_box(station, "RoomFrame", Vector3(0, 2.25, -0.82), Vector3(3.75, 2.42, 0.18), Color("#1b2c38"), 0.58, 0.34, accent, 0.35)
	_add_textured_quad(station, "RoomBackdrop", Vector3(0, 2.25, -0.70), Vector2(3.46, 2.13), AgentCatalog.room_texture(agent_id))
	_box(station, "PortraitFrame", Vector3(-1.30, 1.88, -0.68), Vector3(0.94, 1.26, 0.12), accent, 0.55, 0.28)
	_add_textured_quad(station, "Portrait", Vector3(-1.30, 1.88, -0.59), Vector2(0.78, 1.10), AgentCatalog.portrait_texture(agent_id))

	var agent_model: Node3D = null
	if use_imported_models:
		agent_model = _load_glb("res://assets/generated/agents/%s.glb" % agent_id, station, 0.52)
	if agent_model == null:
		_build_fallback_agent(station, agent_id)
	else:
		agent_model.position = Vector3(0.55, 0.50, 0.16)

	var name_label := Label3D.new()
	name_label.name = "FactionName"
	name_label.text = str(faction.get("name", agent_id))
	name_label.font_size = 34
	name_label.pixel_size = 0.007
	name_label.position = Vector3(0, 3.62, -0.70)
	name_label.modulate = accent.lightened(0.24)
	station.add_child(name_label)

	var role_label := Label3D.new()
	role_label.name = "FactionRole"
	role_label.text = str(faction.get("english", "INVESTMENT AGENT"))
	role_label.font_size = 17
	role_label.pixel_size = 0.006
	role_label.position = Vector3(0, 3.30, -0.70)
	role_label.modulate = Color("#d6e0e6")
	station.add_child(role_label)

	var glow := OmniLight3D.new()
	glow.name = "FactionGlow"
	glow.position = Vector3(0, 2.2, 0.1)
	glow.light_color = accent
	glow.light_energy = 180.0
	glow.omni_range = 4.4
	station.add_child(glow)

	var pick_area := Area3D.new()
	pick_area.name = "PickArea"
	pick_area.collision_layer = 2
	pick_area.collision_mask = 0
	pick_area.set_meta("agent_id", agent_id)
	var collision := CollisionShape3D.new()
	var shape := BoxShape3D.new()
	shape.size = Vector3(3.8, 4.2, 2.8)
	collision.shape = shape
	collision.position = Vector3(0, 1.9, 0)
	pick_area.add_child(collision)
	station.add_child(pick_area)
	return station

func _build_room_views() -> void:
	var room_root := Node3D.new()
	room_root.name = "RoomViews"
	add_child(room_root)
	for agent_id in AGENT_IDS:
		var room := Node3D.new()
		room.name = agent_id
		room.visible = false
		room.set_meta("loaded", false)
		room_root.add_child(room)
		_room_views[agent_id] = room

func _ensure_room_loaded(agent_id: String) -> void:
	if not _room_views.has(agent_id):
		return
	var room := _room_views[agent_id] as Node3D
	if bool(room.get_meta("loaded", false)):
		return
	var faction := AgentCatalog.get_faction(agent_id)
	var accent := AgentCatalog.color_for(agent_id)
	var room_model: Node3D = null
	if use_imported_models:
		room_model = _load_glb("res://assets/generated/rooms/%s.glb" % agent_id, room, 0.92)
	var backdrop_z := -4.72
	if room_model == null:
		_build_fallback_room(room, agent_id, accent)
	else:
		room_model.name = "RoomModel"
		room_model.position = Vector3.ZERO
		backdrop_z = -3.70
	_add_textured_quad(room, "AIEnvironmentBackdrop", Vector3(0, 3.25, backdrop_z), Vector2(10.6, 5.4), AgentCatalog.room_texture(agent_id))
	var agent_model: Node3D = null
	if use_imported_models:
		agent_model = _load_glb("res://assets/generated/agents/%s.glb" % agent_id, room, 0.96)
	if agent_model == null:
		_build_fallback_agent(room, agent_id)
	else:
		agent_model.name = "AgentModel"
		agent_model.position = Vector3(-0.55, 0.05, 1.25)
	var room_label := Label3D.new()
	room_label.name = "RoomTitle"
	room_label.text = "%s  /  %s" % [str(faction.get("room_name", "RESEARCH ROOM")), str(faction.get("english", ""))]
	room_label.font_size = 34
	room_label.pixel_size = 0.009
	room_label.position = Vector3(0, 4.9, backdrop_z + 0.14)
	room_label.modulate = accent.lightened(0.22)
	room.add_child(room_label)
	room.set_meta("loaded", true)

func _build_fallback_room(parent: Node3D, agent_id: String, accent: Color) -> void:
	_box(parent, "RoomFloor", Vector3(0, -0.20, 0), Vector3(13, 0.4, 10), Color("#17232e"), 0.68, 0.42)
	_box(parent, "RoomBackWall", Vector3(0, 2.5, -4.8), Vector3(13, 5.4, 0.22), Color("#1c2c39"), 0.62, 0.52)
	_box(parent, "RoomLeftWall", Vector3(-6.4, 2.5, 0), Vector3(0.22, 5.4, 10), Color("#152431"), 0.58, 0.48)
	_box(parent, "RoomRightWall", Vector3(6.4, 2.5, 0), Vector3(0.22, 5.4, 10), Color("#152431"), 0.58, 0.48)
	_box(parent, "ResearchDesk", Vector3(0, 1.0, -0.4), Vector3(5.8, 0.16, 1.8), Color("#604a35"), 0.72, 0.34)
	_box(parent, "MonitorFrame", Vector3(0, 2.0, -1.25), Vector3(2.7, 1.5, 0.16), Color("#111d28"), 0.52, 0.26, accent, 0.45)
	_box(parent, "MonitorScreen", Vector3(0, 2.0, -1.36), Vector3(2.42, 1.23, 0.04), Color("#081722"), 0.3, 0.18, accent, 0.28)

func _build_fallback_agent(parent: Node3D, agent_id: String) -> void:
	var accent := AgentCatalog.color_for(agent_id)
	var suit_color := Color("#1a2a38")
	if agent_id == "growth":
		suit_color = Color("#b7c0b9")
	elif agent_id == "trend":
		suit_color = Color("#15243a")
	elif agent_id == "quant":
		suit_color = Color("#292537")
	elif agent_id == "sentiment":
		suit_color = Color("#29232a")
	elif agent_id == "macro":
		suit_color = Color("#334254")
	_capsule(parent, "FallbackAgentTorso", Vector3(0, 1.0, 0.35), 0.48, 1.55, suit_color)
	_sphere(parent, "FallbackAgentHead", Vector3(0, 2.10, 0.35), Vector3(0.38, 0.48, 0.36), Color("#d7ad91"))
	_sphere(parent, "FallbackAgentHair", Vector3(0, 2.42, 0.39), Vector3(0.40, 0.25, 0.39), Color("#28252a"))
	_box(parent, "FallbackAgentAccent", Vector3(0, 1.42, -0.02), Vector3(0.12, 0.52, 0.08), accent, 0.24, 0.28)

func _build_camera() -> void:
	_camera = Camera3D.new()
	_camera.name = "ArenaCamera"
	_camera.current = true
	_camera.fov = 50.0
	_camera.position = Vector3(0, 11.8, 18.4)
	add_child(_camera)
	_camera.look_at(Vector3(0, 1.0, 0), Vector3.UP)

func get_camera() -> Camera3D:
	return _camera

func get_station_positions() -> Dictionary:
	return _station_positions.duplicate(true)

func select_agent(agent_id: String) -> bool:
	if not _station_nodes.has(agent_id):
		return false
	selected_agent = agent_id
	current_agent = agent_id
	for id in _station_nodes:
		var station: Node3D = _station_nodes[id]
		var target_scale := Vector3.ONE * (1.06 if id == agent_id else 1.0)
		var accent := AgentCatalog.color_for(str(id))
		var glow := station.get_node_or_null("FactionGlow") as OmniLight3D
		if glow != null:
			glow.light_energy = 260.0 if id == agent_id else 130.0
		var podium := station.get_node_or_null("PodiumAccent") as MeshInstance3D
		if podium != null:
			var mat := _material(accent if id == agent_id else accent.darkened(0.38), 0.62, 0.3)
			podium.material_override = mat
		station.scale = target_scale
	return true

func enter_room(agent_id: String) -> void:
	if not _room_views.has(agent_id):
		return
	_ensure_room_loaded(agent_id)
	selected_agent = agent_id
	current_agent = agent_id
	current_view = "room"
	current_mode = "room"
	_arena_stage.visible = false
	for id in _room_views:
		(_room_views[id] as Node3D).visible = id == agent_id
	if _camera != null:
		_camera.position = Vector3(0, 5.1, 10.6)
		_camera.fov = 54.0
		_camera.look_at(Vector3(0, 1.65, -0.3), Vector3.UP)
	select_agent(agent_id)

func return_to_arena() -> void:
	current_view = "arena"
	current_mode = "arena"
	current_agent = selected_agent
	_arena_stage.visible = true
	for id in _room_views:
		(_room_views[id] as Node3D).visible = false
	if _camera != null:
		_camera.position = Vector3(0, 11.8, 18.4)
		_camera.fov = 50.0
		_camera.look_at(Vector3(0, 1.0, 0), Vector3.UP)
	select_agent(selected_agent)

static func cashflow_direction_for(signed_delta: float) -> String:
	return ArenaSimulation.cashflow_direction(signed_delta)

func animate_cashflow(agent_id: String, signed_delta: float) -> String:
	var direction := ArenaSimulation.cashflow_direction(signed_delta)
	if direction == "none" or not _station_positions.has(agent_id):
		return "none"
	var note := _load_glb("res://assets/generated/banknote.glb", self, 0.46)
	if note == null:
		note = Node3D.new()
		var note_mesh := MeshInstance3D.new()
		var box := BoxMesh.new()
		box.size = Vector3(1.15, 0.055, 0.62)
		note_mesh.mesh = box
		note_mesh.material_override = _material(Color("#8bc39c"), 0.12, 0.48)
		note.add_child(note_mesh)
		add_child(note)
	note.name = "CashflowNote"
	note.add_to_group("cashflow_notes")
	var target: Vector3 = _station_positions[agent_id] + Vector3(0, 2.4, 0)
	if direction == "to_agent":
		note.position = _vault_position + Vector3(0, 1.7, 0)
	else:
		note.position = target
		target = _vault_position + Vector3(0, 1.7, 0)
	note.rotation_degrees = Vector3(0, 0, 18 if direction == "to_agent" else -18)
	var tween := create_tween()
	tween.set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_IN_OUT)
	tween.tween_property(note, "position", target, 0.95)
	tween.parallel().tween_property(note, "rotation_degrees:y", 360.0, 0.95)
	tween.tween_callback(note.queue_free)
	return direction

func _load_glb(path: String, parent: Node3D, model_scale: float) -> Node3D:
	if not ResourceLoader.exists(path):
		return null
	var packed := load(path) as PackedScene
	if packed == null:
		return null
	var instance := packed.instantiate()
	if not instance is Node3D:
		instance.queue_free()
		return null
	var model := instance as Node3D
	model.scale = Vector3.ONE * model_scale
	parent.add_child(model)
	return model

func _add_textured_quad(parent: Node3D, node_name: String, at: Vector3, size: Vector2, texture: Texture2D) -> void:
	if texture == null:
		return
	var mesh_instance := MeshInstance3D.new()
	mesh_instance.name = node_name
	var quad := QuadMesh.new()
	quad.size = size
	mesh_instance.mesh = quad
	mesh_instance.position = at
	var mat := StandardMaterial3D.new()
	mat.albedo_texture = texture
	mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	mat.cull_mode = BaseMaterial3D.CULL_DISABLED
	mat.texture_filter = BaseMaterial3D.TEXTURE_FILTER_LINEAR
	mesh_instance.material_override = mat
	parent.add_child(mesh_instance)

func _box(parent: Node3D, node_name: String, at: Vector3, size: Vector3, color: Color, metallic: float = 0.2, roughness: float = 0.42, emission_color: Color = Color.BLACK, emission_energy: float = 0.0) -> MeshInstance3D:
	var mesh_instance := MeshInstance3D.new()
	mesh_instance.name = node_name
	var mesh := BoxMesh.new()
	mesh.size = size
	mesh_instance.mesh = mesh
	mesh_instance.position = at
	mesh_instance.material_override = _material(color, metallic, roughness, emission_color, emission_energy)
	parent.add_child(mesh_instance)
	return mesh_instance

func _cylinder(parent: Node3D, node_name: String, at: Vector3, radius: float, height: float, color: Color, metallic: float = 0.25) -> MeshInstance3D:
	var mesh_instance := MeshInstance3D.new()
	mesh_instance.name = node_name
	var mesh := CylinderMesh.new()
	mesh.top_radius = radius
	mesh.bottom_radius = radius * 1.03
	mesh.height = height
	mesh.radial_segments = 48
	mesh_instance.mesh = mesh
	mesh_instance.position = at
	mesh_instance.material_override = _material(color, metallic, 0.34)
	parent.add_child(mesh_instance)
	return mesh_instance

func _sphere(parent: Node3D, node_name: String, at: Vector3, scale_value: Vector3, color: Color) -> MeshInstance3D:
	var mesh_instance := MeshInstance3D.new()
	mesh_instance.name = node_name
	var mesh := SphereMesh.new()
	mesh.radius = 1.0
	mesh.height = 2.0
	mesh.radial_segments = 28
	mesh.rings = 16
	mesh_instance.mesh = mesh
	mesh_instance.position = at
	mesh_instance.scale = scale_value
	mesh_instance.material_override = _material(color, 0.05, 0.68)
	parent.add_child(mesh_instance)
	return mesh_instance

func _capsule(parent: Node3D, node_name: String, at: Vector3, radius: float, height: float, color: Color) -> MeshInstance3D:
	var mesh_instance := MeshInstance3D.new()
	mesh_instance.name = node_name
	var mesh := CapsuleMesh.new()
	mesh.radius = radius
	mesh.height = height
	mesh.radial_segments = 24
	mesh.rings = 8
	mesh_instance.mesh = mesh
	mesh_instance.position = at
	mesh_instance.material_override = _material(color, 0.08, 0.52)
	parent.add_child(mesh_instance)
	return mesh_instance

func _material(color: Color, metallic: float, roughness: float, emission_color: Color = Color.BLACK, emission_energy: float = 0.0) -> StandardMaterial3D:
	var mat := StandardMaterial3D.new()
	mat.albedo_color = color
	mat.metallic = metallic
	mat.roughness = roughness
	if emission_energy > 0.0:
		mat.emission_enabled = true
		mat.emission = emission_color
		mat.emission_energy_multiplier = emission_energy
	return mat
