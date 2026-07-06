# Round 50 Shield Effects Data-Driven Pass 1 — 2026-07-03

## Scope

Added the first gameplay-effect pass for custom shields so they are no longer only behavior-equivalent material variants.

This pass implements five low-risk, material-readable shield effects:

- cactus shield retaliation
- glass shield shatter
- redstone shield pulse
- slime shield bounce
- paper shield wet weakness

## Data-driven rules

Added `shield_effects` to:

```text
src/main/resources/data/dream_equipment/set_effects.json
```

Current values:

```json
"shield_effects": {
  "cactus": {
    "enabled": true,
    "retaliate_damage": 1.0,
    "cooldown_ticks": 20
  },
  "glass": {
    "enabled": true,
    "shatter_threshold": 5.0,
    "shatter_chance": 0.25
  },
  "redstone": {
    "enabled": true,
    "pulse_signal": 15,
    "pulse_ticks": 8
  },
  "slime": {
    "enabled": true,
    "knockback_strength": 0.6,
    "vertical_boost": 0.1
  },
  "paper": {
    "enabled": true,
    "wet_damage_interval": 20,
    "wet_damage": 1
  }
}
```

Java owns the trigger logic; JSON owns effect values.

## Java implementation

Added:

```text
src/main/java/com/dreamequipment/DreamEquipmentShieldEffectRules.java
src/main/java/com/dreamequipment/DreamEquipmentShieldEffects.java
```

Updated:

```text
src/main/java/com/dreamequipment/DreamEquipment.java
src/main/java/com/dreamequipment/DreamEquipmentRedstonePower.java
src/main/java/com/dreamequipment/client/DreamEquipmentTooltips.java
```

### Shield effect triggers

`DreamEquipmentShieldEffects` listens to:

- `ServerLivingEntityEvents.AFTER_DAMAGE` for successful blocked attacks.
- `ServerTickEvents.END_SERVER_TICK` for wet paper shield durability decay while blocking.

The active shield is detected from `player.getUseItem()` when the player is blocking.

## Implemented effects

### `cactus_shield`

On successful block against a living attacker:

- retaliates for `retaliate_damage`
- uses `cooldown_ticks` to avoid rapid repeated thorns triggers

### `glass_shield`

On successful block:

- if blocked base damage is at least `shatter_threshold`
- has `shatter_chance` to break the shield directly

### `redstone_shield`

On successful block:

- emits a Dream Equipment redstone pulse at the player's position
- uses `pulse_signal` and `pulse_ticks`

This reuses the redstone pulse infrastructure instead of creating a continuous redstone source.

### `slime_shield`

On successful block against a living attacker:

- pushes/bounces the attacker away from the player
- uses `knockback_strength` and `vertical_boost`

### `paper_shield`

While actively blocking in water/rain:

- every `wet_damage_interval` ticks
- applies `wet_damage` durability loss

## Tooltip updates

Shield tooltips now show shield durability and special shield effects where applicable.

Added/updated lang keys:

- `tooltip.dream_equipment.shield`
- `tooltip.dream_equipment.shield_cactus`
- `tooltip.dream_equipment.shield_glass`
- `tooltip.dream_equipment.shield_redstone`
- `tooltip.dream_equipment.shield_slime`
- `tooltip.dream_equipment.shield_paper`

## Validator updates

Updated:

```text
scripts/validate_set_effects_json.py
scripts/validate_dream_equipment_assets.py
```

Checks include:

- `shield_effects` value ranges
- required shield effect source files
- shield effect source markers

## Validation

Executed:

```bash
python3 scripts/generate_equipment_resources.py
python3 scripts/generate_wood_worn_textures.py
python3 scripts/validate_equipment_families_json.py
python3 scripts/validate_dream_equipment_assets.py
python3 scripts/validate_set_effects_json.py
python3 scripts/audit_equipment_balance.py
JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks
```

Results:

- Equipment resource generator drift check: PASS — 1349 generated resources in sync.
- Wood/log worn texture generator: PASS — 72 worn layer files regenerated.
- Equipment family validator: PASS — 56 families / 368 items.
- Asset validator: PASS — texture-backed item/material checks plus shield special-renderer/effect resources.
- Set-effect validator: PASS — includes shield effect checks.
- Balance audit: PASS — 368 entries including all shields.
- Gradle build: BUILD SUCCESSFUL.

## Client-only checks

1. `cactus_shield`: block melee attacks and confirm small retaliation with cooldown.
2. `glass_shield`: block high-damage attacks and confirm occasional shatter.
3. `redstone_shield`: block an attack beside redstone dust/lamp and confirm a short pulse.
4. `slime_shield`: block a living attacker and confirm bounce/knockback.
5. `paper_shield`: hold block in rain/water and confirm durability loss.
6. Confirm tooltips display the relevant shield effects.
7. Confirm normal shields without special rules still behave like vanilla-like custom shields.

## Deferred

Additional shield effects for obsidian, prismarine, amethyst, bone, coal, quartz, etc. remain deferred until these first five effects are client-tested.
