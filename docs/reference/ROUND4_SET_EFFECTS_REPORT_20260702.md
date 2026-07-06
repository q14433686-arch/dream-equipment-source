# Round 4 Set Effects Report — 2026-07-02

## Scope

Added first-pass gameplay effects for several full sets and one single-piece equipment item. These are intentionally simple, vanilla-effect-based mechanics so they can be live-tested before adding custom effects/components.

## Implemented effects

### Emerald full set

Condition: wearing all four emerald armor pieces.

Effect:

- Grants `Luck I` while the full set is worn.

Intent: emerald gear has a treasure/trading/good-fortune fantasy without becoming direct combat power creep.

### Cactus full set

Condition: wearing all four cactus armor pieces.

Effect:

- When the wearer is damaged by a living attacker, the attacker takes 1 thorns-style damage.

Intent: cactus armor has a clear thorn identity. This is intentionally weaker than high-level Thorns enchantment until tested.

### Armadillo shell boots

Condition: wearing `armadillo_shell_boots`.

Effect:

- After fall damage is applied, heals back 35% of the fall damage taken.

Intent: approximates landing protection without needing a damage-modification mixin yet. This should feel like partial fall protection, not immunity.

### Bone full set

Condition: wearing all four bone armor pieces.

Effect:

- Grants `Night Vision I` while the full set is worn.

Intent: skeleton/bone fantasy with exploration utility.

### Paper full set

Condition: wearing all four paper armor pieces.

Effects:

- When dry: grants `Slow Falling I`.
- When in water or rain: grants `Weakness I` and `Slowness I`.

Intent: paper is light but bad when wet.

### Glass full set

Condition: wearing all four glass armor pieces.

Effect:

- If the wearer takes at least 6 damage, there is a 25% chance one random glass armor piece shatters and is removed, with glass break sound.

Intent: glass armor is visually fun but brittle.

### Obsidian full set

Condition: wearing all four obsidian armor pieces.

Effects:

- Grants `Fire Resistance I`.
- Grants `Resistance I`.
- Also grants `Slowness I` as the weight penalty.

Intent: heavy late-game protective set, strong but not free.

## Java implementation

Added `DreamEquipmentSetEffects`:

- registers `ServerTickEvents.END_SERVER_TICK` for passive full-set effects
- registers `ServerLivingEntityEvents.AFTER_DAMAGE` for cactus retaliation, armadillo fall protection, and glass shatter
- called from `DreamEquipment.onInitialize()` after item registration

## Validation

Executed:

```bash
python3 scripts/validate_dream_equipment_assets.py
JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks
```

Results:

- Asset/source validator: PASS — 42 items, 10 materials.
- Build: PASS.
- Jar contains `DreamEquipmentSetEffects.class`.

## Client-only checks

- Full emerald set shows Luck.
- Cactus retaliation triggers only when attacked and does not loop/crash.
- Armadillo shell boots noticeably reduce effective fall damage.
- Bone full set grants night vision without flicker.
- Paper full set is light when dry and penalized in rain/water.
- Glass armor shatter chance feels fair and removes one piece.
- Obsidian set fire resistance/resistance/slowness balance feels acceptable.
