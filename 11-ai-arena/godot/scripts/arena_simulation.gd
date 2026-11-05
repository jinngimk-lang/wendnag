extends RefCounted
class_name ArenaSimulation

const AgentCatalog = preload("res://scripts/agent_catalog.gd")
const SIMULATOR_VERSION := "godot-paper-v0.2.0"
const FACTION_IDS := ["value", "growth", "trend", "quant", "sentiment", "macro"]
const INVESTOR_ID := "investor"

var starting_capital: float = 100000.0
var trading_days: int = 90
var seed_value: int = 20261104
var scenario_label := "SYNTHETIC MARKET"
var current_day: int = 0
var replay_day: int = 0
var fee_rate: float = 0.001
var slippage_rate: float = 0.0006
var risk_cap: float = 0.90
var rng := RandomNumberGenerator.new()
var market_prices: Array[float] = []
var market_context: Array[Dictionary] = []
var accounts: Dictionary = {}
var investor_account: Dictionary = {}
var investor_mode := "challenge"
var followed_agent_id := "value"
var challenged_agent_id := "value"
var investor_target_weight := 0.50
var investor_last_operation: Dictionary = {}
var events: Array[Dictionary] = []

func configure(capital: float = 100000.0, days: int = 90, seed: int = 20261104, risk_cap_value: float = 0.90, label: String = "SYNTHETIC MARKET") -> void:
	starting_capital = clampf(capital, 1000.0, 10000000.0)
	trading_days = clampi(days, 20, 252)
	seed_value = seed
	risk_cap = clampf(risk_cap_value, 0.10, 0.90)
	scenario_label = label.strip_edges()
	if scenario_label.is_empty():
		scenario_label = "SYNTHETIC MARKET"
	current_day = 0
	replay_day = 0
	events.clear()
	rng.seed = seed_value
	_build_market()
	_reset_accounts()
	_reset_investor_account()

func _build_market() -> void:
	market_prices.clear()
	market_context.clear()
	var price := 100.0
	var macro := 0.0
	var sentiment := 0.0
	var sector := 0.0
	var volatility := 0.018
	for day in range(trading_days + 1):
		var daily_return := 0.0
		var event_name := ""
		var event_shock := 0.0
		if day > 0:
			macro = clampf(macro * 0.84 + rng.randf_range(-0.065, 0.065), -0.24, 0.24)
			sentiment = clampf(sentiment * 0.79 + rng.randf_range(-0.19, 0.19), -1.0, 1.0)
			sector = clampf(sector * 0.88 + rng.randf_range(-0.075, 0.075), -0.28, 0.28)
			volatility = clampf(0.010 + rng.randf_range(0.001, 0.014) + (0.006 if sentiment < -0.48 else 0.0), 0.008, 0.042)
			daily_return = 0.00035 + macro * 0.008 + sector * 0.010 + sentiment * 0.002 + rng.randf_range(-volatility, volatility)
			if day % 29 == 0:
				event_name = "央行政策意外"
				event_shock = rng.randf_range(-0.022, 0.022)
			elif day % 17 == 0:
				event_name = "财报预期重估"
				event_shock = rng.randf_range(-0.028, 0.028)
			daily_return += event_shock
			price *= maxf(0.78, 1.0 + daily_return)
		var momentum := 0.0
		if day >= 5:
			momentum = price / market_prices[day - 5] - 1.0
		elif day > 0:
			momentum = price / market_prices[day - 1] - 1.0
		market_prices.append(price)
		var context := {
			"day": day,
			"price": price,
			"daily_return": daily_return,
			"macro": macro,
			"sentiment": sentiment,
			"sector": sector,
			"volatility": volatility,
			"momentum": momentum,
			"event": event_name,
			"event_shock": event_shock
		}
		market_context.append(context)
		if event_name != "":
			events.append({
				"day": day,
				"type": "MARKET",
				"title": event_name,
				"description": "共同市场因子发生变化；六个派系读取同一事件快照。",
				"shock": event_shock
			})

