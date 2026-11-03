# AegistonTeam V6 — continuity checkpoint

> Date: 2026-11-03  
> Status: active, reversible design iteration; **not production deployment**  
> Repository: `jinngimk-lang/wendnag`  
> Branch: `design/aegistonteam-cinematic-landing-20261103`  
> Review anchor: Draft PR [#27](https://github.com/jinngimk-lang/wendnag/pull/27)

## 1. Current user request

Continue the AegistonTeam landing-page work in a Python virtual environment. Use [x.ai](https://x.ai/) as a reference for the content hierarchy and section order, while retaining the user's own cartoon-sketch elements.

## 2. Source-of-truth hierarchy

1. Latest explicit user instruction.
2. User-approved warm-white comic reference: `aegistonteam协作落地页.png`.
3. `V3-INTERACTIVE-MOTION-2026-11-03.md` — mascot identity, motion principles, authentic screenshot constraints.
4. `V5-CONTINUITY-2026-11-03.md` — offline packaging and natural layout baseline.
5. `V6-XAI-REFERENCE-AND-IA-2026-11-03.md` — current information-architecture mapping.
6. `V6-QA-2026-11-03.md` — current validation evidence.

## 3. Visual constraints

- Warm paper-white / cream surfaces, orange accent, graphite text.
- Keep the original orange, cream and charcoal mascot trio and their distinguishing white diagonal band.
- Reuse the seven approved source assets; do not invent substitute mascots.
- Keep workspace and team-structure screenshots genuine and unredrawn.
- Avoid dark game portals, sci-fi styling, repeated equal-weight card grids, generic chapter labels, decorative arrows and fake UI.
- No unsupported customer, performance, feature, API or production claims.

## 4. V6 information architecture

1. Hero: product value statement, two anchor CTAs, original mascot trio.
2. Product preview: real workspace / team-structure tabs and screenshot lightbox.
3. Proof strip: three grounded collaboration principles; no invented numerical metrics.
4. Capabilities: one large illustrated moment plus two supporting moments.
5. Team structure / workflow: interactive accordion and authentic team screenshot.
6. Choose how to start: workspace path / team-structure path.
7. Footer: original mascot runner and replay.

The x.ai Latest news module is intentionally not copied because no verified public AegistonTeam news feed is available. Its position in the narrative is served by genuine product/workflow proof instead.

## 5. Local virtual environment and files

- Workspace: `/mnt/data/wendnag-v5/`
- Python venv: `/mnt/data/wendnag-v5/.venv/`
- Python: 3.13.5
- Project source: `/mnt/data/wendnag-v5/project/AegistonTeam_V6/`
- Editable template: `source/index.template.html`
- Seven source images: `source/assets/`
- Build command: `/mnt/data/wendnag-v5/.venv/bin/python /mnt/data/wendnag-v5/project/AegistonTeam_V6/build.py`
- Output: `output/AegistonTeam_V6_xai-structure_offline.html`
- QA: `qa_v6.py`, `qa/QA_RESULTS.json`, `qa/screenshots/`

Build uses Python standard-library modules only. The project venv does not contain Playwright; browser QA used the preinstalled system Python Playwright package and system Chromium. Do not claim Playwright was installed into the venv.

## 6. V6 artifact identity

- Offline HTML: `AegistonTeam_V6_xai-structure_offline.html`
- Size: 1,378,797 bytes
- SHA-256: `4cbc058e7dce18f06d518e023fa0dd2f4bff8b5cce4ced9f5c9952bbf999e25a`
- Source + QA ZIP: `AegistonTeam_V6_源码与验收包.zip`
- ZIP SHA-256: `d57ba226b6a6cc8a0e04fdf824ba8b6c7f645bb9bf227157c656ceb73bb7a939`
- Desktop full-page screenshot SHA-256: `5c5bc107fb77cd4c7fc1bd781b049f9b718a1d6299dc703e078d0bf560c268bd`
- Mobile full-page screenshot SHA-256: `1432e32a4a6635320f123485f1ff3c9a27cb5a09ce78164a0c7c8bc82303a7a5`

The HTML and ZIP were delivered as ChatGPT-session downloadable artifacts. The binary HTML/ZIP and screenshots are **not committed to GitHub**; this checkpoint records their exact identities. Do not claim otherwise.

## 7. QA status

- HTML parse, unique IDs and internal anchors: PASS.
- Eight visible content images: 8/8 loaded on desktop and mobile.
- External image/CDN/font/script network requests: 0.
- JavaScript page errors: 0; console errors: 0.
- Scroll reveal: 18/18 desktop and 18/18 mobile.
- No horizontal overflow at 1440 / 1024 / 768 / 390 / 320 CSS px.
- Product tabs, screenshot lightbox, Escape close, focus restoration, story screenshot lightbox, accordion, mobile nav, footer replay and reduced-motion checks: PASS.
- Exact evidence: `V6-QA-2026-11-03.md` and `qa/QA_RESULTS.json`.

## 8. Repository / delivery boundary

- Keep PR #27 open and Draft.
- This remains a design/prototype workstream; do not merge or deploy to the production AegistonTeam website.
- The V6 HTML and ZIP are local deliverables. The current PR update stores durable design, continuity and QA documentation; it does not imply the large binary package was uploaded.
- Do not mix the separate LegalLens video task, the BP deck, or the unrelated AI Arena workstream into this landing-page task.

## 9. Next action

User visual review of the V6 desktop and mobile previews. After feedback, make only necessary corrections, rerun the same QA matrix, update this checkpoint and preserve PR #27 as Draft until explicit visual approval.
