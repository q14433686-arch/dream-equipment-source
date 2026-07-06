# Round 49 Shield Completion for All Families — 2026-07-03

## Scope

Expanded the shield prototype from Round 48 to every current Dream Equipment material family after the first client test passed.

This pass adds shields for all 56 families. It still uses vanilla shield behavior and vanilla special shield rendering; material-specific custom shield base rendering remains deferred.

## Result

Custom item count increased from 320 to 368.

Shield resource count:

```text
56 shield item definitions
56 shield recipes
```

## Added shields

All current families now declare an enabled `shield` entry in `equipment_families.json`.

This includes:

- gem/special families: emerald, lapis, redstone, quartz, amethyst, prismarine, slime, coal, glass, obsidian, bone, cactus, paper, armadillo shell, turtle shell
- plank families: oak, spruce, birch, jungle, acacia, dark oak, mangrove, cherry, pale oak, bamboo, crimson, warped
- stone/rock families: stone, cobblestone, mossy cobblestone, cobbled deepslate, blackstone, sandstone, red sandstone, end stone, tuff, calcite, granite, diorite, andesite, basalt, smooth basalt, dripstone block, netherrack
- log/stem/block families: oak log, spruce log, birch log, jungle log, acacia log, dark oak log, mangrove log, cherry log, pale oak log, bamboo block, crimson stem, warped stem

## Durability approach

Shield durability remains JSON-owned per family.

General tuning logic:

- vanilla-like plank shields: around vanilla shield durability
- bamboo: slightly lower than standard plank
- log/stem/block shields: higher than planks
- brittle materials such as paper/glass/calcite/dripstone/netherrack: low durability
- dense stone/deepslate/blackstone/basalt/end stone: medium-to-high durability
- obsidian: very high durability
- redstone: low durability, consistent with redstone gear's fragile/high-energy identity

## Resource generation

`generate_equipment_resources.py` now manages 1349 files.

Each shield receives:

- `assets/dream_equipment/items/<family>_shield.json`
- `assets/dream_equipment/models/item/<family>_shield.json`
- `assets/dream_equipment/models/item/<family>_shield_blocking.json`
- `data/dream_equipment/recipe/<family>_shield.json`
- zh_cn/en_us lang keys

## Particle texture mapping

The shield base/blocking models are still special-renderer base models, but their particle texture references were improved for non-block ingredients:

- emerald → emerald block
- lapis → lapis block
- redstone → redstone block
- quartz → quartz block side
- amethyst shard → amethyst block
- prismarine shard → prismarine
- coal/charcoal → coal block
- bone → bone block side
- paper → white wool fallback
- armadillo scute → brown wool fallback
- turtle scute → turtle egg fallback

This avoids obviously invalid particle texture references in generated shield base models.

## Fuel behavior

Existing JSON-owned fuel logic now also applies to shields for families with `fuel_burn_time_per_material`.

For wood/plank/log/stem/bamboo-block shields:

```text
shield fuel time = fuel_burn_time_per_material × 6
```

For the current wood/log-like value of 300 ticks per material, that means 1800 ticks per shield.

## Validation

Executed:

```bash
python3 scripts/generate_equipment_resources.py
python3 scripts/generate_wood_worn_textures.py
python3 scripts/validate_equipment_families_json.py
python3 scripts/validate_dream_equipment_assets.py
python3 scripts/validate_set_effects_json.py
python3 scripts/audit_equipment_balance.py
JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks
```

Results:

- Equipment resource generator drift check: PASS — 1349 generated resources in sync.
- Wood/log worn texture generator: PASS — 72 worn layer files regenerated.
- Equipment family validator: PASS — 56 families / 368 items.
- Asset validator: PASS — texture-backed item/material checks plus shield special-renderer resources.
- Set-effect validator: PASS — 24 passive entries / 4 brittle entries.
- Balance audit: PASS — 368 entries including all shields.
- Gradle build: BUILD SUCCESSFUL.
- Shield resource count: 56 item definitions / 56 recipes.

## Client-only checks

1. Confirm all 56 shields appear and localize correctly.
2. Confirm representative shield recipes from each material category.
3. Confirm offhand equip and blocking behavior still work after scaling to all families.
4. Confirm shield durability values feel coherent.
5. Confirm repair materials match existing family repair tags.
6. Confirm wood/log-like shields work as fuel.
7. Confirm no missing-model or missing-texture warnings for generated shield base/blocking models.
8. Confirm visual acceptability of vanilla special-renderer shields before considering custom shield rendering.

## Deferred

Material-specific shield base rendering is still deferred. The vanilla `ShieldSpecialRenderer` uses fixed shield base sprites and banner overlays, so true material-specific shield visuals should be implemented only as a separate client-rendering task if needed.
