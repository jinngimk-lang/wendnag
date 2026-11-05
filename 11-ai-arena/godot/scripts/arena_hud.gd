extends CanvasLayer
class_name ArenaHUD

signal playback_requested(action: String)
signal agent_selected(agent_id: String)
signal room_requested(agent_id: String)
signal room_exit_requested
signal day_scrubbed(day: int)
signal export_requested
signal run_setup_requested
signal run_setup_confirmed(scenario_label: String, trading_days: int, starting_capital: float, risk_cap: float)
signal investor_mode_requested(mode: String, agent_id: String)
signal investor_target_weight_changed(weight: float)
signal investor_view_requested

const AgentCatalog = preload("res://scripts/agent_catalog.gd")
const CJK_FONT = preload("res://assets/fonts/NotoSansSC-Subset.otf")

var _simulator
var _selected_agent := "value"
var _status := "SYNTHETIC PAPER MODE"
var _active_tab := "research"
var _room_mode := false
var _updating_slider := false
var _root: Control
var _header: PanelContainer
var _agent_rail: PanelContainer
var _mobile_agents: PanelContainer
var _detail_panel: PanelContainer
var _bottom_dock: PanelContainer
var _agent_buttons: Dictionary = {}
var _mobile_buttons: Dictionary = {}
var _name_label: Label
var _role_label: Label
var _portrait: TextureRect
var _detail_body: RichTextLabel
var _equity_label: Label
var _return_label: Label
var _cash_label: Label
var _market_label: Label
var _status_label: Label
var _day_label: Label
var _slider: HSlider
var _room_button: Button
var _mobile_room_button: Button
var _tab_buttons: Dictionary = {}
var _market_box: VBoxContainer
var _status_box: VBoxContainer
var _brand_title: Label
var _brand_subtitle: Label
var _header_actions: VBoxContainer
var _header_portfolio_button: Button
var _header_setup_button: Button
var _investor_button: Button
var _mobile_investor_button: Button
var _follow_button: Button
var _challenge_button: Button
var _investor_controls: VBoxContainer
var _investor_target_slider: HSlider
var _investor_target_label: Label
var _updating_investor_slider := false
var _setup_dialog: Window
var _scenario_input: LineEdit
var _days_spin: SpinBox
var _capital_option: OptionButton
var _risk_slider: HSlider
var _risk_label: Label

func _ready() -> void:
	_build_ui()
	apply_responsive_layout(get_viewport().get_visible_rect().size.x)
	get_viewport().size_changed.connect(_on_viewport_size_changed)

static func layout_mode_for(width: float) -> String:
	if width >= 1120.0:
		return "desktop"
	if width >= 680.0:
		return "tablet"
	return "mobile"

func configure(simulator) -> void:
	_simulator = simulator

func update_view(simulator, selected_agent: String, status: String = "") -> void:
	_simulator = simulator
	_selected_agent = selected_agent
	if status != "":
		_status = status
	if _root == null or _simulator == null:
		return
	_refresh_header()
	_refresh_agent_cards()
	_refresh_detail()
	_refresh_replay()

func set_status(message: String) -> void:
	_status = message
	if _status_label != null:
		_status_label.text = message

func set_room_mode(enabled: bool, agent_id: String = "") -> void:
	_room_mode = enabled
	if agent_id != "":
		_selected_agent = agent_id
	if _room_button != null:
		_room_button.visible = _selected_agent != "investor"
	if _mobile_room_button != null:
		_mobile_room_button.visible = _selected_agent != "investor"
	if _room_button != null:
		_room_button.text = "← 返回竞技场" if enabled else "进入研究室  ↗"
	if _mobile_room_button != null:
		_mobile_room_button.text = "← 返回竞技场" if enabled else "进入研究室 ↗"
	_refresh_detail()

