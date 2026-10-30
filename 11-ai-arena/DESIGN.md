# DESIGN — Arena Experience

## 1. Experience goal

The user should feel they have started a live event. The screen must communicate:
- what is being competed over;
- who the competitors are;
- what phase the match is in;
- what just happened and why it matters;
- how the score is changing;
- what evidence supports the result.

Visual excitement must remain subordinate to legibility and trust.

## 2. Core screens

1. **Arena home:** three vertical doors, recent matches, featured match and a single prompt-first CTA.
2. **Match setup:** prompt, preset, timeframe/resources, scoring rules and simulation disclosure.
3. **Live arena:** competitor roster, central stage/world, event timeline, score ticker, round progress and pause/inspect controls.
4. **Competitor profile:** strategy, evidence, actions, constraints, performance curve and history.
5. **Results:** winner, podium, metric breakdown, uncertainty, benchmark, notable turning points and replay.
6. **Replay / branch:** scrub the timeline, inspect state diffs, branch from a selected event and rerun with a changed parameter.

## 3. Interaction principles

- One obvious primary action: **Start Arena**.
- Keep the first run friction low; advanced parameters live behind “Match rules”.
- Introduce agents visually with distinct but professional identities; avoid cartoon mascots as the default.
- Show meaningful state transitions, not decorative fake activity.
- Use suspense through delayed reveal of standings, round milestones and event cards—not deceptive loading.
- Every chart has units, date window, source and simulation/observed label.
- Provide pause, skip-to-result and replay. Do not force users to watch a long simulation.
- Accessible motion: reduced-motion mode, keyboard navigation, contrast and readable data labels.

## 4. Visual direction

Working direction: **premium broadcast control room meets strategy game**.
- Dark graphite/navy base, restrained luminous accents.
- Distinct vertical accent systems: Finance = amber/gold; Marketing = electric cyan; Life = violet.
- Large editorial typography for match title and winner; compact tabular numerals for scores.
- Layered cards, subtle grid, thin borders, status lights and purposeful motion.
- Central arena visualization: finance portfolio arena / social network field / branching life timeline.
- No overdone neon, cluttered sci-fi HUDs or gratuitous glassmorphism.

## 5. Figma workflow

Use Figma for the design system, component variants, responsive layout and prototype flow—not as the simulation runtime.
Recommended component set:
- ArenaHeader, ModeCard, MatchPrompt, RuleDisclosure
- AgentCard, AgentStatus, AgentEvidence, AgentAction
- LiveEvent, RoundProgress, ScoreTicker, Leaderboard
- PortfolioCurve, AudienceNetwork, LifeTimeline
- ResultPodium, MetricBreakdown, ReplayScrubber, BranchControl

Build one high-fidelity desktop live-match screen first, then mobile adaptation. Use realistic but clearly labeled demo data. Connect Figma MCP only after selecting a visual direction and creating/choosing a target Figma file; inspect and verify rendered screenshots at each milestone.

## 6. Visual prototype status

The first reviewable direction is implemented in `prototype/` as a responsive, dependency-free HTML/CSS/JS application.

- Chosen direction: premium broadcast control room meets strategy game.
- Shared visual language: graphite/navy surfaces, editorial headline, tabular scores, fine rules, restrained motion and clear simulation labels.
- Domain accents: Finance = amber/gold; Marketing = electric cyan; Life = violet.
- Primary flow: prompt → agent reveal → live event stream → standings → settlement → report / replay.
- Desktop and mobile layouts have been browser-checked; details are in `prototype/TEST_REPORT.md`.
- The connected Figma account currently reports a View seat, so no editable Figma file was created. Keep the HTML/CSS source as the current design artifact; create a Figma file when an edit-capable seat or target file is available.
