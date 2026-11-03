# Agent Persona & Portrait Visual System — V0.4.0

## Purpose

Each investment faction has one recognizable Agent persona. The portrait is part of the account identity, not decoration. A user should be able to recognize the six roles even when names are hidden.

## Shared art direction

- Six separate single-character portraits; never a contact sheet, collage or six-person group image.
- 4:5 portrait ratio, chest-up / mid-torso framing, face unobstructed and centered for card crops.
- Premium cinematic 3D character portrait with believable human proportions, subtle stylization, sophisticated material detail and a restrained financial-technology environment.
- Same rendering family, portrait scale, camera distance, depth of field and lighting grammar across all six.
- Distinct faces, age, gender presentation, hair silhouette, wardrobe and faction color accents.
- Dark, low-noise background compatible with the product's charcoal / midnight interface. Faction color should appear as a controlled rim light or one wardrobe/accessory accent, not a full-screen color wash.
- No words, numbers, charts, badges containing text, logos, watermarks, flags, national symbols or real-person likenesses.
- No exaggerated cartoon proportions, anime styling, generic stock-photo smiles or low-cost mobile-game NPC look.

## Persona definitions and generation briefs

Each brief is intended to be generated as its own image using the shared art direction above.

### 01 — Value / 价值派

- Age / presence: early-50s male, composed senior investor, salt-and-pepper hair, measured gaze, understated authority.
- Wardrobe: tailored charcoal suit, ivory shirt, restrained champagne-gold tie pin / pocket detail.
- Environment cue: dark wood and brushed brass hints, almost imperceptible balance-sheet / archival-finance geometry.
- Accent: champagne gold #E9C78D.
- Prompt brief: A composed senior value investor in his early 50s, salt-and-pepper hair, thoughtful steady gaze, tailored charcoal suit, ivory shirt and a discreet champagne-gold tie pin, subtle dark-wood and brushed-brass research-office atmosphere.

### 02 — Growth / 成长派

- Age / presence: late-20s to early-30s female, energetic technology investor, curious and optimistic but credible.
- Wardrobe: modern structured blazer with cream base and restrained emerald accents; clean contemporary silhouette.
- Environment cue: abstract glass architecture and subtle forward-moving light geometry, not literal charts.
- Accent: emerald #65D8A5.
- Prompt brief: A confident female technology growth investor around 30, bright focused eyes, contemporary cream blazer with restrained emerald details, poised forward-looking expression, subtle glass architecture and innovation-lab atmosphere.

### 03 — Trend / 趋势派

- Age / presence: early-to-mid-30s male, decisive market operator, alert expression and athletic posture.
- Wardrobe: premium navy technical jacket, glacier-blue seam / collar accents, functional but tailored.
- Environment cue: soft blurred market-terminal light bands suggesting motion, never readable screens.
- Accent: glacier blue #8DB9EE.
- Prompt brief: A decisive male momentum trader in his mid-30s, sharp attentive expression, premium deep-navy technical jacket with restrained glacier-blue details, confident athletic posture, abstract blurred market-terminal light bands behind him.

### 04 — Quant / 量化派

- Age / presence: late-30s female, analytical research scientist, precise and calm; hair tied back, subtle technical glasses.
- Wardrobe: architectural graphite jacket, clean high-neck layer, discreet amethyst accents.
- Environment cue: elegant geometric light structures and faint computational depth, no visible code or numbers.
- Accent: amethyst #C6A1F2.
- Prompt brief: A calm female quantitative research scientist in her late 30s, hair neatly tied back, subtle precision glasses, architectural graphite jacket with restrained amethyst details, intelligent analytical gaze, elegant abstract geometric light structures in the background.

### 05 — Sentiment / 情绪派

- Age / presence: early-30s female, perceptive market-psychology analyst, expressive eyes and emotionally intelligent presence.
- Wardrobe: contemporary dark outfit with a single amber-orange scarf / accessory, tactile fabric.
- Environment cue: layered soft reflections and blurred human-scale city lights hinting at attention and crowd behavior.
- Accent: amber orange #F1A66E.
- Prompt brief: A perceptive female market psychology analyst in her early 30s, expressive observant eyes, emotionally intelligent presence, refined dark contemporary outfit with one amber-orange silk accent, soft layered reflections and distant city-light atmosphere.

### 06 — Macro / 宏观派

- Age / presence: early-to-mid-50s female, globally experienced macro strategist, calm, composed and authoritative.
- Wardrobe: slate-blue tailored suit, subtle cyan scarf / lapel detail, international finance restraint.
- Environment cue: abstract glass-and-steel skyline with atmospheric horizon light, no recognizable landmark.
- Accent: cyan #7DD6DF.
- Prompt brief: A globally experienced female macro strategist in her mid-50s, composed confident gaze, tailored slate-blue suit with a restrained cyan lapel detail, abstract glass-and-steel skyline and atmospheric horizon light behind her.

## Asset contract

| Agent ID | Asset path | Ratio | Intended use |
|---|---|---:|---|
| value | assets/agents/value.webp | 4:5 | Agent card + selected workspace |
| growth | assets/agents/growth.webp | 4:5 | Agent card + selected workspace |
| trend | assets/agents/trend.webp | 4:5 | Agent card + selected workspace |
| quant | assets/agents/quant.webp | 4:5 | Agent card + selected workspace |
| sentiment | assets/agents/sentiment.webp | 4:5 | Agent card + selected workspace |
| macro | assets/agents/macro.webp | 4:5 | Agent card + selected workspace |

The UI already maps each Agent to a stable data-image-src slot. The generated assets should be added under assets/agents/ and then bound as the real img.src values. Do not substitute initials or hand-drawn SVG as the finished portrait artwork.

## Generation / delivery status

- Persona system and prompt briefs: defined.
- Image output: pending explicit user authorization; no image-generation jobs have been submitted.
- Do not mark this asset set complete until all six images are generated, inspected for consistency, added to the repository and loaded by the browser regression.