func apply_responsive_layout(width: float) -> String:
	var mode := layout_mode_for(width)
	set_meta("layout_mode", mode)
	var compact_tablet := mode == "tablet" and width < 920.0
	if _agent_rail != null:
		_agent_rail.visible = mode == "desktop" or (mode == "tablet" and not compact_tablet)
		_agent_rail.offset_right = 210.0 if mode == "tablet" else 284.0
	if _detail_panel != null:
		_detail_panel.visible = mode != "mobile"
		_detail_panel.offset_left = -292.0 if mode == "tablet" else -370.0
		if mode == "mobile":
			_detail_panel.visible = true
			_detail_panel.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
			_detail_panel.offset_left = 12.0
			_detail_panel.offset_right = -12.0
			_detail_panel.offset_top = -390.0
			_detail_panel.offset_bottom = -150.0
			_detail_panel.custom_minimum_size = Vector2.ZERO
		else:
			_detail_panel.set_anchors_preset(Control.PRESET_RIGHT_WIDE)
			_detail_panel.offset_top = 108.0 if mode == "desktop" else 102.0
			_detail_panel.offset_bottom = -128.0
	if _portrait != null:
		_portrait.visible = mode != "mobile" and _selected_agent != "investor"
	if _role_label != null:
		_role_label.visible = mode != "mobile" and _selected_agent != "investor"
	if _name_label != null:
		_name_label.add_theme_font_size_override("font_size", 18 if mode == "mobile" else 23)
	if _detail_body != null:
		_detail_body.custom_minimum_size = Vector2(0, 110 if mode == "mobile" else 220)
	if _mobile_agents != null:
		_mobile_agents.visible = mode == "mobile" or compact_tablet
	if _bottom_dock != null:
		_bottom_dock.offset_top = -142.0 if mode == "mobile" else -108.0
	if _header != null:
		_header.offset_bottom = 76.0
	if _brand_title != null:
		_brand_title.add_theme_font_size_override("font_size", 15 if mode == "mobile" else 19)
	if _brand_subtitle != null:
		_brand_subtitle.visible = mode != "mobile"
	if _header_actions != null:
		_header_actions.custom_minimum_size = Vector2(88 if mode == "mobile" else 112, 0)
	if _header_portfolio_button != null:
		_header_portfolio_button.custom_minimum_size = Vector2(82 if mode == "mobile" else 104, 24 if mode == "mobile" else 28)
		_header_portfolio_button.add_theme_font_size_override("font_size", 10 if mode == "mobile" else 14)
	if _header_setup_button != null:
		_header_setup_button.custom_minimum_size = Vector2(82 if mode == "mobile" else 104, 24 if mode == "mobile" else 28)
		_header_setup_button.add_theme_font_size_override("font_size", 10 if mode == "mobile" else 14)
	if _market_box != null:
		_market_box.visible = mode != "mobile"
	if _status_box != null:
		_status_box.visible = mode != "mobile"
	if _mobile_agents != null:
		_mobile_agents.offset_top = 108.0
		_mobile_agents.offset_bottom = 180.0
	if _agent_rail != null and mode == "tablet":
		_agent_rail.offset_top = 102.0
	return mode

func _on_viewport_size_changed() -> void:
	apply_responsive_layout(get_viewport().get_visible_rect().size.x)

func _build_ui() -> void:
	_root = Control.new()
	_root.name = "HUDRoot"
	_root.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_root.mouse_filter = Control.MOUSE_FILTER_PASS
	var hud_theme := Theme.new()
	hud_theme.default_font = CJK_FONT
	hud_theme.default_font_size = 14
	_root.theme = hud_theme
	add_child(_root)
	_build_header()
	_build_agent_rail()
	_build_mobile_agents()
	_build_detail_panel()
	_build_bottom_dock()
	_build_run_setup_dialog()

func _build_header() -> void:
	_header = _panel("Header")
	_header.set_anchors_preset(Control.PRESET_TOP_WIDE)
	_header.offset_left = 20
	_header.offset_right = -20
	_header.offset_top = 16
	_header.offset_bottom = 92
	_root.add_child(_header)
	var row := HBoxContainer.new()
	row.add_theme_constant_override("separation", 18)
	_header.add_child(row)
	var brand := VBoxContainer.new()
	brand.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	row.add_child(brand)
	_brand_title = _label("AI  /  INVESTMENT ARENA", 19, Color("#f0d6a8"), true)
	_brand_title.name = "BrandTitle"
	brand.add_child(_brand_title)
	_brand_subtitle = _label("SIX AI MANAGERS  ·  YOUR SEVENTH SEAT  ·  ONE MARKET", 10, Color("#8fa2b2"))
	_brand_subtitle.name = "BrandSubtitle"
	brand.add_child(_brand_subtitle)
	_market_box = VBoxContainer.new()
	_market_box.custom_minimum_size = Vector2(220, 0)
	_market_box.alignment = BoxContainer.ALIGNMENT_CENTER
	_market_box.add_child(_label("SHARED MARKET  /  PAPER MODE", 10, Color("#8fa2b2")))
	_market_label = _label("INDEX  100.00   ·   VOL  1.8%", 14, Color("#dce7ed"), true)
	_market_box.add_child(_market_label)
	row.add_child(_market_box)
	_status_box = VBoxContainer.new()
	_status_box.custom_minimum_size = Vector2(145, 0)
	_status_box.alignment = BoxContainer.ALIGNMENT_CENTER
	_status_box.add_child(_label("ENGINE STATUS", 10, Color("#8fa2b2")))
	_status_label = _label(_status, 12, Color("#8de0b2"), true)
	_status_box.add_child(_status_label)
	row.add_child(_status_box)
	_header_actions = VBoxContainer.new()
	_header_actions.custom_minimum_size = Vector2(112, 0)
	_header_actions.alignment = BoxContainer.ALIGNMENT_CENTER
	_header_portfolio_button = Button.new()
	_header_portfolio_button.name = "HeaderInvestorButton"
	_header_portfolio_button.text = "我的组合"
	_header_portfolio_button.custom_minimum_size = Vector2(104, 28)
	_header_portfolio_button.pressed.connect(func(): investor_view_requested.emit())
	_header_actions.add_child(_header_portfolio_button)
	_header_setup_button = Button.new()
	_header_setup_button.name = "RunSetupButton"
	_header_setup_button.text = "配置实验"
	_header_setup_button.custom_minimum_size = Vector2(104, 28)
	_header_setup_button.pressed.connect(func(): run_setup_requested.emit())
	_header_actions.add_child(_header_setup_button)
	row.add_child(_header_actions)

