# Round 23 Redstone + Slime + Icon + Tool/Effect Rebalance — 2026-07-02

## Scope

Implemented the requested A+B follow-up and also folded in the most concrete C+D findings that were already data-driven:

- A: redstone dust detection fix + slime armor rebalance
- B: wood/stone/cobblestone inventory icon pipeline fix
- C: curated tools/weapons for end stone and other sensible materials
- D: first effect rebalance pass, removing/weakening some boring/unreasonable placeholder effects

## A1 — Redstone dust detection fix attempt

### Previous problem

Redstone boots/full redstone set output was not detected by redstone dust.

### Root cause found

Redstone dust uses `RedStoneWireBlock` and `Level.getBestNeighborSignal(pos)` during power calculation. The earlier implementation only injected exact `getSignal` / `getDirectSignal` paths, which was insufficient for dust.

### Changes

`DreamEquipmentRedstonePower` now exposes:

- `signalAt(level, pos)` — exact source block signal
- `bestNeighborSignalAt(level, pos)` — signal if the redstone source block is a neighbor of the queried position

`SignalGetterMixin` now injects:

- `getSignal`
- `getDirectSignal`
- `getBestNeighborSignal`
- `hasNeighborSignal`

`DreamEquipmentSetEffects` now tracks the last redstone source block per player and updates old/new neighborhoods so redstone dust can turn off when the player moves away/removes boots.

### Intended behavior

- `redstone_boots`: block below player contributes signal 7
- full redstone set: block below player contributes signal 15
- adjacent redstone dust should now see the source through best-neighbor signal calculation

## A2 — Slime armor rebalance

### Previous problem

Slime armor used `minecraft:slime_ball`, making a very powerful set cost only 24 slime balls.

### Changes in `equipment_families.json`

- slime ingredient: `minecraft:slime_ball` → `minecraft:slime_block`
- slime armor durability multiplier: `9` → `50`
- slime enchantability: `16` → `12`

### Changes in `set_effects.json`

Slime break returns now:

- helmet: 4 slime balls
- chestplate: 8 slime balls
- leggings: 7 slime balls
- boots: 4 slime balls

This makes slime armor expensive (24 slime blocks for a full set) but much more durable, while still returning a small amount of slime on decay break.

## B — Wood/stone/cobblestone inventory icon fix

### Previous problem

Wood/bamboo/stone/cobblestone armor icons were still visually wrong.

### Changes

Regenerated inventory icons for:

- `wooden_*`
- all 12 plank variant sets
- `stone_*`
- `cobblestone_*`

New approach:

- use user-provided emerald armor templates as the armor item silhouette standard
- apply simplified material-specific wood/stone palettes and pattern hints
- avoid raw noisy block texture fills
- avoid old generic leather/iron silhouette mismatch

## C — Curated tools/weapons added

Added tools/weapons to sensible materials rather than blindly adding full utility toolsets.

### Added tools/weapons

- `mossy_cobblestone`: sword, pickaxe, axe, spear
- `cobbled_deepslate`: sword, pickaxe, axe, spear
- `blackstone`: sword, pickaxe, axe, spear
- `sandstone`: sword, spear
- `red_sandstone`: sword, spear
- `end_stone`: sword, pickaxe, axe, spear
- `tuff`: pickaxe, axe, spear
- `calcite`: sword, spear
- `bone`: sword, spear
- `cactus`: spear

Tool scope remains curated:

- brittle materials do not get full utility sets
- cactus only gets spear
- sandstone/red_sandstone only get sword/spear
- heavy stone materials get pickaxe/heavy weapons

## D — First effect rebalance pass

The previous effects included some placeholder buffs. This pass changes the most obvious issues:

### Removed / reduced

- redstone full set no longer grants generic Speed; redstone identity should be signal output
- coal full set no longer grants Fire Resistance; coal as fuel should not be treated as fireproof armor by default
- calcite full set no longer grants Night Vision; calcite now relies on brittle material identity

### Adjusted

- mossy cobblestone regeneration now only applies when wet/raining (`condition: wet`)
- sandstone/red_sandstone speed now only applies when dry (`condition: dry`)

This keeps effects more material-contextual while leaving additional rebalance for later live testing.

## Content totals

After this round:

- equipment families: 37
- items: 212
- materials: 37
- managed resource files from generator: 781

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

- generator drift check: PASS — 781 files
- equipment family validator: PASS — 37 families / 212 items
- set effect validator: PASS — 25 passive effects / 4 brittle entries
- asset validator: PASS — 212 items / 37 materials
- build: PASS

## Client-only checks

- Retest redstone dust with redstone boots/full set.
- Confirm signal turns off when moving/removing boots.
- Confirm slime recipes now require slime blocks and durability feels acceptable.
- Confirm wood/bamboo/stone/cobblestone icons follow the emerald armor template style.
- Test new stone/end/bone/cactus weapons/tools and animations.
- Confirm removed/adjusted effects feel more reasonable.

## Risk

Redstone remains the most likely area needing another live-test fix. If dust still fails, the next pass should target `RedStoneWireBlock`'s exact power calculation method directly rather than relying on `SignalGetter` paths.
