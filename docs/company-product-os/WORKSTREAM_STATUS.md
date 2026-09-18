# Company Product OS — Workstream Status

Date: 2026-09-18
Branch: `concept/company-product-os-20260918`

## Current state

The first implementation blueprint is complete and persisted as an additive workstream. It intentionally does not modify the BP project truth in root `PROJECT.md` / `STATUS.md`.

## Durable files

1. `docs/company-product-os/CONTEXT_CHECKPOINT.md`
   - Original user intent
   - Key scenario
   - Architecture direction
   - Persistence/recovery rule

2. `docs/company-product-os/RESEARCH_EVIDENCE.md`
   - Apple HIG
   - IBM Carbon / IBM Cloud case study
   - Figma design-system evidence
   - GitHub Copilot controlled experiment
   - Google DORA 2025
   - McKinsey software-engineering estimate
   - DTCG Design Tokens
   - JSON Schema / OPA / MCP implementation primitives
   - Scope/caveat notes for quantitative claims

3. `docs/company-product-os/COMPANY_PRODUCT_OS_BLUEPRINT.md`
   - Category definition
   - Company Genome / Product Compiler / Conformance Engine
   - Customer meeting-to-product workflow
   - Evidence extraction and conflict resolution
   - Rule strengths and inheritance
   - Product Context Pack
   - Product IR
   - Conformance/eval architecture
   - Canonical repo structure
   - Security/privacy/governance/versioning
   - MVP and customer-delivery motion
   - Metrics/ROI/risk/defensibility
   - Concrete first implementation recommendation

4. `docs/company-product-os/COMPANY_OS_CANONICAL_EXAMPLE.yaml`
   - Machine-readable example of:
     - company ontology / principles
     - evidence
     - design/engineering/content rules
     - patterns
     - exceptions
     - Product Context Pack
     - Product IR
     - conformance result

## Current preferred category language

**Company Product OS** = product/category

Submodules:
- **Company Genome** — stable identity and decision logic
- **Product Compiler** — resolves company rules + product intent into a Product IR and artifacts
- **Conformance Engine** — deterministic + structural + semantic + runtime validation

Core philosophy:

> Standardize the solved. Preserve the identity. Maximize the new.

Chinese:
> 已解决的问题标准化，公司的基因被继承，真正新的问题留给创新。

## Core implementation decision

Do **not** implement this as one giant prompt or fine-tuned customer model.

Preferred architecture:

```text
Raw Evidence
→ Normalized Evidence
→ Candidate Rules
→ Approved Company Genome / Registries
→ Scope + inheritance resolver
→ Product Context Pack
→ Product IR
→ Design/code/docs/tests
→ Conformance Engine
→ Product
→ Outcome evidence
→ Governance / OS evolution
```

Company-wide knowledge grows over time, but each agent receives only a compiled, task-specific **Product Context Pack**, preventing context bloat and rule dilution.

## Recovery instruction

In any later conversation about this concept, read in this order:

1. `docs/company-product-os/CONTEXT_CHECKPOINT.md`
2. `docs/company-product-os/WORKSTREAM_STATUS.md`
3. `docs/company-product-os/COMPANY_PRODUCT_OS_BLUEPRINT.md`
4. `docs/company-product-os/COMPANY_OS_CANONICAL_EXAMPLE.yaml`
5. `docs/company-product-os/RESEARCH_EVIDENCE.md`

Then continue from repository evidence rather than relying on chat memory.
