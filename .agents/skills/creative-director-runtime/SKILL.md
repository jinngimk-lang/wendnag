---
name: creative-director-runtime
description: Direct short-form branded video and multimodal sequences using dramatic purpose, motivated camera, performance blocking, edit logic, continuity, sound, and product-proof integration.
---

# Creative Director Runtime

## Mission

Direct the audience's attention, emotion, information, and time.

A director is not a camera-move generator. The job is to decide:

- what the audience should want to know;
- what changes in the scene;
- what must be seen and what should be withheld;
- where attention goes first and next;
- why the camera or performer moves;
- why the cut happens now;
- how picture and sound express the same underlying transformation.

Resolve dramatic purpose before model syntax, lens language, or prompt polish.

## Scene engine — resolve before shot design

For every scene or micro-sequence, state internally:

1. **Audience question** — what are viewers waiting to discover or feel?
2. **Immediate desire** — what does the viewpoint character want right now?
3. **Obstacle** — what prevents it now?
4. **Geometry** — where are subject, obstacle, goal/exit, and key object in space?
5. **Gaze** — where should the viewer look first, then second?
6. **Rhythm** — where should the scene hold, accelerate, interrupt, or cut?
7. **Change** — what is different at the end of the beat?

If these are unresolved, do not compensate with prettier cinematography.

## Every shot must earn its place

A shot should do at least one real job:

- alter an emotional or power relationship;
- reveal or hide meaningful information;
- advance a physical action;
- increase or release pressure;
- prove a product capability;
- establish necessary geography or continuity;
- create a deliberate transition or payoff.

Delete decorative coverage that does none of these.

## The concrete-detail triad

For important shots, identify:

- **environmental pressure** — a physical fact of the location that affects the character;
- **micro-action** — an observable body/object behavior carrying performance;
- **anchor** — a sound, object, light, reflection, color, UI element, or texture binding the sequence.

Prefer observable behavior over abstract labels such as “stressed,” “cinematic,” or “premium.”

Example: instead of “she is overwhelmed,” use “her eyes jump from the unread-email badge to the contract stack; she rubs the bridge of her nose; another calendar alert appears before she finishes the first page.”

## Performance direction

Do not direct actors with emotion words alone.

Use playable actions and circumstances:

- checks the time but delays standing up;
- begins packing, then notices another urgent contract;
- exhales through the nose, closes eyes for half a second, reopens them and continues;
- after the solution, posture opens, shoulders drop, grip on the mug loosens.

Track start and end state:

- position;
- posture;
- gaze;
- object possession;
- orientation;
- energy level.

This is especially important for image-to-video continuity.

## Motivated camera rule

Every meaningful camera move must answer: **what changed?**

Legitimate triggers include:

- a decision;
- new information;
- a look motivating a reveal;
- rising pressure requiring tighter framing;
- a physical action that must remain readable;
- a spatial relationship changing;
- a release that justifies opening the frame.

If nothing changes, a locked camera may be stronger.

Describe the visible effect first; use hardware/lens numbers only when they matter.

Useful movement vocabulary:

- locked-off;
- pan / tilt;
- push in / pull back;
- lateral track;
- dolly follow;
- crane/reveal;
- handheld follow;
- restrained orbit;
- rack focus.

For significant moves, define start frame, movement reason, and end frame.

## Framing as psychology

Use shot size to control relationship, not as decoration.

- Wide: geography, isolation, burden, environment.
- Medium: behavior and work process.
- Close-up: decision, realization, emotional pressure.
- Insert: proof, object stakes, UI information, time reminder.
- OTS/two-shot: relationship and comparison.

Change framing when the scene's relationship to the subject changes.

## Spatial continuity

Maintain unless deliberately broken:

- dominant screen direction;
- entrances/exits;
- eyelines;
- 180-degree axis;
- object placement;
- match-on-action phase;
- light direction and time of day.

If crossing an axis or changing geography, reorient the viewer intentionally.

At every cut, know where the viewer's eye is. Put the next important information where the eye can find it quickly unless disorientation is the intended effect.

## Edit logic

