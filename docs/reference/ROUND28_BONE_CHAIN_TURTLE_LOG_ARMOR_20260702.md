# Round 28 Bone / Chainmail / Turtle / Log Armor Implementation — 2026-07-02

## Scope

Implemented the user's requested next batch:

- bone products shatter into bone meal
- vanilla chainmail full set approximates Projectile Protection II
- turtle shell full armor set
- remove the problematic generic `wooden_*` armor family
- add all log/stem/bamboo-block armor families instead of replacing plank variants

## Wooden armor change

The old generic `wooden_*` family was removed from `equipment_families.json` and its resources were deleted.

Reason: the user clarified that “wood armor” was acting as a real early-game item, not a shorthand, and it occupied the design space for proper wood variants.

The existing plank variants remain:

- oak / spruce / birch / jungle / acacia / dark_oak / mangrove / cherry / pale_oak / bamboo / crimson / warped

New log/stem/block variants were added separately.

## Added log/stem armor families

Added 12 armor families, 48 items total:

- `oak_log_*`
- `spruce_log_*`
- `birch_log_*`
- `jungle_log_*`
- `acacia_log_*`
- `dark_oak_log_*`
- `mangrove_log_*`
- `cherry_log_*`
- `pale_oak_log_*`
- `bamboo_block_*`
- `crimson_stem_*`
- `warped_stem_*`

These use log/stem/block ingredients rather than planks.

## Added turtle shell full set

Added:

- `turtle_shell_helmet`
- `turtle_shell_chestplate`
- `turtle_shell_leggings`
- `turtle_shell_boots`

Material:

- `minecraft:turtle_scute`

Set effects:

- Resistance II
- Slowness I
- Water Breathing

This follows the user's idea: high mitigation and noticeable slowness.

## Bone shatter behavior

Bone weapons are now listed in `brittle_weapons`:

- 4% chance to shatter on hit

Bone armor is listed in `stone_armor_physics` with low-ish density/fragility values.

Shatter drop behavior was adjusted:

- bone armor/tool shatter returns bone meal, not bones
- obsidian weapon shatter still returns nothing
- armor shatter for other materials can return 1–2 source materials where applicable

## Chainmail set projectile protection

Implemented vanilla chainmail full-set behavior:

- if the player wears full vanilla chainmail armor and takes projectile damage, the mod heals back about 28% of the damage after it is applied
- this approximates Projectile Protection II without modifying enchantments or item NBT

Affected vanilla items:

- `minecraft:chainmail_helmet`
- `minecraft:chainmail_chestplate`
- `minecraft:chainmail_leggings`
- `minecraft:chainmail_boots`

## Content totals

After this round:

- families: 56
- items: 284
- generator-managed files: 1034

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

- generator drift check: PASS — 1034 files
- equipment families: PASS — 56 families / 284 items
- set effects: PASS — 24 passive effects / 4 brittle armor entries
- assets: PASS — 284 items / 56 materials
- build: PASS

## Client-only checks

- Generic `wooden_*` armor should no longer exist.
- Plank variants should still exist.
- Log/stem/bamboo-block armor variants should appear and craft.
- Turtle shell full set should appear, craft, and apply Resistance/Slowness/Water Breathing.
- Bone weapons should shatter into bone meal.
- Bone armor shatter should return bone meal.
- Full vanilla chainmail should reduce effective projectile damage.
