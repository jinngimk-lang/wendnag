# AI Investment Arena — Godot 3D Client

This folder is the native Godot client for the Finance Arena. Open \`project.godot\` with **Godot 4.7.1 stable**.

## What this build is

A spectator-first 3D paper-trading arena with six visibly different AI investment managers and a dedicated seventh-investor seat. Six AI portfolios and the user's personal portfolio share one synthetic market path, equal starting capital, transaction costs and a common risk cap; each keeps its own cash, shares, equity and operation ledger.

- **Engine:** Godot 4.7.1 stable, GDScript, Compatibility renderer.
- **3D content:** Blender-authored \`.blend\` source plus optimized GLB exports.
- **Reference art:** crops from the three user-provided AI Arena reference boards. Only the character and room crops needed by this project are included.
- **Runtime:** no API keys, broker connection, network access or external runtime dependency.
- **Truth boundary:** all prices, factors, events, research signals and fills are synthetic paper-mode fixtures. Nothing places a real order.

## The seventh investor

The user is a separate personal portfolio, not a seventh AI faction and not an extra AI account in the six-manager roster.

- **Follow strategy:** choose any AI manager and synchronize the personal account's daily target exposure to that manager. The user still has a separate portfolio, cash balance and ledger, but uses the same market, capital, fees, slippage and risk cap.
- **Challenge independently:** select an AI manager to challenge, then set a personal target stock exposure. The personal portfolio rebalances to that user-selected target under the same execution assumptions and risk cap.
- **Compare:** the risk-adjusted leaderboard ranks all six managers plus 我的组合; the personal account also has its own detail, account and trade-ledger views.
- A dedicated gold-accented investor desk is placed in the 3D arena. The user's gain/loss note animation stays local to this seat and never moves money between accounts.

## Run locally

1. Install Godot 4.7.1 stable.
2. Open \`11-ai-arena/godot/project.godot\` in Godot Project Manager.
3. Press **F5** to run the project.
4. To rebuild the 3D source assets, install Blender 4.x and run:

   \`\`\`bash
   blender --background --factory-startup --python blender/build_ai_arena_assets.py
   \`\`\`

   The script writes \`assets/source/ai_arena_assets.blend\` and exports six Agent GLBs, six room GLBs and a banknote GLB into \`assets/generated/\`.

GitHub Actions builds the Blender assets, imports the Godot project, runs headless simulation/world/UI tests, captures desktop and mobile visual-QA screenshots under Xvfb, and publishes downloadable artifacts.

## Python asset checks (isolated virtual environment)

From this folder, create and activate a local environment before running the asset contracts:

```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
python -m unittest discover -s tests -p "test_*.py" -v
python tools/verify_generated_assets.py --require-generated
```

The checks use the Python standard library; Blender 4.x is required only when regenerating the source project and GLB exports. Local virtual environments, Godot import caches, Python bytecode and Blender versioned backup files are excluded from source control and CI packages.

To force a fresh Blender source/GLB rebuild in GitHub Actions, include `[rebuild-ai-arena-assets]` in the commit message. This rebuild is still followed by the full Godot import and test suite.

## Controls

- On an Agent detail, choose 跟随策略 + to synchronize your daily target exposure, or 亲自挑战 to use your own target exposure against that Agent.
- In your portfolio, adjust 个人目标仓位 while in challenge mode. Follow mode hides this control because its exposure is synchronized from the selected Agent.
- 配置实验 opens the run-setup modal; all seven accounts receive the same capital and risk cap.
- The seven-seat leaderboard and JSON export include your personal account and operation ledger.

- Select any Agent card or click a 3D podium.
- **Enter research room** to move into that faction's 3D workspace.
- **Run / Pause / Next day / +5 days / Settle / Reset** control the paper simulation.
- Scrub the replay slider to inspect a prior day; future events remain hidden.
- **Export JSON** saves the complete synthetic run and daily operation ledger to \`user://\`.
- A positive signed daily equity delta sends paper notes upward from that Agent’s own account marker; a negative delta returns notes toward the same Agent’s marker. There is no shared vault or inter-Agent transfer. The effect is visual only and never changes account balances.

## Art and generation notes

The project includes six portrait crops and six research-room background crops taken from the supplied AI-generated reference boards. They are used as image textures behind Blender geometry and in the Agent detail panel. The connected image-generation route in this runtime exposes GPT 2.5 only through a Premium-gated Magnific model, so this implementation does not claim to have generated new GPT images or spend credits. Six replacement-ready scene prompts are in \`IMAGE_GENERATION_BRIEFS.md\`.

## Verification

Run the project tests in Godot:

\`\`\`bash
godot --headless --editor --path . --quit
godot --headless --path . --script res://tests/test_arena.gd
godot --headless --path . --script res://tests/test_world_contract.gd
godot --headless --path . --script res://tests/test_ui_contract.gd
godot --headless --path . --quit-after 4

godot --path . --script res://tests/capture_visual.gd
\`\`\`

See \`GODOT_STATUS.md\` for the latest CI and asset-generation evidence.
