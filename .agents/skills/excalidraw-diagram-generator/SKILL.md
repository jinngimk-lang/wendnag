---
name: excalidraw-diagram-generator
description: Use when a diagram needs clear primitive-shape composition, flow direction, hierarchy, relationship layout, spacing discipline or an editable sketch source before conversion to another editable format.
license: MIT
---

# Excalidraw Diagram Generator — project-local install

Pinned/adapted from `github/awesome-copilot` at commit `2ba72cd14253500bbb747b5f01e72dd03fbafcb0`, skill path `skills/excalidraw-diagram-generator/`.

## Core rules used by Wendnag BP

1. Extract the diagram type before drawing: flow, relationship, hierarchy, architecture, data flow or timeline.
2. Identify key entities and relationships explicitly before placing shapes.
3. Prefer a small set of primitives: rectangle/rounded rectangle, ellipse, arrow, line and text.
4. Maintain consistent spacing and alignment. For business diagrams, use grid-based layout rather than hand-wavy placement.
5. Keep element count reasonable; split detail rather than shrinking text until unreadable.
6. Use stable IDs and deterministic coordinates so diagrams can be regenerated and audited.
7. Keep text readable at presentation scale and ensure text fits its container.
8. Use a restrained color system. The Wendnag BP overrides the upstream sketch palette with consulting-style navy + pale blue + neutral gray.
9. Validate overlap, text fit, arrow logic, unique IDs and expected element count before delivery.

## Wendnag conversion target

Excalidraw principles are used as a layout/primitive discipline. The investor-facing DOCX must be Word-native: each text box, rectangle, circle, bar, line or arrow is a real Word DrawingML object. No `.excalidraw`, SVG or raster image is used as the final consultation figure.

## Validation checklist

- All elements have stable IDs.
- No unintended overlap.
- Text size is presentation-readable.
- Arrow direction matches the intended business logic.
- Colors follow the BP palette.
- Figure structure matches the approved reference silhouette.
- Factual copy is source-backed and unchanged.

See `UPSTREAM.md` for provenance and license.