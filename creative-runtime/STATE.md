# Creative Runtime State

Last updated: 2026-09-17

## Active creative task

Create a 15-second promotional video for **合约智审 LegalLens**, using the user's supplied office/character/product screenshots and current node-based video canvas.

The purpose is not to make a generic software demo. The story is a **human time-reclamation arc**:

> overwhelming contract/office work consumes personal time → the character realizes she may miss her after-work date/life → LegalLens enters as the causal hinge → product proof makes contract review orderly, traceable, and efficient → the same person regains calm and leaves work with her evening intact.

The strongest remembered idea should be: **the product gives control of time back to the person.**

## Reference image map from the current conversation

Use the user's numbering as the authoritative visual map:

- **图1** — base office environment. Modern bright office, desk crowded with reports, folders, sticky notes, laptop, mugs; visual language of workload overload.
- **图2** — isolated female character reference: blue-and-white striped shirt, dark skirt, beige heels, hair in loose updo, worried/tired expression. Primary identity/wardrobe reference.
- **图3** — same character integrated into the overloaded office. Strong reference for the “before” state: hand to head, fatigue, files and notifications surrounding her.
- **图4** — LegalLens landing/home product screen. Hero message and risk-card area; suitable for restrained 2.5D/parallax/product-reveal treatment.
- **图5** — LegalLens contract review analysis screen. Shows original clause, risk analysis, risk score, legal basis, modification suggestions. Core proof screen.
- **图6** — LegalLens document/workbench screen with risk list, highlighted clause, and AI Q&A. Core traceability / deep-review proof screen.
- **图7** — same character in the office after the workload is under control. Relaxed posture, coffee, cleaner desk, warm light. Primary “after” state / life-restored payoff.
- **图8** — user's current node-based video canvas and connections. Multiple visual references feed a 15-second video node; this is the current production context.

## Current 15-second narrative architecture

### Beat A — pressure / work consumes life
Approx. 0–4s.

- Start with 图1/图3 world.
- Character is visibly buried in contract/admin work.
- Use observable micro-actions rather than generic “stress”: eyes bouncing between notifications and paperwork, hand to forehead, incomplete packing-up motion, checking time, another task arriving.
- Introduce one simple after-work-life stake: an evening/date reminder, without cluttered fake UI text.
- Camera behavior can feel slightly more compressed/pressured here, but should remain premium and realistic.

### Beat B — hinge
Approx. 4–5s.

- Noise/notifications stop or freeze.
- Clean brand-colored light/scan/order transition.
- This is the audiovisual reversal point.
- Avoid cheap cyberpunk particles or explosive sci-fi effects.

### Beat C — product proof
Approx. 5–12s.

- 图4: product entry / overview; use restrained 2.5D, local depth, push-in, or small orbit. Do not warp the entire UI.
- 图5: follow information hierarchy — clause → risk → legal basis → modification suggestion.
- 图6: connect risk list → exact clause → AI/analysis as traceable workflow proof.
- Product screenshots are truth sources. Preserve real text/layout when possible; compositing is preferred over asking a video model to regenerate legible Chinese UI.
- Proof should be selective; do not turn the middle into a feature dump.

### Beat D — human payoff
Approx. 12–15s.

- Return to 图7.
- Same person, same office, same wardrobe, same identity.
- Posture opens, shoulders relax, grip and gaze soften, desk feels manageable, light can warm subtly toward evening.
- She checks time and is able to leave / resume ordinary life.
- End frame may retain character + product presence rather than becoming a sterile full-screen logo card.

## Current voiceover direction

Working version:

> 繁琐审批，工作越堆越晚，连今晚的约会，都要错过。  
> 合约智审。多视角并行分析，风险、依据、建议一屏看清，结论全程可追溯。  
> 审得更快、更准，把下班还给生活。

Important claim discipline:

- Avoid unsupported absolute claims such as “保证精准度” unless the company has public evidence and approved wording.
- “更快、更准” is currently treated as advertising direction, not a quantified factual metric.
- Product truth visible in references: multi-view analysis, risk identification/scoring, original clause, legal basis, modification suggestion, traceability, AI Q&A/workbench.

## Current music/sound direction

Overall sound story: **pressure → interruption/silence → ordered intelligence → warm release**.

- Approx. 0–4s: restrained low pulse, subtle ticking/clicks, office/notification textures integrated into rhythm; unresolved tension.
- At hinge: brief subtraction/silence, reverse swell, clean soft impact, bright restrained product chime.
- Approx. 5–12s: clean intelligent electronic groove, soft bass/pulse, sparse pluck, UI sonic accents only on important proof events.
- Approx. 12–15s: reduce electronic tension, introduce warmer piano/guitar-like harmonic texture, finish with a simple 2–3 note sonic logo.
- Approximate tempo direction discussed: ~96–108 BPM / around 100 BPM, but musical psychology matters more than the exact number.
- Voiceover must remain foregrounded; music should make room for the “date/life stake” line and product name.

## Current art-direction constraints

- Premium real corporate photography, not obvious AI render.
- Same female identity, hair, clothing, accessories across all live-action beats.
- Same office topology and desk logic across before/after.
- Product UI must remain recognizably LegalLens; avoid generated gibberish replacing source screenshots.
- Avoid exaggerated cyberpunk blue, particle storms, EDM/trailer aesthetics, huge camera spins, unnecessary holograms.
- Product reveal should feel like **order entering chaos**, not “magic tech destroys reality.”

## Current director-level interpretation

The product is **not the emotional protagonist**. The person is.

LegalLens is the **causal hinge** that changes her relationship with time. Therefore:

- open on a human goal/cost, not a product logo;
- make the workload physically visible before describing efficiency;
- let the product section prove only what is needed to earn the final relief;
- return to the human after the product proof;
- judge every VFX/camera move by whether it clarifies this transformation.

## Next concrete production step

Convert the current master concept into **node-ready shot prompts**, each with:

- duration;
- reference image authority;
- immutable character/location/UI anchors;
- start state;
- micro-action;
- framing;
- motivated camera behavior;
- lighting;
- sound cue;
- end state;
- handoff to next shot;
- negative constraints.

Prefer 6–7 tightly controlled beats over one undifferentiated long prompt if the video tool allows shot/node segmentation.

## Open decisions

- Exact number of generation nodes / whether the current tool is best run as one 15s generation or several controlled segments.
- Final approved VO length after actual speech timing test.
- Exact after-work/date visual cue (calendar reminder vs. phone glimpse vs. simple time cue) should remain visually simple.
- Final brand lockup wording and whether the final frame uses “把下班还给生活” as the primary line.

## Continuity checkpoint rule

Before any major new creative phase or when the conversation becomes materially long, update this file rather than relying on chat history. Preserve only durable state; put reusable principles in `LEARNINGS.md`.