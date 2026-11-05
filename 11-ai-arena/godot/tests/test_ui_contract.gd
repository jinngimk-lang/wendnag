extends SceneTree

const MainScene = preload("res://scenes/main.tscn")

var _failed := false

func _initialize() -> void:
	call_deferred("_run")

func _run() -> void:
	var app = MainScene.instantiate()
	if app == null:
		push_error("Main scene failed to instantiate")
		quit(1)
		return
	app.use_imported_models = false
	root.add_child(app)
	var agent_button := app.find_child("Agent_value", true, false) as Button
	var mobile_button := app.find_child("MobileAgent_value", true, false) as Button
	var investor_button := app.find_child("InvestorPortfolioButton", true, false) as Button
	var mobile_investor_button := app.find_child("MobileInvestorButton", true, false) as Button
	var follow_button := app.find_child("FollowStrategyButton", true, false) as Button
	var challenge_button := app.find_child("ChallengeStrategyButton", true, false) as Button
	_check(agent_button != null, "desktop Agent button must be created")
	_check(mobile_button != null, "mobile Agent button must be created")
	_check(investor_button != null, "the seventh investor must have a desktop portfolio entry")
	_check(mobile_investor_button != null, "the seventh investor must have a mobile portfolio entry")
	_check(follow_button != null, "Agent detail must expose a follow action")
	_check(challenge_button != null, "Agent detail must expose an independent challenge action")
	if agent_button != null:
		_check(agent_button.get_theme_constant("icon_max_width") == 48, "desktop portrait icon width must use a theme override")
	if mobile_button != null:
		_check(mobile_button.get_theme_constant("icon_max_width") == 28, "mobile portrait icon width must use a theme override")
	_check(app.apply_responsive_layout(1600.0) == "desktop", "wide desktop layout must be selected")
	_check(app.apply_responsive_layout(1024.0) == "tablet", "tablet layout must be selected")
	_check(app.apply_responsive_layout(768.0) == "tablet", "small tablet layout must be selected")
	_check(app.apply_responsive_layout(390.0) == "mobile", "phone layout must be selected")
	_check(app.apply_responsive_layout(320.0) == "mobile", "minimum-width layout must be selected")
	_check(app.simulation.current_day == 0, "the UI must start on the opening market day")
	var setup_dialog := app.find_child("RunSetupDialog", true, false) as Window
	var scenario_input := app.find_child("ScenarioLabelInput", true, false) as LineEdit
	var days_input := app.find_child("TradingDaysInput", true, false) as SpinBox
	var risk_input := app.find_child("RiskCapInput", true, false) as HSlider
	_check(setup_dialog != null, "the run setup modal must exist")
	_check(scenario_input != null and days_input != null and risk_input != null, "run setup must expose scenario, days and risk controls")
	if scenario_input != null and days_input != null and risk_input != null:
		scenario_input.text = "UI CONTRACT SCENARIO"
		days_input.value = 120
		risk_input.value = 70
		var apply_setup := app.find_child("ApplyRunSetupButton", true, false) as Button
		_check(apply_setup != null, "run setup must expose an apply action")
		if apply_setup != null:
			apply_setup.emit_signal("pressed")
		_check(app.simulation.scenario_label == "UI CONTRACT SCENARIO", "run setup applies the scenario label")
		_check(app.simulation.trading_days == 120, "run setup applies the trading-day window")
		_check(is_equal_approx(app.simulation.risk_cap, 0.70), "run setup applies the shared risk cap")
	app.advance_one_day()
	_check(app.simulation.current_day == 1, "the Next Day action must advance the simulator once")
	app.enter_research_room("quant")
	_check(app.current_view == "room", "the Agent room action must change the visible workspace")
	_check(app.selected_agent == "quant", "the Agent room must retain the selected faction")
	app.return_to_arena()
	_check(app.current_view == "arena", "the back action must restore the arena view")
	app._on_investor_mode_requested("follow", "growth")
	_check(app.simulation.investor_mode == "follow", "follow action must activate the personal follow mode")
	_check(app.simulation.followed_agent_id == "growth", "follow action must retain the selected Agent")
	_check(app.selected_agent == "investor", "follow action must open the seventh investor portfolio")
	app._on_investor_mode_requested("challenge", "quant")
	_check(app.simulation.investor_mode == "challenge", "challenge action must switch to independent investing")
	_check(app.simulation.challenged_agent_id == "quant", "challenge action must retain the selected rival")
	app._on_investor_target_weight_changed(0.35)
	_check(is_equal_approx(app.simulation.investor_target_weight, 0.35), "the personal target-weight slider must update the investor policy")
	_check(app.find_child("InvestorSeatTitle", true, false) != null, "the 3D arena must include a dedicated seventh-investor seat")
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