func _build_agent_rail() -> void:
	_agent_rail = _panel("AgentRail")
	_agent_rail.set_anchors_preset(Control.PRESET_LEFT_WIDE)
	_agent_rail.offset_left = 20
	_agent_rail.offset_right = 304
	_agent_rail.offset_top = 108
	_agent_rail.offset_bottom = -128
	_root.add_child(_agent_rail)
	var scroll := ScrollContainer.new()
	scroll.name = "AgentRailScroll"
	scroll.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
	_agent_rail.add_child(scroll)
	var column := VBoxContainer.new()
	column.add_theme_constant_override("separation", 8)
	column.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	scroll.add_child(column)
	column.add_child(_label("STRATEGY TEAMS", 12, Color("#aab9c5"), true))
	column.add_child(_label("Select an Agent to inspect its account", 10, Color("#7e93a3")))
	for faction in AgentCatalog.all():
		var agent_id := str(faction.id)
		var button := Button.new()
		button.name = "Agent_" + agent_id
		button.custom_minimum_size = Vector2(0, 68)
		button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		button.alignment = HORIZONTAL_ALIGNMENT_LEFT
		button.icon = AgentCatalog.portrait_texture(agent_id)
		button.add_theme_constant_override("icon_max_width", 48)
		button.expand_icon = true
		button.text = "%s   %s\n%s" % [str(faction.get("english", "")), str(faction.get("name", "")), str(faction.get("analyst", ""))]
		button.add_theme_font_size_override("font_size", 11)
		button.add_theme_color_override("font_color", Color("#dce6eb"))
		button.pressed.connect(_on_agent_pressed.bind(agent_id))
		column.add_child(button)
		_agent_buttons[agent_id] = button
	_investor_button = Button.new()
	_investor_button.name = "InvestorPortfolioButton"
	_investor_button.custom_minimum_size = Vector2(0, 58)
	_investor_button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_investor_button.text = "第七位投资者 · 我的组合\n$100,000   +0.00%"
	_investor_button.pressed.connect(func(): investor_view_requested.emit())
	_investor_button.add_theme_color_override("font_color", Color("#f1d19b"))
	column.add_child(_investor_button)

func _build_mobile_agents() -> void:
	_mobile_agents = _panel("MobileAgents")
	_mobile_agents.set_anchors_preset(Control.PRESET_TOP_WIDE)
	_mobile_agents.offset_left = 12
	_mobile_agents.offset_right = -12
	_mobile_agents.offset_top = 94
	_mobile_agents.offset_bottom = 168
	_root.add_child(_mobile_agents)
	var scroll := ScrollContainer.new()
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_AUTO
	scroll.vertical_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	_mobile_agents.add_child(scroll)
	var row := HBoxContainer.new()
	row.add_theme_constant_override("separation", 7)
	scroll.add_child(row)
	for faction in AgentCatalog.all():
		var agent_id := str(faction.id)
		var button := Button.new()
		button.name = "MobileAgent_" + agent_id
		button.custom_minimum_size = Vector2(108, 52)
		button.icon = AgentCatalog.portrait_texture(agent_id)
		button.add_theme_constant_override("icon_max_width", 28)
		button.expand_icon = true
		button.text = str(faction.get("name", agent_id))
		button.pressed.connect(_on_agent_pressed.bind(agent_id))
		row.add_child(button)
		_mobile_buttons[agent_id] = button
	_mobile_investor_button = Button.new()
	_mobile_investor_button.name = "MobileInvestorButton"
	_mobile_investor_button.custom_minimum_size = Vector2(116, 52)
	_mobile_investor_button.text = "我的组合\n+0.0%"
	_mobile_investor_button.pressed.connect(func(): investor_view_requested.emit())
	row.add_child(_mobile_investor_button)
	_mobile_room_button = Button.new()
	_mobile_room_button.name = "MobileRoomButton"
	_mobile_room_button.custom_minimum_size = Vector2(132, 52)
	_mobile_room_button.text = "进入研究室 ↗"
	_mobile_room_button.pressed.connect(_on_room_button_pressed)
	row.add_child(_mobile_room_button)

