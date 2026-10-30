# RESEARCH — Open-source patterns and reuse assessment

Research snapshot: 2026-10-30. Repository links and upstream licenses must be rechecked before any code is copied, vendored, or deployed. A conceptual reference does not imply endorsement or production readiness.

## A. High-value references

### 1. TauricResearch/TradingAgents
- URL: https://github.com/TauricResearch/TradingAgents
- Why relevant: specialized analyst roles, bullish/bearish researcher debate, trader, risk managers and portfolio manager; simulated exchange; backtesting; persistent decision logs; checkpoint/resume.
- Patterns to study: structured agent outputs, role separation, common decision context, point-in-time data integrity, portfolio-aware scoring, run isolation, decision ledger and resumable orchestration.
- Product fit: direct reference for Finance Arena's competitor roster and event timeline.
- Caution: upstream explicitly positions it as a research framework, not investment advice. Do not assume its simulated performance predicts real returns. Review its current license, data vendor terms, model costs and backtest assumptions before integration.
- Reuse decision: study architecture and benchmark locally first; do not blindly embed upstream trading logic as a production trading system.

### 2. CAMEL-AI/OASIS
- URL: https://github.com/camel-ai/oasis
- Why relevant: large-scale LLM social interaction simulation, actions such as follow/comment/repost, recommendation mechanisms, dynamic social environments.
- Product fit: Marketing Arena's audience/network layer; helps move beyond a static “estimated views” number toward content exposure, interaction and diffusion dynamics.
- Caution: a social simulator is not the same as an accurate model of TikTok/Reddit/X/Instagram ranking systems. Platform rules, API access, rate limits, terms and actual campaign calibration remain separate work.
- Reuse decision: prototype a small-scale adapter before considering large-scale agent populations. Start with hundreds or fewer simulated personas, measure value, then scale.

### 3. Stanford Generative Agents
- URL: https://github.com/joonspk-research/generative_agents
- Paper: https://doi.org/10.1145/3586183.3606763
- Why relevant: memory stream, reflection, retrieval, planning and emergent social behavior in a sandbox environment.
- Product fit: Life Arena's persistent agents and evolving social context; useful for relationships, workplace dynamics and long-horizon branching.
- Caution: believable behavior is not validated forecasting. Human behavior models can reproduce stereotypes or amplify bias. Avoid presenting emergent stories as probability-calibrated life predictions.
- Reuse decision: adapt memory/planning concepts only after defining a transparent state model and evaluation rubric.

### 4. Microsoft AutoGen
- URL: https://github.com/microsoft/autogen
- Why relevant: multi-agent conversation and tool-use orchestration patterns, agent runtime and extensibility.
- Product fit: useful candidate for agent execution layer or reference for role orchestration.
- Caution: compare current project status, framework generation, license and operational complexity against alternatives before selecting.

### 5. LangGraph
- URL: https://github.com/langchain-ai/langgraph
- Why relevant: graph-based orchestration, durable state, checkpoints, interrupts and human-in-the-loop control.
- Product fit: likely strong candidate for the Arena match state machine and resumable runs.
- Caution: use only if graph semantics and persistence justify the added abstraction; benchmark latency and operational burden.

### 6. MetaGPT
- URL: https://github.com/FoundationAgents/MetaGPT
- Why relevant: role-based agent workflows, artifacts, task decomposition and structured handoffs.
- Product fit: useful reference for role contracts and structured outputs.
- Caution: a software-company simulation workflow is not itself a domain simulator or scoring engine.

## B. Product and research implications

1. Use an explicit state machine, not a free-form group chat.
2. Separate language-model deliberation from deterministic domain calculations.
3. Treat each run as an immutable experiment: inputs, data snapshot IDs, model/version, prompts, tool outputs, random seed, costs and scoring version.
4. Use point-in-time data in financial tests; record publication timestamps, not merely fiscal periods.
5. For marketing, simulate audience cohorts and exposure mechanics before attempting huge populations.
6. For life simulation, persistent memory and reflection are useful but require explicit uncertainty and bias controls.
7. Render event summaries and decisions, not private hidden reasoning traces. Show concise rationales, evidence, dissent and decision deltas.

