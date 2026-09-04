# Word-native Editable BP Diagrams Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Recreate the approved consulting-style BP figures as native editable Word shapes without changing their visual silhouette or factual content.

**Architecture:** Maintain a semantic Python figure model with normalized geometry, render it to grouped Word drawing shapes through LibreOffice UNO, and verify the resulting DOCX at both OOXML and rendered-page levels. Vendor the requested diagram skills locally so future diagram work follows stable editable-diagram conventions.

**Tech Stack:** Python 3, python-docx, LibreOffice UNO, Wordprocessing DrawingML/OOXML, pytest, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-09-03-word-native-editable-bp-diagrams-design.md`

## Global Constraints
- Figures 1, 2, 3, 10, 11, 12, 15 and 16 must be native Word shapes, not images or table substitutes.
- Visual silhouette follows the approved SVG edition.
- Product screenshots remain untouched.
- BP facts and numeric values may not change.
- Final branding uses AegisClaw only outside untouched screenshot pixels.

---

### Task 1: Install requested diagram skills

**Files:**
- Create: `.agents/skills/drawio-skill/SKILL.md`
- Create: `.agents/skills/drawio-skill/LICENSE`
- Create: `.agents/skills/drawio-skill/UPSTREAM.md`
- Create: `.agents/skills/excalidraw-diagram-generator/SKILL.md`
- Create: `.agents/skills/excalidraw-diagram-generator/LICENSE`
- Create: `.agents/skills/excalidraw-diagram-generator/UPSTREAM.md`

- [ ] Pin Draw.io skill to upstream commit `65f5fa0505f43d8af104d00c6087cb02c8c0e2f3` and Excalidraw skill to `2ba72cd14253500bbb747b5f01e72dd03fbafcb0`.
- [ ] Include MIT license attribution and source links.
- [ ] Verify both `.agents/skills/*/SKILL.md` paths exist.

### Task 2: Add failing structural/editability tests

**Files:**
- Create: `tests/test_word_native_figures.py`

**Interfaces:**
- Consumes final generated DOCX path.
- Produces assertions for native Word group/shape counts, absence of image rels for the eight figures, expected text/numeric tokens and absence of obsolete branding.

- [ ] Write tests expecting at least eight Wordprocessing groups (`wpg:wgp`) and native child shapes (`wps:wsp`).
- [ ] Write tests requiring the eight figure titles and approved values `67.6`, `460.4`, `47%`, `40%`, `20%`, `12%`, `8%`, `12 个月`, `24 个月`, `36 个月` in DrawingML text.
- [ ] Run against the current table-based Word-native edition and confirm failure because figures are table structures rather than DrawingML groups.

### Task 3: Add semantic figure model and Word shape renderer

**Files:**
- Create: `tools/bp_word_shapes/model.py`
- Create: `tools/bp_word_shapes/figures.py`
- Create: `tools/bp_word_shapes/uno_renderer.py`
- Modify: `tools/build_bp_word_native.py`

**Interfaces:**
- `build_figure_spec(number: int) -> FigureSpec`
- `render_figure_group(doc, anchor, spec: FigureSpec) -> object`

- [ ] Implement shape primitives with stable IDs and normalized coordinates.
- [ ] Encode the eight approved SVG silhouettes in `figures.py`.
- [ ] Render text boxes, rounded rectangles, bars, circles, lines and arrows as native UNO drawing shapes.
- [ ] Group each figure so it moves as one object while children remain editable.
- [ ] Preserve the existing product screenshots and captions.

### Task 4: Add figure geometry/factual invariants

**Files:**
- Modify: `tests/test_word_native_figures.py`
- Create: `tests/test_figure_specs.py`

- [ ] Assert Fig 1 has three top product cards plus four base-requirement cards.
- [ ] Assert Fig 2 has exactly two market bars and the CAGR callout.
- [ ] Assert Fig 3 has four ascending steps and four requirement pills.
- [ ] Assert Fig 12 has four inputs, one central standardization block and three outputs.
- [ ] Assert Fig 15 funding percentages total 100 and amounts total 1000.
- [ ] Assert Fig 16 has 12/24/36 month nodes in left-to-right order.
- [ ] Run all tests and confirm pass.

### Task 5: Build and render the final DOCX

**Files:**
- Generate: `08-output/西安智瞳安宇科技有限公司商业计划书-20260903A-Word原生图形可编辑版.docx`

- [ ] Build from the archived original BP, keeping styled native Word tables and untouched product screenshots.
- [ ] Render DOCX to PDF/pages with LibreOffice.
- [ ] Inspect pages containing figures 1, 2, 3, 10, 11, 12, 15 and 16 for clipping, overlap and visual hierarchy.
- [ ] Adjust only geometry/typography; do not change factual copy.

### Task 6: Final verification and delivery

**Files:**
- Update: `STATUS.md`
- Update: `BINARY-MANIFEST.md`

- [ ] Run `pytest -q` and record zero failures.
- [ ] Inspect OOXML and confirm native DrawingML groups/shapes for all eight figures.
- [ ] Confirm only eight raster product screenshots remain as the intended image figures.
- [ ] Confirm no `InkClaw` text remains outside screenshot pixel content.
- [ ] Record output SHA-256 and size.
- [ ] Compare branch against `main`, open PR, verify mergeability/CI, merge, and re-read `main` to confirm the source changes landed.