# AI Arena Godot 3D Client Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (\`- [ ]\`) syntax for tracking.

**Goal:** Deliver a runnable Godot 4.7.1 Finance Arena with Blender-authored 3D Agents and rooms, six independent paper portfolios, responsive UI, replay and signed-P&L cash-note animations.

**Architecture:** Godot owns the native runtime and deterministic paper simulator. Blender creates editable source geometry and exports GLB assets. Supplied AI Arena reference boards provide portrait and room textures; a CI workflow builds assets and validates the Godot project.

**Tech Stack:** Godot 4.7.1, GDScript, Blender 4.x Python API, GLB, Python 3.13 + pytest for asset/manifest checks, GitHub Actions.

**Spec:** \`11-ai-arena/godot/DESIGN.md\`

## Global Constraints

- Six stable faction IDs: value, growth, trend, quant, sentiment, macro.
- Every faction starts with the same capital and shares the same synthetic market path and fee/slippage assumptions.
- Account cash, shares, equity and ledgers remain independent.
- No live trading, broker API, live data or real LLM workers.
- Money animation is a one-way visual representation of signed P&L; it never changes account state.
- Replay exposes only days already simulated.
- Godot 4.7.1 is the minimum supported runtime; Blender 4.x is the asset authoring runtime.
- Do not claim new GPT images were generated in this milestone; use supplied reference crops and keep prompts ready.

## Review Focus

- A replay scrub must never expose a future event or mutate current simulation state.
- A failed/paused simulation must not duplicate a day's six ledger entries.
- A zero or tiny P&L delta must not create a misleading zero-dollar bill animation.
- Missing GLB assets must fall back to procedural geometry so the project still opens.
- At narrow window widths, the Agent inspector must not cover the primary simulation controls.

---

### Task 1: Godot project and failing simulation contract

**Files:**
- Create: \`11-ai-arena/godot/project.godot\`
- Create: \`11-ai-arena/godot/scenes/main.tscn\`
- Create: \`11-ai-arena/godot/tests/test_arena.gd\`
- Create: \`.github/workflows/ai-arena-godot.yml\`

**Interfaces:**
- Produces the Godot project entry point and the initial red test for \`ArenaSimulation\`.

- [ ] Write the GDScript simulation test first. Assert six independent accounts, one decision per faction per day, replay clamping and signed cashflow direction.
- [ ] Run Godot headless and verify the test fails because \`arena_simulation.gd\` does not yet exist.
- [ ] Add project configuration and a minimal main scene.
- [ ] Commit the red test and CI harness.

### Task 2: Deterministic six-account simulator

**Files:**
- Create: \`scripts/agent_catalog.gd\`
- Create: \`scripts/arena_simulation.gd\`
- Modify: \`tests/test_arena.gd\`

**Interfaces:**
- \`ArenaSimulation.configure(starting_capital: float, days: int, seed: int)\`
- \`ArenaSimulation.advance_day() -> Array[Dictionary]\`
- \`ArenaSimulation.set_replay_day(day: int) -> int\`
- \`ArenaSimulation.get_account_snapshot(agent_id: String, day: int = -1) -> Dictionary\`
- \`ArenaSimulation.get_rankings(day: int = -1) -> Array[Dictionary]\`
- \`ArenaSimulation.get_visible_events(day: int = -1) -> Array[Dictionary]\`
- \`ArenaSimulation.export_payload() -> Dictionary\`

- [ ] Implement the smallest GDScript module that makes Task 1 pass.
- [ ] Verify all six accounts receive exactly one ledger record per simulated day.
- [ ] Verify replay can inspect only the current simulated range.
- [ ] Commit the simulator and green tests.

### Task 3: Blender source models and scene assets

**Files:**
- Create: \`blender/build_ai_arena_assets.py\`
- Create: \`assets/portraits/{value,growth,trend,quant,sentiment,macro}.webp\`
- Create: \`assets/backgrounds/rooms/{value,growth,trend,quant,sentiment,macro}.webp\`
- Generate: \`assets/source/ai_arena_assets.blend\`
- Generate: \`assets/generated/agents/*.glb\`
- Generate: \`assets/generated/rooms/*.glb\`
- Generate: \`assets/generated/banknote.glb\`

**Interfaces:**
- Blender script is runnable with \`blender --background --factory-startup --python blender/build_ai_arena_assets.py\`.
- Output GLBs are imported by \`ArenaWorld\`; if absent, the world uses procedural fallbacks.

- [ ] Add asset-manifest and Blender-script syntax tests.
- [ ] Implement six recognizable busts, six differentiated research rooms and a banknote prop.
- [ ] Run Blender in CI, verify every GLB magic header and file size, and save the editable .blend source.
- [ ] Commit generated assets from the CI job only after Godot import and tests pass.

### Task 4: 3D world and cashflow choreography

**Files:**
- Create: \`scripts/arena_world.gd\`
- Create: \`tests/test_world_contract.gd\`
- Modify: \`scenes/main.tscn\`

**Interfaces:**
- \`ArenaWorld.enter_room(agent_id: String)\`
- \`ArenaWorld.return_to_arena()\`
- \`ArenaWorld.select_agent(agent_id: String)\`
- \`ArenaWorld.animate_cashflow(agent_id: String, signed_delta: float)\`

- [ ] Write the world contract test for six station anchors, room switching and opposite signed cashflow routes.
- [ ] Verify RED.
- [ ] Implement the central vault, six podiums, Agent GLB loading, six room environments and fallback geometry.
- [ ] Animate notes from vault to Agent on positive equity delta and Agent to vault on negative equity delta.
- [ ] Verify GREEN and commit.

### Task 5: Responsive Godot UI and interaction loop

**Files:**
- Create: \`scripts/arena_app.gd\`
- Modify: \`scenes/main.tscn\`
- Create: \`tests/test_ui_contract.gd\`

**Interfaces:**
- \`ArenaApp.apply_responsive_layout(width: float) -> String\`
- \`ArenaApp.enter_research_room(agent_id: String)\`
- \`ArenaApp.return_to_arena()\`
- \`ArenaApp.advance_one_day()\`

- [ ] Write the UI contract test for desktop/tablet/mobile layout modes and room entry/exit.
- [ ] Verify RED.
- [ ] Implement top bar, navigation, six portrait cards, selected-Agent inspector, research/account/ledger tabs, timeline and controls.
- [ ] Verify GREEN at 1600 / 1024 / 768 / 390 / 320 logical widths.

### Task 6: Package, docs and whole-project verification

**Files:**
- Create: \`GODOT_STATUS.md\`
- Create: \`tools/verify_generated_assets.py\`
- Modify: \`README.md\`, \`../STATUS.md\`, \`.github/workflows/ai-arena-godot.yml\`

- [ ] Add Blender + Godot CI build, import, smoke and package artifact steps.
- [ ] Run the full Godot tests and Python asset checks.
- [ ] Perform a fresh self-review of the full branch and fix all Critical/Important findings with RED→GREEN tests.
- [ ] Record the exact CI run, commit SHA and local Godot launch steps.