func _build_detail_panel() -> void:
	_detail_panel = _panel("DetailPanel")
	_detail_panel.set_anchors_preset(Control.PRESET_RIGHT_WIDE)
	_detail_panel.offset_left = -370
	_detail_panel.offset_right = -20
	_detail_panel.offset_top = 108
	_detail_panel.offset_bottom = -128
	_root.add_child(_detail_panel)
	var scroll := ScrollContainer.new()
	scroll.name = "DetailScroll"
	scroll.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
	_detail_panel.add_child(scroll)
	var column := VBoxContainer.new()
	column.add_theme_constant_override("separation", 8)
	column.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	scroll.add_child(column)
	_portrait = TextureRect.new()
	_portrait.name = "AgentPortrait"
	_portrait.custom_minimum_size = Vector2(0, 152)
	_portrait.expand_mode = TextureRect.EXPAND_FIT_WIDTH_PROPORTIONAL
	_portrait.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
	column.add_child(_portrait)
	_name_label = _label("价值派", 23, Color("#f2d7a5"), true)
	column.add_child(_name_label)
	_role_label = _label("资深价值投资经理", 11, Color("#91a5b4"))
	column.add_child(_role_label)
	var metrics := GridContainer.new()
	metrics.columns = 2
	metrics.add_theme_constant_override("h_separation", 8)
	metrics.add_theme_constant_override("v_separation", 6)
	column.add_child(metrics)
	_equity_label = _metric_card(metrics, "账户净值", "$100,000")
	_return_label = _metric_card(metrics, "累计收益", "+0.00%")
	_cash_label = _metric_card(metrics, "可用现金", "$100,000")
	_metric_card(metrics, "市场模式", "SYNTHETIC")
	var tabs := HBoxContainer.new()
	tabs.add_theme_constant_override("separation", 5)
	column.add_child(tabs)
	for tab in ["research", "account", "ledger"]:
		var label := "研究" if tab == "research" else "账户" if tab == "account" else "交易"
		var button := Button.new()
		button.text = label
		button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		button.pressed.connect(_on_tab_pressed.bind(tab))
		tabs.add_child(button)
		_tab_buttons[tab] = button
	_detail_body = RichTextLabel.new()
	_detail_body.name = "DetailBody"
	_detail_body.bbcode_enabled = false
	_detail_body.fit_content = true
	_detail_body.scroll_active = false
	_detail_body.custom_minimum_size = Vector2(0, 220)
	_detail_body.add_theme_color_override("default_color", Color("#c4d0d8"))
	_detail_body.add_theme_font_size_override("normal_font_size", 12)
	column.add_child(_detail_body)
	var investor_actions := HBoxContainer.new()
	investor_actions.name = "InvestorActions"
	investor_actions.add_theme_constant_override("separation", 6)
	_follow_button = Button.new()
	_follow_button.name = "FollowStrategyButton"
	_follow_button.text = "跟随策略 +"
	_follow_button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_follow_button.pressed.connect(_on_follow_pressed)
	investor_actions.add_child(_follow_button)
	_challenge_button = Button.new()
	_challenge_button.name = "ChallengeStrategyButton"
	_challenge_button.text = "亲自挑战"
	_challenge_button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_challenge_button.pressed.connect(_on_challenge_pressed)
	investor_actions.add_child(_challenge_button)
	column.add_child(investor_actions)
	_investor_controls = VBoxContainer.new()
	_investor_controls.name = "InvestorControls"
	_investor_controls.add_theme_constant_override("separation", 4)
	_investor_controls.visible = false
	_investor_controls.add_child(_label("自主挑战 · 目标股票仓位", 10, Color("#c9b17e"), true))
	_investor_target_label = _label("目标仓位 50%", 12, Color("#f1d19b"), true)
	_investor_controls.add_child(_investor_target_label)
	_investor_target_slider = HSlider.new()
	_investor_target_slider.name = "InvestorTargetWeightSlider"
	_investor_target_slider.min_value = 0.0
	_investor_target_slider.max_value = 0.90
	_investor_target_slider.step = 0.05
	_investor_target_slider.value = 0.50
	_investor_target_slider.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_investor_target_slider.value_changed.connect(_on_investor_target_changed)
	_investor_controls.add_child(_investor_target_slider)
	column.add_child(_investor_controls)
	_room_button = Button.new()
	_room_button.text = "进入研究室  ↗"
	_room_button.custom_minimum_size = Vector2(0, 42)
	_room_button.pressed.connect(_on_room_button_pressed)
	column.add_child(_room_button)

func _build_bottom_dock() -> void:
	_bottom_dock = _panel("BottomDock")
	_bottom_dock.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	_bottom_dock.offset_left = 20
	_bottom_dock.offset_right = -20
	_bottom_dock.offset_top = -108
	_bottom_dock.offset_bottom = -16
	_root.add_child(_bottom_dock)
	var column := VBoxContainer.new()
	column.add_theme_constant_override("separation", 5)
	_bottom_dock.add_child(column)
	var controls_scroll := ScrollContainer.new()
	controls_scroll.name = "PlaybackControlsScroll"
	controls_scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_AUTO
	controls_scroll.vertical_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	controls_scroll.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	controls_scroll.custom_minimum_size = Vector2(0, 34)
	column.add_child(controls_scroll)
	var controls := HBoxContainer.new()
	controls.name = "PlaybackControlsRow"
	controls.custom_minimum_size = Vector2(650, 0)
	controls.add_theme_constant_override("separation", 6)
	controls_scroll.add_child(controls)
	_action_button(controls, "▶ 运行", "play")
	_action_button(controls, "Ⅱ 暂停", "pause")
	_action_button(controls, "下一日", "next")
	_action_button(controls, "+5 日", "next5")
	_action_button(controls, "结算", "finish")
	_action_button(controls, "重置", "reset")
	var export_button := Button.new()
	export_button.text = "导出 JSON"
	export_button.pressed.connect(func(): export_requested.emit())
	controls.add_child(export_button)
	_day_label = _label("DAY 000 / 090", 10, Color("#9eb0bd"), true)
	column.add_child(_day_label)
	_slider = HSlider.new()
	_slider.name = "ReplaySlider"
	_slider.min_value = 0
	_slider.max_value = 1
	_slider.step = 1
	_slider.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_slider.value_changed.connect(_on_slider_changed)
	column.add_child(_slider)

