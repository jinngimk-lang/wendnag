# Godot 3D Client — Status

Updated: 2026-11-04

## Working scope

- Repository: `jinngimk-lang/wendnag`
- Working branch: `feat/ai-arena-godot-3d-experience-v01`
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

## Verification

- Python asset contract and Godot project import have passed in GitHub Actions.
- Earlier CI exposed two GDScript compile defects; both were fixed.
- World/UI test setup is deferred until the SceneTree is ready. The next CI run is the gate for the world, responsive UI and main-scene runtime contracts.
- The last failing run before this correction was `41809420086`; it showed that a SceneTree test instantiated the world before `_ready()` ran. The test now uses `call_deferred`, and cashflow assertions now verify per-Agent-local endpoints.

## Local run

1. Install Godot 4.7.1 stable.
2. Open `11-ai-arena/godot/project.godot` and press F5.
3. Run the headless tests listed in `README.md`.
4. Blender 4.x is required only to regenerate the editable source and GLB exports; normal Godot runtime uses the committed GLBs.