Never ask only “what is the next shot?” Ask “why should the cut happen at this exact moment?”

Preferred cut priority:

1. emotional truth;
2. story/product information;
3. rhythm;
4. eye trace;
5. screen-plane continuity;
6. geography.

Useful transition families:

- match on action;
- eye-trace match;
- shape/color match;
- sound bridge;
- hard contrast cut;
- motion continuation;
- idea match;
- silence interruption.

A transition is earned when picture, movement, sound, idea, or dramatic state actually carries across it.

## Sound direction

Plan sound at the same time as picture.

Separate:

- voiceover/dialogue;
- ambience;
- Foley;
- UI/product sonic cues;
- designed transitions;
- music;
- deliberate silence.

Use silence as an event. In a pressure→solution story, the most powerful hinge may be the instant the noise stops.

Do not over-sync every animation to sound. Reserve a few precise audiovisual accents for moments of change.

## Product-commercial directing

The product should be a **causal mechanism**, not a floating hero object.

A branded short should make viewers understand:

1. a human cost or desire;
2. the visible friction causing it;
3. the product entering at a decisive hinge;
4. proof of how the product changes the workflow;
5. the human consequence after the product works.

Feature density is not story strength. Select the few product details that prove the promise.

For software UI:

- preserve screenshot truth whenever product fidelity matters;
- prefer 2.5D separation, restrained push-ins, masks, highlights, and local parallax over aggressive full-screen 3D deformation;
- move the camera to follow information hierarchy;
- do not generate fake text to replace legible source UI if the source can be composited;
- connect UI proof to the pain shown earlier.

## Short-form time compression

For a 10–20 second commercial, think in beats rather than trying to reproduce a long-form scene.

A useful but non-mandatory archetype is:

- **hook / pressure** — establish the human problem quickly;
- **stakes** — show what the problem costs outside the product;
- **hinge** — interrupt the old state;
- **proof** — show the product doing specific work;
- **payoff** — return to the human with a visibly changed state.

Do not mechanically reuse timings. Let the actual concept determine where the beats land.

## Shot prompt packet

When writing a generation prompt for a shot, resolve these fields:

- shot ID / duration;
- dramatic job;
- reference image(s) and what each controls;
- immutable continuity anchors;
- start frame/state;
- subject micro-action;
- environment behavior;
- framing/composition;
- camera behavior and movement reason;
- lighting logic;
- sound intent;
- end frame/state;
- handoff to next shot;
- forbidden drift/errors.

This makes a prompt directable rather than merely descriptive.

## Sequence design

Before generating isolated shots, define the sequence's:

- dominant emotional curve;
- visual density curve;
- camera stability curve;
- recurring object/UI/sound anchor;
- reversal or break;
- final image or final sound.

Then make each shot a local expression of that structure.

## Continuity gate for generated video

Check:

- same person / face / age / hair;
- same wardrobe and accessories;
- same office/location layout;
- consistent desk props and screen placement;
- consistent time of day unless transition is deliberate;
- stable UI and logo;
- physical start/end states that can connect;
- motion direction and speed;
- hands and object contact;
- background drift and lighting flicker.

If a shot asks the model to change identity, camera, location, UI, lighting, and major action simultaneously, split the shot or composite it. Too many simultaneous transformations increase failure risk.

## Director–critic pass

After the first cut/plan, perform a second pass as a skeptical director:

- Is the central desire legible without explanation?
- Is the obstacle visible rather than narrated only?
- Does the product arrive too early or too late?
- Does every feature shot prove the stated benefit?
- Does camera behavior mirror the emotional change?
- Does sound create a meaningful hinge?
- Does the final human payoff feel causally earned?
- Is the final remembered idea the product benefit, not just a pretty effect?
- Can one shot or effect be removed to make the piece clearer?

## Source-derived directing principles

This runtime is original project guidance but incorporates and adapts general production ideas learned from the Apache-2.0 `badgids/Story-Film-Skills` project, particularly its `director-book`, `shot-design`, `performance-blocking`, `FILM_GRAMMAR`, and `DRAMATURGY_RULES` materials. See `creative-runtime/ATTRIBUTION.md`.