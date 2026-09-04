---
name: drawio-skill
description: Use when creating, reviewing or editing structured business/architecture diagrams that require stable geometry, explicit relationships, editable shapes, visual validation or source-to-diagram traceability.
license: MIT
---

# Draw.io Architecture Studio — project-local install

Pinned/adapted from `Agents365-ai/drawio-skill` at commit `65f5fa0505f43d8af104d00c6087cb02c8c0e2f3`.

## Core rules used by Wendnag BP

1. **Editable source first.** Never flatten a diagram when the requested deliverable must remain editable.
2. **Stable semantic identity.** Every shape has a stable ID; local edits preserve unrelated geometry.
3. **Source-backed claims.** Diagram text, numbers and relationships must trace to the BP source; inferred content is never silently presented as fact.
4. **Deliberate diagram type.** Use hierarchy, flow, architecture layers, timeline or quantitative chart according to the message rather than forcing every idea into boxes.
5. **Preserve geometry during conversion.** Conversion from an editable design representation to Word DrawingML must preserve relative order, proportions, routing and information hierarchy.
6. **Visual validation.** Inspect the rendered draft for overlap, clipping, crossed connectors, stacked labels and unreadable type. Automatic repair must not change facts.
7. **Professional style preset.** For this BP use restrained consulting graphics: white background, navy text, pale blue support fills, one accent blue, thin neutral borders, high whitespace, direct labels and no decorative 3D effects.
8. **No guessed icons/shapes.** Prefer primitive geometric forms unless a verified icon library is explicitly needed.

## Wendnag conversion target

The final BP does **not** ship `.drawio` as the investor document. Draw.io principles are used for diagram structure, while final figures are rendered as native Word DrawingML groups so users can directly select and edit text boxes, rectangles, circles, lines and arrows inside Microsoft Word.

## Validation checklist

- Shape count and topology match the approved figure spec.
- Text is editable text, not outlines.
- No raster element replaces a consultation figure.
- Connectors terminate cleanly and do not cross unrelated nodes.
- All numeric values match the BP source.
- Final DOCX render is visually reviewed page by page.

See `UPSTREAM.md` for provenance and license.