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

V0.1 `prototype/` demonstrates all three arenas; V0.2 `experience-v2/` tests the Capital Theater visual direction; V0.3.2 `experience-v3/` adds the Finance Research Lab flow: six faction research views, configurable simulation days, synthetic market/sentiment changes, independent paper portfolios, daily operation logs, replay and accounting-linked cash-flow motion. `backend/` now contains a provider-agnostic evidence contract core plus a no-network SEC submissions/companyfacts parser that anchors facts to filing acceptance timestamps and defaults to license review required; it does not include a live fetcher or data service. No real company data, live LLM workers, broker execution, ad buying, auto-publishing, personal data collection or life-outcome prediction is performed.

See `IMPLEMENTATION.md` for the original front-end architecture, `experience-v3/ARCHITECTURE.md` for the Finance research-to-simulation contract, and `experience-v3/TEST_REPORT.md` for current browser verification.

## Context recovery

At the start of every future AI Arena session, read in this order:
1. `AGENTS.md` at repository root;
2. `11-ai-arena/PROJECT.md`;
3. `11-ai-arena/STATUS.md`;
4. `11-ai-arena/CHECKPOINT.md`;
5. relevant research/design/architecture files.

Update STATUS and CHECKPOINT after material decisions, phase changes, meaningful implementation, or before context becomes unwieldy. Repository evidence outranks chat recollection.