func _build_run_setup_dialog() -> void:
	_setup_dialog = Window.new()
	_setup_dialog.name = "RunSetupDialog"
	_setup_dialog.title = "配置本轮模拟实验"
	_setup_dialog.size = Vector2i(520, 500)
	_setup_dialog.min_size = Vector2i(460, 460)
	_setup_dialog.transient = true
	_setup_dialog.exclusive = true
	_setup_dialog.unresizable = true
	_setup_dialog.close_requested.connect(func(): _setup_dialog.hide())
	_setup_dialog.visible = false
	_setup_dialog.theme = _root.theme
	add_child(_setup_dialog)
	var panel := PanelContainer.new()
	panel.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	var style := StyleBoxFlat.new()
	style.bg_color = Color("#0b1520")
	style.border_color = Color("#596d79")
	style.set_border_width_all(1)
	style.set_corner_radius_all(12)
	style.content_margin_left = 22
	style.content_margin_right = 22
	style.content_margin_top = 18
	style.content_margin_bottom = 18
	panel.add_theme_stylebox_override("panel", style)
	_setup_dialog.add_child(panel)
	var column := VBoxContainer.new()
	column.add_theme_constant_override("separation", 10)
	panel.add_child(column)
	column.add_child(_label("RUN CONFIGURATION  /  PAPER SIMULATION", 11, Color("#e9c78d"), true))
	column.add_child(_label("所有价格、事件与收益均为合成演示数据；场景名称只用于标注，不会触发真实公司研究。", 10, Color("#8fa2b2")))
	column.add_child(_label("模拟场景名称", 10, Color("#c4d0d8"), true))
	_scenario_input = LineEdit.new()
	_scenario_input.name = "ScenarioLabelInput"
	_scenario_input.placeholder_text = "例如：SYNTHETIC MARKET"
	_scenario_input.text = "SYNTHETIC MARKET"
	column.add_child(_scenario_input)
	column.add_child(_label("交易日窗口  /  20–252", 10, Color("#c4d0d8"), true))
	_days_spin = SpinBox.new()
	_days_spin.name = "TradingDaysInput"
	_days_spin.min_value = 20
	_days_spin.max_value = 252
	_days_spin.step = 1
	_days_spin.value = 90
	column.add_child(_days_spin)
	column.add_child(_label("起始资金  /  七个账户相同", 10, Color("#c4d0d8"), true))
	_capital_option = OptionButton.new()
	_capital_option.name = "StartingCapitalInput"
	for amount in [50000, 100000, 250000, 500000]:
		_capital_option.add_item("$%s" % _money_grouped(float(amount)))
		_capital_option.set_item_metadata(_capital_option.item_count - 1, float(amount))
	_capital_option.select(1)
	column.add_child(_capital_option)
	column.add_child(_label("统一风险上限  /  同时作用于六位 Agent 与个人账户", 10, Color("#c4d0d8"), true))
	_risk_label = _label("最大股票仓位 90%", 12, Color("#f1d19b"), true)
	column.add_child(_risk_label)
	_risk_slider = HSlider.new()
	_risk_slider.name = "RiskCapInput"
	_risk_slider.min_value = 10
	_risk_slider.max_value = 90
	_risk_slider.step = 5
	_risk_slider.value = 90
	_risk_slider.value_changed.connect(func(value: float): _risk_label.text = "最大股票仓位 %.0f%%" % value)
	column.add_child(_risk_slider)
	var note := _label("第七位投资者拥有独立的个人模拟账户。跟随会同步所选 Agent 的目标仓位；自主挑战使用个人目标仓位。七个账户共享同一合成市场、费用与风险上限。", 10, Color("#91a5b4"))
	column.add_child(note)
	var spacer := Control.new()
	spacer.size_flags_vertical = Control.SIZE_EXPAND_FILL
	column.add_child(spacer)
	var buttons := HBoxContainer.new()
	buttons.alignment = BoxContainer.ALIGNMENT_END
	buttons.add_theme_constant_override("separation", 8)
	var cancel := Button.new()
	cancel.text = "取消"
	cancel.pressed.connect(func(): _setup_dialog.hide())
	buttons.add_child(cancel)
	var apply := Button.new()
	apply.name = "ApplyRunSetupButton"
	apply.text = "应用配置并重置"
	apply.pressed.connect(_on_setup_apply_pressed)
	buttons.add_child(apply)
	column.add_child(buttons)

func open_run_setup(simulator) -> void:
	if simulator != null:
		_scenario_input.text = str(simulator.scenario_label)
		_days_spin.value = int(simulator.trading_days)
		_risk_slider.value = float(simulator.risk_cap) * 100.0
		for index in range(_capital_option.item_count):
			if is_equal_approx(float(_capital_option.get_item_metadata(index)), float(simulator.starting_capital)):
				_capital_option.select(index)
				break
	_setup_dialog.popup_centered()

