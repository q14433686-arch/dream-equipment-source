# Round 38 Cherry Texture Fix and Fuel Values — 2026-07-03

## Scope

Implemented two client-reported fixes:

1. Cherry wood armor inventory icons had broken/incomplete silhouettes for helmet, leggings, and boots.
2. Coal equipment plus wooden/plank and log/stem/bamboo-block equipment should be valid furnace fuel, with burn time derived from crafting material count and the base material burn time.

## Cherry armor item texture fix

### Issue

`cherry_helmet.png`, `cherry_leggings.png`, and `cherry_boots.png` were still 16×16 legacy/partial icons while most accepted wood/plank/log armor icons use the current 128×128 full armor silhouettes. In inventory, this made the helmet, leggings, and boots appear visibly incomplete.

### Fix

Regenerated all four `cherry_*` armor item icons from the accepted `oak_*` armor silhouettes and recolored them using the vanilla `cherry_planks` palette from Minecraft 26.1.2.

Changed textures:

- `src/main/resources/assets/dream_equipment/textures/item/cherry_helmet.png`
- `src/main/resources/assets/dream_equipment/textures/item/cherry_chestplate.png`
- `src/main/resources/assets/dream_equipment/textures/item/cherry_leggings.png`
- `src/main/resources/assets/dream_equipment/textures/item/cherry_boots.png`

All four are now 128×128 and match the current complete wood armor icon silhouette style.

## Fuel values

### Architecture decision

Fuel values are data-driven from `equipment_families.json`:

- Added optional family field `fuel_burn_time_per_material`.
- Java owns the furnace fuel registration mechanism via `DreamEquipmentFuelValues` and Fabric `FuelValueEvents.BUILD`.
- Java computes equipment fuel time as:

```text
fuel_burn_time = fuel_burn_time_per_material × armor_recipe_material_count
```

Armor recipe material counts follow the vanilla-shaped armor patterns:

```text
helmet     = 5 materials
chestplate = 8 materials
leggings   = 7 materials
boots      = 4 materials
```

This follows the user's requested rule: fuel time is based on the number of recipe ingredients and the ingredient's burn time.

### Data values added

Coal armor:

- `coal`: `1600` ticks per material.

Wood/plank/log/stem/bamboo-block armor:

- All plank families: `300` ticks per material.
- All log/stem/bamboo-block families: `300` ticks per material.

Affected fuel families:

- `coal`
- `oak`, `spruce`, `birch`, `jungle`, `acacia`, `dark_oak`, `mangrove`, `cherry`, `pale_oak`, `bamboo`, `crimson`, `warped`
- `oak_log`, `spruce_log`, `birch_log`, `jungle_log`, `acacia_log`, `dark_oak_log`, `mangrove_log`, `cherry_log`, `pale_oak_log`, `bamboo_block`, `crimson_stem`, `warped_stem`

### Resulting burn times

For wood/plank/log/stem/bamboo-block armor with `300` ticks per material:

- Helmet: `1500` ticks.
- Chestplate: `2400` ticks.
- Leggings: `2100` ticks.
- Boots: `1200` ticks.

For coal armor with `1600` ticks per material:

- Helmet: `8000` ticks.
- Chestplate: `12800` ticks.
- Leggings: `11200` ticks.
- Boots: `6400` ticks.

## Files changed

- `src/main/java/com/dreamequipment/DreamEquipment.java`
  - Registers fuel values during initialization.
- `src/main/java/com/dreamequipment/DreamEquipmentFuelValues.java`
  - New data-driven fuel registration mechanism.
- `src/main/java/com/dreamequipment/DreamEquipmentFamilyRules.java`
  - Loads optional `fuel_burn_time_per_material` from family JSON.
- `src/main/resources/data/dream_equipment/equipment_families.json`
  - Adds fuel burn values for coal and all wood/log-like armor families.
- `scripts/validate_equipment_families_json.py`
  - Validates `fuel_burn_time_per_material` is non-negative.
- `scripts/validate_dream_equipment_assets.py`
  - Checks fuel source exists and required fuel families declare positive fuel values.
- `src/main/resources/assets/dream_equipment/textures/item/cherry_*.png`
  - Fixed inventory icons.

## Validation

Executed:

```bash
python3 scripts/generate_equipment_resources.py --write
python3 scripts/generate_equipment_resources.py
python3 scripts/validate_equipment_families_json.py
python3 scripts/validate_dream_equipment_assets.py
python3 scripts/validate_set_effects_json.py
python3 scripts/audit_equipment_balance.py
JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks
```

Results:

- Generator write/check: PASS — 1125 generated resources in sync.
- Equipment family validator: PASS — 56 families / 312 items.
- Asset validator: PASS — 312 items / 56 materials.
- Set-effect validator: PASS — 24 passive entries / 4 brittle entries.
- Balance audit: PASS.
- Gradle build: BUILD SUCCESSFUL.

## Client-only checks

1. Confirm cherry helmet/chestplate/leggings/boots inventory icons are complete and visually consistent.
2. Confirm coal armor pieces work as furnace fuel with expected relative burn times.
3. Confirm all plank armor and log/stem/bamboo-block armor pieces work as furnace fuel.
4. Confirm non-fuel materials such as stone, glass, redstone, lapis, etc. did not become fuel unintentionally.
