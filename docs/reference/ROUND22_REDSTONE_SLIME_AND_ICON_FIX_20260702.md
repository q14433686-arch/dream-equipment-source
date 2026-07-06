# Round 22 Redstone, Slime Cost, and Wood/Stone Icon Fix — 2026-07-02

## Scope

Implemented the concrete A+B follow-up from the user report:

1. Redstone boots/full set signal was not detected by redstone dust.
2. Slime armor was too cheap for its mechanics.
3. Bamboo/wood/stone/cobblestone inventory icons were still visually wrong.

## Redstone signal fix attempt

### Root cause

The first redstone implementation only injected `SignalGetter#getSignal` and `getDirectSignal`, but redstone dust calculates power through `RedStoneWireBlock` and `Level.getBestNeighborSignal(pos)`. Therefore a generic exact-position signal was not enough for redstone dust.

### Changes

`DreamEquipmentRedstonePower` now exposes:

- `signalAt(level, pos)` — exact source block signal
- `bestNeighborSignalAt(level, pos)` — signal if a redstone-boot source block is neighboring the queried position

`SignalGetterMixin` now injects:

- `getSignal`
- `getDirectSignal`
- `getBestNeighborSignal`
- `hasNeighborSignal`

`DreamEquipmentSetEffects` now tracks the last redstone source position per player and notifies both old and new source neighborhoods. This should help dust turn off after the player moves away or removes boots.

### Intended behavior

- Redstone boots: block below player contributes signal 7.
- Full redstone set: block below player contributes signal 15.
- Adjacent redstone dust should now see the source through `getBestNeighborSignal`.

## Slime armor rebalance

### Problem

Slime armor used `minecraft:slime_ball`, making the full set cost only 24 slime balls despite strong mechanics.

### Changes

In `equipment_families.json`:

- slime ingredient changed from `minecraft:slime_ball` to `minecraft:slime_block`
- slime armor durability multiplier changed from `9` to `50`
- slime enchantability adjusted from `16` to `12`

In `set_effects.json`:

- slime break return increased:
  - helmet: 4 slime balls
  - chestplate: 8 slime balls
  - leggings: 7 slime balls
  - boots: 4 slime balls

The set is now expensive but lasts longer and returns a small amount of slime when consumed.

## Wood/stone/cobblestone item icon fix

### Problem

The item icons generated from vanilla leather/iron silhouettes plus raw block texture fills were still visually wrong, especially bamboo and other plank variants.

### Changes

Regenerated inventory icons for:

- `wooden_*`
- all 12 plank variant sets
- `stone_*`
- `cobblestone_*`

The new pipeline uses the user-provided emerald armor templates as the item-icon silhouettes, then applies material-specific wood/stone palettes and simplified pattern hints. This avoids raw noisy block-texture fills while staying visually aligned with the accepted emerald armor style.

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

- generator drift check: PASS
- equipment family validator: PASS — 37 families / 184 items
- set effect validator: PASS — 28 passive effects / 4 brittle entries
- asset validator: PASS — 184 items / 37 materials
- build: PASS

## Client-only checks

- Retest redstone dust adjacent to the block below the player wearing redstone boots/full redstone set.
- Verify dust powers off when the player moves away/removes boots.
- Confirm slime recipes now require slime blocks and feel appropriately expensive.
- Confirm wood/bamboo/stone/cobblestone inventory icons now align with emerald armor template style.

## Risk

Redstone is still the highest-risk area because individual redstone components can use specialized query/update paths. If redstone dust still fails, the next pass should target `RedStoneWireBlock`'s exact power calculation directly rather than only `SignalGetter` default methods.
