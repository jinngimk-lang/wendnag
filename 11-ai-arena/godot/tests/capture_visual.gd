extends SceneTree

const MainScene = preload("res://scenes/main.tscn")

var _failed := false

func _initialize() -> void:
	call_deferred("_capture")

func _capture() -> void:
	var app = MainScene.instantiate()
	if app == null:
		push_error("Visual QA could not instantiate the main scene")
		quit(1)
		return
	root.add_child(app)
	await process_frame
	await process_frame
	root.size = Vector2i(1600, 900)
	app.apply_responsive_layout(1600.0)
	await RenderingServer.frame_post_draw
	_save_capture("arena-desktop.png")

	app._on_investor_mode_requested("challenge", "growth")
	app._on_investor_target_weight_changed(0.65)
	await process_frame
	root.size = Vector2i(1600, 900)
	app.apply_responsive_layout(1600.0)
	await RenderingServer.frame_post_draw
	_save_capture("investor-desktop.png")

	root.size = Vector2i(390, 844)
	app.apply_responsive_layout(390.0)
	await process_frame
	await RenderingServer.frame_post_draw
	var detail_panel := app.find_child("DetailPanel", true, false) as Control
	if detail_panel != null:
		print("MOBILE DETAIL RECT: %s" % str(detail_panel.get_global_rect()))
	_save_capture("investor-mobile.png")

	if _failed:
		quit(1)
	else:
		print("AI ARENA VISUAL QA CAPTURE: PASS")
		quit(0)

func _save_capture(filename: String) -> void:
	var directory := ProjectSettings.globalize_path("res://visual-qa")
	var make_dir_error := DirAccess.make_dir_recursive_absolute(directory)
	if make_dir_error != OK and make_dir_error != ERR_ALREADY_EXISTS:
		_failed = true
		push_error("Could not create visual QA directory: %s" % error_string(make_dir_error))
		return
	var image := root.get_texture().get_image()
	if image == null or image.is_empty():
		_failed = true
		push_error("Visual QA viewport image is empty: " + filename)
		return
	var output_path := directory.path_join(filename)
	var save_error := image.save_png(output_path)
	if save_error != OK:
		_failed = true
		push_error("Could not save visual QA image: %s" % output_path)
		return
	print("VISUAL QA IMAGE: %s (%dx%d)" % [output_path, image.get_width(), image.get_height()])
