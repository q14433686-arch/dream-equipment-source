# Round 14 Curated Stone Variant Armor — 2026-07-02

## Scope

Implemented the curated stone variant batch recommended after the wood variant pass.

## Added stone-like armor variants

Added 8 stone-material armor families, 32 items total:

1. `mossy_cobblestone_helmet/chestplate/leggings/boots` — 苔石套
2. `cobbled_deepslate_helmet/chestplate/leggings/boots` — 深板岩圆石套
3. `blackstone_helmet/chestplate/leggings/boots` — 黑石套
4. `sandstone_helmet/chestplate/leggings/boots` — 砂岩套
5. `red_sandstone_helmet/chestplate/leggings/boots` — 红砂岩套
6. `end_stone_helmet/chestplate/leggings/boots` — 末地石套
7. `tuff_helmet/chestplate/leggings/boots` — 凝灰岩套
8. `calcite_helmet/chestplate/leggings/boots` — 方解石套

## Texture method

Each item icon and worn equipment layer is generated from the corresponding vanilla block texture:

- mossy_cobblestone
- cobbled_deepslate
- blackstone
- sandstone
- red_sandstone
- end_stone
- tuff
- calcite

Item icons use vanilla iron armor icon silhouettes with material-specific texture fills. Worn layers use vanilla 26.1 equipment UV templates with alpha-safe stone texture overlays.

## Basic mechanics

Added first-pass full-set effects:

- Mossy cobblestone: Regeneration
- Cobbled deepslate: Resistance + Slowness
- Blackstone: Fire Resistance + Slowness
- Sandstone / Red sandstone: Speed
- End stone: Slow Falling
- Tuff: Haste
- Calcite: Night Vision

These are intentionally simple and should be tuned after client testing.

## Content totals

After this round:

- Items: 184
- Armor/equipment materials: 37
- Added this round: 32 items / 8 materials

## Validation

Executed:

```bash
python3 scripts/validate_dream_equipment_assets.py
JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks
```

Results:

- Asset validator: PASS — 184 items, 37 materials.
- Build: PASS.

## Client-only checks

- Confirm all 8 stone variants appear and craft.
- Confirm inventory icons look like their source block material.
- Confirm worn layers are not banded/misaligned.
- Tune set effects after playtest.