func _reset_accounts() -> void:
	accounts.clear()
	for faction in AgentCatalog.all():
		var agent_id := str(faction.id)
		var account := _new_account(agent_id)
		account.history.append(_make_snapshot(account, 0, 100.0, 0.0, "HOLD", "开盘状态"))
		accounts[agent_id] = account

func _reset_investor_account() -> void:
	investor_mode = "challenge"
	followed_agent_id = "value"
	challenged_agent_id = "value"
	investor_target_weight = minf(0.50, risk_cap)
	investor_account = _new_account(INVESTOR_ID)
	investor_account["mode"] = investor_mode
	investor_account["followed_agent_id"] = followed_agent_id
	investor_account["challenged_agent_id"] = challenged_agent_id
	investor_account.history.append(_make_snapshot(investor_account, 0, 100.0, 0.0, "HOLD", "第七位投资者开盘状态"))
	investor_last_operation = {}

func _new_account(account_id: String) -> Dictionary:
	return {
		"id": account_id,
		"cash": starting_capital,
		"shares": 0.0,
		"equity": starting_capital,
		"peak_equity": starting_capital,
		"max_drawdown": 0.0,
		"target_weight": 0.0,
		"last_decision": "HOLD",
		"last_reason": "等待首个市场交易日。",
		"ledger": [],
		"history": [],
		"daily_returns": []
	}

func set_investor_mode(mode: String, agent_id: String = "") -> bool:
	if mode not in ["follow", "challenge"]:
		return false
	if mode == "follow":
		if not FACTION_IDS.has(agent_id):
			return false
		followed_agent_id = agent_id
		investor_target_weight = clampf(float(accounts[agent_id].get("target_weight", investor_target_weight)), 0.0, risk_cap)
	elif agent_id in FACTION_IDS:
		challenged_agent_id = agent_id
	investor_mode = mode
	investor_account["mode"] = investor_mode
	investor_account["followed_agent_id"] = followed_agent_id
	investor_account["challenged_agent_id"] = challenged_agent_id
	var title := "第七位投资者开始跟随 %s" % str(AgentCatalog.get_faction(followed_agent_id).get("name", followed_agent_id)) if mode == "follow" else "第七位投资者向 %s 发起自主挑战" % str(AgentCatalog.get_faction(challenged_agent_id).get("name", challenged_agent_id))
	events.append({
		"day": current_day,
		"type": "INVESTOR_MODE",
		"agent_id": INVESTOR_ID,
		"title": title,
		"description": "独立个人模拟账户；与六位 Agent 使用相同市场、起始资金、费用和风险上限。"
	})
	return true

func set_investor_target_weight(weight: float) -> float:
	investor_target_weight = clampf(weight, 0.0, risk_cap)
	if investor_mode == "challenge":
		investor_account["target_weight"] = investor_target_weight
		investor_account["mode"] = investor_mode
		investor_account["followed_agent_id"] = followed_agent_id
		investor_account["challenged_agent_id"] = challenged_agent_id
	return investor_target_weight

func get_investor_snapshot(day: int = -1) -> Dictionary:
	if investor_account.is_empty():
		return {}
	var history: Array = investor_account.history
	var target_day := replay_day if day < 0 else clampi(day, 0, current_day)
	if target_day >= history.size():
		return {}
	var snapshot: Dictionary = history[target_day].duplicate(true)
	snapshot["mode"] = str(snapshot.get("mode", investor_mode))
	snapshot["followed_agent_id"] = str(snapshot.get("followed_agent_id", followed_agent_id))
	snapshot["scenario_label"] = scenario_label
	return snapshot

