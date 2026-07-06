# Round 34 Emerald Armor Recipe Rebalance — 2026-07-02

## Scope

The user felt the emerald armor set effect was strong and requested making the recipe more expensive: primarily emerald blocks, secondarily emeralds.

## Changes

Updated `equipment_families.json` recipe overrides for emerald armor.

### Emerald helmet

```text
BEB
E E
```

### Emerald chestplate

```text
E E
BBB
BEB
```

### Emerald leggings

```text
BBB
E E
B B
```

### Emerald boots

```text
B B
E E
```

Where:

```text
B = minecraft:emerald_block
E = minecraft:emerald
```

## Resulting cost

Full emerald armor set now costs:

- 11 emerald blocks
- 8 emeralds

Equivalent to 107 emeralds total.

This preserves the powerful emerald set identity while making it a late/high-cost trade-and-village reward set.

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
- equipment families: PASS — 56 families, 312 items
- assets: PASS — 312 items, 56 materials
- set effects: PASS — 24 passive effects, 4 brittle entries
- build: PASS

## Client-only checks

- Confirm emerald armor recipes require emerald blocks + emeralds.
- Confirm recipe book display and crafting work.
- Confirm high cost feels appropriate for Luck + Hero of the Village set effects.
