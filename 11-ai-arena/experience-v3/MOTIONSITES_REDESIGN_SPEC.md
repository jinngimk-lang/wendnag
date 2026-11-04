# AI Arena / Finance Research Lab — MotionSites Redesign Spec V0.3.3

## 0. Brief

Redesign the existing Finance Research Lab as a complete, single-file research-and-paper-trading workspace for users who want to compare six independent investment theses under one shared synthetic market. This is an application dashboard, not a marketing landing page; the first viewport must establish the subject, disclose the simulation boundary, and make the research action obvious without hiding the rest of the workflow.

**Mood:** nocturnal, precise, composed.  
**Signature:** a central aggregate P&L vault surrounded by six independent faction portfolios. On a one-day advance, paper bills and amount chips travel between the vault and a faction only when that faction's signed daily equity delta warrants it. The animation remains a view of accounting data, never a source of accounting data.  
**Output:** one dependency-free index.html, with inline CSS and JS; no npm, remote font, CDN, image or API dependency.

## 1. Reference calibration

The visual study used three MotionSites examples as calibration rather than templates:

- [Halo / USD Halo](https://motionsites.ai/?prompt=halo-usd-landing): fintech restraint, strong typographic hierarchy and controlled use of one accent.
- [Intelligence Layer](https://motionsites.ai/?prompt=intelligence-layer): dark infrastructure palette, precise mono metadata and disciplined contrast.
- [Agent Wave](https://motionsites.ai/?prompt=agent-wave): technical information hierarchy and staged entrance motion.

The product keeps its own six-faction information architecture and original accounting-linked capital-flow interaction. No example's brand, copy, asset, or exact composition is reused. A moving video was deliberately rejected: this is a dense analytical tool, and a video plane would compete with charts, controls and ledger readability. The signature motion is already supplied by the real simulation state.

## 2. Stack and typography

- Semantic HTML5; CSS variables; vanilla JavaScript; existing deterministic simulation engine preserved.
- Display and UI: Inter, Noto Sans SC, PingFang SC, system fallbacks; no remote font loading, preventing layout shift and preserving offline use.
- Metadata: system monospace stack for indices, prices, run IDs, factor values and timestamps.
- Numeric fields use tabular figures where the browser font supports them. Body copy stays 11–13px in dense analytical modules; primary headings scale with clamp().

## 3. Colour and surfaces

| Token | Value | Use |
|---|---|---|
| Background | #080d13 | page and first paint |
| Surface | #111b25 / #15232e | panels and nested cards |
| Foreground | #f2f4f2 | primary text |
| Muted | #91a1ab | supporting text |
| Line | rgba(164,184,195,.16) | dividers and outlines |
| Gold | #e9c78d | primary action, active state, vault edge |
| Green / red | #70dfad / #ff887e | positive / negative accounting state |

Faction accents remain semantic and local to their cards and portfolio pods; they are not promoted into unrelated controls. Panels share one dark-glass material: restrained gradient fill, 1px low-alpha outline, 18px outer radius, a single inset top highlight and a soft shadow. Buttons are consistent 999px pills. No purple glow-orbs, random stock images, decorative placeholder blocks or heavy glass blur.

## 4. Desktop composition

- Shell: 76px vertical navigation rail + flexible application column. Header: 68px high, sticky, translucent graphite with an 18px backdrop blur.
- Content: max-width 1600px; horizontal padding clamp(22px,4.2vw,68px); vertical start 38px.
- Hero: two-line Chinese headline, 34–58px, 1.08 line-height, -0.045em tracking; one muted paragraph; compact mono summary on a gold hairline at right. The headline carries the product point of view; no marketing badge stack.
- Setup: one bordered surface with five aligned controls. Input/select height 46px; labels 9px mono; CTA uses a warm gold inverse finish. A separate left-accent disclosure keeps the synthetic-data boundary visible.
- Research: three-column grid at wide widths, two columns on compact desktop/tablet, one column on phones. Each faction card uses its own accent only on the top rule, icon and role labels. Thesis, signals, role templates and expandable risk/trigger details remain legible.
- Cross-examination: three-column comparison panel with hairline dividers.
- Simulation: the arena is the main visual anchor. Six portfolio pods occupy a 3×3 composition around a 190–230px vault; the center grid is deliberately quiet. A subtle 38px technical grid and low-opacity orbit ring support spatial orientation without competing with numbers.
- Market factors, equity curve, events and risk standings form a two-column analytical layer. The ledger is a full-width table with sticky headings and its own horizontal scroll container.

## 5. Interaction and motion

The existing IDs, event handlers, simulator, replay cursor, filters, export schema, accounting and cash-flow algorithm remain intact. UI animation never changes simulation state.

- First load: header/hero/setup use a fail-safe blur-rise (translateY(18px), blur(5px), 0.82s, cubic-bezier(.16,1,.3,1), stagger 80–200ms). The rest state is visible if animation does not run.
- Section reveal: 0.72s ease-out when a hidden research/simulation section becomes visible.
- Portfolio vault orbit: a low-contrast dashed ring, 42s linear rotation. It is removed under reduced motion.
- Cash-flow notes: existing 1.15s bill flight and amount-pop; direction, amount and bill intensity remain derived from signed daily equity delta. Multi-day jumps and replay scrubs do not invent intermediate transfers.
- Hover transitions: 200–240ms; cards lift at most 3px; active controls compress to 0.98 scale. Keyboard focus uses a 2px gold outline.
- prefers-reduced-motion: reduce disables nonessential transitions and animation while preserving final visual states.

## 6. Responsive rules

- ≥1180px: five-column setup, three research columns, three-column portfolio arena.
- 851–1179px: setup becomes four columns with a full-row CTA; research becomes two columns.
- 701–850px: 60px rail; setup two columns; arena becomes vault-first two-column pods.
- ≤700px: fixed 62px bottom navigation, 58px header, single-column research and debate, two-column setup, two-column arena pods, two-column market metrics and a scroll-contained ledger.
- ≤380px: setup and factor controls become one column; demo pill is hidden; pod type is reduced without clipping.
- Root uses overflow-x: clip; safe-area bottom padding is applied to the mobile navigation.

## 7. Acceptance and trust boundary

The browser must remain free of page/console errors and horizontal overflow at 1440, 1024, 768, 390 and 320px. The six factions, 18 role templates, one-day/five-day/settle/reset/replay controls, daily BUY/SELL/HOLD ledger, deterministic rerun, JSON export and 252-day / 1,512-decision stress run must continue to pass.

**Product truth is unchanged:** V0.3.3 remains a synthetic local prototype. Company text is a label and deterministic seed; prices, reports, events, factors, fills and returns are synthetic. The six strategies are local deterministic rules, and 18 role cards are workflow templates, not live LLM calls. No licensed market data, actual issuer research, broker, or real orders are connected. Results are not a historical backtest, forecast or investment advice.