# Round 30 Amethyst Sonic Boom Immunity — 2026-07-02

## Scope

Implemented the user's request: full amethyst armor set should be immune to the Warden's sonic boom attack.

## Data

Added to `data/dream_equipment/set_effects.json`:

```json
"damage_immunities": [
  {
    "material": "amethyst",
    "damage_type": "minecraft:sonic_boom"
  }
]
```

## Java behavior

`DreamEquipmentSetEffectRules` now loads `damage_immunities` as data-driven rules.

`DreamEquipmentSetEffects.allowDamage(...)` checks those rules before normal damage handling:

- if the player is wearing a full matching material set
- and incoming `DamageSource` matches the configured damage type
- then damage is canceled

Current concrete behavior:

- full `amethyst` armor set cancels `minecraft:sonic_boom` damage

## Tooltip

Amethyst armor tooltip now includes an immunity line sourced from the new JSON rule:

- zh: `免疫：坚守者声波`
- en template: `Immune to: %s`

## Validation

Executed:

```bash
python3 scripts/generate_equipment_resources.py --write
python3 scripts/generate_equipment_resources.py
python3 scripts/validate_equipment_families_json.py
python3 scripts/validate_dream_equipment_assets.py
python3 scripts/validate_set_effects_json.py
JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks
```

Results:

- generator write/check: PASS
- equipment families: PASS — 56 families / 284 items
- assets: PASS — 284 items / 56 materials
- set effects: PASS — 24 passive effects / 4 brittle armor entries, with damage immunity validation
- build: PASS

## Client-only checks

- Wear full amethyst armor.
- Get hit by Warden sonic boom.
- Confirm the sonic boom damage is canceled.
- Confirm other damage types still apply normally.
- Confirm tooltip shows the sonic immunity line.
