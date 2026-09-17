# Creative Runtime Learnings

This file stores reusable discoveries that should survive across chats. It is not a dump of every idea; only keep principles that materially improve future work.

## 2026-09-17 — From the Max-Potential manifesto + directing research

### 1. Direct transformations, not features

For strong product films, define a single underlying transformation first, then let story, camera, edit, UI, music, light, and performance all express it.

For the current LegalLens film, the transformation is:

**chaos / time loss → interruption → order / traceability → regained personal time**

This is stronger than “show 5 features quickly.”

### 2. The product is often the hinge, not the protagonist

In human-centered B2B advertising, the software does not need to become a glowing hero object. The person has a desire; friction blocks it; the product changes the causal chain; the human payoff proves the benefit.

This keeps enterprise software emotionally legible without becoming sentimental or generic.

### 3. One structure can travel across modalities

The same narrative can be encoded repeatedly:

- frame density: cluttered → frozen → ordered → open;
- camera: pressured push/limited space → hinge → controlled movement → relaxed pullback;
- sound: notifications/pulse → silence → clean groove → warm resolution;
- light: neutral/cool work pressure → cleaner product light → warmer end-of-day light;
- performance: closed/tensed posture → attention shift → controlled action → open/rested posture;
- edit: accumulating cuts → interruption → proof chain → longer payoff hold.

Cross-modal rhyme creates perceived polish because every department is telling the same story.

### 4. Camera movement should be caused by change

Do not add an orbit, push-in, whip, or parallax simply because a video model can perform it.

For each move, explicitly answer:

> What changed in action, information, pressure, attention, or spatial relationship that makes the camera need to move now?

If no answer exists, keep the camera still or let performer/UI motion carry the beat.

### 5. Product UI should follow gaze hierarchy

When showing software, direct it like a scene:

- choose what the eye sees first;
- reveal the causal relation next;
- highlight only the proof needed for the promise;
- use local parallax / masks / 2.5D / clean push-ins;
- avoid rotating the whole screen in 3D when text fidelity matters.

A good software shot is closer to guided attention than to a flashy device commercial.

### 6. Human stakes can be tiny and still be powerful

A 15-second film cannot support a complicated subplot. One small off-screen life cue — e.g. an evening reminder or checking the time while the desk is still buried — can establish a real cost without adding another character or location.

The key is that the cue changes the meaning of the workload: it is no longer only “a lot of work”; it is “work consuming life.”

### 7. Use micro-actions instead of emotion labels

“Stressed,” “relieved,” “confident,” and “premium” are weak directions by themselves.

Use physical behaviors that a performer or model can render:

- gaze switches;
- hand stops halfway through packing;
- fingers release a tight grip;
- shoulders drop;
- breath changes;
- an object is set down deliberately;
- the body occupies more space after pressure is released.

The viewer infers emotion from behavior.

### 8. Silence is a visual-effects tool

In a pressure-to-solution ad, a short silence at the hinge can be more powerful than adding more VFX. Removing notification noise can make the product entrance feel like order arrived before any visual scan line appears.

Design silence as an event, not as empty audio.

### 9. Avoid simultaneous instability

Generated video becomes fragile when one shot asks for too many major transformations at once: identity change + camera move + location change + UI recreation + lighting shift + complex hand action.

Split the sequence or composite stable source elements. Preserve anchors and change only what the shot needs.

### 10. Prompts should encode end-state handoff

A strong node/shot prompt should specify not only what happens but where the shot ends:

- final performer pose/gaze;
- final camera framing;
- final UI state;
- motion direction;
- sound tail;
- what the next shot inherits.

This improves continuity and makes editing intentional.

### 11. Explore internally, converge for the user

The creative agent should test obvious, minimal, cinematic, commercial, emotional, metaphorical, extreme, and counterintuitive possibilities internally. It should not make the user act as the search algorithm unless they ask for options.

The output should reflect broad exploration but arrive as a coherent recommendation.

### 12. Diagnose before rerolling

When a result fails, first decide whether the cause is:

- story/intent;
- shot purpose;
- blocking;
- camera;
- continuity;
- prompt ambiguity;
- product fidelity;
- tool mismatch;
- sound-picture mismatch;
- aesthetic excess.

Only then regenerate or edit. Random rerolls waste good information.

## Maintenance rule

Add a new entry only when it is:

- broadly reusable across creative tasks; or
- a project insight likely to matter again after chat context is gone.

Keep transient shot wording and current decisions in `STATE.md` or task-specific checkpoints.