func advance_day() -> Array[Dictionary]:
	var operations: Array[Dictionary] = []
	if current_day >= trading_days:
		return operations
	var day := current_day + 1
	var context: Dictionary = market_context[day]
	var price := float(context.price)
	for agent_id in FACTION_IDS:
		var account: Dictionary = accounts[agent_id]
		var previous_equity := float(account.equity)
		var marked_equity := float(account.cash) + float(account.shares) * price
		var target_weight := clampf(_target_weight(agent_id, context), 0.0, risk_cap)
		var target_shares := marked_equity * target_weight / price
		var share_delta := target_shares - float(account.shares)
		var action := "HOLD"
		var quantity := 0.0
		var notional := 0.0
		var fee := 0.0
		var slippage := 0.0
		if absf(share_delta * price) >= marked_equity * 0.012:
			if share_delta > 0.0:
				var affordable := float(account.cash) / (price * (1.0 + fee_rate + slippage_rate))
				quantity = minf(share_delta, affordable)
				if quantity > 0.000001:
					notional = quantity * price
					fee = notional * fee_rate
					slippage = notional * slippage_rate
					account.cash = float(account.cash) - notional - fee - slippage
					account.shares = float(account.shares) + quantity
					action = "BUY"
			else:
				quantity = minf(absf(share_delta), float(account.shares))
				if quantity > 0.000001:
					notional = quantity * price
					fee = notional * fee_rate
					slippage = notional * slippage_rate
					account.cash = float(account.cash) + notional - fee - slippage
					account.shares = float(account.shares) - quantity
					action = "SELL"
		var equity := float(account.cash) + float(account.shares) * price
		var delta_equity := equity - previous_equity
		account.equity = equity
		account.target_weight = target_weight
		account.last_decision = action
		account.last_reason = _decision_reason(agent_id, action, context, target_weight)
		account.peak_equity = maxf(float(account.peak_equity), equity)
		var drawdown := 0.0
		if float(account.peak_equity) > 0.0:
			drawdown = maxf(0.0, (float(account.peak_equity) - equity) / float(account.peak_equity))
		account.max_drawdown = maxf(float(account.max_drawdown), drawdown)
		var daily_return := 0.0
		if previous_equity > 0.0:
			daily_return = delta_equity / previous_equity
		account.daily_returns.append(daily_return)
		var operation := {
			"day": day,
			"agent_id": agent_id,
			"action": action,
			"price": price,
			"fill_price": price * (1.0 + slippage_rate if action == "BUY" else 1.0 - slippage_rate if action == "SELL" else 1.0),
			"quantity": quantity,
			"notional": notional,
			"fee": fee,
			"slippage": slippage,
			"cash": float(account.cash),
			"shares": float(account.shares),
			"equity": equity,
			"delta_equity": delta_equity,
			"target_weight": target_weight,
			"reason": str(account.last_reason),
			"market_return": float(context.daily_return),
			"macro": float(context.macro),
			"sentiment": float(context.sentiment),
			"sector": float(context.sector),
			"volatility": float(context.volatility),
			"momentum": float(context.momentum),
			"event": str(context.event),
			"event_shock": float(context.event_shock)
		}
		account.ledger.append(operation)
		account.history.append(_make_snapshot(account, day, price, delta_equity, action, str(account.last_reason)))
		operations.append(operation)
		if action != "HOLD":
			events.append({
				"day": day,
				"type": "TRADE",
				"agent_id": agent_id,
				"action": action,
				"title": "%s · %s" % [str(AgentCatalog.get_faction(agent_id).name), action],
				"description": str(account.last_reason),
				"notional": notional,
				"delta_equity": delta_equity
			})
	_advance_investor(day, context)
	current_day = day
	replay_day = current_day
	return operations

