# STATUS — 2026-10-30

## Current phase
Concept definition and reference research. No application code or Figma artifact has been created yet.

## Repository state
- Parent repository: `jinngimk-lang/wendnag`
- Existing main branch at start: `6070ad2f4ee07e37a1d293cc243f59254dba34b2`
- Work branch: `feat/ai-arena-concept-research`
- Dedicated folder: `11-ai-arena/`
- Existing BP project files remain untouched.

## Completed
- Read root `AGENTS.md`, `PROJECT.md`, `STATUS.md`, and `README.md`.
- Confirmed the repository is primarily the Aegiston BP workstream; new product work must remain isolated.
- Defined the three verticals and common Arena Engine.
- Researched TradingAgents, OASIS, Generative Agents, AutoGen, LangGraph and MetaGPT as candidate references.
- Recorded architecture, UX, roadmap, safety and context recovery principles.

## Important product decisions
- “Watch a competition unfold” is the core differentiated interaction.
- Finance first: historical/paper trading only, with point-in-time data and risk-aware scoring.
- Marketing: platform-specific audience/network simulation, not ungrounded view-count generation.
- Life: editable branching scenarios, not deterministic personal predictions.
- Shared orchestration, event ledger, simulator adapters, scoring and replay.
- No real-world side effects in MVP (no live trades, paid ad spend or auto-publishing).

## Current blockers / limitations
- Product Design plugin's full workflow is not supported in standard ChatGPT chat. For the visual ideation/build workflow, switch to Work mode and continue with this repository context. No prototype should be claimed before that.
- No Figma file has been selected or created.
- Market-data sources, platform APIs, and data/model licenses still require due diligence.
- The current research is an initial shortlist, not a complete competitor landscape.

## Next actions
1. Validate target audience and first use case; current recommendation is Finance Arena for measurable outcomes.
2. In Work mode, run Product Design visual ideation and select one of three directions.
3. Build an HTML prototype of setup → live competition → result → replay.
4. Inspect TradingAgents/OASIS source/license/dependency details at pinned commits before any code reuse.
5. Define deterministic match protocol and benchmark fixtures.

## Session update policy
After each meaningful decision, update this file and CHECKPOINT.md. Keep unresolved items explicit.
