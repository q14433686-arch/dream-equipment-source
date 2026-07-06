# Round 51 Shield Effects Data-Driven Pass 2 — 2026-07-03

## Scope

Added the second shield-effect batch after the first five shield effects were implemented.

This pass adds material-readable effects for:

- obsidian shield
- prismarine shield
- amethyst shield
- bone shield
- coal shield
- quartz shield

## Data-driven rules

Extended `shield_effects` in:

```text
src/main/resources/data/dream_equipment/set_effects.json
```

New entries:

```json
"obsidian": {
  "enabled": true,
  "refund_damage": 2,
  "slowness_duration_ticks": 40,
  "slowness_amplifier": 0
},
"prismarine": {
  "enabled": true,
  "water_refund_damage": 1
},
"amethyst": {
  "enabled": true,
  "sonic_boom_damage_cost": 8
},
"bone": {
  "enabled": true,
  "undead_refund_damage": 1
},
"coal": {
  "enabled": true,
  "fire_refund_damage": 2
},
"quartz": {
  "enabled": true,
  "projectile_refund_damage": 1
}
```

## Implemented effects

### `obsidian_shield`

- While actively blocking, applies short Slowness to represent heavy shield weight.
- On successful block against fire/explosion damage, refunds part of shield durability loss.

### `prismarine_shield`

- In water, successful blocks refund part of shield durability loss.

### `amethyst_shield`

- Can block Warden sonic boom damage by cancelling the damage while costing shield durability.
- Uses `DamageTypes.SONIC_BOOM` in the allow-damage hook.

### `bone_shield`

- Successful blocks against undead-like attackers refund part of shield durability loss.
- Undead-like detection currently covers entity ids containing zombie/skeleton plus drowned, husk, stray, bogged, parched, and wither-like ids.

### `coal_shield`

- Successful blocks against fire damage refund part of shield durability loss.

### `quartz_shield`

- Successful blocks against projectile damage refund part of shield durability loss.

## Java/resource changes

Updated:

- `DreamEquipmentShieldEffectRules`
- `DreamEquipmentShieldEffects`
- `DreamEquipmentTooltips`
- `set_effects.json`
- `generate_equipment_resources.py`
- `validate_set_effects_json.py`

Tooltip lines were added for the new shield effects.

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
- Asset validator: PASS — texture-backed item/material checks plus shield resources/effects.
- Set-effect validator: PASS — includes shield effect checks.
- Balance audit: PASS — 368 entries including all shields.
- Gradle build: BUILD SUCCESSFUL.

## Client-only checks

1. `obsidian_shield`: confirm Slowness while blocking and improved durability behavior against fire/explosions.
2. `prismarine_shield`: confirm water blocks refund durability.
3. `amethyst_shield`: confirm Warden sonic boom is blocked/cancelled at shield durability cost.
4. `bone_shield`: confirm undead attacks refund durability.
5. `coal_shield`: confirm fire damage blocks refund durability.
6. `quartz_shield`: confirm projectile blocks refund durability.
7. Confirm tooltip lines for all six new effects.
8. Confirm first-pass shield effects still work.

## Notes

These effects intentionally use small durability refunds rather than full custom damage math, because vanilla shield blocking already applies its own damage and disable rules through `BlocksAttacks`. The refund approach is low-risk and keeps shield behavior close to vanilla while expressing material identity.
