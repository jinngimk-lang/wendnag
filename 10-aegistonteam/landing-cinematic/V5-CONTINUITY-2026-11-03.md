# AegistonTeam V5 — continuity checkpoint

> Date: 2026-11-03  
> Status: active, reversible design iteration; **not production deployment**  
> Working repository: `jinngimk-lang/wendnag`  
> Working branch: `design/aegistonteam-cinematic-landing-20261103`  
> Existing review anchor: Draft PR [#27](https://github.com/jinngimk-lang/wendnag/pull/27)

## 1. Current task and user intent

Continue refining the AegistonTeam warm-white illustrated landing page. The user explicitly asked to continue in a virtual environment and persist continuity documents in this repository so future sessions retain high precision.

The immediate user-visible defects in the latest supplied browser captures (2026-11-03, files `image(20261103-073151).png`, `image(20261103-073232).png`, `image(20261103-073236).png`) are broken image assets:
- Hero mascot image fails to load.
- All three partner/mascot card images fail to load.
- Team-structure screenshot fails to load.

The user also judged the section layout and typography too AI-like / too templated and asked for a more natural continuation.

## 2. Authoritative visual direction — do not drift

The unique visual anchor remains the user-approved recovered image `aegistonteam协作落地页.png` (warm paper-white background, original orange / cream / charcoal mascot trio, hand-drawn outlines and motion marks, natural Chinese typography, genuine product screenshot).

Preserve:
- The original three AegistonTeam mascots, their identities, proportions, facial features, orange / cream / charcoal palette, and characteristic white diagonal band.
- Warm off-white / cream surfaces, restrained orange accent, graphite/navy text, subtle hand-drawn marks and breathing room.
- Real AegistonTeam workspace and team-structure screenshots, with source UI text/pixels intact.
- Product-site clarity: users should understand the product and the next step, not mistake the page for an illustration poster.

Avoid:
- Dark / deep-blue game portal or sci-fi background.
- Switching to a Sony-like editorial system unless the user explicitly asks for it. That direction is not part of the approved brief.
- Generic repeated three-card grids, repeated eyebrow/kicker labels, template-like equal-weight sections, dense arrows, large English chapter numbers, generic pill labels, gratuitous particles, and AI-looking typography.
- Replacing the user's mascots or generating fake product UI / Chinese text.
- Unsupported feature, performance, customer, or production claims.

## 3. Source-of-truth hierarchy

1. Latest explicit user instruction and latest supplied screenshots.
2. `aegistonteam协作落地页.png` — unique approved visual anchor.
3. This checkpoint and `V3-INTERACTIVE-MOTION-2026-11-03.md`.
4. `V4-FIGMA-MOTION-2026-11-03.md` and local V4 package as implementation references.
5. V1 / V2 documents only for history; do not restore superseded visual directions.

## 4. Existing work and exact locations

### GitHub
- PR #27 is open and Draft; keep it Draft until the user reviews the iteration.
- PR #27 currently stores design / QA documents and an early `site/index.html`; **that remote HTML is not the V3 or V4 deliverable**.
- The V3 complete HTML/assets were delivered in a session ZIP but were not committed to GitHub.
- `creative-runtime/STATE.md` and `creative-runtime/LEARNINGS.md` are the durable creative continuity files.

### Current session files
- Approved visual anchor: `/mnt/data/aegistonteam协作落地页.png`
- V3 working package: `/mnt/data/aegistonteam_v3/`
- V4 working package: `/mnt/data/aegistonteam_v4/`
- V4 HTML: `/mnt/data/aegistonteam_v4/index.html`
- V4 assets: `/mnt/data/aegistonteam_v4/assets/`
- V4 motion spec: `/mnt/data/aegistonteam_v4/MOTION_SPEC.md`
- Latest broken-image evidence: `/mnt/data/image(20261103-073151).png`, `/mnt/data/image(20261103-073232).png`, `/mnt/data/image(20261103-073236).png`
- Latest page/section captures are evidence of failed external asset URLs; they are not a new visual style reference.

V4 source already uses relative local `./assets/*` paths. The failed screenshots correspond to the earlier preview page whose hero/card/story images were hosted on a separate asset deployment. Do not conflate the old broken preview with V4's local package.

## 5. V5 implementation target

Build a self-contained, downloadable offline HTML review artifact from the approved V3/V4 work, with all visual assets embedded as data URIs or otherwise packaged locally. Prefer a single HTML file that does not depend on external image hosts, CDNs, fonts, or runtime APIs for its primary visual content.

Improve naturalness through layout rhythm, not a wholesale style change:
- Keep the mascot-led hero, but make the visual and headline balance feel intentional.
- Let the real product screenshot occupy a clear, larger proof area.
- Replace the repeated equal-card rhythm with a more varied editorial composition while preserving the same illustrations and meaning.
- Use a more human sequence of story / collaboration steps, with fewer repeated labels and more whitespace.
- Keep the team structure proof and the running mascot finale.
- Use restrained, purposeful motion states inspired by Figma Smart Animate: stable matching layers, short eased transitions, scroll entrance, screenshot switching/zoom, accordion disclosure, mobile navigation, and reduced-motion fallback.

Do not call the result approved until the user reviews it. Do not claim a native Figma file or native Figma Motion timeline exists; this is a web implementation of those motion principles.

## 6. Virtual-environment and QA workflow

Workspace: `/mnt/data/wendnag-v5/`  
Python environment: `/mnt/data/wendnag-v5/.venv/`

The isolated Python virtual environment has been created. Package installation from PyPI is unavailable in this session because the container has no DNS/network access. Use Python standard-library scripts and the installed local Chromium binary; do not silently depend on unavailable packages.

Required checks:
- Parse the HTML and inspect every image source.
- Confirm there are no remote image URLs, missing local assets, or broken image placeholders.
- Confirm all source UI screenshots remain genuine and unaltered internally.
- Chromium desktop and 390px mobile screenshots; check no horizontal overflow.
- Check JS console/page errors, menu, screenshot tabs/zoom/ESC, accordion, footer runner/replay, and `prefers-reduced-motion`.
- Record actual results and limitations in a QA report. Never mark an unrun check as passed.

## 7. Delivery and repository rules

- Deliver the V5 single-file HTML and, if useful, a ZIP with editable source/assets and QA artifacts.
- Commit the source, assets, motion notes, and QA report to the existing PR #27 branch using a verified binary-capable Git path. Do not claim binary assets are in GitHub until verified by reading the committed tree.
- Update this file, `creative-runtime/STATE.md`, and reusable `creative-runtime/LEARNINGS.md` before context loss or phase changes.
- Keep PR #27 Draft and do not merge or deploy to the production AegistonTeam website.
- Do not mix the separate LegalLens video task or the unrelated BP project into this landing-page work.

## 8. Next concrete action

Create the V5 offline HTML candidate in the virtual-environment workspace using V4's interaction model and source assets; make the image references self-contained, improve section rhythm, run the listed QA, then write actual outputs and test evidence back into this checkpoint and PR #27.
