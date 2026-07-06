# Round 37 Repair Ingredient Expansion — 2026-07-03

## Scope

Addressed client feedback that some equipment still could not be repaired with the material players naturally expected.

The root issue was not missing durability or missing item registration. Every family already had a repair tag, but each tag was generated from the single `ingredient` value in `equipment_families.json`. That was too narrow for several families whose recipes/mechanics imply multiple valid repair materials or vanilla material tags.

## Architecture decision

Kept the existing Java/resource split:

- Java continues to point armor/tools at one generated repair tag per material family.
- JSON now may declare optional `repair_ingredients` per family.
- The resource generator writes those values into `data/dream_equipment/tags/item/repairs_*_*.json`.
- If `repair_ingredients` is absent, the generator falls back to the existing single `ingredient` behavior.

This keeps repair-material tuning data-driven and avoids hardcoding repair exceptions in Java.

## Changed data model

Added optional family field:

```json
"repair_ingredients": [
  "minecraft:item_id",
  "#minecraft:item_tag"
]
```

Supported value forms:

- Direct item ids, for example `minecraft:slime_ball`.
- Item tag references, for example `#minecraft:oak_logs`.

## Expanded repair coverage

### Multi-material repair families

- Emerald equipment: `emerald`, `emerald_block`.
- Bone equipment: `bone`, `bone_meal`.
- Glass equipment: `glass`, `glass_pane`.
- Lapis equipment: `lapis_lazuli`, `lapis_block`.
- Redstone equipment: `redstone`, `redstone_block`.
- Quartz equipment: `quartz`, `quartz_block`.
- Amethyst equipment: `amethyst_shard`, `amethyst_block`.
- Slime armor: `slime_ball`, `slime_block`.
- Coal armor: `coal`, `charcoal`, `coal_block`.

### Vanilla tag-based log/stem repair families

- Oak log armor: `#minecraft:oak_logs`.
- Spruce log armor: `#minecraft:spruce_logs`.
- Birch log armor: `#minecraft:birch_logs`.
- Jungle log armor: `#minecraft:jungle_logs`.
- Acacia log armor: `#minecraft:acacia_logs`.
- Dark oak log armor: `#minecraft:dark_oak_logs`.
- Mangrove log armor: `#minecraft:mangrove_logs`.
- Cherry log armor: `#minecraft:cherry_logs`.
- Pale oak log armor: `#minecraft:pale_oak_logs`.
- Bamboo block armor: `#minecraft:bamboo_blocks`.
- Crimson stem armor: `#minecraft:crimson_stems`.
- Warped stem armor: `#minecraft:warped_stems`.

This allows stripped logs/wood/hyphae variants where vanilla's item tags include them, instead of requiring only the one exact block item used in the recipe.

## Files changed

- `src/main/resources/data/dream_equipment/equipment_families.json`
  - Added optional `repair_ingredients` arrays to selected families.
- `scripts/generate_equipment_resources.py`
  - Generator now writes repair tag values from `repair_ingredients` when present.
- `scripts/validate_equipment_families_json.py`
  - Validator now checks optional repair ingredient arrays and supports `#namespace:tag` syntax.
- Generated repair tags under `src/main/resources/data/dream_equipment/tags/item/`.
- Workflow docs and release outputs updated.

## Validation

Executed:

```bash
python3 scripts/generate_equipment_resources.py --write
python3 scripts/generate_equipment_resources.py
python3 scripts/validate_equipment_families_json.py
python3 scripts/validate_dream_equipment_assets.py
python3 scripts/validate_set_effects_json.py
python3 scripts/audit_equipment_balance.py
JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks
```

Results:

- generator write/check: PASS — 1125 generated resources in sync.
- equipment family validator: PASS — 56 families / 312 items.
- asset validator: PASS — 312 items / 56 materials.
- set-effect validator: PASS — 24 passive entries / 4 brittle entries.
- balance audit: PASS.
- Gradle build: BUILD SUCCESSFUL.

## Client-only checks

Repair behavior should be checked in a live anvil/grindstone-style repair workflow for representative cases:

1. Slime armor with both slime ball and slime block.
2. Bone weapons/armor with both bone and bone meal.
3. Glass equipment with glass pane.
4. Log/stem/bamboo-block armor with stripped log/wood/hyphae variants where vanilla tags include them.
5. Redstone/lapis/quartz/amethyst/emerald equipment with both item and block forms.
