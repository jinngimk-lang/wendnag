# AI Investment Arena — Godot 3D Client

This folder is the native Godot client for the Finance Arena. Open \`project.godot\` with **Godot 4.7.1 stable**.

## What this build is

A spectator-first 3D paper-trading arena with six visibly different investment personas, six dedicated research rooms, six independent paper accounts, a shared synthetic market, an auditable daily decision ledger, replay controls and signed-P&L banknote motion.

- **Engine:** Godot 4.7.1 stable, GDScript, Compatibility renderer.
- **3D content:** Blender-authored \`.blend\` source plus optimized GLB exports.
- **Reference art:** crops from the three user-provided AI Arena reference boards. Only the character and room crops needed by this project are included.
- **Runtime:** no API keys, broker connection, network access or external runtime dependency.
- **Truth boundary:** all prices, factors, events, research signals and fills are synthetic paper-mode fixtures. Nothing places a real order.

## Run locally

1. Install Godot 4.7.1 stable.
2. Open \`11-ai-arena/godot/project.godot\` in Godot Project Manager.
3. Press **F5** to run the project.
4. To rebuild the 3D source assets, install Blender 4.x and run:

   \`\`\`bash
   blender --background --factory-startup --python blender/build_ai_arena_assets.py
   \`\`\`

   The script writes \`assets/source/ai_arena_assets.blend\` and exports six Agent GLBs, six room GLBs and a banknote GLB into \`assets/generated/\`.

GitHub Actions builds the Blender assets, imports the Godot project, runs headless simulation tests and publishes a downloadable package artifact.

## Python asset checks (isolated virtual environment)

From this folder, create and activate a local environment before running the asset contracts:

```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
python -m unittest discover -s tests -p "test_*.py" -v
python tools/verify_generated_assets.py --require-generated
```

The checks use the Python standard library; Blender 4.x is required only when regenerating the source project and GLB exports. Local virtual environments, Godot import caches, Python bytecode and Blender versioned backup files are excluded from source control and CI packages.

## Controls

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
godot --headless --path . --quit-after 4
\`\`\`

See \`GODOT_STATUS.md\` for the latest CI and asset-generation evidence.