func _on_setup_apply_pressed() -> void:
	var label := _scenario_input.text.strip_edges()
	if label.is_empty():
		label = "SYNTHETIC MARKET"
	var capital := float(_capital_option.get_item_metadata(_capital_option.selected))
	var days := int(_days_spin.value)
	var risk := float(_risk_slider.value) / 100.0
	_setup_dialog.hide()
	run_setup_confirmed.emit(label, days, capital, risk)

func _action_button(parent: Control, caption: String, action: String) -> void:
	var button := Button.new()
	button.text = caption
	button.custom_minimum_size = Vector2(0, 30)
	button.pressed.connect(func(): playback_requested.emit(action))
	parent.add_child(button)

func _metric_card(parent: Control, caption: String, value: String) -> Label:
	var box := PanelContainer.new()
	box.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	parent.add_child(box)
	var column := VBoxContainer.new()
	box.add_child(column)
	column.add_child(_label(caption, 9, Color("#8fa4b3")))
	var value_label := _label(value, 13, Color("#edf3f6"), true)
	column.add_child(value_label)
	return value_label

func _panel(node_name: String) -> PanelContainer:
	var panel := PanelContainer.new()
	panel.name = node_name
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.025, 0.047, 0.065, 0.92)
	style.border_color = Color("#425969")
	style.set_border_width_all(1)
	style.set_corner_radius_all(12)
	style.content_margin_left = 12
	style.content_margin_right = 12
	style.content_margin_top = 9
	style.content_margin_bottom = 9
	panel.add_theme_stylebox_override("panel", style)
	return panel

func _label(value: String, size: int, color: Color, strong: bool = false) -> Label:
	var label := Label.new()
	label.text = value
	label.add_theme_font_size_override("font_size", size)
	label.add_theme_color_override("font_color", color)
	if strong:
		label.add_theme_color_override("font_shadow_color", Color(0, 0, 0, 0.24))
	label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	return label

func _refresh_header() -> void:
	var day := int(_simulator.replay_day)
	var context: Dictionary = _simulator.market_context[day]
	_market_label.text = "INDEX  %.2f   ·   VOL  %.1f%%   ·   SENTIMENT %+.2f" % [float(context.price), float(context.volatility) * 100.0, float(context.sentiment)]
	_status_label.text = _status

func _refresh_agent_cards() -> void:
	var rankings: Array = _simulator.get_rankings(_simulator.replay_day)
	var rank_map: Dictionary = {}
	for row in rankings:
		rank_map[str(row.agent_id)] = row
	for agent_id in _agent_buttons:
		var snapshot: Dictionary = _simulator.get_account_snapshot(str(agent_id), _simulator.replay_day)
		var row: Dictionary = rank_map.get(agent_id, {})
		var change := float(snapshot.get("cumulative_return_pct", 0.0))
		var rank := int(row.get("rank", 0))
		var faction := AgentCatalog.get_faction(str(agent_id))
		var caption := "%s   %s\n$%s   %+.2f%%   ·   #%d" % [
			str(faction.get("name", agent_id)),
			str(faction.get("analyst", "")),
			_format_money(float(snapshot.get("equity", 0.0))),
			change,
			rank
		]
		(_agent_buttons[agent_id] as Button).text = caption
		(_mobile_buttons[agent_id] as Button).text = str(faction.get("name", agent_id)) + "\n" + ("%+.1f%%" % change)
	var investor_snapshot: Dictionary = _simulator.get_account_snapshot("investor", _simulator.replay_day)
	var investor_rank: Dictionary = rank_map.get("investor", {})
	var investor_return := float(investor_snapshot.get("cumulative_return_pct", 0.0))
	var investor_equity := float(investor_snapshot.get("equity", _simulator.starting_capital))
	_investor_button.text = "第七位投资者 · 我的组合\n#%d  $%s   %+.2f%%" % [int(investor_rank.get("rank", 7)), _format_money(investor_equity), investor_return]
	_mobile_investor_button.text = "我的组合\n#%d  %+.1f%%" % [int(investor_rank.get("rank", 7)), investor_return]

func _refresh_detail() -> void:
	if _selected_agent == "investor":
		_refresh_investor_detail()
		return
	var faction := AgentCatalog.get_faction(_selected_agent)
	if faction.is_empty():
		return
	var snapshot: Dictionary = _simulator.get_account_snapshot(_selected_agent, _simulator.replay_day)
	_portrait.visible = true
	_portrait.texture = AgentCatalog.portrait_texture(_selected_agent)
	_name_label.text = str(faction.get("name", "Agent"))
	_role_label.text = "%s  ·  %s" % [str(faction.get("role", "")), str(faction.get("analyst", ""))]
	_equity_label.text = "$" + _format_money(float(snapshot.get("equity", 0.0)))
	_return_label.text = "%+.2f%%" % float(snapshot.get("cumulative_return_pct", 0.0))
	_cash_label.text = "$" + _format_money(float(snapshot.get("cash", 0.0)))
	for tab in _tab_buttons:
		var button := _tab_buttons[tab] as Button
		button.modulate = Color("#f1d19b") if tab == _active_tab else Color("#d1dce2")
	_detail_body.text = _detail_text(faction, snapshot)
	_follow_button.visible = true
	_challenge_button.visible = true
	_investor_controls.visible = false
	_room_button.visible = true
	_mobile_room_button.visible = true
	_room_button.text = "← 返回竞技场" if _room_mode else "进入研究室  ↗"
	if _simulator != null and str(_simulator.investor_mode) == "follow" and str(_simulator.followed_agent_id) == _selected_agent:
		_follow_button.text = "正在跟随 ✓"
	else:
		_follow_button.text = "跟随策略 +"
	if _simulator != null and str(_simulator.investor_mode) == "challenge" and str(_simulator.challenged_agent_id) == _selected_agent:
		_challenge_button.text = "正在挑战 ✓"
	else:
		_challenge_button.text = "亲自挑战"