## C. License and integration gate

Before integration:
- Read the exact upstream LICENSE and any model/data asset licenses.
- Check transitive dependencies, model weights, datasets and API terms separately.
- Pin a release/commit and record source URL, commit, license, modifications and security review.
- Prefer clean-room adapters over copying large code sections when license or dependency provenance is unclear.
- Run a small reproducible benchmark against a baseline and document results.
- Do not introduce a dependency solely because it has high stars.

## D. Additional source links to investigate

- TradingAgents research paper: https://arxiv.org/abs/2412.20138
- OASIS paper/project: https://github.com/camel-ai/oasis
- Generative Agents paper: https://doi.org/10.1145/3586183.3606763
- AutoGen: https://github.com/microsoft/autogen
- LangGraph: https://github.com/langchain-ai/langgraph
- MetaGPT: https://github.com/FoundationAgents/MetaGPT

## E. Research gaps

- Current Figma MCP capabilities and best workflow for a design-system-backed prototype.
- Current social-platform API and advertising-policy constraints for publishing/measurement.
- Market data licensing and point-in-time data vendors for US, HK and A-share equities.
- A robust deterministic scoring engine and anti-leakage benchmark dataset.
- Human-in-the-loop evaluation for life-simulation usefulness and bias.
- UX research: whether users prefer spectating, steering, or comparing after each round.


## F. Repository and license spot-check — 2026-10-30

The following default-branch snapshots and root license files were fetched from the upstream repositories on 2026-10-30. These checks support architectural study only; they are not a substitute for a full dependency, model-weight, dataset, API-terms or legal review.

| Project | Snapshot commit | Root license observed | Current reuse stance |
|---|---|---|---|
| [TradingAgents](https://github.com/TauricResearch/TradingAgents) | `c4544913a14ed3df5f1ed7b9e8483270ce20682a` | Apache-2.0 | Strong Finance reference; study role separation, debate, simulated execution and logs. Pin and benchmark before reuse. |
| [OASIS](https://github.com/camel-ai/oasis) | `ba892e0667eb84b312e4c0e5630f275154bbb98f` | Apache-2.0 | Strong Marketing social-interaction reference; do not equate simulator outputs with actual platform ranking or reach. |
| [Generative Agents](https://github.com/joonspk-research/generative_agents) | `fe05a71d3e4ed7d10bf68aa4eda6dd995ec070f4` | Apache-2.0 | Life simulation memory/reflection reference; research snapshot is old (2023), and believability is not forecast validity. |
| [LangGraph](https://github.com/langchain-ai/langgraph) | `6f2df053f4487ce6ea8decc0d7482c8e46e0f132` | MIT | Candidate durable orchestration layer; evaluate persistence and checkpoint semantics against the simpler explicit state machine. |
| [AutoGen](https://github.com/microsoft/autogen) | `d07c667a3239ea4ab7af62a53b0f4ff205a1f23d` | Root `LICENSE` observed as CC BY 4.0; repository landing page marked archived | Do not adopt as the default new runtime or copy code based on the root license alone. Inspect package-specific licensing and successor guidance first. |
| [Concordia](https://github.com/google-deepmind/concordia) | `95b2e2c1ea85be27dbbf549f652999bad6b4348b` | Apache-2.0 | Additional Life Arena reference for composable generative social simulation; evaluate model validity and cost. |
| [AgentSociety](https://github.com/tsinghua-fib-lab/AgentSociety) | `0ca73abca877b43eefb01f7d3cdf588461489861` | Apache-2.0 | Additional social/urban multi-agent simulation reference; inspect datasets, model dependencies and scale requirements before integration. |

### Consequences for AI Arena

1. Prefer a small, domain-specific simulator and structured Agent contracts over copying a large agent framework wholesale.
2. Use TradingAgents for finance-role inspiration, OASIS for audience interaction patterns, and Concordia / Generative Agents / AgentSociety for social-state and memory concepts.
3. AutoGen's archived status and root license make it a weaker default choice for new integration.
4. No upstream source code has been copied or vendored into this prototype.
