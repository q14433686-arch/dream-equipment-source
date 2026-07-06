# Round 55 Vanilla Material Shields — 2026-07-03

## Scope

Added shield-only families for selected vanilla equipment materials that are not otherwise part of Dream Equipment's family list:

- copper
- golden
- diamond
- netherite

This follows the user's request to add original/vanilla material shields. Netherite is tuned to be very strong, but not unlimited or outside the existing balance scale.

## Added items

New custom shields:

```text
copper_shield
golden_shield
diamond_shield
netherite_shield
```

Current totals:

```text
families: 60
custom items: 372
shields: 60
```

## Data model

Added four shield-only family declarations to:

```text
src/main/resources/data/dream_equipment/equipment_families.json
```

These families have no armor/tools, only shield declarations.

## Durability tuning

```text
copper_shield    420
golden_shield    224
diamond_shield   780
netherite_shield 1100
```

Balance notes:

- Golden shield is low durability, matching gold's fragile identity.
- Copper shield sits above vanilla wood shield but below high-tier gem/stone heavy shields.
- Diamond shield is strong, but still below obsidian/netherite.
- Netherite shield is the strongest shield currently, but not excessive: it is only modestly above obsidian shield and remains vanilla-like in blocking behavior.

## Repair materials

Added `repair_ingredients` for the new families:

- copper: copper ingot / copper block
- golden: gold ingot / gold block
- diamond: diamond / diamond block
- netherite: netherite ingot / netherite block

## Netherite behavior

`netherite_shield` is marked fire-resistant at item registration time.

This is a Java-owned mechanism consistent with netherite item expectations, while its durability and content declaration remain JSON-owned.

## Resource generation

`generate_equipment_resources.py` now emits shield resources for 60 shield families.

Generator-managed file count increased:

```text
1349 → 1369
```

The shield texture generator now emits:

```text
60 shield base textures
```

Particle/source texture mapping was extended for:

- copper ingot → copper block
- gold ingot → gold block
- diamond → diamond block
- netherite ingot → netherite block

## Validation

Executed:

```bash
python3 scripts/generate_equipment_resources.py
python3 scripts/generate_wood_worn_textures.py
python3 scripts/generate_shield_textures.py
python3 scripts/validate_equipment_families_json.py
python3 scripts/validate_dream_equipment_assets.py
python3 scripts/validate_set_effects_json.py
python3 scripts/audit_equipment_balance.py
JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks
```

Results:

- Equipment resource generator drift check: PASS — 1369 generated resources in sync.
- Wood/log worn texture generator: PASS — 72 worn layer files regenerated.
- Shield texture generator: PASS — 60 shield base textures generated.
- Equipment family validator: PASS — 60 families / 372 items.
- Asset validator: PASS — includes shield resources/textures and vanilla shield recipe override.
- Set-effect validator: PASS — includes shield effect checks.
- Balance audit: PASS — 372 entries including all shields.
- Gradle build: BUILD SUCCESSFUL.

## Client-only checks

1. Confirm the four new shields appear and localize correctly.
2. Confirm recipes craft correctly.
3. Confirm offhand equip and blocking behavior.
4. Confirm repair materials work.
5. Confirm `netherite_shield` is fire-resistant and durability feels strong but not excessive.
6. Confirm shield custom base textures render for all four new shields.
7. Confirm vanilla shield recipe remains disabled and does not conflict.
