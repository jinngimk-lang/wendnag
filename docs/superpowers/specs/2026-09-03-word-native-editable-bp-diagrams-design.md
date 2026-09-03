# Word-native editable BP diagrams — design

## Goal
Keep the visual language and geometry of the approved light-blue consulting/SVG figures while making every diagram element directly editable inside Microsoft Word.

## Scope
Figures 1, 2, 3, 10, 11, 12, 15 and 16 only. Product screenshots in figures 4–9 and 13–14 remain untouched.

## Hard constraints
- Do not flatten diagrams to PNG/SVG/PDF inside the final DOCX.
- Do not substitute the figures with Word tables merely to obtain editability.
- Use Word-native DrawingML shapes/groups: text boxes, rounded rectangles, rectangles, circles, lines/connectors and arrows.
- Preserve the approved figure geometry and message hierarchy from the previous SVG edition; visual refinements may improve spacing, alignment and typography but must not change factual content.
- Use restrained McKinsey-style visual conventions: conclusion-led title, high whitespace, dark navy text, pale blue fills, one primary accent blue, thin neutral borders, direct labels, minimal decoration.
- All text/numbers remain directly editable in Word.
- AegisClaw naming only; no “曾用名 InkClaw” or InkClaw text outside untouched historical product screenshot pixels.
- No BP numeric fact may be changed by visual work.

## Diagram source model
Each figure is defined in Python as a list of semantic primitives with normalized coordinates. The source model is independent of Word so geometry can be tested and rendered consistently.

Primitive types:
- text
- rounded_rect / rect
- line / arrow
- circle
- group

Each primitive carries stable `id`, position, size, style and text. Stable IDs allow later edits without reconstructing the whole document.

## Word rendering
LibreOffice UNO is used as the deterministic bridge to create grouped Word drawing objects, then export to DOCX. The resulting DOCX must contain Wordprocessing DrawingML (`wps:wsp` / `wpg:wgp`) for the consultation figures rather than image relationships.

Each figure is inserted as one group for easy movement, while child shapes remain independently selectable/editable after ungrouping or entering the group in Word.

## Fidelity standard
The SVG version is the reference for silhouette and information structure:
- Fig 1: three top cards feeding a broad enterprise-intelligence-base band with four requirement cards.
- Fig 2: true bar-chart silhouette with 2025/2030 bars, growth callout and direct labels.
- Fig 3: four-step ascending stair with four enterprise requirements below.
- Fig 10: three equal delivery cards with use-case footer chips.
- Fig 11: four horizontal architecture layers with modular sub-boxes.
- Fig 12: four revenue inputs → central standardization engine → three replication outputs.
- Fig 15: proportional 1000万元 funding-use bar plus direct labels.
- Fig 16: horizontal 12/24/36-month timeline with milestone cards.

## Quality gates
1. Structural: all eight figures contain native Word shapes; no image rel is used for these figures.
2. Editability: text appears in DrawingML text bodies, not outlines or raster images.
3. Fidelity: each figure passes layout invariants (relative ordering, number of cards/bars/nodes, key proportions).
4. Content: expected numeric/text tokens equal the approved BP values.
5. Rendering: final DOCX renders without clipping, overlaps or accidental page breaks; page count remains stable unless a justified layout correction is documented.

## Installed diagram skills
Project-local copies of the requested upstream Draw.io and Excalidraw skills are pinned under `.agents/skills/` with MIT license attribution. Their layout/shape/editability principles inform the diagram source model; the final deliverable remains Word-native DrawingML because the user requires editing directly in Word.