# Round 25 Physics Rebalance and Redstone Retry — 2026-07-02

## Scope

Follow-up to the user's combined A+B+C+D feedback.

## Implemented

### Redstone signal retry

Redstone signal handling now includes:

- exact signal from the block below the player
- best-neighbor signal for adjacent redstone dust queries
- `hasNeighborSignal` override
- old/new source position neighbor updates

Expected behavior remains:

- redstone boots: signal 7
- full redstone set: signal 15

### Slime armor cost rebalance

In `equipment_families.json`:

- slime ingredient changed to `minecraft:slime_block`
- durability multiplier changed to `50`
- enchantability changed to `12`

In `set_effects.json`:

- slime return values changed to helmet 4, chestplate 8, leggings 7, boots 4

### Wood/stone/glass icon and layer correction

- Wood and plank armor icons use muted vanilla leather-style reskins rather than high-gloss emerald-template highlights.
- Stone/cobblestone use muted stone palette reskins.
- Glass item and worn layer visuals use the supplied glass pane reference without semi-transparent alpha, because normal player armor transparency is not reliably supported by vanilla equipment layers.

### Curated tool/weapon pass

- Removed blackstone tools/weapons; blackstone armor remains.
- Added curated tools/weapons for cactus, bone, mossy cobblestone, cobbled deepslate, sandstone, red sandstone, end stone, tuff, and calcite.
- Added stone-like armor variants: granite, diorite, andesite, basalt, smooth basalt, dripstone block, netherrack.

### Material physics pass

Added JSON-driven physics rules:

- `wet_repair`: mossy cobblestone repairs durability in water/rain.
- `brittle_weapons`: obsidian weapons have 5% chance to break on successful damage and return 1–2 obsidian.
- `stone_armor_physics`: hard/dense materials gain per-piece damage-cancel chance, shatter threshold, and slowness scaling.

Obsidian weapon stats were changed:

- durability: 120
- attack damage bonus: diamond-like `3.0`
- 5% break chance on hit

Brittle/stone shatter now returns 1–2 source material items when possible.

## Validation

Executed:

```bash
python3 scripts/validate_equipment_families_json.py
python3 scripts/validate_set_effects_json.py
python3 scripts/validate_dream_equipment_assets.py
JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks
```

Results:

- equipment families: PASS — 44 families / 236 items
- set effects: PASS — 21 passive effects / 4 brittle entries
- assets: PASS — 236 items / 44 materials
- build: PASS

## Client-only checks

- Redstone dust/repeater detection.
- Slime block recipes and durability feel.
- Glass visuals from pane reference.
- Wood icons after muted reskin.
- Obsidian weapon 5% break chance and damage feel.
- Mossy repair in water/rain.
- Stone physics: cancel chance, shatter thresholds, slowness severity.
