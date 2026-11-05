# Godot 3D Client — Status

Updated: 2026-11-05

## Working scope

- Repository: `jinngimk-lang/wendnag`
- Working branch: `feat/ai-arena-godot-3d-experience-v01`
- Target PR base: `feat/ai-arena-independent-agent-workspace-v04`
- Engine target: Godot 4.7.1 stable, Compatibility renderer
- Additive native client; the existing HTML Finance Arena remains untouched.

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
- Godot's source folder is marked with `.gdignore`; the project `.gitignore` excludes Godot caches, Python virtual environments/bytecode and Blender backup files.
- The supplied portrait and room atlases are reused as source textures. No paid GPT image-generation call or new generated scene background is claimed.

## Verification

<badge>CI PASS</badge>

- GitHub Actions run `41949187541` passed at commit `4f2e7e286704ac758b602021b561a25982b557d4`.
- Passed steps: Python asset contract, Godot 4.7.1 project import, simulation contract, 3D world contract, responsive UI contract, main-scene smoke test, generated-asset verification, packaging and artifact upload.
- Latest artifact: `ai-investment-arena-godot`, artifact ID `13379977035`.
- Downloaded artifact was inspected; local caches, bytecode and Blender backups are absent from the package.
- Local isolated Python 3.13.5 `.venv`: 11/11 unit tests passed; `tools/verify_generated_assets.py --require-generated` passed.
- Earlier Blender rebuild run `41810847462` successfully generated the source and GLBs and committed them as `84aa7187`. The latest run skipped Blender because the generated assets already existed; a forced rebuild is still needed to validate the new backup-suppression setting itself.

## Local run

1. Install Godot 4.7.1 stable.
2. Open `11-ai-arena/godot/project.godot` and press F5.
3. Run the Python asset checks in an isolated environment as documented in `README.md`.
4. Run the Godot headless commands in `README.md`.
5. Blender 4.x is required only to regenerate the editable source and GLB exports; normal Godot runtime uses the committed GLBs.

## Follow-on product work

1. Add a run-setup modal for a synthetic scenario label, trading-day window, starting capital and risk cap.
2. Add the seventh-investor follow/challenge interactions without changing the six independent-account rules.
3. Perform visual QA in the local Godot editor for camera framing, portrait/room visibility, mobile layout and cash-note choreography. Headless CI is not a substitute for visual review.