func _refresh_investor_detail() -> void:
	if _simulator == null:
		return
	var snapshot: Dictionary = _simulator.get_account_snapshot("investor", _simulator.replay_day)
	_portrait.visible = false
	_name_label.text = "你 · 第七位投资者"
	_role_label.text = "独立个人模拟账户  ·  与六位 AI 经理同场比较"
	_equity_label.text = "$" + _format_money(float(snapshot.get("equity", _simulator.starting_capital)))
	_return_label.text = "%+.2f%%" % float(snapshot.get("cumulative_return_pct", 0.0))
	_cash_label.text = "$" + _format_money(float(snapshot.get("cash", _simulator.starting_capital)))
	for tab in _tab_buttons:
		var button := _tab_buttons[tab] as Button
		button.modulate = Color("#f1d19b") if tab == _active_tab else Color("#d1dce2")
	var mode := str(_simulator.investor_mode)
	var followed := str(_simulator.followed_agent_id)
	var challenged := str(_simulator.challenged_agent_id)
	var mode_line := "自主挑战 · 对比 %s" % str(AgentCatalog.get_faction(challenged).get("name", challenged)) if mode == "challenge" else "跟随策略 · %s" % str(AgentCatalog.get_faction(followed).get("name", followed))
	var lines := PackedStringArray()
	if _active_tab == "ledger":
		lines.append("我的交易记录  /  已回放至 DAY %03d" % int(snapshot.get("day", 0)))
		lines.append("")
		var ledger: Array = _simulator.investor_account.ledger
		var visible_count := mini(ledger.size(), int(_simulator.replay_day))
		var start := maxi(0, visible_count - 10)
		if visible_count == 0:
			lines.append("当前回放位置尚无已完成交易。")
		else:
			for index in range(start, visible_count):
				var entry: Dictionary = ledger[index]
				lines.append("DAY %03d   %s   $%s   %+.2f%%" % [int(entry.day), str(entry.action), _format_money(float(entry.notional)), float(entry.delta_equity) / maxf(float(_simulator.starting_capital), 1.0) * 100.0])
				lines.append("  " + str(entry.reason))
	elif _active_tab == "account":
		lines.append("个人账户状态  /  DAY %03d" % int(snapshot.get("day", 0)))
		lines.append("")
		lines.append("账户净值      $%s" % _format_money(float(snapshot.get("equity", 0.0))))
		lines.append("可用现金      $%s" % _format_money(float(snapshot.get("cash", 0.0))))
		lines.append("持有份额      %.3f" % float(snapshot.get("shares", 0.0)))
		lines.append("实际敞口      %.1f%%" % float(snapshot.get("exposure_pct", 0.0)))
		lines.append("目标仓位      %.1f%%" % (float(snapshot.get("target_weight", 0.0)) * 100.0))
		lines.append("最大回撤      %.2f%%" % float(snapshot.get("max_drawdown_pct", 0.0)))
		lines.append("年化波动      %.2f%%" % float(snapshot.get("volatility_pct", 0.0)))
		lines.append("")
		lines.append("当前模式：%s" % mode_line)
		lines.append("统一风险上限：%.0f%%" % (float(_simulator.risk_cap) * 100.0))
	else:
		lines = PackedStringArray([
			"第七位投资者  /  %s" % mode_line,
			"模拟场景：%s" % str(_simulator.scenario_label),
			"",
			"账户净值      $%s" % _format_money(float(snapshot.get("equity", 0.0))),
			"可用现金      $%s" % _format_money(float(snapshot.get("cash", 0.0))),
			"持有份额      %.3f" % float(snapshot.get("shares", 0.0)),
			"累计收益      %+.2f%%" % float(snapshot.get("cumulative_return_pct", 0.0)),
			"最大回撤      %.2f%%" % float(snapshot.get("max_drawdown_pct", 0.0)),
			"统一风险上限  %.0f%%" % (float(_simulator.risk_cap) * 100.0),
			"",
			"最近决策：%s" % str(snapshot.get("last_decision", "HOLD")),
			str(snapshot.get("last_reason", "等待首个市场交易日。")),
			"",
			"七席排名  /  风险调整分"
		])
		for row in _simulator.get_rankings(_simulator.replay_day):
			lines.append("#%d  %s  %+.2f%%  ·  回撤 %.2f%%" % [int(row.rank), str(row.name), float(row.return_pct), float(row.drawdown_pct)])
	_detail_body.text = "\n".join(lines)
	_follow_button.visible = false
	_challenge_button.visible = false
	_investor_controls.visible = mode == "challenge"
	_updating_investor_slider = true
	_investor_target_slider.max_value = float(_simulator.risk_cap)
	_investor_target_slider.value = minf(float(_simulator.investor_target_weight), float(_simulator.risk_cap))
	_investor_target_label.text = "个人目标仓位  %.0f%%" % (_investor_target_slider.value * 100.0)
	_updating_investor_slider = false
	_room_button.visible = false
	_mobile_room_button.visible = false

