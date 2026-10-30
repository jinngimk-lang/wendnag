# AI Arena — Multi-Agent Simulation & Competition Platform

> Think. Compete. Simulate.

AI Arena is a proposed product platform where users submit a company, product, campaign, or life decision and watch specialized AI agents compete inside a shared, rule-governed simulation. The product sells an observable decision process—not merely a generated answer.

## Three arenas

1. **Finance Arena** — company research, competing investment theses, historical/paper trading, portfolio scoring and replay.
2. **Marketing Arena** — creative strategy competition, platform-specific content, audience/network simulation, scenario-based reach and conversion estimates.
3. **Life Arena** — parallel life-path scenarios across career, city, relationships, finances and lifestyle, with branching decisions and long-horizon consequences.

## Product thesis

One shared Arena Engine; three domain-specific worlds. Every match has:
- a user-defined question and explicit rules;
- independent competitors with distinct objectives and constraints;
- a deterministic or explicitly stochastic environment;
- observable events and evidence;
- transparent scoring and a replayable decision ledger.

## Workspace map

- `PROJECT.md` — product charter, principles and scope.
- `STATUS.md` — current state, decisions, open questions and next actions.
- `RESEARCH.md` — external projects, methods, references and evaluation.
- `ARCHITECTURE.md` — shared engine, domain adapters, data contracts and safety.
- `DESIGN.md` — interaction principles, visual system and screen concepts.
- `ROADMAP.md` — phased build plan and acceptance gates.
- `CHECKPOINT.md` — compact recovery point for long-context sessions.

## Current phase

Concept research and product definition. This is not yet a production system and no real trading, ad buying, or personal-life outcome prediction is performed. The first prototype should demonstrate a transparent, replayable **simulated** match.

## Context recovery

At the start of every future AI Arena session, read in this order:
1. `AGENTS.md` at repository root;
2. `11-ai-arena/PROJECT.md`;
3. `11-ai-arena/STATUS.md`;
4. `11-ai-arena/CHECKPOINT.md`;
5. relevant research/design/architecture files.

Update STATUS and CHECKPOINT after material decisions, phase changes, meaningful implementation, or before context becomes unwieldy. Repository evidence outranks chat recollection.
