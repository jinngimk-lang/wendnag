# Agent Persona & Portrait Visual System — V0.5.0

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

| Faction | Portrait atlas cell | Research-room atlas cell | Ratio / use |
|---|---:|---:|---|
| value | (0, 0) | (0, 0) | 4:5 portrait / card + selected workspace |
| growth | (1, 0) | (1, 0) | 4:5 portrait / card + selected workspace |
| trend | (2, 0) | (2, 0) | 4:5 portrait / card + selected workspace |
| quant | (0, 1) | (0, 1) | 4:5 portrait / card + selected workspace |
| sentiment | (1, 1) | (1, 1) | 4:5 portrait / card + selected workspace |
| macro | (2, 1) | (2, 1) | 4:5 portrait / card + selected workspace |

- Portrait atlas: assets/agents-sprite.webp (3 columns × 2 rows, six 120 × 150 cells).
- Research-room atlas: assets/rooms-sprite.webp (3 columns × 2 rows, six 160 × 90 cells).
- Each Agent definition owns stable spriteX/spriteY and roomX/roomY coordinates. Cards and the selected-Agent workspace crop the mapped cell using CSS; they do not render the composite atlas as an image.
- Keep the faction IDs stable if replacing the compact atlases with separate full-resolution files later.

## Generation / delivery status

- Persona briefs and six generated individual portraits: complete and integrated.
- Six generated research-room scenes: complete and integrated.
- Asset files committed and loaded by Playwright in the V0.5.0 browser suite.
- Visual mapping, portrait load, room scene count and selected workspace are verified in GitHub Actions run #41797576138.
- No image-generation job or paid generation balance was needed in this continuation; the existing generated assets were reused.
 
## V0.5.0 generated asset integration

The six individual portraits and six room references have now been integrated into the running prototype. The six portraits were mapped in faction order (value, growth, trend, quant, sentiment, macro); the six research-room images use the same faction order. The two source atlases are WebP files:

- assets/agents-sprite.webp — 3 columns × 2 rows; each portrait occupies one 120 × 150 cell.
- assets/rooms-sprite.webp — 3 columns × 2 rows; each research room occupies one 160 × 90 cell.

CSS positions each card and detail avatar against its faction cell. The room banner and card background use the corresponding room cell. These are implementation atlases only: the UI crops one cell at a time and never displays the composite atlas as a contact sheet.

| Faction | Portrait cell | Room cell | Accent |
|---|---:|---:|---|
| Value / 价值派 | (0, 0) | (0, 0) | Champagne gold |
| Growth / 成长派 | (1, 0) | (1, 0) | Emerald |
| Trend / 趋势派 | (2, 0) | (2, 0) | Glacier blue |
| Quant / 量化派 | (0, 1) | (0, 1) | Soft violet |
| Sentiment / 情绪派 | (1, 1) | (1, 1) | Warm amber |
| Macro / 宏观派 | (2, 1) | (2, 1) | Ice cyan |

The portrait atlas is deliberately compact for workstation rendering. If a later large-screen art direction requires full-bleed portraits, replace the atlas with six separate optimized WebP assets without changing faction IDs or visual-role mapping.
