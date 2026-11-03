# Figma-ready specification — Capital Theater V0.2

Native Figma design was **not** created. At last check the connected Figma seat was **View** on Starter. The canonical editable visual source is `index.html` until a Design seat is available.

## Frame hierarchy and constraints

- Desktop reference: 1440 × 1000 (content scrolls). Root Shell is a 72px sticky rail + flexible main column, max-width 1600px. Main has 70px top bar and responsive horizontal padding.
- Tablet: 768px breakpoint. Analytical panels stack; stage pods stay around central vault.
- Mobile: 390px (also tested 320px). Navigation shifts to 64px fixed bottom dock; stage pods occupy four corners, center vault shrinks; financial data cards become a 2×2 grid.
- No intentional horizontal scroll in any tested viewport. Display all ranking values in tabular numerals.

## Component contract

| Component | Variants | Inputs/events |
|---|---|---|
| `ArenaStage` | standby / live / paused / settled | round, competitionSubject, totalPnl, status |
| `AgentPod` | neutral / gain / loss / champion | name, balance, roundDelta, rank |
| `VaultPnl` | neutral / positive / negative | aggregate absolute USD and percentage |
| `MoneyFlow` | inflow / outflow / disabled-reduced-motion | agentId, deltaSign, normalizedIntensity |
| `ReplayBar` | idle / playing / paused / end | `step: 0..6`, play, pause, scrub, finish, reset |
| `LeaderboardRow` | 1st–4th | returnPct, drawdownPct, riskScore |
| `EventCard` | routine / positive / risk | title, short summary, round |
| `RuleDisclosure` | closed / modal | dataLabel, formula, limits |

## Core tokens

- Background: `#080d13`, panel: `#121b24`, fine rule: `#2b3640`.
- Gold `#e9c78d`: stage authority, trim, vault, winner.
- Positive green `#62edb0` and negative salmon `#fa887e`: account state. Do **not** make losses green via stylistic effects.
- White `#f4f3ed`, secondary text `#a2aeb7`.
- Fonts: local system fallback sans and tabular monospace. No external font or unlicensed asset dependency.
- Motion: per event, money flies 0.84–1.5s; reduced-motion uses instant numerical update and no money particles.

## Image generation considerations

Use an original, layered vault/stage set that avoids bank trademarks and reproductions of real banknotes. Keep legible scores in HTML/Figma text layers; do not bake digits into generated images. Prefer photo-like surface textures as backgrounds only, with transparent masks above. Validate realistic reflections, key light, scale, original graphic copyrights and mobile crop before shipping.

## Review checklist

Capture desktop 1440px, mobile 390px, first profit, first loss, settled champion, and an empty/paused state. Compare Figma screenshot 1:1 to real browser screenshot. Reject a redesign if the gold/green/red attraction makes users mistake hypothetical dollars for real money.