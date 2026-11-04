extends SceneTree

const ArenaSimulation = preload("res://scripts/arena_simulation.gd")

func _initialize() -> void:
	var sim = ArenaSimulation.new()
	sim.configure(100000.0, 90, 20261104)

	_check(sim.accounts.size() == 6, "six factions must receive six separate accounts")
	_check(sim.accounts["value"] != sim.accounts["growth"], "accounts must be distinct dictionaries")
	_check(is_equal_approx(sim.accounts["value"].cash, 100000.0), "all accounts start with equal capital")
	_check(sim.current_day == 0, "simulation starts at day zero")

	var day_one = sim.advance_day()
	_check(day_one.size() == 6, "one day must produce exactly six faction operations")
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

	_check(ArenaSimulation.cashflow_direction(250.0) == "to_agent", "positive P&L must flow toward the Agent")
	_check(ArenaSimulation.cashflow_direction(-250.0) == "to_vault", "negative P&L must flow back to the vault")
	_check(ArenaSimulation.cashflow_direction(0.0) == "none", "zero P&L must not animate cash")

	sim.set_replay_day(999)
	_check(sim.replay_day == sim.current_day, "replay must clamp to the latest simulated day")
	print("AI ARENA SIMULATION CONTRACT: PASS")
	quit(0)

func _check(condition: bool, message: String) -> void:
	if not condition:
		push_error("CONTRACT FAILED: " + message)
		quit(1)
