# Round 17 Equipment Families Data-Driven Registration — 2026-07-02

## Scope

User requested full decoupling/data-driven work split across two rounds. This is round 1 of 2.

This round moves equipment family declarations and registration-time material stats out of hardcoded Java tables and into JSON.

## Added JSON

New file:

```text
src/main/resources/data/dream_equipment/equipment_families.json
```

It owns:

- family id
- ingredient
- zh/en display base names for future generators
- armor pieces included in the family
- armor defense values
- armor durability multiplier
- armor enchantability
- armor toughness and knockback resistance
- equip sound category
- tool types included in the family
- tool mining tier tag / incorrect-blocks tag
- tool durability
- tool speed
- tool attack damage bonus
- tool enchantability

Current data scope:

- 37 equipment families
- 184 generated/registered items expected from the data

## Added loader

New class:

```text
DreamEquipmentFamilyRules
```

It loads `equipment_families.json` at startup and exposes the parsed family records.

## Refactored registration

`DreamEquipmentItems` was rewritten to register families dynamically from `DreamEquipmentFamilyRules.current().families`.

Before this round:

- material definitions were hardcoded as many Java fields
- tool/armor registration was a long manual block
- adding/removing a family required Java edits

After this round:

- Java owns the registration mechanism
- JSON owns the material families and registration-time values
- registration loops over the family data
- existing 184 item ids remain stable

Specialized tool classes are preserved:

- `AxeItem`
- `ShovelItem`
- `HoeItem`

Spears still use 26.1 `Item.Properties().spear(...)`.

## Added validator

New script:

```text
scripts/validate_equipment_families_json.py
```

It validates:

- duplicate ids
- namespaced ingredients
- armor piece names
- tool type names
- equip sound names
- non-negative values
- expected item count
- required resources for every generated item

## What remains for round 2

This round does not yet generate assets/recipes/lang/tags from `equipment_families.json`. The resource files are still checked in as concrete files.

Round 2 should complete decoupling by adding a deterministic generator that reads `equipment_families.json` and regenerates:

- item definitions
- item models
- recipes
- repair tags
- tool tags
- lang keys
- optionally texture generation metadata / reports

Then validators should verify generated output is in sync with the JSON.

## Validation

Executed:

```bash
python3 scripts/validate_equipment_families_json.py
python3 scripts/validate_dream_equipment_assets.py
python3 scripts/validate_set_effects_json.py
JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks
```

Results:

- `equipment_families` validator: PASS — 37 families, 184 items.
- asset validator: PASS — 184 items, 37 materials.
- set-effect validator: PASS — 28 passive effects, 4 brittle entries.
- build: PASS.
