# Round 24 A+B+C+D Material Fixes — 2026-07-02

## Scope

Implemented the user's combined request:

- A/B: fix wood-family icons, glass armor style, redstone dust signal, slime cost
- C: add curated tools/weapons for suitable materials, remove blackstone tools/weapons
- D: continue effect rebalance so not every set has arbitrary strong buffs

## Wood armor icon change

The wood/plank armor inventory icons were changed away from shiny emerald-template highlights. They now use a vanilla leather-armor icon reskin approach:

- vanilla leather armor icon silhouettes
- muted material recolor from the corresponding plank texture
- no extra high-gloss emerald-style highlights

Affected:

- generic wooden
- oak, spruce, birch, jungle, acacia, dark oak, mangrove, cherry, pale oak, bamboo, crimson, warped

Worn wood layers were also regenerated from vanilla leather equipment templates with muted plank colors.

## Glass armor change

The glass set was regenerated using the supplied `Invicon_Glass_Pane.png` as the visual/material source.

Affected:

- `glass_helmet`
- `glass_chestplate`
- `glass_leggings`
- `glass_boots`
- glass worn equipment layers

The worn layers now use a translucent glass-pane-like palette based on the supplied image.

## Redstone signal fix attempt

Redstone handling was expanded further:

- exact signal: `signalAt`
- adjacent dust/repeater query support: `bestNeighborSignalAt`
- mixin now covers `getSignal`, `getDirectSignal`, `getBestNeighborSignal`, and `hasNeighborSignal`
- old/new source positions are tracked so signal should update off when the player moves/removes boots

Expected:

- redstone boots: signal 7 from block below player
- full redstone set: signal 15

## Slime rebalance

Slime armor is now much more expensive:

- ingredient: `minecraft:slime_block`
- durability multiplier: 50
- enchantability: 12

Return values remain partial:

- helmet 4 slime balls
- chestplate 8 slime balls
- leggings 7 slime balls
- boots 4 slime balls

## Curated tools/weapons

### Removed

Blackstone tools/weapons were removed because vanilla already allows blackstone in stone-tool recipes.

Removed resource families:

- `blackstone_sword`
- `blackstone_pickaxe`
- `blackstone_axe`
- `blackstone_spear`

Blackstone armor remains.

### Added

Curated tools/weapons added based on material logic:

- cactus: spear
- bone: sword, spear
- mossy cobblestone: sword, pickaxe, axe, spear
- cobbled deepslate: sword, pickaxe, axe, spear
- sandstone: sword, spear
- red sandstone: sword, spear
- end stone: sword, pickaxe, axe, spear
- tuff: pickaxe, axe, spear
- calcite: sword, spear

## Added stone-like armor variants

Added additional reskin armor families:

- granite
- diorite / 闪长岩
- andesite
- basalt
- smooth basalt
- dripstone block
- netherrack

These are mostly decorative/simple material variants and do not receive arbitrary strong set effects by default.

## Effect rebalance

Removed or contextualized weak placeholder effects:

- redstone speed removed earlier; redstone identity is signal output
- coal fire resistance removed earlier
- calcite night vision removed earlier
- mossy cobblestone regeneration removed from always-on behavior
- sandstone/red sandstone generic speed removed/contextualized away from constant strong effect
- tuff haste removed from always-on behavior

Current philosophy:

- cheap/decorative sets can have no effect
- heavy sets can have protection plus slowness
- brittle sets can shatter
- redstone is redstone signal, not generic speed
- slime is strong but costly and consumable

## Content totals

After this round:

- families: 44
- items: 236
- materials/equipment definitions: 44
- generator-managed resource files: 866

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

- generator drift check: PASS — 866 files
- equipment families: PASS — 44 families / 236 items
- set effects: PASS — 21 passive effects / 4 brittle entries
- assets: PASS — 236 items / 44 materials
- build: PASS

## Client-only checks

- Check bamboo/wood icons after muted vanilla-reskin change.
- Check glass armor inventory and worn appearance against the supplied glass pane reference.
- Retest redstone dust/repeater detection.
- Confirm blackstone tools/weapons are gone.
- Test new curated tools/weapons.
- Check whether no-effect/decorative sets feel acceptable.
