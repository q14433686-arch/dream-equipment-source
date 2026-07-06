# Round 11 Wood/Stone/Cobblestone Variant Audit and Plan — 2026-07-02

## User request

The user pointed out that wood, stone, and cobblestone equipment are not diverse enough, and that their render icons are currently wrong. This round is investigation/planning first: count what exists, identify available vanilla raw materials in MC 26.1.2, determine root causes, and propose a next-round implementation plan.

## Current project count

Current `dream_equipment` items in these families:

### Wooden

- `wooden_helmet`
- `wooden_chestplate`
- `wooden_leggings`
- `wooden_boots`

Count: 4

### Stone

- `stone_helmet`
- `stone_chestplate`
- `stone_leggings`
- `stone_boots`

Count: 4

### Cobblestone / 圆石

- `cobblestone_helmet`
- `cobblestone_chestplate`
- `cobblestone_leggings`
- `cobblestone_boots`

Count: 4

Total current wood/stone/cobblestone-style equipment: 12 items.

## Vanilla 26.1.2 material audit

Checked the local MC 26.1.2 merged jar assets/item definitions.

### Plank / wood variants available

Vanilla has 12 plank variants with item/block resources:

1. `oak_planks`
2. `spruce_planks`
3. `birch_planks`
4. `jungle_planks`
5. `acacia_planks`
6. `dark_oak_planks`
7. `mangrove_planks`
8. `cherry_planks`
9. `pale_oak_planks`
10. `bamboo_planks`
11. `crimson_planks`
12. `warped_planks`

If made as one armor set per plank type, this is 12 × 4 = 48 wooden-variant armor items.

### Stone-like items available

Vanilla has these stone-like item definitions/resources relevant for equipment variants:

1. `stone`
2. `cobblestone`
3. `mossy_cobblestone`
4. `deepslate`
5. `cobbled_deepslate`
6. `blackstone`
7. `basalt`
8. `smooth_basalt`
9. `tuff`
10. `calcite`
11. `dripstone_block`
12. `granite`
13. `diorite`
14. `andesite`
15. `sandstone`
16. `red_sandstone`
17. `end_stone`
18. `netherrack`
19. `obsidian`

Some already exist in the mod as generic families:

- `stone_*`
- `cobblestone_*`
- `obsidian_*`

Potential additional full armor sets from stone-like families, excluding existing generic stone/cobblestone/obsidian: 16 × 4 = 64 more armor items.

If everything is added literally, wood + stone variants alone could add 48 + 64 = 112 new armor items. That may be too many unless the mod intentionally becomes a large material-expansion pack.

## Why the current render icons are wrong

### 1. Wood/stone/cobblestone are generic, not material-specific

Current project has only:

- `wooden_*`
- `stone_*`
- `cobblestone_*`

This means all wood types collapse to one generic brown armor set, and all stone/cobble variants collapse to one generic gray set. This does not match the user's expectation that different raw material item styles should produce different visuals/mechanics.

### 2. Current icons are generated patterns, not true material-derived icons

The current item icons are armor silhouettes filled with simplified procedural patterns. They are not derived from actual vanilla block texture palettes/structure. This is especially visible for:

- planks: should show real plank grain/color differences
- cobblestone/round stone: should show real stone/cobble block feel
- blackstone/deepslate/sandstone/end stone/etc.: should be visually distinct, not generic gray armor

### 3. The worn armor layers are also too generic

The current equipment layers are recolored from a vanilla diamond UV template. This fixes UV correctness, but it does not make each material visually distinctive enough. Wood, cactus, paper, glass, slime, and stone variants need material-specific overlays, not only recolored diamond geometry.

## Naming issue confirmed

The previous Chinese name problem was confirmed and should remain fixed:

- Wrong: `原石...`
- Correct: `圆石...`

Future docs and lang should use `圆石` for `cobblestone`, not `原石`.

## Proposed next-round implementation strategy

