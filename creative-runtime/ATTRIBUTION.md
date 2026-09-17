# Creative Runtime — Attribution and Research Notes

## External directing reference studied

### Story-Film Skills

- Repository: `badgids/Story-Film-Skills`
- Author/Developer: Alan Guice (Badgids)
- License: Apache License 2.0
- Version observed during research: README displayed v0.0.40 / canonical 00.00.40.

The local `creative-director-runtime` skill does not copy the upstream package wholesale. It synthesizes and rewrites general directing/production principles relevant to this project's short-form branded-video workflow.

Particularly useful upstream materials reviewed:

- `skills/director-book/SKILL.md`
- `skills/shot-design/SKILL.md`
- `skills/performance-blocking/SKILL.md`
- `references/FILM_GRAMMAR.md`
- `references/DRAMATURGY_RULES.md`

Useful principles learned and adapted in project language:

- resolve dramaturgy before model-specific prompt syntax;
- state the audience question / desire / obstacle / spatial geometry / gaze / rhythm before shot design;
- every shot must have a dramatic or practical job;
- motivate camera motion by a real change in action, information, pressure, attention, or spatial relationship;
- use concrete physical behavior instead of abstract emotion-only direction;
- track performer start/end state for continuity;
- treat eyelines, screen direction, eye trace, match-on-action, and axis management as first-class concerns;
- design the minimum useful coverage rather than piling on angles;
- plan sound and intentional silence as part of direction rather than an afterthought;
- preserve durable shot/scene intent outside chat memory.

## User-provided creative foundation

The repository's `max-potential-multimodal-creative-agent` skill is an operational distillation of the user's supplied “Max Potential Multimodal Creative Agent Manifesto / 多模态创作 Agent 最大潜力原则.” It is treated as the creative philosophy layer above the director runtime.

Its most important retained ideas are:

- understand rather than merely constrain;
- explore broadly but converge precisely;
- transfer structures across image, video, music, language, UI, and narrative;
- separate creator mode from critic mode;
- diagnose failures instead of blindly rerolling;
- keep uncertainty explicit;
- preserve useful surprise when it strengthens the real goal;
- do not let the currently available tool dictate the creative idea;
- treat durable project files as long-term creative memory.

## Maintenance rule

When a new external skill or directing method materially improves the runtime:

1. record the source and license here;
2. extract principles rather than blindly copying implementation-specific rules;
3. update the relevant local skill only when the new principle is broadly reusable;
4. put project-specific insights in `LEARNINGS.md`, not in the universal skill;
5. update `STATE.md` only for current project facts/decisions.