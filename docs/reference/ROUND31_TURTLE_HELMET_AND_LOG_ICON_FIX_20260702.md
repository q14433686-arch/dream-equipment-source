# Round 31 Turtle Helmet and Log Armor Icon Fix — 2026-07-02

## Scope

Fixed two repeated client-side visual/design issues:

1. All log armor inventory icons looked incomplete/broken.
2. Turtle shell helmet duplicated the vanilla turtle helmet role.

## Log armor icon fix

The log/stem/bamboo-block armor inventory icons were regenerated using a cleaner vanilla-leather-style reskin approach.

Families affected:

- `oak_log`
- `spruce_log`
- `birch_log`
- `jungle_log`
- `acacia_log`
- `dark_oak_log`
- `mangrove_log`
- `cherry_log`
- `pale_oak_log`
- `bamboo_block`
- `crimson_stem`
- `warped_stem`

The approach:

- use vanilla leather armor item silhouettes
- use the corresponding log/stem/block texture palette
- remove emerald-style highlights
- keep clear 16x16 vanilla-like shapes

Worn layers for these families were regenerated from vanilla leather equipment templates.

## Turtle shell set fix

The user clarified that the vanilla turtle shell is already the turtle helmet. Therefore:

- removed custom `turtle_shell_helmet`
- deleted its item/model/texture/recipe resources
- `equipment_families.json` now lists turtle shell armor pieces as chestplate, leggings, and boots only
- full turtle shell set logic uses:
  - `minecraft:turtle_helmet`
  - `dream_equipment:turtle_shell_chestplate`
  - `dream_equipment:turtle_shell_leggings`
  - `dream_equipment:turtle_shell_boots`

Tooltip support was also added so hovering vanilla `minecraft:turtle_helmet` can show the Dream Equipment turtle-shell set information.

## Turtle textures

The remaining turtle shell armor textures were regenerated using vanilla turtle visual references:

- `minecraft:item/turtle_helmet`
- `minecraft:item/turtle_scute`
- vanilla turtle equipment texture where available

The chestplate/leggings/boots now follow turtle-shell palette and the worn layers combine turtle-shell coloring with correct equipment UV layout.

## Validation

Executed:

```bash
python3 scripts/generate_equipment_resources.py
python3 scripts/validate_equipment_families_json.py
python3 scripts/validate_set_effects_json.py
python3 scripts/validate_dream_equipment_assets.py
JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks
```

Results:

- generator drift check: PASS — 1031 files
- equipment families: PASS — 56 families / 283 items
- set effects: PASS — 24 passive effects / 4 brittle entries
- assets: PASS — 283 items / 56 materials
- build: PASS

## Client-only checks

- Log armor inventory icons should no longer look broken/incomplete.
- Custom `turtle_shell_helmet` should be gone.
- Vanilla turtle helmet should count toward full turtle shell set effects.
- Turtle chestplate/leggings/boots should visually match vanilla turtle shell style better.