Do not add all 112 possible variants blindly in one pass. Recommended staged approach:

### Stage A — wood diversity first

Add per-plank armor sets for all 12 plank variants:

- oak armor
- spruce armor
- birch armor
- jungle armor
- acacia armor
- dark oak armor
- mangrove armor
- cherry armor
- pale oak armor
- bamboo armor
- crimson armor
- warped armor

Recommended behavior:

- Overworld wood variants: same weak defense, mostly visual diversity.
- Bamboo: slightly lighter / mobility-flavored if a set effect is desired.
- Crimson: small fire/desert/nether flavor later, but not full fire immunity.
- Warped: odd/end-like flavor later, maybe brief slow falling or enderman-style utility later.

Texture plan:

- Use each vanilla plank texture as source palette/pattern.
- Generate armor item icons by applying actual plank texture samples inside armor silhouettes.
- Generate worn armor layers using correct 26.1 equipment UV plus plank-grain overlay.

### Stage B — stone diversity curated set

Add a curated set first rather than every stone block:

Recommended first stone-variant armor sets:

1. `mossy_cobblestone` — mossy/green cracked style; maybe minor regeneration or nature theme later.
2. `cobbled_deepslate` — heavier dark stone; higher durability, small slowness if needed.
3. `blackstone` — nether dark stone; fire/nether theme later.
4. `sandstone` — desert light armor; weak but maybe heat/desert flavor later.
5. `red_sandstone` — visual variant of sandstone.
6. `end_stone` — end-themed armor; later could interact with levitation/ender effects.
7. `tuff` — rough mid-stone style.
8. `calcite` — light/white fragile mineral style.

Defer or skip unless requested:

- granite/diorite/andesite: visually useful, but mechanically redundant unless the user wants full decorative coverage.
- basalt/smooth_basalt: can be nether-heavy variants but overlap with blackstone/obsidian.
- netherrack: very weak/flaky nether joke armor or future special case.

Texture plan:

- Use actual vanilla block textures as source palette/pattern.
- Do not use generic procedural gray for all.
- Keep cobblestone named `圆石` and visually distinct from smooth `stone`.

### Stage C — mechanisms by material category

Instead of making every set a stat clone, group mechanics by raw material feel:

#### Planks

- generic low defense, low durability
- mostly visual diversity
- bamboo could be light/mobility
- crimson/warped could have nether/fungus flavor later

#### Smooth stone / cobble / deepslate / blackstone

- heavier and more durable than wood
- slower/weight penalty only for the heaviest sets if needed
- blackstone/deepslate can lean defensive

#### Sandstone / calcite / glass-like fragile materials

- lower durability
- potential brittle/shatter mechanics later

#### Mossy / organic materials

- small passive utility later, not direct strong combat buffs

#### End/nether materials

- niche environmental utility later
- avoid making them stronger than diamond unless intentionally late-game

## Concrete next-round recommendation

Next round should implement **wood variant armor first** because:

1. There are exactly 12 known vanilla plank variants.
2. The user specifically complained that wood is not diverse.
3. Wood variant armor is mostly visual and low-risk mechanically.
4. It creates the texture pipeline needed for stone variants.

Suggested next implementation target:

- Add 12 plank armor families, 48 items.
- Keep old `wooden_*` either as oak alias or deprecated generic set. Prefer migrate/keep old generic as `oak`? Needs decision.
- Generate item icons from actual vanilla plank texture palettes.
- Generate correct 26.1 worn equipment layers with plank-grain overlays.
- Then do a second pass for curated stone variants.

## Decision needed before next code pass

For existing `wooden_*`, choose one:

A. Keep as generic wooden armor and add new variants alongside it.
B. Treat `wooden_*` as oak armor and add only the other 11 variants.
C. Rename/migrate to `oak_*` and remove generic `wooden_*`.

Recommended: A for compatibility and simplicity, then add explicit variants. Later, if desired, hide/deprecate generic wooden armor.
