# Round 13 Wood/Stone/Cobblestone Render Fix — 2026-07-02

## User feedback addressed

The user provided a screenshot showing wooden armor has meaningless horizontal black lines/floating bands when worn, and noted that wooden/stone/cobblestone inventory render icons are still wrong.

## Root cause

### Worn armor black bands

The wood variant equipment-layer generator drew plank seam lines across the entire 64×32 image after recoloring. Those lines were not clipped to the non-transparent armor pixels, so semi-transparent dark lines existed in transparent areas. In game, those transparent-area lines rendered as black horizontal bands around the player.

### Bad item render icons

Wood/stone/cobblestone icons were using simplified generated silhouettes/fills instead of vanilla armor icon templates. They did not read like proper Minecraft armor icons and did not use the source block texture strongly enough.

## Fix applied

### 1. Inventory/item icons

Regenerated the following item icons from vanilla armor item templates:

- wood and all 12 plank variants: based on vanilla `leather_helmet/chestplate/leggings/boots` silhouettes
- stone and cobblestone: based on vanilla `iron_helmet/chestplate/leggings/boots` silhouettes

Then filled the vanilla template shading with the corresponding block texture palette/pattern:

- `oak_planks`, `spruce_planks`, ..., `warped_planks`
- `stone`
- `cobblestone`

### 2. Worn armor layers

Regenerated worn layers using the correct 26.1 equipment texture layout and vanilla templates:

- wood and plank variants: vanilla leather humanoid/humanoid_baby/humanoid_leggings UV template
- stone/cobblestone: vanilla iron humanoid/humanoid_baby/humanoid_leggings UV template

Material grain/crack accents are now only applied to pixels whose source armor template is non-transparent. No lines are drawn over transparent areas anymore.

## Families fixed

- `wooden_*`
- `oak_*`
- `spruce_*`
- `birch_*`
- `jungle_*`
- `acacia_*`
- `dark_oak_*`
- `mangrove_*`
- `cherry_*`
- `pale_oak_*`
- `bamboo_*`
- `crimson_*`
- `warped_*`
- `stone_*`
- `cobblestone_*`

## Validation

Executed:

```bash
python3 scripts/validate_dream_equipment_assets.py
```

Result:

- PASS — 152 items, 29 materials.

Full build should be run before release refresh.

## Client-only checks

- Verify wooden/plank variant armor no longer shows floating horizontal bands.
- Verify inventory icons for wood/stone/cobblestone now resemble vanilla armor icons with material texture fills.
- Verify worn layers still align correctly with player model.
