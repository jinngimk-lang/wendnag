# AI Investment Arena — Godot 3D Experience Design

**Status:** implementation target for the Godot client; this is an additive native client, not a destructive rewrite of the existing HTML research lab.

## Product intent

The user should feel that six independent investment managers are physically present in a shared competition venue. Each faction owns a recognizable person, a dedicated research environment, a separate account and a decision history. The user can move between the arena and a faction's room, inspect its thesis and risk controls, advance the shared market one day at a time, watch signed P&L become physical cash-note motion, and replay prior decisions.

## Binding product invariants

1. Six stable faction IDs: \`value\`, \`growth\`, \`trend\`, \`quant\`, \`sentiment\`, \`macro\`.
2. One shared synthetic market path and one common execution-cost model.
3. Six distinct account objects with separate cash, shares, equity, drawdown and append-only operation ledgers.
4. The same start capital and risk cap for every faction.
5. Paper-only. No live brokerage, real orders, live company research or external LLM workers are implied.
6. Money animation is driven by signed account equity change and never modifies accounting state. Each animation remains local to the same Agent account; no central vault, shared cash pool or inter-Agent transfer exists.
7. Replay can only inspect days already simulated; it cannot reveal future events or ledger entries.
8. Every decision exposes a concise reason, target exposure, price, fee, slippage and market context; no hidden chain-of-thought is exposed.

## Chosen architecture

- **Godot 4.7.1 / GDScript** owns the native runtime, input, responsive UI, 3D world, simulation controls and replay.
- **Blender 4.x** is the editable source of truth for six Agent busts, six room sets, six per-Agent account markers and the banknote prop. Each asset is exported as GLB for Godot.
- **Image textures** use the user's supplied reference boards: six portrait crops and six room-scene crops. Each room GLB includes its matching environment backplate texture; Godot also uses portrait crops in the detail panel.
- **One 3D viewport** switches between the central arena and the selected faction room. UI remains a separate Control layer.
- **Deterministic simulation** is a GDScript module with seeded synthetic market factors, six independent portfolios, daily operations, account snapshots and replay-safe event access.
- **GitHub Actions** builds Blender assets, imports the Godot project, runs headless simulation tests and packages the project.

## Interaction map

### Arena
- A shared-market information display, six illuminated Agent podiums and a cinematic financial-lab environment. Each podium has its own account marker; there is no central capital vault.
- Six faction cards show portraits, identity, account equity, P&L, rank and latest decision.
- Top metrics show shared price, market sentiment, macro liquidity, sector momentum and volatility.
- Live controls: run, pause, next day, next five days, settle, reset and replay scrubber.
- Signed-P&L paper notes move only between one Agent’s own account marker and its local podium: gains rise from that account; losses return to the same account marker. No inter-Agent movement or shared vault.

### Agent research room
- A distinct 3D room for the selected faction, not a recolored generic card.
- Character is placed in the room with its portrait and faction-specific set dressing.
- Research tab: thesis, supporting signals, bear challenge, invalidation and risk officer.
- Account tab: cash, shares, equity, exposure, return and drawdown.
- Ledger tab: chronological BUY / SELL / HOLD decisions and fill details.
- Return-to-arena action preserves selected faction and current simulation state.

### Responsive behavior
- Desktop (>= 1120 px): left navigation, 3D stage, six cards and right Agent inspector.
- Tablet (680–1119 px): compact navigation and overlay Agent inspector.
- Mobile (< 680 px): compact rail, two-column faction cards, hidden inspector until requested and vertically stacked content.
- Reduced-motion mode disables bill travel and non-essential camera movement while retaining accounting feedback.

## Visual language

- Institutional cinematic 3D, not a flat dashboard and not a cartoon mobile game.
- Midnight graphite, dark navy and brushed-metal surfaces; restrained faction accents:
  - Value: champagne gold.
  - Growth: emerald.
  - Trend: glacier blue.
  - Quant: amethyst.
  - Sentiment: warm amber.
  - Macro: ice cyan.
- Realistic proportions, readable silhouettes, believable desk/monitor/room geometry and clear depth layers.
- UI remains legible over 3D scenes; important numbers use tabular numerals and high-contrast surfaces.

## Image-generation boundary

The connected image tool in this runtime exposes GPT 2.5 through a Premium-gated route. No new paid image-generation call is made in this milestone. The supplied AI-generated reference boards are cropped into reusable room/portrait textures, and replacement prompts are supplied in \`IMAGE_GENERATION_BRIEFS.md\`. Blender sets provide real geometry and depth around those images; they are not presented as newly GPT-generated art.

## Explicitly rejected alternatives

- Continuing to patch the HTML dashboard as the primary runtime: it does not satisfy the requested native Godot deployment.
- Replacing the simulator with visual-only animations: the market, account and ledger remain the source of truth.
- Using a shared capital pool: each Agent's portfolio remains independent.
- Generating six expensive 3D characters through a paid external model service: Blender procedural source assets are editable and reproducible without per-model generation charges.
- Claiming the generated reference crops are newly created images: their provenance is documented as user-supplied references.

## Acceptance criteria

- Godot 4.7.1 opens and runs \`project.godot\` without parse/import errors.
- Six distinct Agent portraits and room backgrounds load.
- Six Blender GLBs and a Blender source project are generated by CI.
- Selecting an Agent, entering/exiting its room, and switching research/account/ledger views work.
- Simulation advances, pauses, fast-forwards, settles and resets.
- Each day creates exactly six independent account operations.
- Positive/negative signed equity deltas trigger opposite cash-note directions; animation never changes account balances.
- Replay clamps to simulated history and hides future events.
- Responsive layout modes are verified at 1600, 1024, 768, 390 and 320 logical widths.
- JSON export includes simulator version, seed, synthetic-data declaration, assumptions, six account histories and operation ledger.
