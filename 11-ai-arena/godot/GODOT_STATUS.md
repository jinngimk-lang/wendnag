# Godot 3D Client — Status

Updated: 2026-11-05

## Working scope

- Repository: `jinngimk-lang/wendnag`
- Current review branch: `fix/ai-arena-godot-hud-runtime-errors-20261105`
- Native-client feature branch: `feat/ai-arena-godot-3d-experience-v01`
- Draft PR: [#28](https://github.com/jinngimk-lang/wendnag/pull/28)
- Target PR base: `feat/ai-arena-independent-agent-workspace-v04`
- Engine target: Godot 4.7.1 stable, Compatibility renderer
- Additive native client; the existing HTML Finance Arena and draft PR #26 remain untouched.

## Product invariants

- Six stable factions, six independent paper accounts, and one shared synthetic market path.
- Each account owns its own cash, shares, equity, drawdown, history and operation ledger.
- The 3D center is a shared-market information display, not a capital vault.
- P&L notes stay inside the same Agent's station/account marker. Positive deltas rise from that account; negative deltas return to the same account marker. No shared cash pool or inter-Agent transfers.
- All prices, research signals, events and fills are synthetic paper-mode data. No broker, real orders, external LLM workers or licensed live feed are connected.

## Current implementation

- Editable Blender source project plus six Agent GLBs, six research-room GLBs and a banknote GLB.
- Godot world builds six clickable faction stations, a shared-market display and lazily loaded faction research rooms.
- HUD supports Agent selection, research/account/ledger tabs, playback, replay scrubbing, JSON export and responsive desktop/tablet/mobile layouts.
- Button icon sizing uses the Godot theme constant `icon_max_width`; the desktop and mobile values are covered by the UI contract.
- `tools/run_godot_check.sh` wraps Godot import, simulation, world, UI and main-scene checks and fails on `SCRIPT ERROR:` or `Parse Error:` log entries.
- Godot's source folder is marked with `.gdignore`; the project `.gitignore` excludes Godot caches, Python virtual environments/bytecode and Blender backup files.
- Supplied portrait and room atlases are reused as source textures. No paid GPT image-generation call or new generated scene background is claimed.

## Verification

- Forced Blender rebuild: GitHub Actions run [#41950047674](https://github.com/jinngimk-lang/wendnag/actions/runs/41950047674) passed with Blender 4.0.2, regenerated the editable source and all GLBs, then ran the Godot import/contracts, asset verification, packaging and upload.
- The build run validated commit `392e616d1fdc57231b51536c743c992ca06c1bf7`, then committed the generated source and model files as `a4387d3496d679fbd6680d9a0139897245434b79`. The package was created after that push.
- HUD runtime correction and stricter error detection: PR Actions run [#41952957967](https://github.com/jinngimk-lang/wendnag/actions/runs/41952957967) passed at commit `1b6f7f985a27bc7d5d0c7001ebdae0fb53c01783`.
- Run #41952957967 passed all 14 Python tests, Godot 4.7.1 project import, simulation contract, 3D world contract, responsive UI contract, main-scene smoke test, generated-asset verification, packaging and artifact upload. Its logs contain zero `SCRIPT ERROR:` or `Parse Error:` entries.
- Latest artifact: `ai-investment-arena-godot`, ID `13382140939`. The downloaded package contains 6 Agent GLBs, 6 room GLBs, 6 room WebP atlases, the banknote GLB, the editable 11.23 MB Blender source and the runtime-check helper. No `.blend1`, `.blend2`, `.godot`, `.venv`, `__pycache__`, `.pyc` or `.pyo` residue was found.
- Isolated local Python `.venv`: 13 tests passed; the workflow-only test was skipped because the standalone downloaded project does not contain `.github/workflows`. `tools/verify_generated_assets.py --require-generated` passed. The runtime-check helper was tested with clean output and intentionally injected script-error output.
- Blender reported that the optional Draco compression library was unavailable. The exported files are valid glTF 2.0 assets without the Draco extension; generated-asset verification passed.

## Local run

1. Install Godot 4.7.1 stable.
2. Open `11-ai-arena/godot/project.godot` and press F5.
3. Run the Python asset checks in an isolated environment as documented in `README.md`.
4. Run the Godot headless commands in `README.md`; CI additionally uses `tools/run_godot_check.sh` to reject script and parse errors.
5. Blender 4.x is required only to regenerate the editable source and GLB exports; normal Godot runtime uses the committed GLBs.

## Follow-on product work

1. Add a run-setup modal for a synthetic scenario label, trading-day window, starting capital and risk cap. The current runtime still starts with fixed defaults of $100,000 and 90 trading days.
2. Add the seventh-investor follow/challenge interactions without changing the six independent-account rules.
3. Perform visual QA in the local Godot editor for camera framing, portrait/room visibility, mobile layout and cash-note choreography. Headless CI is not a substitute for visual review.
