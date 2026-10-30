# ARCHITECTURE — Shared Arena Engine

## 1. Core services

- **Match API:** create, configure, pause, resume, cancel and retrieve matches.
- **Orchestrator:** deterministic state machine controlling rounds, agent scheduling, budgets and timeouts.
- **Agent Runtime:** isolated agent workers with typed inputs/outputs and scoped tools.
- **Domain Simulator:** deterministic state transitions and domain-specific rules.
- **Data Gateway:** source adapters, timestamps, provenance, cache and licensing metadata.
- **Event Ledger:** append-only event log with run IDs, sequence numbers and replay support.
- **Scoring Service:** versioned metrics, eligibility rules, tie-breaking and awards.
- **Presentation Gateway:** WebSocket/SSE event stream and normalized view models.
- **Artifact Store:** reports, charts, content drafts and simulation snapshots.

## 2. Match lifecycle

`DRAFT → VALIDATING → READY → RUNNING → PAUSED → SETTLING → COMPLETED`

Terminal alternatives: `FAILED`, `CANCELLED`, `EXPIRED`.

Each transition must be validated. A match cannot settle until all required competitor actions are resolved or explicitly marked as timed out/forfeited.

## 3. Agent contract

Every competitor declares:
- stable agent ID and version;
- role, objective and strategy description;
- allowed tools and data sources;
- starting resources and per-round budget;
- required structured output schema;
- constraints and risk limits;
- action proposal and evidence references;
- confidence/uncertainty and known limitations.

Agents do not directly mutate the authoritative world state. They submit typed actions; the simulator validates and applies them.

## 4. Event schema (conceptual)

- match_id
- sequence
- timestamp_simulated and timestamp_wall
- round_id
- actor_id
- event_type
- input_snapshot_id
- action_payload
- evidence_refs
- state_before_hash / state_after_hash
- scoring_version
- visibility (public summary / audit detail)

The event ledger is the source for live UI and replay. The UI should never invent progress independently of backend events.

## 5. Domain adapters

### Finance adapter
- market data, corporate filings, news and sentiment sources;
- point-in-time snapshots and market calendars;
- execution simulator with spread, fees, slippage, liquidity and position limits;
- portfolio state and benchmark;
- scoring: returns, risk, consistency and attribution.

### Marketing adapter
- content and audience schema;
- platform policy/ranking abstractions;
- audience cohorts, graph edges and behavior profiles;
- exposure, impression, interaction and conversion transitions;
- content fatigue, negative feedback and moderation events;
- scenario distributions and calibration metadata.

### Life adapter
- starting-state profile with explicit optional fields;
- time-step model (month/quarter/year);
- state variables: skills, career, income, expenses, savings, housing, relationships, time and wellbeing proxies;
- external shocks and uncertain transitions;
- branch points and sensitivity analysis;
- strict privacy controls and non-deterministic scenario labeling.

## 6. Scoring contract

Every metric includes:
- metric ID and version;
- formula or deterministic evaluator;
- source fields and unit;
- aggregation window;
- missing-data behavior;
- eligibility and tie-breaking rules;
- uncertainty/calibration label.

Never compare competitors with different resource budgets or information cutoffs unless the match is explicitly a handicap format.

## 7. Frontend event model

The browser subscribes to normalized events:
- `agent_joined`
- `research_started`
- `evidence_added`
- `thesis_submitted`
- `challenge_raised`
- `action_proposed`
- `action_accepted`
- `world_event`
- `score_updated`
- `round_completed`
- `match_settled`

Use these events to drive the stage, agent cards, timeline, progress, charts and leaderboard. Avoid fake token-by-token “thinking” animation. Stream useful milestones and concise summaries.

## 8. Recommended implementation direction

Prototype:
- Frontend: React/Next.js + TypeScript; charts via ECharts or lightweight SVG; motion via Framer Motion / CSS.
- API: Python FastAPI or TypeScript service; choose based on simulator ecosystem.
- Orchestration: evaluate LangGraph for durable graph execution/checkpoints; keep match state and domain transitions explicit.
- Storage: PostgreSQL for matches/events/results; object storage for artifacts; Redis or a queue for worker dispatch if required.
- Streaming: SSE for one-way match events; WebSocket only if real-time bidirectional controls are required.
- Observability: structured logs, traces, per-agent token/cost/time budgets and simulator version tags.

Do not prematurely adopt all components. First deliver one end-to-end match with replay using seeded fixtures.