func _advance_investor(day: int, context: Dictionary) -> void:
	var agent_id := followed_agent_id if investor_mode == "follow" else ""
	var target_weight := investor_target_weight
	var challenge_name := str(AgentCatalog.get_faction(challenged_agent_id).get("name", challenged_agent_id))
	var reason := "自主挑战 %s；个人目标仓位 %.0f%%。" % [challenge_name, target_weight * 100.0]
	if investor_mode == "follow" and accounts.has(agent_id):
		target_weight = clampf(float(accounts[agent_id].get("target_weight", 0.0)), 0.0, risk_cap)
		reason = "跟随 %s；同步其目标仓位 %.0f%%。" % [str(AgentCatalog.get_faction(agent_id).get("name", agent_id)), target_weight * 100.0]
	var account: Dictionary = investor_account
	var price := float(context.price)
	var previous_equity := float(account.equity)
	var marked_equity := float(account.cash) + float(account.shares) * price
	var target_shares := marked_equity * target_weight / price
	var share_delta := target_shares - float(account.shares)
	var action := "HOLD"
	var quantity := 0.0
	var notional := 0.0
	var fee := 0.0
	var slippage := 0.0
	if absf(share_delta * price) >= marked_equity * 0.012:
		if share_delta > 0.0:
			var affordable := float(account.cash) / (price * (1.0 + fee_rate + slippage_rate))
			quantity = minf(share_delta, affordable)
			if quantity > 0.000001:
				notional = quantity * price
				fee = notional * fee_rate
				slippage = notional * slippage_rate
				account.cash = float(account.cash) - notional - fee - slippage
				account.shares = float(account.shares) + quantity
				action = "BUY"
		else:
			quantity = minf(absf(share_delta), float(account.shares))
			if quantity > 0.000001:
				notional = quantity * price
				fee = notional * fee_rate
				slippage = notional * slippage_rate
				account.cash = float(account.cash) + notional - fee - slippage
				account.shares = float(account.shares) - quantity
				action = "SELL"
	var equity := float(account.cash) + float(account.shares) * price
	var delta_equity := equity - previous_equity
	account.equity = equity
	account.target_weight = target_weight
	account.last_decision = action
	account.last_reason = reason
	account.peak_equity = maxf(float(account.peak_equity), equity)
	var drawdown := 0.0
	if float(account.peak_equity) > 0.0:
		drawdown = maxf(0.0, (float(account.peak_equity) - equity) / float(account.peak_equity))
	account.max_drawdown = maxf(float(account.max_drawdown), drawdown)
	var daily_return := delta_equity / previous_equity if previous_equity > 0.0 else 0.0
	account.daily_returns.append(daily_return)
	account.mode = investor_mode
	account.followed_agent_id = followed_agent_id
	account.challenged_agent_id = challenged_agent_id
	var operation := {
		"day": day,
		"agent_id": INVESTOR_ID,
		"actor": "investor",
		"mode": investor_mode,
		"followed_agent_id": followed_agent_id,
		"challenged_agent_id": challenged_agent_id,
		"action": action,
		"price": price,
		"fill_price": price * (1.0 + slippage_rate if action == "BUY" else 1.0 - slippage_rate if action == "SELL" else 1.0),
		"quantity": quantity,
		"notional": notional,
		"fee": fee,
		"slippage": slippage,
		"cash": float(account.cash),
		"shares": float(account.shares),
		"equity": equity,
		"delta_equity": delta_equity,
		"target_weight": target_weight,
		"reason": reason,
		"market_return": float(context.daily_return),
		"macro": float(context.macro),
		"sentiment": float(context.sentiment),
		"sector": float(context.sector),
		"volatility": float(context.volatility),
		"momentum": float(context.momentum),
		"event": str(context.event),
		"event_shock": float(context.event_shock)
	}
	account.ledger.append(operation)
	account.history.append(_make_snapshot(account, day, price, delta_equity, action, reason))
	investor_last_operation = operation.duplicate(true)
	if action != "HOLD":
		events.append({
			"day": day,
			"type": "INVESTOR_TRADE",
			"agent_id": INVESTOR_ID,
			"action": action,
			"title": "我的组合 · %s" % action,
			"description": reason,
			"notional": notional,
			"delta_equity": delta_equity
		})

func set_replay_day(day: int) -> int:
	replay_day = clampi(day, 0, current_day)
	return replay_day

