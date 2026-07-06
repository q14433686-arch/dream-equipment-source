# Round 26 Narrow Brittle Rules and Density Rebalance — 2026-07-02

## Scope

Addressed user feedback:

- Calcite armor shatter tooltip/rule appeared too broad and included tools/weapons conceptually.
- Check other tools/weapons for similarly broad shatter logic.
- Obsidian weapons should not drop raw material when they shatter.
- Stone armor physics should vary by real-ish density, including mossy cobblestone and netherrack.

## Changes

### Brittle armor vs brittle weapons separated in tooltips

Tooltips now distinguish armor-set mechanics from tool/weapon mechanics:

- armor set effects and armor shatter rules only display on armor pieces
- brittle weapon rules only display on tools/weapons

This fixes the apparent issue where calcite tool/weapon items showed armor shatter logic as if they were part of the armor set.

### Obsidian weapon shatter no longer drops material

Previously brittle weapon break logic reused the armor shatter return helper, causing obsidian weapons to return material on break.

Now:

- obsidian weapons still have 5% break chance on hit
- no obsidian is returned from weapon break
- armor shatter rules still return 1–2 source material items where applicable

### Stone armor physics retuned by material density/fragility

`stone_armor_physics` in `set_effects.json` was rewritten to include broader stone families and more differentiated values.

General direction:

- low-density/fragile materials have low cancel chance, low damage threshold, low slowness
- common stone/cobble sit in the middle
- dense volcanic/deepslate materials have higher cancel chance, higher threshold, more slowness
- obsidian is hard/glassy: lower slowness than basalt but still brittle at high damage
- mossy cobblestone is included, slightly weaker than ordinary cobblestone
- netherrack is included as porous/weak stone with low threshold and low slowness

Examples:

- `netherrack`: very low cancel, threshold 4.5, low slowness
- `mossy_cobblestone`: threshold 6.0, lower than normal cobble
- `granite/diorite/andesite`: middle-high density
- `basalt/smooth_basalt`: high cancel and high slowness
- `obsidian`: hard but glassy, threshold 9.5, moderate slowness

### Added validation coverage

`validate_set_effects_json.py` now validates:

- `wet_repair`
- `brittle_weapons`
- `stone_armor_physics`

## Validation

Executed:

```bash
python3 scripts/generate_equipment_resources.py --write
python3 scripts/generate_equipment_resources.py
python3 scripts/validate_equipment_families_json.py
python3 scripts/validate_set_effects_json.py
python3 scripts/validate_dream_equipment_assets.py
JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks
```

Results:

- generator write/check: PASS
- equipment families: PASS — 44 families, 236 items
- set effects: PASS — 21 passive effects, 4 brittle armor entries, plus extended rule validation
- assets: PASS — 236 items, 44 materials
- build: PASS

## Client-only checks

- Calcite tools/weapons should no longer show armor shatter tooltip lines.
- Calcite armor should still show appropriate brittle/stone-physics lines.
- Obsidian weapons should shatter without dropping obsidian.
- Stone armor density differences should feel more coherent: heavier materials protect more but slow more.
