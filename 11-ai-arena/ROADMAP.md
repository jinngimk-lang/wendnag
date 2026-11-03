# ROADMAP

## Phase 0 — Concept validation
- Complete competitive/open-source research.
- Confirm first audience and first vertical.
- Validate the “spectator competition” interaction with 5–8 target users.
- Define a measurable match and a believable demo scenario.
- Gate: users understand the rules and can distinguish simulation from fact.

## Phase 1 — Clickable visual prototype <DONE 2026-10-30>
- Established the premium broadcast-control-room direction from the project design brief.
- Built a responsive, dependency-free HTML/CSS/JS prototype in `prototype/`.
- Implemented Finance, Marketing and Life mode adapters with prompt setup, six Agent cards, seeded event stream, live standings, pause/resume, fast-forward, settlement, report and agent-detail dialogs.
- Added desktop/tablet/mobile browser smoke tests and a test report.
- Gate passed for the front-end prototype: all three modes work, no page/console errors, and 1024/768/390px widths have no horizontal overflow.
- Figma artifact deferred because the connected account currently reports a View seat; HTML/CSS remains the editable source.

## Phase 2 — Finance Arena vertical slice (interaction prototype V0.3.2 completed; production slice pending)
- Interaction prototype V0.3.2: six factions, independent theses, configurable duration, shared synthetic market path, daily context ledger, replay and accounting-linked bidirectional money-flow animation.
- Backend contract V0.1 delivered: exact issuer-resolution outcomes, immutable point-in-time evidence records/snapshots, typed evidence-linked faction outputs, append-only in-memory hash chain and GitHub Actions validation.
- SEC parser V0.1 delivered: joins companyfacts observations to accession acceptance timestamps; defaults license status to review-required; 19 backend tests pass.
- Production slice still pending: compliant SEC fetcher, reviewed/licensed market-data adapter, persisted point-in-time evidence pack, six typed faction workflows, event-triggered policy updates and deterministic paper execution.
- Provider-specific data provenance, SEC accession/accepted-time lineage and point-in-time validation.
- Durable snapshot/event persistence and replay-by-sequence; current hash chain is in-memory only.
- Use experience-v3/REAL_DATA_BLUEPRINT.md as the integration contract; keep demo labels separate from actual issuer research.
- Deterministic paper-trading simulator and versioned scoring.
- Event ledger, SSE stream, leaderboard and replay.
- Gate: reproducible runs, no look-ahead leakage, independent baseline comparison.

## Phase 3 — Marketing Arena pilot
- Small audience cohort simulation and 3–4 channels.
- Platform-specific content drafts and response hypotheses.
- Calibration import for real campaign data.
- Gate: error bands and calibration disclosed; no unverified “predicted views” claims.

## Phase 4 — Life Arena pilot
- Small set of user-controlled life scenarios.
- Transparent assumptions and editable parameters.
- Branching timelines and sensitivity analysis.
- Gate: privacy review, bias evaluation and qualitative user study.

## Phase 5 — Shared platform hardening
- User accounts, saved matches, team workspaces, cost budgets, queueing and observability.
- Versioned simulator/model/prompt provenance.
- Abuse prevention, data governance and operational runbooks.
- Gate: reliability, cost, safety and retention metrics justify scale.