func get_account_snapshot(agent_id: String, day: int = -1) -> Dictionary:
	if agent_id == INVESTOR_ID:
		return get_investor_snapshot(day)
	if not accounts.has(agent_id):
		return {}
	var history: Array = accounts[agent_id].history
	var target_day := replay_day if day < 0 else clampi(day, 0, current_day)
	if target_day >= history.size():
		return {}
	return history[target_day].duplicate(true)

func get_rankings(day: int = -1) -> Array[Dictionary]:
	var rows: Array[Dictionary] = []
	for faction in AgentCatalog.all():
		var agent_id := str(faction.id)
		var snapshot := get_account_snapshot(agent_id, day)
		if snapshot.is_empty():
			continue
		var return_pct := float(snapshot.cumulative_return_pct)
		var drawdown_pct := float(snapshot.max_drawdown_pct)
		var volatility_pct := float(snapshot.volatility_pct)
		var score := return_pct - drawdown_pct * 0.48 - volatility_pct * 0.12
		rows.append({
			"agent_id": agent_id,
			"name": str(faction.name),
			"equity": float(snapshot.equity),
			"return_pct": return_pct,
			"drawdown_pct": drawdown_pct,
			"score": score
		})
	var investor_snapshot := get_investor_snapshot(day)
	if not investor_snapshot.is_empty():
		var investor_return := float(investor_snapshot.get("cumulative_return_pct", 0.0))
		var investor_drawdown := float(investor_snapshot.get("max_drawdown_pct", 0.0))
		var investor_volatility := float(investor_snapshot.get("volatility_pct", 0.0))
		rows.append({
			"agent_id": INVESTOR_ID,
			"name": "我的组合",
			"equity": float(investor_snapshot.get("equity", starting_capital)),
			"return_pct": investor_return,
			"drawdown_pct": investor_drawdown,
			"score": investor_return - investor_drawdown * 0.48 - investor_volatility * 0.12
		})
	rows.sort_custom(func(a: Dictionary, b: Dictionary) -> bool: return float(a.score) > float(b.score))
	for index in range(rows.size()):
		rows[index]["rank"] = index + 1
	return rows

func get_visible_events(day: int = -1) -> Array[Dictionary]:
	var target_day := replay_day if day < 0 else clampi(day, 0, current_day)
	var visible: Array[Dictionary] = []
	for event in events:
		if int(event.day) <= target_day:
			visible.append(event.duplicate(true))
	return visible

func export_payload() -> Dictionary:
	var account_export: Dictionary = {}
	for agent_id in FACTION_IDS:
		account_export[agent_id] = accounts[agent_id].duplicate(true)
	return {
		"schema_version": "ai-arena-godot-run-v0.2",
		"simulator_version": SIMULATOR_VERSION,
		"run_id": "%s-%s" % [str(seed_value), str(Time.get_unix_time_from_system())],
		"seed": seed_value,
		"synthetic_demo_only": true,
		"broker_connected": false,
		"scenario_label": scenario_label,
		"starting_capital": starting_capital,
		"trading_days": trading_days,
		"fee_rate": fee_rate,
		"slippage_rate": slippage_rate,
		"risk_cap": risk_cap,
		"current_day": current_day,
		"market_context": market_context.slice(0, current_day + 1),
		"events": get_visible_events(current_day),
		"accounts": account_export,
		"investor": investor_account.duplicate(true),
		"investor_mode": investor_mode,
		"followed_agent_id": followed_agent_id,
		"challenged_agent_id": challenged_agent_id,
		"investor_target_weight": investor_target_weight,
		"rankings": get_rankings(current_day)
	}

func settle() -> Array[Dictionary]:
	var final_operations: Array[Dictionary] = []
	while current_day < trading_days:
		final_operations = advance_day()
	return final_operations

