extends CanvasLayer
class_name ArenaHUD

signal playback_requested(action: String)
signal agent_selected(agent_id: String)
signal room_requested(agent_id: String)
signal room_exit_requested
signal day_scrubbed(day: int)
signal export_requested

const AgentCatalog = preload("res://scripts/agent_catalog.gd")

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
			_detail_panel.offset_top = -408.0
			_detail_panel.offset_bottom = -150.0
		else:
			_detail_panel.set_anchors_preset(Control.PRESET_RIGHT_WIDE)
			_detail_panel.offset_top = 108.0 if mode == "desktop" else 102.0
			_detail_panel.offset_bottom = -128.0
	if _mobile_agents != null:
		_mobile_agents.visible = mode == "mobile" or compact_tablet
	if _bottom_dock != null:
		_bottom_dock.offset_top = -142.0 if mode == "mobile" else -108.0
	if _header != null:
		_header.offset_bottom = 82.0 if mode == "mobile" else 76.0
	if _mobile_agents != null:
		_mobile_agents.offset_top = 94.0
		_mobile_agents.offset_bottom = 168.0
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
	add_child(_root)
	_build_header()
	_build_agent_rail()
	_build_mobile_agents()
	_build_detail_panel()
	_build_bottom_dock()

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
	brand.add_child(_label("AI  /  INVESTMENT ARENA", 19, Color("#f0d6a8"), true))
	brand.add_child(_label("SIX STRATEGIES  ·  ONE MARKET  ·  INDEPENDENT CAPITAL", 10, Color("#8fa2b2")))
	var market_box := VBoxContainer.new()
	market_box.alignment = BoxContainer.ALIGNMENT_CENTER
	market_box.add_child(_label("SHARED MARKET  /  PAPER MODE", 10, Color("#8fa2b2")))
	_market_label = _label("INDEX  100.00   ·   VOL  1.8%", 14, Color("#dce7ed"), true)
	market_box.add_child(_market_label)
	row.add_child(market_box)
	var status_box := VBoxContainer.new()
	status_box.alignment = BoxContainer.ALIGNMENT_CENTER
	status_box.add_child(_label("ENGINE STATUS", 10, Color("#8fa2b2")))
	_status_label = _label(_status, 12, Color("#8de0b2"), true)
	status_box.add_child(_status_label)
	row.add_child(status_box)

func _build_agent_rail() -> void:
	_agent_rail = _panel("AgentRail")
	_agent_rail.set_anchors_preset(Control.PRESET_LEFT_WIDE)
	_agent_rail.offset_left = 20
	_agent_rail.offset_right = 304
	_agent_rail.offset_top = 108
	_agent_rail.offset_bottom = -128
	_root.add_child(_agent_rail)
	var column := VBoxContainer.new()
	column.add_theme_constant_override("separation", 8)
	_agent_rail.add_child(column)
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
	var controls := HBoxContainer.new()
	controls.add_theme_constant_override("separation", 6)
	column.add_child(controls)
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

func _refresh_detail() -> void:
	var faction := AgentCatalog.get_faction(_selected_agent)
	if faction.is_empty():
		return
	var snapshot: Dictionary = _simulator.get_account_snapshot(_selected_agent, _simulator.replay_day)
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
	_room_button.text = "← 返回竞技场" if _room_mode else "进入研究室  ↗"

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
