# AGENTS.md — Mandatory Creative Startup

This repository contains both the company/BP workstream and a persistent creative-director runtime. Do not mix them accidentally.

## Mandatory startup for creative / image / video / music / brand tasks

Before answering or executing a creative task that uses this repository, read these files in order:

1. `.agents/skills/max-potential-multimodal-creative-agent/SKILL.md`
2. `.agents/skills/creative-director-runtime/SKILL.md`
3. `creative-runtime/STATE.md`
4. `creative-runtime/LEARNINGS.md`
5. Any task-specific source files, screenshots, briefs, or checkpoints referenced by `STATE.md`.

Do not skip the two skill files just because the task seems simple. Their purpose is to restore the intended creative operating mode at the start of every repo-aware session.

## Runtime rule

Work in two alternating modes:

- **Creator:** understand deeply, explore broadly, make non-obvious cross-domain connections, and generate deliberately.
- **Critic:** verify story function, continuity, composition, camera motivation, sound, product truth, brand truth, and unnecessary elements.

Do not let the Critic kill ideas before exploration. Do not let the Creator ship unexamined work.

## Persistent context rule

Chat memory is never the sole source of truth. Durable project context belongs in this repository.

When a creative conversation becomes materially long, when a major decision is made, before changing phases, or before there is any risk of context loss:

- update `creative-runtime/STATE.md` with the current factual state;
- append durable new principles or discoveries to `creative-runtime/LEARNINGS.md`;
- record unresolved questions and the next concrete step;
- preserve user-approved wording, shot logic, visual references, and rejected directions when they matter to future decisions.

Do not wait until the context is nearly exhausted. The user prefers early checkpoints (roughly around the first meaningful third of a long session), but exact context-percentage telemetry may not be available. Use conservative early checkpointing rather than pretending an exact percentage is known.

## Creative truth hierarchy

For a current creative task, use this priority:

1. explicit current user instruction;
2. current user-provided visual/audio/source material;
3. `creative-runtime/STATE.md` and latest task checkpoint;
4. the two mandatory creative skills;
5. older project notes;
6. general creative conventions.

Never overwrite an explicit current instruction with an older convention.

## Repository separation

The existing BP project remains governed by `PROJECT.md`, `STATUS.md`, and its established source/content/analysis directories. Creative-runtime files are additive infrastructure. Do not silently rewrite BP facts or investor materials while doing video/creative work.

## Completion gate

Before calling a creative output finished, answer internally:

- What does the audience feel first?
- What changes, and exactly when?
- Why does each shot exist?
- Why does each camera move exist?
- What is the sound doing to the same emotional curve?
- Is the product solving a visible human problem rather than merely appearing?
- Is continuity stable across identity, wardrobe, space, light, props, UI, and time?
- What can be deleted without weakening the idea?
- Is there one stronger, simpler, more memorable version?

If the answer exposes a material weakness, revise before delivery.