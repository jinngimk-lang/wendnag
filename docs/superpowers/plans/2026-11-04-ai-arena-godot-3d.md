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
- Money animation is a local visual representation of signed P&L, bounded to the same Agent account marker and podium; it never changes account state.
- No central capital vault, shared cash pool or inter-Agent cash transfer.
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

- [x] Write the GDScript simulation test first. Assert six independent accounts, one decision per faction per day, replay clamping and signed cashflow direction.
- [ ] Run Godot headless and verify the test fails because \`arena_simulation.gd\` does not yet exist.
- [x] Add project configuration and a minimal main scene.
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

- [x] Implement the smallest GDScript module that makes Task 1 pass.
- [x] Verify all six accounts receive exactly one ledger record per simulated day.
- [x] Verify replay can inspect only the current simulated range.
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

- [x] Add asset-manifest and Blender-script syntax tests.
- [x] Implement six recognizable busts, six differentiated research rooms and a banknote prop.
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

- [x] Write the world contract test for six station anchors, room switching and opposite signed local-account cashflow routes.
- [ ] Verify RED.
- [x] Implement the shared-market information display, six independent account podiums, Agent GLB loading, six room environments and fallback geometry. No central vault or cross-Agent cashflow route is used.
- [x] Animate positive notes upward from the same Agent’s account marker and negative notes back to that same marker.
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

- [x] Write the UI contract test for desktop/tablet/mobile layout modes and room entry/exit.
- [ ] Verify RED.
- [x] Implement top bar, navigation, six portrait cards, selected-Agent inspector, research/account/ledger tabs, timeline and controls.
- [ ] Verify GREEN at 1600 / 1024 / 768 / 390 / 320 logical widths.

### Task 6: Package, docs and whole-project verification

**Files:**
- Create: \`GODOT_STATUS.md\`
- Create: \`tools/verify_generated_assets.py\`
- Modify: \`README.md\`, \`../STATUS.md\`, \`.github/workflows/ai-arena-godot.yml\`

- [x] Add Blender + Godot CI build, import, smoke and package artifact steps.
- [x] Run the full Godot tests and Python asset checks. GitHub Actions run 41810429080 passed all Godot and asset steps; local isolated .venv passed 8/8 Python tests and the generated-asset verifier.
- [ ] Perform a fresh self-review of the full branch and fix all Critical/Important findings with RED→GREEN tests.
- [x] Record the exact CI run, commit SHA and local Godot launch steps in `11-ai-arena/godot/GODOT_STATUS.md`.


## Current checkpoint — 2026-11-04

- Passing Godot CI: run `41810429080`, commit `d7d83ec09131baf2328cae42099c2eb2b343668a`.
- Passed: Godot 4.7.1 import, simulation, 3D world, responsive UI, main-scene smoke, generated-asset integrity, package and upload.
- Local `.venv`: 8/8 Python contract tests passed; generated Blender asset verifier passed.
- Existing GLB and editable `.blend` assets are committed. The latest normal CI skipped regeneration because all assets were already present; a one-off rebuild gate is being run to prove the Blender builder is reproducible.
- No new GPT scene-background generation is claimed; supplied portrait/room reference atlases are used, with room briefs and an arena brief ready for a future non-paid generation route.

## Follow-on product work (not part of this verified baseline)

1. Add a dedicated run-setup modal for scenario/company label, duration, starting capital and risk cap; keep the label explicitly synthetic/demo-only.
2. Add the user's seventh-investor interaction: follow an Agent or challenge its strategy, without changing the six independent-account accounting rules.
3. Perform visual QA in the user's local Godot editor for camera framing, portrait/room visibility, mobile layout and note choreography; CI evidence is headless and is not a substitute for visual review.
4. If a non-paid image-generation route becomes available, replace room backplates using the included prompts without changing the scene or account contracts.


## Current checkpoint — 2026-11-05

- Latest Godot CI: run `41949187541`, commit `4f2e7e286704ac758b602021b561a25982b557d4`; all Godot and Python asset steps passed.
- Local isolated Python 3.13.5 `.venv`: 11/11 tests passed; generated asset verifier passed.
- Artifact `13379977035` was inspected and contains no local caches, bytecode or Blender backup files.
- Blender rebuild run `41810847462` passed and produced the current committed GLBs/source. The current workflow's Blender step skipped because assets existed; force one new build after the backup-suppression fix to verify that code path.
- Removed the accidental `ai_arena_assets.blend1` backup; project ignore rules, builder save-version setting, verifier guard, CI cleanup and package exclusions are now in place.
- Final whole-branch self-review is in progress; no merge or deployment has been performed.

## Follow-on product work (separate implementation tasks)

1. Add a run-setup modal for a clearly synthetic scenario label, trading-day window, starting capital and risk cap.
2. Add the user's seventh-investor interaction: follow an Agent or challenge its strategy, preserving six independent paper accounts.
3. Perform visual QA in the Godot editor for camera framing, room/portrait visibility, mobile layout and cash-note choreography.


## Current checkpoint — 2026-11-05 final mobile closure

- The native client now has six independent AI paper accounts plus a separate seventh-investor personal portfolio, with follow/challenge modes, a shared synthetic market, common capital/fees/slippage/risk cap, seven-seat risk-adjusted ranking, personal ledger and export.
- Run setup supports a display-only scenario label, 20–252 trading days, starting capital and a shared 10–90% risk cap. The dialog now sizes itself to the physical viewport and is runtime-tested at 390×844 and 320×560.
- Mobile HUD regression was reproduced with a red UI contract, then fixed: 240px bottom sheet, hidden portrait/role block, compact header and Agent rail below it, horizontally scrollable playback controls, physical viewport coordinates and a closer portrait camera.
- Latest Godot Actions run #41996618038 passed at commit `14f07545025cd129ff1fbcb6f0e7aac1f00fac83`; companion validation run #41996618004 passed. Desktop and 390×844 mobile screenshots were inspected.
- Isolated Python 3.13.5 `.venv`: 20 tests passed, 1 workflow-only test skipped; generated Blender asset verification, bytecode compilation and package hygiene passed. Final package artifact #13400188144 has 90 entries and no caches/backups.
- The six-Agent roster remains unchanged; no live market data, broker, external LLM worker or real orders are connected. The original HTML Finance Arena V0.5.0 remains unchanged.
- Remaining gate: independent code-review challenge and resolve stacked PR base branch identity before integration. PR #28 remains draft; parent PR #26 and main remain untouched.
