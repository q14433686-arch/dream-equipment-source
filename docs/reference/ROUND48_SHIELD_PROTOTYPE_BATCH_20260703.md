# Round 48 Shield Prototype Batch — 2026-07-03

## Scope

Implemented the first behavior-focused custom shield prototype batch after the Round 47 shield feasibility audit.

This pass intentionally keeps the batch small and uses vanilla shield behavior/rendering first. It does **not** attempt custom material-specific shield base rendering yet.

## Added prototype shields

Added 8 shield items:

- `oak_shield`
- `cherry_shield`
- `bamboo_shield`
- `emerald_shield`
- `redstone_shield`
- `amethyst_shield`
- `prismarine_shield`
- `obsidian_shield`

Total registered item count is now 320.

## Data model

Added optional `shield` declarations to selected families in:

```text
src/main/resources/data/dream_equipment/equipment_families.json
```

Example:

```json
"shield": {
  "enabled": true,
  "durability": 336
}
```

Shield durability is JSON-owned.

Prototype durability values:

- oak: 336
- cherry: 336
- bamboo: 300
- emerald: 672
- redstone: 180
- amethyst: 520
- prismarine: 560
- obsidian: 900

## Java implementation

Updated:

```text
src/main/java/com/dreamequipment/DreamEquipmentFamilyRules.java
src/main/java/com/dreamequipment/DreamEquipmentItems.java
src/main/java/com/dreamequipment/DreamEquipmentFuelValues.java
```

### Family loader

`DreamEquipmentFamilyRules` now parses optional `shield` data.

### Item registration

`DreamEquipmentItems` registers shields as `ShieldItem` with vanilla-like shield components:

- durability from JSON
- `DataComponents.BANNER_PATTERNS = BannerPatternLayers.EMPTY`
- repairable through the existing family repair tag
- offhand equippable-unswappable
- delayed `DataComponents.BLOCKS_ATTACKS`
- `SoundEvents.SHIELD_BREAK` break sound

The blocking behavior recreates the vanilla shield `BlocksAttacks` setup:

- 0.25s block delay
- 90-degree damage reduction entry
- shield item damage function
- `DamageTypeTags.BYPASSES_SHIELD`
- `SoundEvents.SHIELD_BLOCK`
- `SoundEvents.SHIELD_BREAK`

### Fuel behavior

Because wood/plank equipment already has JSON-owned fuel values, wood/plank prototype shields are also registered as fuel:

```text
fuel time = fuel_burn_time_per_material × 6 material slots
```

For oak/cherry/bamboo shield prototypes this is currently `300 × 6 = 1800` ticks.

## Resource generation

Updated:

```text
scripts/generate_equipment_resources.py
```

For each shield it now generates:

- item definition under `assets/dream_equipment/items/<id>.json`
- base model under `assets/dream_equipment/models/item/<id>.json`
- blocking model under `assets/dream_equipment/models/item/<id>_blocking.json`
- shaped recipe under `data/dream_equipment/recipe/<id>.json`
- zh_cn/en_us lang keys

The shield item definition mirrors vanilla's current special-renderer structure:

- condition on `minecraft:using_item`
- special shield model
- normal and blocking base models

Important limitation: these shields currently use vanilla special shield rendering. Material-specific base shield textures are deferred until the prototype behavior is tested.

## Recipes

Default prototype recipe mirrors vanilla shield shape but uses the family material:

```text
MIM
MMM
 M
```

Where:

- `M` = family ingredient
- `I` = `minecraft:iron_ingot`

## Validator updates

Updated:

- `scripts/validate_equipment_families_json.py`
  - validates optional `shield` declarations and positive durability
  - expects shield item definition/model/blocking-model/recipe resources
- `scripts/validate_dream_equipment_assets.py`
  - checks shield resources and Java shield registration markers
- `scripts/audit_equipment_balance.py`
  - includes shield durability entries in the total count and summary

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

- Equipment resource generator drift check: PASS — 1157 generated resources in sync.
- Wood/log worn texture generator: PASS — 72 worn layer files regenerated.
- Equipment family validator: PASS — 56 families / 320 items.
- Asset validator: PASS — 312 texture-backed items / 56 materials, plus shield special-renderer resources.
- Set-effect validator: PASS — 24 passive entries / 4 brittle entries.
- Balance audit: PASS — 320 entries including shield prototypes.
- Gradle build: BUILD SUCCESSFUL.

Jar spot-check confirmed shield resources are packed, including:

- `assets/dream_equipment/items/oak_shield.json`
- `assets/dream_equipment/models/item/oak_shield.json`
- `assets/dream_equipment/models/item/oak_shield_blocking.json`
- `data/dream_equipment/recipe/oak_shield.json`

## Client-only checks

Required live-client checks:

1. Confirm all 8 prototype shields appear in the combat creative tab.
2. Confirm recipes craft correctly and recipe book display is sane.
3. Equip shields in offhand and confirm normal/blocking transforms.
4. Confirm right-click/use blocking works in first and third person.
5. Confirm blocked attacks reduce damage and damage shield durability.
6. Confirm axe/disable behavior matches vanilla expectations.
7. Confirm anvil repair uses existing family repair tags.
8. Confirm oak/cherry/bamboo shields work as furnace fuel if expected.
9. Confirm visual acceptability of vanilla special-renderer output.
10. Test whether banner decoration works or whether custom shields should intentionally not support it.

## Known limitation

Material-specific shield base textures are not implemented in this prototype. The vanilla `ShieldSpecialRenderer` uses fixed shield base sprites, so material-specific shield visuals will require a separate client-rendering decision if the vanilla special-renderer output is not acceptable.

Do not expand shields to all families until this prototype batch is tested.
