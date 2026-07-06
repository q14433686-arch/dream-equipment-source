# Round 32 Log Icon and Rock Tool Completion — 2026-07-02

## Scope

Fixed the repeated log armor item-icon issue and completed the second part of the user's request for rock-family tools/weapons.

## Log armor icon fix

All log/stem/bamboo-block armor inventory icons were regenerated from the accepted user emerald armor templates, not vanilla leather partial silhouettes.

Affected families:

- oak_log
- spruce_log
- birch_log
- jungle_log
- acacia_log
- dark_oak_log
- mangrove_log
- cherry_log
- pale_oak_log
- bamboo_block
- crimson_stem
- warped_stem

The new generation keeps the full helmet/leggings/boots silhouettes and applies muted log/stem material colors/patterns. This should fix the issue where helmet, leggings, and boots looked incomplete in the inventory.

## Rock tool/weapon completion

Added/generated missing tool textures for the curated rock-family tools/weapons previously added to `equipment_families.json`:

- granite: sword, pickaxe, axe, spear
- diorite: sword, pickaxe, axe, spear
- andesite: sword, pickaxe, axe, spear
- basalt: pickaxe, axe, spear
- smooth_basalt: axe, spear
- dripstone_block: spear
- netherrack: spear

Tool textures are generated from the corresponding vanilla block texture palettes and the accepted tool/spear templates.

## Current totals

- families: 56
- items: 302
- materials/equipment definitions: 56
- generator-managed files: 1095

## Validation

Executed:

```bash
python3 scripts/generate_equipment_resources.py
python3 scripts/validate_equipment_families_json.py
python3 scripts/validate_dream_equipment_assets.py
python3 scripts/validate_set_effects_json.py
JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks
```

Results:

- generator drift check: PASS — 1095 files
- equipment families: PASS — 56 families / 302 items
- assets: PASS — 302 items / 56 materials
- set effects: PASS
- build: PASS

## Client-only checks

- Log/stem/bamboo-block armor icons should no longer be incomplete.
- Granite/diorite/andesite/basalt/smooth basalt/dripstone/netherrack tools should appear and render correctly.
