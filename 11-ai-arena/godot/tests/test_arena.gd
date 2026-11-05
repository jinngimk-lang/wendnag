extends SceneTree

const ArenaSimulation = preload("res://scripts/arena_simulation.gd")
const AgentCatalog = preload("res://scripts/agent_catalog.gd")

var _failed := false

func _initialize() -> void:
	var sim = ArenaSimulation.new()
	sim.configure(100000.0, 90, 20261104)

	_check(AgentCatalog.all().size() == 6, "six faction catalog entries must be present")
	_check(AgentCatalog.portrait_texture("value") != null, "portrait sprite atlas must resolve a value portrait")
	_check(AgentCatalog.room_texture("macro") != null, "room sprite atlas must resolve a macro environment")
	_check(sim.accounts.size() == 6, "the AI roster must remain exactly six independent accounts")
	_check(sim.accounts["value"] != sim.accounts["growth"], "AI accounts must be distinct dictionaries")
	_check(is_equal_approx(sim.accounts["value"].cash, 100000.0), "all AI accounts start with equal capital")
	_check(not sim.accounts.has("investor"), "the seventh investor must not be inserted into the six-agent roster")
	_check(sim.investor_account.id == "investor", "the user must receive a separate seventh portfolio")
	_check(is_equal_approx(sim.investor_account.cash, 100000.0), "the seventh investor starts with the same capital")
	_check(sim.get_rankings(0).size() == 7, "the leaderboard must compare all six Agents and the user")
	_check(sim.current_day == 0, "simulation starts at day zero")

	var day_one = sim.advance_day()
	_check(day_one.size() == 6, "one day must preserve exactly six AI faction operations")
	_check(sim.investor_last_operation.day == 1, "the seventh investor receives a separately recorded daily operation")
	_check(sim.investor_account.ledger.size() == 1, "the seventh investor has an independent operation ledger")
	_check(sim.current_day == 1, "one advance must move exactly one day")
	for faction_id in ["value", "growth", "trend", "quant", "sentiment", "macro"]:
		_check(sim.accounts[faction_id].ledger.size() == 1, "%s must receive one ledger entry" % faction_id)
		_check(sim.accounts[faction_id].history.size() == 2, "%s must retain opening and day-one snapshots" % faction_id)

	var current_day = sim.current_day
	var visible = sim.set_replay_day(0)
	_check(visible == 0, "replay can inspect the opening state")
	_check(sim.current_day == current_day, "replay must not mutate the live simulation")
	_check(sim.get_account_snapshot("value").day == 0, "replay snapshot must match the selected day")
	_check(sim.get_visible_events().all(func(event): return int(event.day) <= 0), "replay must hide future events")

	_check(ArenaSimulation.cashflow_direction(250.0) == "gain", "positive P&L must register as a gain")
	_check(ArenaSimulation.cashflow_direction(-250.0) == "loss", "negative P&L must register as a loss")
	_check(ArenaSimulation.cashflow_direction(0.0) == "none", "zero P&L must not animate cash")

	var follow_sim = ArenaSimulation.new()
	follow_sim.configure(100000.0, 90, 20261104, 0.90, "FOLLOW TEST")
	_check(follow_sim.set_investor_mode("follow", "growth"), "the user can follow a valid Agent")
	var followed_ops = follow_sim.advance_day()
	_check(followed_ops.size() == 6, "following must not create a seventh AI operation")
	_check(is_equal_approx(float(follow_sim.investor_last_operation.target_weight), float(follow_sim.accounts.growth.target_weight)), "follow mode synchronizes the Agent target weight")
	_check(is_equal_approx(float(follow_sim.investor_account.equity), float(follow_sim.accounts.growth.equity)), "same capital, market and costs make a followed account comparable")
	_check(follow_sim.investor_last_operation.mode == "follow", "follow mode is recorded in the personal ledger")

	var challenge_sim = ArenaSimulation.new()
	challenge_sim.configure(100000.0, 90, 20261104, 0.30, "CHALLENGE TEST")
	_check(challenge_sim.set_investor_mode("challenge", "quant"), "the user can independently challenge an Agent")
	challenge_sim.set_investor_target_weight(0.75)
	_check(is_equal_approx(challenge_sim.investor_target_weight, 0.30), "the personal target weight respects the shared risk cap")
	challenge_sim.advance_day()
	_check(is_equal_approx(float(challenge_sim.investor_last_operation.target_weight), 0.30), "challenge mode executes the user's own capped target weight")
	_check(challenge_sim.investor_last_operation.challenged_agent_id == "quant", "challenge target is recorded")
	_check(challenge_sim.export_payload().has("investor"), "JSON export includes the seventh investor account")
	_check(challenge_sim.export_payload().scenario_label == "CHALLENGE TEST", "JSON export preserves the scenario label")

	sim.set_replay_day(999)
	_check(sim.replay_day == sim.current_day, "replay must clamp to the latest simulated day")

	var twin = ArenaSimulation.new()
	twin.configure(100000.0, 90, 20261104)
	_check(is_equal_approx(sim.market_prices[1], twin.market_prices[1]), "same seed must reproduce the same market path")
	if _failed:
		quit(1)
	else:
		print("AI ARENA SIMULATION CONTRACT: PASS")
		quit(0)

func _check(condition: bool, message: String) -> void:
	if not condition:
		_failed = true
		push_error("CONTRACT FAILED: " + message)
