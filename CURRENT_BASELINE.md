# CURRENT_BASELINE

## Current baseline

- Date: 2026-07-06
- Project: `dream-equipment` / `dream_equipment`
- Scope: standalone Fabric mod project, separate from `yansheng-source`.
- Target environment:
  - Minecraft: `26.1.2`
  - Fabric Loader: `0.19.3`
  - Fabric API: `0.152.1+26.1.2` (`0.152.0+26.1.2` is not published)
  - Java: `25+`
  - Local validation JDK used this pass: Temurin `25.0.3+9-LTS` at `/tmp/herbcraft-jdk25/jdk-25`
  - Gradle wrapper: `9.4.1`
  - Loom: declared `1.16-SNAPSHOT`, resolved as Fabric Loom `1.16.3`
- Current status: environment setup/report-brief pass completed (Round 56, 2026-07-06). No gameplay Java or generated gameplay/resource content was changed this pass. This is a continuation of the same content state as 2026-07-03 (Round 55 vanilla material shields).
- Current output files:
  - `release_output/dream-equipment-0.1.0.jar`
  - `release_output/dream-equipment-source-current-20260706.zip`

## Implemented content

Current item count: 372.

- Emerald tools + armor.
- 12 plank-variant armor families: oak, spruce, birch, jungle, acacia, dark oak, mangrove, cherry, pale oak, bamboo, crimson, warped.
- Stone armor.
- Cobblestone armor.
- Curated stone/rock variants and related tools where declared by JSON: mossy cobblestone, cobbled deepslate, blackstone armor, sandstone, red sandstone, end stone, tuff, calcite, granite, diorite, andesite, basalt, smooth basalt, dripstone block, netherrack.
- Cactus armor + spear.
- Armadillo shell boots.
- Bone armor + weapons.
- Paper armor.
- Glass armor + weapon-only tools.
- Obsidian armor + weapon-only tools.
- Lapis tools + armor.
- Redstone tools + armor.
- Quartz weapon-only tools + armor.
- Amethyst tools + armor.
- Prismarine tools + armor.
- Slime armor.
- Coal armor.
- Turtle shell set using vanilla `minecraft:turtle_helmet` plus custom chestplate/leggings/boots.
- Log/stem/bamboo-block armor families.
- Shields for all 56 Dream Equipment material families plus vanilla-material copper, golden, diamond, and netherite shields.

All declared custom items have item definitions, models, textures, recipes, lang keys, equipment definitions where needed, and repair/tool/tag resources as managed by `scripts/generate_equipment_resources.py`.

## Data-driven architecture boundary

- Java owns mechanisms, loaders, registration, synchronization-facing behavior, UI/tooltips, validation-facing mechanics, events, mixins, redstone integration, and enchanting support.
- JSON/resources own equipment content, values, rule tables, compatibility/content declarations, lang text, recipes, tags, models, and generated resource data where a loader/generator exists.
- Content/rule changes that can be represented by `equipment_families.json` or `set_effects.json` must not be hardcoded into Java.

## Current JSON/resource state

- `src/main/resources/data/dream_equipment/equipment_families.json`: 60 families / 372 items.
- `src/main/resources/data/dream_equipment/set_effects.json`: 24 passive effect entries / 4 brittle entries, plus wet durability/repair, redstone signal, armadillo terrain speed, held effects, stone armor physics, brittle weapons, damage immunities, and shield effects.
- `scripts/generate_equipment_resources.py` check mode reports `equipment resources in sync — files=1369`.

## Reference boundary

- Vanilla+ / VKL+ is recorded as a style/scope reference in `docs/reference/VANILLA_PLUS_REFERENCE_NOTES_20260702.md`.
- Its Modrinth license is All Rights Reserved, so no texture pixels are copied. Dream Equipment textures are original generated assets except user-provided templates explicitly supplied in earlier rounds.

## Last updated

- Date: 2026-07-06
- Change: Round 56 — environment setup and report brief pass. Installed Temurin 25.0.3+9-LTS, confirmed all validators and Gradle build pass on the fresh clone. Re-created `release_output/` directory (was absent in fresh clone), copied jar, and built new source zip. No gameplay content changed.
- Current item count: 372 registered custom items, including 60 shields.
- Output updated: yes. `release_output/dream-equipment-0.1.0.jar` and `release_output/dream-equipment-source-current-20260706.zip` present.
- Validations executed:
  - Generator drift check: PASS — `files=1369`
  - Equipment-family validator: PASS — `families=60, items=372`
  - Asset validator: PASS — `items=312, materials=56`
  - Set-effect validator: PASS — `passive=24, brittle=4`
  - Balance audit: PASS
  - Gradle build: PASS — `BUILD SUCCESSFUL` (Gradle 9.4.1 / Loom 1.16.3)
- Client-only: no new client checks added this pass. Carry-forward client checks from Round 55 (vanilla material shields) apply.

### Previous update

- Date: 2026-07-03
- Change: Added vanilla material shields: copper, golden, diamond, and netherite. Current totals are 60 families / 372 custom items / 60 shields. Netherite shield is fire-resistant and tuned as very strong but not excessive at 1100 durability. Added `docs/reference/ROUND55_VANILLA_MATERIAL_SHIELDS_20260703.md`.
- Current item count: 372 registered custom items, including 60 shields.
- Output updated: yes. `release_output/dream-equipment-0.1.0.jar` and `release_output/dream-equipment-source-current-20260703.zip` refreshed.
- Validations: equipment resource drift check, wood/log worn texture generator, shield texture generator, equipment family validator, asset validator, set-effect validator, balance audit, and Gradle build all passed.
- Client-only: test copper/golden/diamond/netherite shields for visibility, recipes, repair, blocking, custom textures, netherite fire resistance, and netherite balance.

