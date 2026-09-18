# Company Product OS — Context Checkpoint

Date: 2026-09-18
Branch: `concept/company-product-os-20260918`

## User intent

Build a practical concept and implementation blueprint for a **company-native product generation system**: instead of repeatedly prompting an agent with brand, product, UI, UX, technical and cultural rules for each new product, a company maintains a reusable, machine-executable operating layer that every product and agent inherits.

The system should encode, at minimum:

- company ontology / identity (本体)
- mission, values, vision
- corporate culture
- product design language
- human-computer interaction philosophy
- product design principles
- technical principles
- UI/UX principles
- terminology, content voice, accessibility, privacy, security and other cross-product rules
- canonical patterns, components, design tokens and implementation examples
- validation/evaluation rules

The user explicitly wants the framework to **guide rather than constrain agent creativity**. Stable/repetitive decisions should be inherited; product-specific innovation should remain open.

## Key target scenario

A future customer engagement can work approximately as follows:

1. Meet customer and record the conversation with consent.
2. Ingest meeting transcript/recording plus customer product materials, website, brand docs, design files, existing software screenshots/code/docs, technical/security requirements and organizational context.
3. Extract a structured **Company Genome / Company Product OS** with evidence and confidence.
4. Ask humans only about unresolved contradictions or high-impact unknowns.
5. Compile a product brief from customer needs + company genome.
6. Generate a prototype/product that already feels native to that company.
7. Run automated evaluators for brand, interaction, architecture, accessibility, security, terminology and cross-product consistency.
8. Let customer staff test it using familiar interaction patterns, reducing training and adoption friction.
9. Convert validated innovations back into reusable patterns so the Company Product OS evolves over time.

## Core conceptual distinction

This is **above a conventional design system**.

A design system typically focuses on tokens/components/patterns. The proposed system also encodes organizational intent, product philosophy, technical architecture, interaction semantics, governance, exceptions, evidence, inheritance and machine-executable evaluation.

Working names:
- Company Product OS
- Company Genome
- Product Constitution
- Product Compiler
- Living Product Operating System

Current preferred framing: **Company Product OS** as the product/category name; **Company Genome** as its stable identity layer; **Product Compiler** as the generation mechanism.

## Architecture direction

Proposed stack:

```text
Evidence Layer
(meetings, docs, products, code, design, policies)
        ↓
Company Genome / Knowledge Model
        ↓
Executable Standards
(tokens, patterns, components, schemas, policies, architecture)
        ↓
Product Compiler
(customer need + company context → product specification → design/code)
        ↓
Evaluators / Conformance Gates
        ↓
Generated Product
        ↓
Usage + feedback + accepted innovations
        ↺
Company Product OS evolution
```

Rules should have strength classes rather than all being hard constraints:
- Principle
- Must
- Default
- Prefer
- Pattern
- Free
- Experimental

Every important rule should ideally carry:
- source/evidence
- owner
- scope
- strength
- rationale
- examples
- counterexamples
- version
- confidence
- exception process
- automated checks when possible

## External evidence already found

Research signals to incorporate carefully:

- Apple HIG (2026) explicitly emphasizes familiarity and consistent visuals/interactions; consistency helps people learn faster and predict how new interactions work.
- W3C Design Tokens Community Group published its first stable Design Tokens format in 2025.10, including aliases/inheritance and cross-platform interoperability.
- Figma’s controlled design-system experiment reported participants completed applicable design tasks 34% faster with a relevant design system; Figma cautions this represents an upper-bound-style context because the system was directly applicable and current.
- A controlled GitHub Copilot experiment (Peng et al.; Microsoft Research publication) reported the treatment group completed a narrow JavaScript HTTP-server task 55.8% faster than control; do not generalize this directly to all software work.
- Google DORA 2025 surveyed nearly 5,000 technology professionals and describes AI as an **amplifier** of organizational strengths and dysfunctions. This supports the need for strong organizational/product foundations before scaling agentic development.
- Figma 2026 cites design-system case studies such as Freshworks attributing a 28% reduction in customer-service costs to its new design system; treat case-study attribution as company-reported rather than universal causal evidence.

## Document to produce

Produce a comprehensive Chinese blueprint, with enough detail to serve as:
- concept paper / category definition
- product architecture
- customer-delivery SOP
- technical implementation specification
- governance model
- MVP roadmap
- business/value narrative
- evaluation/KPI framework

The document should include:
1. executive summary and one-sentence definition
2. problem shift in agentic software development
3. category boundary vs design system / brand guide / prompt library / RAG / templates
4. Company Product OS layered model
5. customer-meeting-to-product workflow
6. evidence ingestion and ontology extraction
7. canonical machine-readable schema
8. inheritance/cascade/exception model
9. Product Compiler pipeline
10. evaluator/conformance architecture
11. UI/UX, design-token and component implementation
12. technical architecture/security/privacy
13. governance and versioning
14. learning/evolution loop
15. example company and example generated product
16. implementation phases/MVP
17. metrics and ROI hypotheses
18. risks/failure modes
19. defensibility/business model possibilities
20. concrete first build recommendation

## Persistence rule for this workstream

Do not overwrite the existing BP project truth in `PROJECT.md` / `STATUS.md`. Keep this concept as an additive workstream under `docs/company-product-os/`.

If the session becomes long or a major design decision is made, update this checkpoint before continuing. On context recovery, read this file first, then the latest blueprint file.
