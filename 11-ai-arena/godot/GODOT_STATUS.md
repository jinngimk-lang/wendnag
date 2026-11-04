# Godot 3D Client — Status

Updated: 2026-11-04

## Working scope

- Repository: `jinngimk-lang/wendnag`
- Working branch: `feat/ai-arena-godot-3d-experience-v01`
- Target PR base: `feat/ai-arena-independent-agent-workspace-v04`
- Engine target: Godot 4.7.1 stable, Compatibility renderer
- This is an additive native client; the existing HTML Finance Arena remains untouched.

## Product invariants

- Six stable factions, six independent paper accounts, and one shared synthetic market path.
- Each account owns its own cash, shares, equity, drawdown, history and operation ledger.
- The 3D center is a shared-market information display, not a capital vault.
- P&L notes stay inside the same Agent's station/account marker. Positive deltas rise from that account; negative deltas return to the same account marker. No shared cash pool or inter-Agent transfers.
- All prices, research signals, events and fills are synthetic paper-mode data. No broker, real orders, external LLM workers or licensed live feed are connected.

## Current implementation

- Blender source project plus six Agent GLBs, six research-room GLBs and a banknote GLB are committed.
- Godot world builds six clickable faction stations, a shared-market display and lazily loaded faction research rooms.
- HUD supports Agent selection, research/account/ledger tabs, playback, replay scrubbing, JSON export and responsive desktop/tablet/mobile layouts.
- Godot's source folder is marked with `.gdignore` so the editor does not try to import the editable `.blend` file as a runtime resource; GLB exports remain importable.
- The supplied portrait and room atlases are reused as source textures. Replacement prompts are included; no paid GPT image-generation call or new generated scene background is claimed.

## Verification

<badge>CI PASS</badge>

- GitHub Actions run `41810176381` passed at commit `000fa607bf4160b84fe1a4ed0cb89123b419bf6e`.
- Passed steps: Python asset contract, Godot 4.7.1 project import, simulation contract, 3D world contract, responsive UI contract, main-scene smoke test, generated-asset verification, packaging and artifact upload.
- Downloadable CI artifact: `ai-investment-arena-godot` (artifact ID `13311482622`).
- Local isolated `.venv` verification: 8/8 Python unit tests passed; `tools/verify_generated_assets.py --require-generated` passed.
- Blender rebuild was skipped on the latest CI run because the committed editable source and GLB exports were already present; the generated-asset integrity check did run and pass.
- Earlier compile and SceneTree test-timing failures were corrected and are covered by the passing run above.

## Local run

1. Install Godot 4.7.1 stable.
2. Open `11-ai-arena/godot/project.godot` and press F5.
3. Run the headless tests listed in `README.md`.
4. Blender 4.x is required only to regenerate the editable source and GLB exports; normal Godot runtime uses the committed GLBs.
