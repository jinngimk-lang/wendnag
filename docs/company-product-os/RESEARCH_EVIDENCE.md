# Company Product OS — Research Evidence Notes

Date: 2026-09-18

This file records external evidence used by the Company Product OS blueprint. Numbers are intentionally accompanied by scope/caveats to avoid treating case studies as universal causal estimates.

## 1. Why familiarity and consistency matter

### Apple Human Interface Guidelines — Design Principles (2026)

Source:
https://developer.apple.com/design/human-interface-guidelines/design-principles

Relevant guidance:
- “Familiarity” means building on concepts people already know.
- Apple explicitly advises keeping visuals and interactions consistent.
- It states that consistency helps people learn faster and gives them confidence that new interactions will work as expected.
- Apple also emphasizes agency, recoverability, privacy/transparency and accessibility.

Implication for Company Product OS:
Cross-product consistency should cover **behavior and semantics**, not only appearance. The operating layer should encode predictable actions, feedback, recovery, permissions and cross-platform context.

## 2. Design-system productivity evidence

### Figma — Measuring the value of design systems (2019)

Source:
https://www.figma.com/blog/measuring-the-value-of-design-systems/

Reported result:
Participants with access to a relevant, current design system completed the experimental objective **34% faster** than without it.

Important caveat:
Figma explicitly notes that the system was directly applicable and up to date, so the result should be treated as an optimistic/upper-bound-style context rather than a universal productivity multiplier.

Implication:
A good Company Product OS should remove repetitive micro-decisions and free people/agents to focus on product-specific decisions.

### Figma — New business case for design systems (2026)

Source:
https://www.figma.com/blog/the-new-business-case-for-design-systems/

Selected company-reported examples:
- Freshworks credited its new design system with a **28% reduction in customer-service costs**.
- Figma reports that design systems are increasingly linked not just to design speed but to customer outcomes, adoption, retention, support and revenue.

Caveat:
These are company/design-system case studies, not controlled cross-industry causal estimates.

## 3. Multi-product consistency and operational effects

### IBM Carbon — About Carbon / Who uses Carbon

Sources:
https://carbondesignsystem.com/all-about-carbon/what-is-carbon/
https://carbondesignsystem.com/all-about-carbon/who-uses-carbon/

Carbon’s stated rationale:
- Product experiences built on the same foundation reduce cognitive load, errors, questions, training and onboarding needs.
- Learning can transfer across products/spaces.
- Designers get a resolved foundation so effort can shift from universal decisions to product-specific decisions.

This directly mirrors the Company Product OS thesis, but Company Product OS extends beyond the traditional design-system boundary into company ontology, technical philosophy, agent execution and automated evaluation.

### IBM Cloud + Carbon 10 / Cloud PAL case study

Source:
https://v10.carbondesignsystem.com/case-studies/consistency-in-the-cloud/

Reported case-study outcomes:
- 22 Cloud patterns covered **90% of Cloud UIs**.
- NPS reportedly improved **57%** in the first three months after transition.
- Average time to provision a service improved **4%**.
- Support tickets decreased **18%** in areas where teams implemented and followed the Carbon 10 / Cloud PAL guidance.
- IBM Cloud estimated design/development teams saved **2,000 hours per pattern**, described as about **80% more efficient** than designing/coding screens from scratch.
- 116 of 155 services had adopted Carbon 10 by January 2021; 21 had approved exceptions.

Caveat:
This is an IBM case study around a major coordinated migration and should not be treated as a guaranteed outcome for other organizations. It is especially valuable as evidence for:
- governance,
- mandatory vs exception rules,
- reusable coded patterns,
- top-down adoption,
- coverage metrics,
- explicit conformance reviews.

## 4. AI makes implementation cheaper — but organizational foundations matter more

### Peng et al. / Microsoft Research — GitHub Copilot controlled experiment

Source:
https://www.microsoft.com/en-us/research/publication/the-impact-of-ai-on-developer-productivity-evidence-from-github-copilot/
Paper:
https://arxiv.org/abs/2302.06590

Reported result:
The Copilot treatment group completed a narrow JavaScript HTTP-server task **55.8% faster** than the control group.

Caveat:
This was a specific programming task and does not imply all software delivery becomes 55.8% faster. It is useful as evidence that code production can be materially compressed, increasing the relative importance of architecture, product decisions, organizational standards and validation.

### Google DORA 2025 — State of AI-assisted Software Development

Source:
https://research.google/pubs/dora-2025-state-of-ai-assisted-software-development-report/

Research base:
- more than 100 hours of qualitative data
- survey responses from nearly **5,000 technology professionals**

Key framing:
DORA describes AI as an **amplifier**: it magnifies the strengths of high-performing organizations and the dysfunctions of struggling ones.

Implication:
Agentic product generation should not merely add more generation capacity. It needs a strong company-level operating substrate that tells agents which decisions are stable, which rules are binding, and how outputs are validated.

### McKinsey — Economic potential of generative AI

Source:
https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/the-economic-potential-of-generative-ai-the-next-productivity-frontier

Estimate:
McKinsey estimated the direct impact of generative AI on software-engineering productivity could equal **20–45% of current annual spending** on the function, primarily through activities such as initial code drafts, correction/refactoring, root-cause analysis and system design.

Caveat:
This is an economic model/estimate, not a measured universal productivity gain.

## 5. Machine-readable design decisions are becoming standardized

### Design Tokens Community Group — stable 2025.10 specification

Sources:
https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/
https://www.w3.org/community/reports/design-tokens/CG-FINAL-format-20251028/

Relevant capabilities:
- first stable Design Tokens format (2025.10)
- vendor-neutral exchange of design decisions
- aliases/references and hierarchy
- theming and multi-brand support
- cross-platform use across web, iOS, Android and Flutter

Important status note:
The format is a W3C Community Group final report and considered stable, but it is **not a W3C Recommendation/standards-track specification**.

Implication:
Company Product OS should use interoperable tokens where possible rather than inventing an incompatible visual-token format.

## 6. Machine-readable rules and integration building blocks

### JSON Schema

Source:
https://json-schema.org/specification

Use:
Represent and validate Company Genome, rule objects, product briefs, evidence records and evaluator results.

### Open Policy Agent (OPA)

Source:
https://www.openpolicyagent.org/docs

Use:
Policy-as-code engine for hard enforceable constraints such as security, deployment, data residency, forbidden patterns, entitlement or architecture decisions.

### Model Context Protocol (MCP)

Sources:
https://docs.anthropic.com/en/docs/mcp
https://blog.modelcontextprotocol.io/posts/2026-07-28/

Use:
An optional standardized integration boundary through which agents can access Company Product OS resources/tools and connected systems. The 2026-07-28 MCP specification update also continues to evolve authorization and caching behavior.

Company Product OS should **not depend on MCP exclusively**. The internal canonical model should remain protocol-agnostic and may be exposed via MCP, APIs, SDKs, files or IDE/agent plugins.

## Research synthesis

The external evidence supports five design conclusions:

1. **Consistency is a usability primitive**, not cosmetic polish.
2. **Reusable resolved decisions can produce substantial speed gains**, especially when the system is relevant and adopted.
3. **Cross-product patterns can lower training/support burden and enable learning transfer**.
4. **AI increases generation throughput, which makes organizational/product coherence more important, not less**.
5. **The technical pieces now exist** to make company philosophy executable: machine-readable tokens, schemas, policy engines, component libraries and agent integration protocols.

The unproven part—and therefore the innovation opportunity—is integrating these pieces into one company-level executable product ontology that can be extracted from evidence, inherited by agents, compiled into new products, evaluated automatically, and evolved through validated product learning.