func _make_snapshot(account: Dictionary, day: int, price: float, delta_equity: float, action: String, reason: String) -> Dictionary:
	var equity := float(account.cash) + float(account.shares) * price
	var cumulative_return := 0.0
	if starting_capital > 0.0:
		cumulative_return = (equity / starting_capital - 1.0) * 100.0
	var peak := maxf(float(account.get("peak_equity", starting_capital)), equity)
	var drawdown := 0.0
	if peak > 0.0:
		drawdown = maxf(0.0, (peak - equity) / peak) * 100.0
	var returns: Array = account.get("daily_returns", [])
	var volatility_pct := 0.0
	if returns.size() > 1:
		var mean := 0.0
		for value in returns:
			mean += float(value)
		mean /= float(returns.size())
		var variance := 0.0
		for value in returns:
			variance += pow(float(value) - mean, 2.0)
		variance /= float(returns.size() - 1)
		volatility_pct = sqrt(variance) * sqrt(252.0) * 100.0
	return {
		"day": day,
		"price": price,
		"cash": float(account.cash),
		"shares": float(account.shares),
		"equity": equity,
		"target_weight": float(account.get("target_weight", 0.0)),
		"exposure_pct": (float(account.shares) * price / equity * 100.0) if equity > 0.0 else 0.0,
		"last_decision": action,
		"last_reason": reason,
		"daily_change": delta_equity,
		"max_drawdown_pct": maxf(float(account.get("max_drawdown", 0.0)), drawdown),
		"cumulative_return_pct": cumulative_return,
		"volatility_pct": volatility_pct,
		"mode": str(account.get("mode", "")),
		"followed_agent_id": str(account.get("followed_agent_id", "")),
		"challenged_agent_id": str(account.get("challenged_agent_id", ""))
	}

func _target_weight(agent_id: String, context: Dictionary) -> float:
	var macro := float(context.macro)
	var sentiment := float(context.sentiment)
	var sector := float(context.sector)
	var volatility := float(context.volatility)
	var momentum := float(context.momentum)
	match agent_id:
		"value":
			return clampf(0.54 - momentum * 0.62 + maxf(-macro, 0.0) * 0.28, 0.24, 0.76)
		"growth":
			return clampf(0.56 + maxf(sector, 0.0) * 0.62 + momentum * 0.85 - maxf(-macro, 0.0) * 0.30, 0.22, 0.88)
		"trend":
			return clampf(0.22 + maxf(momentum, 0.0) * 4.8 - maxf(-momentum, 0.0) * 2.2, 0.12, 0.88)
		"quant":
			return clampf(0.49 + sector * 0.24 + macro * 0.12 - maxf(volatility - 0.018, 0.0) * 3.0, 0.25, 0.72)
		"sentiment":
			return clampf(0.38 + sentiment * 0.31 + momentum * 0.22, 0.14, 0.78)
		"macro":
			return clampf(0.34 + maxf(macro, 0.0) * 1.15 - maxf(-macro, 0.0) * 0.72 - volatility * 1.8, 0.16, 0.74)
	return 0.40

func _decision_reason(agent_id: String, action: String, context: Dictionary, target_weight: float) -> String:
	var prefix := "维持风险预算 %.0f%%" % (target_weight * 100.0)
	match agent_id:
		"value":
			prefix = "估值安全边际与现金流质量；" + prefix
		"growth":
			prefix = "行业成长与收入动能；" + prefix
		"trend":
			prefix = "价格动量与趋势确认；" + prefix
		"quant":
			prefix = "因子组合与波动约束；" + prefix
		"sentiment":
			prefix = "情绪温度与预期差；" + prefix
		"macro":
			prefix = "流动性与宏观周期；" + prefix
	if action == "HOLD":
		return prefix + "，当前不值得支付额外交易成本。"
	return prefix + ("，增加目标敞口。" if action == "BUY" else "，降低目标敞口。")

static func cashflow_direction(signed_delta: float, minimum_delta: float = 5.0) -> String:
	if absf(signed_delta) < minimum_delta:
		return "none"
	return "gain" if signed_delta > 0.0 else "loss"