### Earlier update

- Date: 2026-07-03
- Change: Fixed incomplete cherry wood armor item icons by regenerating all four cherry armor inventory textures as complete 128×128 silhouettes. Added data-driven furnace fuel values for coal armor and all wood/plank/log/stem/bamboo-block armor through optional JSON `fuel_burn_time_per_material` and new `DreamEquipmentFuelValues`; burn time is base material burn time × armor recipe material count. Added `docs/reference/ROUND38_CHERRY_TEXTURE_AND_FUEL_VALUES_20260703.md`.
- Output updated: yes.
- Validations: generator write/check, equipment family validator, asset validator, set-effect validator, balance audit, and Gradle build all passed.
- Client-only: recheck cherry item icons in inventory; recheck furnace fuel behavior for coal armor and all plank/log/stem/bamboo-block armor; confirm non-fuel equipment did not become fuel unexpectedly.

### Earlier update

- Date: 2026-07-03
- Change: Expanded anvil repair coverage by adding optional JSON-owned `repair_ingredients` arrays to selected families. Repair tags now support multiple direct item ids and vanilla item tags. Added `docs/reference/ROUND37_REPAIR_INGREDIENT_EXPANSION_20260703.md`.
- Output updated: yes.
- Validations: generator write/check, equipment family validator, asset validator, set-effect validator, balance audit, and Gradle build all passed.
- Client-only: recheck live anvil repair for representative expanded materials.

### Earlier update

- Date: 2026-07-03
- Change: Completed local Java 25/Gradle build environment setup; confirmed current generator/validators/build pass; created `docs/reports/CURRENT_AGENT_BRIEF.md`, `docs/DOCUMENTATION_INDEX.md`, and `docs/reference/ROUND36_ENVIRONMENT_SETUP_AND_REPORT_BRIEF_20260703.md`. No gameplay source/resource content changed.
- Output updated: yes.
- Validations: generator drift check, equipment family validator, asset validator, set-effect validator, balance audit, and Gradle build all passed.
- Client-only: live MC client/world checks remain required for item visibility/localization, recipes, rendering, redstone signal behavior, enchanting refund, sonic-boom immunity, turtle helmet integration, brittle/decay mechanics, and tooltip durability values.

### Earlier update

- Date: 2026-07-02
- Change: Rebalanced clearly unreasonable tool durability and mining-tier values; armor tooltip now displays actual max durability per piece instead of durability multiplier; added `scripts/audit_equipment_balance.py`; added `docs/reference/ROUND35_DURABILITY_AND_MINING_TIER_AUDIT_20260702.md`.
- Output updated: yes.
- Validations: balance audit, equipment family validator, asset validator, set-effect validator, and Gradle build all passed.

### Earlier update (2026-07-06 — worn texture audit)

- Date: 2026-07-06
- Change: Completed full diagnostic audit of 22 stone/rock/mineral family worn equipment textures. No worn textures or source files were changed. Key findings: obsidian/lapis/quartz have severe color deviation from source block palette; redstone/amethyst have moderate deviation. UV alpha shapes are all correct. Extracted vanilla block palettes from MC 26.1.2 jar. Wrote rework plan at `docs/reports/ROUND56_WORN_TEXTURE_REWORK_PLAN.md`. Next task marked as worn texture batch regeneration.
- Output updated: no (analysis-only pass).
- Validations: not re-run (no resource changes). Previous build PASS still current.
- Client-only: no new client checks required for this pass.

### Latest update — 2026-07-06 — 石质/矿物穿戴贴图批量重做（Round 57）

- Date: 2026-07-06
- Change: Added `scripts/generate_rock_worn_textures.py`. Regenerated 66 worn equipment texture files (22 rock/mineral families × 3 layers). P0 fixes: obsidian (near-black restored), lapis (deep blue + gold highlight), quartz (cold white corrected). P1 fixes: redstone (dark/bright contrast circuit pattern), amethyst (blue-purple vs magenta). P2 fixes: cobblestone/cobbled_deepslate (seam lines), blackstone (purple veins), diorite (salt-and-pepper speckle), granite (pink mineral spots), mossy_cobblestone (stone seams + moss green). P3 refresh: all remaining 11 families remapped from vanilla block textures. All 22 families at ΔE ≤ 20 vs vanilla block palette.
- Output updated: yes. `release_output/dream-equipment-0.1.0.jar` and `release_output/dream-equipment-source-current-20260706b.zip` refreshed.
- Validations: generate_equipment_resources PASS (1369), generate_rock_worn_textures PASS (22 families), validate_equipment_families PASS (60/372), validate_assets PASS, validate_set_effects PASS, audit_balance PASS, Gradle BUILD SUCCESSFUL.
- Client-only: visually confirm obsidian (near-black), lapis (deep blue + gold), quartz (cold white), redstone (dark-red + bright circuit contrast), amethyst (blue-purple), cobblestone (seams), blackstone (veins), basalt vs smooth_basalt distinction.