func _detail_text(faction: Dictionary, snapshot: Dictionary) -> String:
	match _active_tab:
		"account":
			return "账户状态  /  DAY %03d\n\n账户净值      $%s\n可用现金      $%s\n持有份额      %.3f\n目标敞口      %.1f%%\n最大回撤      %.2f%%\n年化波动      %.2f%%\n\n最近决策：%s\n%s" % [
				int(snapshot.get("day", 0)),
				_format_money(float(snapshot.get("equity", 0.0))),
				_format_money(float(snapshot.get("cash", 0.0))),
				float(snapshot.get("shares", 0.0)),
				float(snapshot.get("exposure_pct", 0.0)),
				float(snapshot.get("max_drawdown_pct", 0.0)),
				float(snapshot.get("volatility_pct", 0.0)),
				str(snapshot.get("last_decision", "HOLD")),
				str(snapshot.get("last_reason", ""))
			]
		"ledger":
			var lines := PackedStringArray(["最近交易记录  /  已回放至 DAY %03d" % int(snapshot.get("day", 0)), ""])
			var ledger: Array = _simulator.accounts[_selected_agent].ledger
			var visible_count := mini(ledger.size(), int(_simulator.replay_day))
			var start := maxi(0, visible_count - 8)
			if visible_count == 0:
				lines.append("当前回放位置尚无已完成交易。")
			else:
				for index in range(start, visible_count):
					var entry: Dictionary = ledger[index]
					lines.append("DAY %03d   %s   $%s   %+.2f%%" % [
						int(entry.day),
						str(entry.action),
						_format_money(float(entry.notional)),
						float(entry.delta_equity) / maxf(float(_simulator.starting_capital), 1.0) * 100.0
					])
					lines.append("  " + str(entry.reason))
			return "\n".join(lines)
		_:
			return "投资方法  /  %s\n\n%s\n\n核心论点\n%s\n\n反方挑战\n%s\n\n风险官\n%s\n\n关注信号\n%s\n\n%s" % [
				str(faction.get("english", "")),
				str(faction.get("strategy", "")),
				str(faction.get("thesis", "")),
				str(faction.get("bear", "")),
				str(faction.get("risk", "")),
				str(faction.get("signal", "")),
				str(faction.get("quote", ""))
			]

func _refresh_replay() -> void:
	var day := int(_simulator.replay_day)
	var total := int(_simulator.trading_days)
	_day_label.text = "REPLAY  ·  DAY %03d / %03d   ·   %s" % [day, total, "LIVE EDGE" if day == int(_simulator.current_day) else "HISTORY"]
	_updating_slider = true
	_slider.max_value = maxi(1, int(_simulator.current_day))
	_slider.value = day
	_updating_slider = false

func _on_agent_pressed(agent_id: String) -> void:
	_selected_agent = agent_id
	_active_tab = "research"
	agent_selected.emit(agent_id)
	_refresh_detail()

func _on_follow_pressed() -> void:
	if _selected_agent != "investor":
		investor_mode_requested.emit("follow", _selected_agent)

func _on_challenge_pressed() -> void:
	if _selected_agent != "investor":
		investor_mode_requested.emit("challenge", _selected_agent)

func _on_investor_target_changed(value: float) -> void:
	if _updating_investor_slider:
		return
	_investor_target_label.text = "个人目标仓位  %.0f%%" % (value * 100.0)
	investor_target_weight_changed.emit(value)

func _on_tab_pressed(tab: String) -> void:
	_active_tab = tab
	_refresh_detail()

func _on_room_button_pressed() -> void:
	if _room_mode:
		_room_mode = false
		room_exit_requested.emit()
	else:
		_room_mode = true
		room_requested.emit(_selected_agent)
	_room_button.text = "← 返回竞技场" if _room_mode else "进入研究室  ↗"
	if _mobile_room_button != null:
		_mobile_room_button.text = "← 返回竞技场" if _room_mode else "进入研究室 ↗"

func _on_slider_changed(value: float) -> void:
	if not _updating_slider:
		day_scrubbed.emit(int(value))

func _format_money(value: float) -> String:
	return _money_grouped(value)

func _money_grouped(value: float) -> String:
	var raw := String.num(absf(value), 2)
	var parts := raw.split(".")
	var whole := str(parts[0])
	var grouped := ""
	for index in range(whole.length()):
		if index > 0 and (whole.length() - index) % 3 == 0:
			grouped += ","
		grouped += whole[index]
	return ("-" if value < 0.0 else "") + grouped + "." + (str(parts[1]) if parts.size() > 1 else "00")
