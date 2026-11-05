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

- Six stable AI factions, six independent Agent paper accounts, one separate seventh-investor personal account, and one shared synthetic market path.
- The six-agent roster remains exactly six; the user portfolio is not a seventh AI Agent.
- All seven accounts use the same starting capital, fee/slippage assumptions, market path and shared risk cap.
- Follow mode synchronizes the user's daily target exposure with one selected Agent while keeping the user's cash, shares, fills and ledger independent.
- Challenge mode uses the user's own target stock exposure and records the selected rival for comparison.
- The 3D center is a shared-market information display, not a capital vault. P&L notes stay local to the same account marker; there is no shared cash pool or inter-account transfer.
- All prices, research signals, events and fills are synthetic paper-mode data. No broker, real orders, external LLM workers or licensed live feed are connected.

## Current implementation

- Editable Blender source project plus six Agent GLBs, six research-room GLBs and a banknote GLB.
- Godot world builds six clickable faction stations, a shared-market display, a gold-accented seventh-investor desk and lazily loaded faction research rooms.
- HUD supports Agent selection, research/account/ledger tabs, playback, replay scrubbing, JSON export and responsive desktop/tablet/mobile layouts.
- A project-specific Noto Sans SC subset is generated and applied to HUD controls, run setup and 3D labels to avoid missing CJK glyphs on clean hosts. CI installs Noto CJK/fontTools and generates the subset before Godot import; the font and OFL notice are included in the downloadable package but excluded from source control.
- Responsive 3D camera presets and softened local faction lights improve portrait-screen framing; mobile investor detail is given a larger bottom-sheet viewport. Canvas stretching is disabled so the HUD lays out in actual window coordinates instead of shrinking a 1600px desktop canvas onto a phone.
- Run-setup modal configures a display-only scenario label, 20–252 trading days, starting capital and a shared 10–90% risk cap.
- Seventh-investor panel exposes follow/challenge state, personal account metrics, account and ledger views, a personal target-exposure slider and a seven-seat risk-adjusted leaderboard.
- tests/capture_visual.gd captures the desktop arena, desktop investor panel and mobile investor layout for CI visual inspection.
- Button icon sizing uses the Godot theme constant `icon_max_width`; the desktop and mobile values are covered by the UI contract.
- `tools/run_godot_check.sh` wraps Godot import, simulation, world, UI and main-scene checks and fails on `SCRIPT ERROR:` or `Parse Error:` log entries.
- Godot's source folder is marked with `.gdignore`; the project `.gitignore` excludes Godot caches, Python virtual environments/bytecode and Blender backup files.
- Supplied portrait and room atlases are reused as source textures. No paid GPT image-generation call or new generated scene background is claimed.

## Verification

- Forced Blender rebuild: GitHub Actions run [#41950047674](https://github.com/jinngimk-lang/wendnag/actions/runs/41950047674) passed with Blender 4.0.2, regenerated the editable source and all GLBs, then ran the Godot import/contracts, asset verification, packaging and upload.
- The build run validated commit `392e616d1fdc57231b51536c743c992ca06c1bf7`, then committed the generated source and model files as `a4387d3496d679fbd6680d9a0139897245434b79`. The package was created after that push.
- HUD runtime correction and stricter error detection: PR Actions run [#41952957967](https://github.com/jinngimk-lang/wendnag/actions/runs/41952957967) passed at commit `1b6f7f985a27bc7d5d0c7001ebdae0fb53c01783`.
- Run #41952957967 passed all 14 Python tests, Godot 4.7.1 project import, simulation contract, 3D world contract, responsive UI contract, main-scene smoke test, generated-asset verification, packaging and artifact upload. Its logs contain zero `SCRIPT ERROR:` or `Parse Error:` entries.
- Code-fix verification artifact: `ai-investment-arena-godot`, ID `13382140939`. The downloaded package contains 6 Agent GLBs, 6 room GLBs, 6 room WebP atlases, the banknote GLB, the editable 11.23 MB Blender source and the runtime-check helper. No `.blend1`, `.blend2`, `.godot`, `.venv`, `__pycache__`, `.pyc` or `.pyo` residue was found.
- Documentation-sync PR run [#41953215975](https://github.com/jinngimk-lang/wendnag/actions/runs/41953215975) also passed at commit `ea120585e75369531bbd460a4eedc700deb66b43`; its artifact `13381398583` was downloaded and inspected with the same asset counts and zero cache/backup residue.
- Companion HTML regression run [#41953215990](https://github.com/jinngimk-lang/wendnag/actions/runs/41953215990) passed backend evidence contracts and the Finance Lab browser regression. The existing HTML V0.5.0 remained unchanged; responsive QA at 1440/1024/768/390/320px reported no horizontal overflow or browser errors. Artifacts: runnable package `13381931491` and visual QA `13381896589`.
- Previous isolated Python baseline: 13 tests passed; the workflow-only test was skipped because the standalone downloaded project does not contain `.github/workflows`.
- Current isolated Python 3.13.5 `.venv`: 17 tests passed, 1 workflow-only test skipped; `tools/verify_generated_assets.py --require-generated` passed.
- Current Godot GDScript and screenshot changes require the next PR CI run; Python source-contract checks are not a substitute for Godot import/runtime validation.
- The local sandbox has no Godot 4.7.1 executable or graphical display, so the Xvfb-backed GitHub Actions run must validate the runtime and produce screenshots before visual QA is considered complete.
- Blender reported that the optional Draco compression library was unavailable. The exported files are valid glTF 2.0 assets without the Draco extension; generated-asset verification passed.

## Local run

1. Install Godot 4.7.1 stable.
2. Open `11-ai-arena/godot/project.godot` and press F5.
3. Run the Python asset checks in an isolated environment as documented in `README.md`.
4. Run the Godot headless commands in `README.md`; CI additionally uses `tools/run_godot_check.sh` to reject script and parse errors.
5. Blender 4.x is required only to regenerate the editable source and GLB exports; normal Godot runtime uses the committed GLBs.

## Follow-on product work

1. Inspect the next PR CI run for GDScript parse/runtime errors and all simulation/world/UI contracts.
2. Download and visually inspect the Xvfb screenshot artifact for seat framing, modal layout, detail-panel clipping and mobile control reachability.
3. Keep PR #28 as draft until runtime checks are green and the visual artifact has been inspected.
