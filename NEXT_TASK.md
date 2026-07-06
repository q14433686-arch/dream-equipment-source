# NEXT_TASK

## ✅ 已完成 — 石质/矿物穿戴贴图批量重做（Round 57，2026-07-06）

### 完成内容
- 新建 `scripts/generate_rock_worn_textures.py`。
- 重新生成 66 个穿戴贴图文件（22 家族 × 3 层）。
- P0/P1/P2/P3 全量修复，所有 22 家族 ΔE ≤ 20。
- 所有验证器 PASS，Gradle BUILD SUCCESSFUL。
- `release_output/` 已刷新。

### 客户端检查清单（本轮）
1. 穿戴 obsidian 套装 → 近黑色，不再偏蓝紫
2. 穿戴 lapis 套装 → 深蓝，有金色亮斑
3. 穿戴 quartz 套装 → 冷白，不再偏暖黄
4. 穿戴 redstone 套装 → 暗红底 + 亮红电路线对比
5. 穿戴 amethyst 套装 → 蓝紫，不再偏洋红
6. 穿戴 cobblestone 套装 → 可见石块分割缝
7. 穿戴 blackstone 套装 → 可见深色层纹/紫色基调
8. 穿戴 basalt vs smooth_basalt → 两套可视觉区分
9. 穿戴 granite / diorite / granite → 确认矿点/斑驳感
10. 穿戴所有其他石质套装 → 确认整体颜色与原材料对应

# NEXT_TASK

## ★ 下一轮优先任务 — 石质/矿物穿戴贴图批量重做

**状态：准备完成，待下一轮执行**

### 执行目标
为以下材质的穿戴贴图（humanoid / humanoid_leggings / humanoid_baby）执行基于原版 block 材质的确定性重新生成。

### P0 必改（颜色严重偏离，视觉无法辨认材料）
| 家族 | 问题 | 修正方向 |
|---|---|---|
| `obsidian` | 穿戴主色 `#190751` 偏蓝紫，原版近黑 `#0f0a18` | B 通道从 ≈81 压至 ≈24 |
| `lapis` | 穿戴蓝色偏亮，缺金色亮点 | 降低 B 约 43，补金色高光 |
| `quartz` | 穿戴偏暖黄，原版冷白 | R-B 差从 32→13 |

### P1 必改（材质特征丢失）
| 家族 | 问题 | 修正方向 |
|---|---|---|
| `redstone` | 缺少暗红/亮红强对比 | 保留 `#e62008` + `#730c00` 双色对比 |
| `amethyst` | 偏洋红，原版为蓝紫 | G+12，R-25 向蓝紫偏移 |

### P2 建议改（颜色可接受但材质感缺失）
- `cobblestone` — 缺石块分割线图案
- `blackstone` — 缺紫色层纹特征
- `diorite` — 缺黑白斑驳感
- `granite` — 缺粉色矿点

### 执行方式
新建 `scripts/generate_rock_worn_textures.py`，参考 `generate_wood_worn_textures.py` 架构。  
详细方案见：`docs/reports/ROUND56_WORN_TEXTURE_REWORK_PLAN.md`

### 调色板参考（已从 MC 26.1.2 jar 提取，直接可用）
见规划文档第六节。

---

# NEXT_TASK

## Current turn status — environment setup / report brief — 2026-07-06

- Pulled fresh clone of `q14433686-arch/dream-equipment-source-current`.
- Read `AGENT_BRIEF.md`, `CURRENT_BASELINE.md`, `NEXT_TASK.md`, `CHANGELOG.md`, `docs/reports/CURRENT_AGENT_BRIEF.md`, and `docs/DOCUMENTATION_INDEX.md`.
- Confirmed `scripts/generate_agent_brief.py` still absent — recorded as pre-existing gap.
- Confirmed `docs/JSON_EXTENSION_SPEC_1_1_3.md` and `docs/EXTENDING_HERBCRAFT.md` still absent — recorded as pre-existing documentation gap.
- Installed Temurin 25.0.3+9-LTS at `/tmp/herbcraft-jdk25/jdk-25.0.3+9` (symlinked to `/tmp/herbcraft-jdk25/jdk-25`).
- `release_output/` was absent in fresh clone; re-created and populated with jar and source zip.
- No gameplay Java or resource content changed.

## Validation executed this turn

1. `python3 scripts/generate_equipment_resources.py` — PASS, `equipment resources in sync — files=1369`.
2. `python3 scripts/validate_equipment_families_json.py` — PASS, `families=60, items=372`.
3. `python3 scripts/validate_dream_equipment_assets.py` — PASS, `items=312, materials=56`.
4. `python3 scripts/validate_set_effects_json.py` — PASS, `passive=24, brittle=4`.
5. `python3 scripts/audit_equipment_balance.py` — PASS, armor durability formula OK.
6. `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — PASS, `BUILD SUCCESSFUL`.

## Client test checklist (carry-forward from Round 55)

1. Check `copper_shield`, `golden_shield`, `diamond_shield`, and `netherite_shield` in creative tab.
2. Test recipes and repair materials for all four vanilla-material shields.
3. Test blocking behavior and custom shield base textures.
4. Test `netherite_shield` fire resistance.
5. Confirm vanilla shield recipe is still disabled in survival.
6. Confirm 372 custom items appear/localize correctly.
7. Check representative recipes and recipe book unlock/display behavior.
8. Validate armor/tool rendering, especially log/stem/bamboo and rock tools.
9. Test redstone boots/full redstone set signal behavior with dust/repeaters and signal shutoff.
10. Test lapis enchanting refund, amethyst sonic-boom immunity, turtle helmet integration, bone shatter, slime decay/bounce, paper wet decay, stone physics, and tooltip durability values.

## Recommended next tasks

1. Implement any user-requested content or mechanic changes.
2. If `scripts/generate_agent_brief.py` is desired, create it as a Python script that reads CURRENT_BASELINE.md + NEXT_TASK.md + CHANGELOG.md and writes docs/reports/CURRENT_AGENT_BRIEF.md automatically.
3. Add `docs/JSON_EXTENSION_SPEC_1_1_3.md` if a JSON extension spec for this project is desired.
4. Continue client testing per checklist above.


## Current turn status — vanilla material shields — 2026-07-03

- Added requested vanilla material shields: copper, golden, diamond, and netherite.
- Implemented them as shield-only families in `equipment_families.json`.
- Added JSON-owned shield durability values and repair ingredient lists.
- Tuned netherite shield as very strong but not extreme: 1100 durability, modestly above obsidian shield.
- Marked `netherite_shield` fire-resistant in Java item registration.
- Updated shield texture source mapping for copper/gold/diamond/netherite.
- Current totals: 60 families / 372 custom items / 60 shields.
- Added report `docs/reference/ROUND55_VANILLA_MATERIAL_SHIELDS_20260703.md`.
- Refreshed release jar/source zip after validation.

## Validation executed this turn

1. `python3 scripts/generate_equipment_resources.py` — PASS, `equipment resources in sync — files=1369`.
2. `python3 scripts/generate_wood_worn_textures.py` — PASS, 72 files regenerated.
3. `python3 scripts/generate_shield_textures.py` — PASS, 60 shield textures generated.
4. `python3 scripts/validate_equipment_families_json.py` — PASS, `families=60, items=372`.
5. `python3 scripts/validate_dream_equipment_assets.py` — PASS, includes shield resources/textures.
6. `python3 scripts/validate_set_effects_json.py` — PASS, includes shield effect checks.
7. `python3 scripts/audit_equipment_balance.py` — PASS, 372 entries including all shields.
8. `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — PASS, `BUILD SUCCESSFUL`.

## Client test checklist

1. Check `copper_shield`, `golden_shield`, `diamond_shield`, and `netherite_shield` in creative tab.
2. Test recipes and repair materials.
3. Test blocking behavior and custom shield base textures.
4. Test `netherite_shield` fire resistance.
5. Confirm netherite feels strong but not excessive.
6. Confirm vanilla shield recipe is still disabled.

## Current turn status — project cover art — 2026-07-03

- User selected the minimal 2D logo-style cover image.
- Added the cover to documentation at `docs/assets/dream_equipment_cover.png`.
- Added a packaged resource mirror at `src/main/resources/assets/dream_equipment/cover.png`.
- Updated `README.md` to display the cover near the top.
- Updated `validate_dream_equipment_assets.py` with cover existence/dimension checks.
- Added report `docs/reference/ROUND54_PROJECT_COVER_ART_20260703.md`.
- Refreshed release jar/source zip after validation.

## Validation executed this turn

1. `python3 scripts/generate_equipment_resources.py` — PASS, `equipment resources in sync — files=1349`.
2. `python3 scripts/generate_wood_worn_textures.py` — PASS, 72 files regenerated.
3. `python3 scripts/generate_shield_textures.py` — PASS, 56 shield textures generated.
4. `python3 scripts/validate_equipment_families_json.py` — PASS, `families=56, items=368`.
5. `python3 scripts/validate_dream_equipment_assets.py` — PASS, includes cover image checks.
6. `python3 scripts/validate_set_effects_json.py` — PASS, includes shield effect checks.
7. `python3 scripts/audit_equipment_balance.py` — PASS, 368 entries including all shields.
8. `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — PASS, `BUILD SUCCESSFUL`.

## Follow-up

- No gameplay client test required for the cover.
- Optional: check the README/Modrinth-like preview to ensure the cover crops and displays well.

## Current turn status — disable vanilla shield recipe — 2026-07-03

- User reported recipe conflict between vanilla shield and Dream Equipment plank shields.
- Added `src/main/resources/data/minecraft/recipe/shield.json` override requiring 9 `minecraft:barrier` items.
- This effectively disables normal vanilla shield crafting while preserving the vanilla shield item for existing worlds/loot/commands/compatibility.
- Did not disable vanilla shield decoration recipe because it targets `minecraft:shield` and does not conflict with custom shield recipes.
- Updated asset validator to require the barrier-based vanilla shield recipe override.
- Added report `docs/reference/ROUND53_DISABLE_VANILLA_SHIELD_RECIPE_20260703.md`.
- Refreshed release jar/source zip after validation.

## Validation executed this turn

1. `python3 scripts/generate_equipment_resources.py` — PASS, `equipment resources in sync — files=1349`.
2. `python3 scripts/generate_wood_worn_textures.py` — PASS, 72 files regenerated.
3. `python3 scripts/generate_shield_textures.py` — PASS, 56 shield textures generated.
4. `python3 scripts/validate_equipment_families_json.py` — PASS, `families=56, items=368`.
5. `python3 scripts/validate_dream_equipment_assets.py` — PASS, includes vanilla shield recipe override check.
6. `python3 scripts/validate_set_effects_json.py` — PASS, includes shield effect checks.
7. `python3 scripts/audit_equipment_balance.py` — PASS, 368 entries including all shields.
8. `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — PASS, `BUILD SUCCESSFUL`.

## Client recipe retest checklist

1. Vanilla shield recipe shape should no longer produce `minecraft:shield`.
2. Dream Equipment plank shield recipes should produce their intended custom shields.
3. Recipe book should not offer a normal vanilla shield recipe in survival progression.
4. Existing vanilla shield items should remain valid if already present.

## Current turn status — custom shield base textures — 2026-07-03

- Researched vanilla MC 26.1 shield resources/rendering before implementation.
- Confirmed vanilla shield rendering uses `ShieldSpecialRenderer`, `Sheets.SHIELD_BASE(_NO_PATTERN)`, and `assets/minecraft/atlases/shield_patterns.json` directory source.
- Added `DreamEquipmentDataComponents.SHIELD_BASE_TEXTURE` as a synchronized item component.
- Added `ShieldSpecialRendererMixin` to replace the shield base sprite only for Dream Equipment shields that carry the custom component.
- Added `scripts/generate_shield_textures.py`, which derives custom shield base textures from vanilla `shield_base_nopattern.png` and each family source material.
- Generated 56 shield base textures under `assets/minecraft/textures/entity/shield/dream_equipment/`.
- Added audit image `docs/reports/ROUND52_CUSTOM_SHIELD_TEXTURE_AUDIT_20260703.png`.
- Added report `docs/reference/ROUND52_CUSTOM_SHIELD_BASE_TEXTURES_20260703.md`.
- Refreshed release jar/source zip after validation.

## Validation executed this turn

1. `python3 scripts/generate_equipment_resources.py` — PASS, `equipment resources in sync — files=1349`.
2. `python3 scripts/generate_wood_worn_textures.py` — PASS, 72 files regenerated.
3. `python3 scripts/generate_shield_textures.py` — PASS, 56 shield textures generated.
4. `python3 scripts/validate_equipment_families_json.py` — PASS, `families=56, items=368`.
5. `python3 scripts/validate_dream_equipment_assets.py` — PASS, includes shield texture/mixin/component checks.
6. `python3 scripts/validate_set_effects_json.py` — PASS, includes shield effect checks.
7. `python3 scripts/audit_equipment_balance.py` — PASS, 368 entries including all shields.
8. `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — PASS, `BUILD SUCCESSFUL`.

## Client shield texture test checklist

1. Check representative shields: oak, cherry, emerald, redstone, prismarine, obsidian, glass, cactus, bone, quartz.
2. Confirm normal and blocking poses both use material-adapted base texture.
3. Confirm enchanted glint still works.
4. Confirm no missing shield atlas texture warnings.
5. Confirm shield effects from passes 1/2 still work.
6. Confirm server join/multiplayer stability with synchronized `shield_base_texture` component.

## Recommended next round

- If shield textures are accepted, consider whether banner decoration should be supported, ignored, or explicitly disabled/documented for Dream Equipment shields.
- If any material looks poor, tune `scripts/generate_shield_textures.py` per material rather than changing shield behavior.

## Current turn status — shield effects data-driven pass 2 — 2026-07-03

- Added second-pass shield effects for obsidian, prismarine, amethyst, bone, coal, and quartz.
- Extended `shield_effects` in `set_effects.json` with JSON-owned values.
- Updated `DreamEquipmentShieldEffectRules` and `DreamEquipmentShieldEffects`.
- Added tooltip lines for all six new shield effects.
- Updated `validate_set_effects_json.py` for new shield effect value checks.
- Added report `docs/reference/ROUND51_SHIELD_EFFECTS_DATA_DRIVEN_PASS2_20260703.md`.
- Refreshed release jar/source zip after validation.

## Validation executed this turn

1. `python3 scripts/generate_equipment_resources.py` — PASS, `equipment resources in sync — files=1349`.
2. `python3 scripts/generate_wood_worn_textures.py` — PASS, 72 files regenerated.
3. `python3 scripts/validate_equipment_families_json.py` — PASS, `families=56, items=368`.
4. `python3 scripts/validate_dream_equipment_assets.py` — PASS, texture-backed item/material checks plus shield special-renderer/effect resources.
5. `python3 scripts/validate_set_effects_json.py` — PASS, including shield effect checks.
6. `python3 scripts/audit_equipment_balance.py` — PASS, 368 entries including all shields.
7. `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — PASS, `BUILD SUCCESSFUL`.

## Client shield effect test checklist

1. `obsidian_shield`: Slowness while blocking and durability refund against fire/explosions.
2. `prismarine_shield`: durability refund when blocking in water.
3. `amethyst_shield`: Warden sonic boom blocked at durability cost.
4. `bone_shield`: undead attack blocks refund durability.
5. `coal_shield`: fire damage blocks refund durability.
6. `quartz_shield`: projectile blocks refund durability.
7. Confirm tooltip lines.
8. Regression-test cactus/glass/redstone/slime/paper shield effects.

## Recommended next round

- If these shield effects pass, consider whether custom shield visuals are needed.
- Otherwise, tune `shield_effects` values only before adding more mechanics.

## Current turn status — shield effects data-driven pass 1 — 2026-07-03

- Added `shield_effects` values to `set_effects.json`.
- Added `DreamEquipmentShieldEffectRules` loader and `DreamEquipmentShieldEffects` event logic.
- Implemented five first-pass shield effects: cactus retaliation, glass shatter, redstone pulse, slime bounce, and paper wet blocking durability loss.
- Updated shield tooltips to show shield durability and special shield effects.
- Updated `validate_set_effects_json.py` and `validate_dream_equipment_assets.py` for shield effect rules/source checks.
- Added report `docs/reference/ROUND50_SHIELD_EFFECTS_DATA_DRIVEN_PASS1_20260703.md`.
- Refreshed release jar/source zip after validation.

## Validation executed this turn

1. `python3 scripts/generate_equipment_resources.py` — PASS, `equipment resources in sync — files=1349`.
2. `python3 scripts/generate_wood_worn_textures.py` — PASS, 72 files regenerated.
3. `python3 scripts/validate_equipment_families_json.py` — PASS, `families=56, items=368`.
4. `python3 scripts/validate_dream_equipment_assets.py` — PASS, texture-backed item/material checks plus shield special-renderer/effect resources.
5. `python3 scripts/validate_set_effects_json.py` — PASS, including shield effect checks.
6. `python3 scripts/audit_equipment_balance.py` — PASS, 368 entries including all shields.
7. `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — PASS, `BUILD SUCCESSFUL`.

## Client shield effect test checklist

1. `cactus_shield`: block melee attacks and confirm small retaliation with cooldown.
2. `glass_shield`: block high-damage attacks and confirm occasional shatter.
3. `redstone_shield`: block an attack beside redstone dust/lamp and confirm a short pulse.
4. `slime_shield`: block a living attacker and confirm bounce/knockback.
5. `paper_shield`: hold block in water/rain and confirm durability loss.
6. Confirm tooltips show the relevant shield effect lines.
7. Confirm ordinary shields without special shield effects still behave normally.

## Recommended next round

- After testing these five, add second-pass shield effects for obsidian/prismarine/amethyst/bone/coal/quartz only if the first pass feels stable.

## Current turn status — shield completion for all families — 2026-07-03

- Client prototype shield test passed.
- Expanded shield declarations from the 8-item prototype batch to all 56 current material families.
- Current custom item count is now 368.
- Every family now has a JSON-owned shield durability value.
- `generate_equipment_resources.py` now manages 1349 resources and generates shield item definitions, base models, blocking models, recipes, and lang keys for every family.
- Improved generated shield base-model particle texture mapping for non-block ingredients.
- Wood/log-like shield fuel follows existing fuel rule: 6 material slots × `fuel_burn_time_per_material`.
- Added report `docs/reference/ROUND49_SHIELD_COMPLETION_ALL_FAMILIES_20260703.md`.
- Refreshed release jar/source zip after validation.

## Validation executed this turn

1. `python3 scripts/generate_equipment_resources.py` — PASS, `equipment resources in sync — files=1349`.
2. `python3 scripts/generate_wood_worn_textures.py` — PASS, 72 files regenerated.
3. `python3 scripts/validate_equipment_families_json.py` — PASS, `families=56, items=368`.
4. `python3 scripts/validate_dream_equipment_assets.py` — PASS, texture-backed item/material checks plus shield special-renderer resources.
5. `python3 scripts/validate_set_effects_json.py` — PASS, `passive=24, brittle=4`.
6. `python3 scripts/audit_equipment_balance.py` — PASS, 368 entries including all shields.
7. `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — PASS, `BUILD SUCCESSFUL`.

## Client shield completion checklist

1. Confirm all 56 shields appear/localize correctly.
2. Test representative recipes from each category: plank, log, stone, gem, brittle, special.
3. Confirm offhand equip and blocking behavior still work.
4. Confirm shield durability values feel coherent.
5. Confirm anvil repair follows family repair tags.
6. Confirm wood/log-like shields work as fuel.
7. Watch logs for missing model/texture warnings from generated shield base/blocking models.
8. Decide whether vanilla special-renderer shield visuals are acceptable or custom shield rendering is needed later.

## Recommended next round

- If all shield behavior passes, decide whether to leave vanilla shield visuals as acceptable for this release.
- If visuals are not acceptable, make custom shield rendering a separate, explicitly scoped client-rendering task.

## Current turn status — shield prototype batch — 2026-07-03

- Implemented the Round 48 behavior-first shield prototype batch after the shield feasibility audit.
- Added 8 prototype shields: oak, cherry, bamboo, emerald, redstone, amethyst, prismarine, and obsidian.
- Added optional JSON-owned `shield` declarations to selected families.
- Extended `DreamEquipmentFamilyRules` to parse shields.
- Extended `DreamEquipmentItems` to register `ShieldItem` with vanilla-like durability, repair tags, offhand equip behavior, `BLOCKS_ATTACKS`, banner pattern data, and break/block sounds.
- Extended `DreamEquipmentFuelValues` so wood/plank prototype shields can be furnace fuel based on 6 material slots × material burn time.
- Extended `scripts/generate_equipment_resources.py` for shield item definitions, base/blocking models, recipes, and lang keys.
- Updated family/asset validators and balance audit for shields.
- Added report `docs/reference/ROUND48_SHIELD_PROTOTYPE_BATCH_20260703.md`.
- Refreshed release jar/source zip after validation.

## Validation executed this turn

1. `python3 scripts/generate_equipment_resources.py` — PASS, `equipment resources in sync — files=1157`.
2. `python3 scripts/generate_wood_worn_textures.py` — PASS, 72 worn layer files regenerated.
3. `python3 scripts/validate_equipment_families_json.py` — PASS, `families=56, items=320`.
4. `python3 scripts/validate_dream_equipment_assets.py` — PASS, texture-backed item/material checks plus shield special-renderer resources.
5. `python3 scripts/validate_set_effects_json.py` — PASS, `passive=24, brittle=4`.
6. `python3 scripts/audit_equipment_balance.py` — PASS, 320 entries including shields.
7. `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — PASS, `BUILD SUCCESSFUL`.

## Client shield test checklist

1. Confirm all 8 prototype shields appear in the combat creative tab.
2. Confirm recipes craft correctly and recipe book display is sane.
3. Equip shields in offhand and confirm normal/blocking transforms.
4. Confirm right-click/use blocking works in first and third person.
5. Confirm blocked attacks reduce damage and damage shield durability.
6. Confirm axe/disable behavior matches vanilla expectations.
7. Confirm anvil repair uses existing family repair tags.
8. Confirm oak/cherry/bamboo shields work as furnace fuel if expected.
9. Confirm visual acceptability of vanilla special-renderer output.
10. Test whether banner decoration works or whether custom shields should intentionally not support it.

## Recommended next round

- Do not expand shields beyond the prototype batch until client behavior and visuals are accepted.
- If visuals are unacceptable, decide whether to accept vanilla shield rendering, use banner/base-color approximations, or implement custom shield rendering as a separate client-rendering task.

## Current turn status — shield feasibility audit — 2026-07-03

- Audited vanilla MC 26.1.2 shield registration and resources after the cover art highlighted shields as a missing equipment category.
- Confirmed vanilla uses `ShieldItem` plus component-driven blocking behavior rather than a simple `Item.Properties.shield()` helper.
- Key vanilla shield components: durability 336, empty banner patterns, repairable wooden material tag, offhand equippable-unswappable, delayed `DataComponents.BLOCKS_ATTACKS`, and `SoundEvents.SHIELD_BREAK`.
- Confirmed vanilla shield item definition uses `minecraft:special` shield renderer with `using_item` condition and separate shield/blocking base models.
- Confirmed vanilla `ShieldSpecialRenderer` uses fixed shield base sprites plus banner patterns, so material-specific shield base textures are not trivial through JSON alone.
- Added report `docs/reference/ROUND47_SHIELD_FEASIBILITY_AUDIT_20260703.md`.
- No shield items were registered in this pass.

## Validation executed this turn

1. `python3 scripts/generate_equipment_resources.py` — PASS, `equipment resources in sync — files=1125`.
2. `python3 scripts/validate_equipment_families_json.py` — PASS, `families=56, items=312`.
3. `python3 scripts/validate_dream_equipment_assets.py` — PASS, `items=312, materials=56`.
4. `python3 scripts/validate_set_effects_json.py` — PASS, `passive=24, brittle=4`.
5. `python3 scripts/audit_equipment_balance.py` — PASS.
6. `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — PASS, `BUILD SUCCESSFUL`.

## Recommended next round

- Implement a small behavior-first shield prototype batch, not all materials at once.
- Suggested first batch: `oak_shield`, `cherry_shield`, `bamboo_shield`, `emerald_shield`, `redstone_shield`, `amethyst_shield`, `prismarine_shield`, `obsidian_shield`.
- Add optional `shield` declarations to `equipment_families.json`, extend Java registration with `ShieldItem`, and extend the generator for shield item definitions/models/recipes/lang.
- Accept vanilla special shield rendering initially unless material-specific custom shield rendering is explicitly required after testing.

## Future client shield test checklist

1. Startup with prototype shields.
2. First/third-person blocking animation.
3. Offhand equip behavior.
4. Durability loss on block.
5. Anvil repair.
6. Recipe book/crafting.
7. Shield disable behavior.
8. Visual acceptability of vanilla special-renderer shield output.

## Current turn status — plank component mapping for all plank families — 2026-07-03

- User accepted the cherry component-local plank worn-layer style.
- Expanded `PIECE_AWARE_PLANK_FAMILIES` from only `cherry` to all plank families via `set(PLANK_TEXTURES.keys())`.
- Regenerated worn equipment layers so every plank armor family maps each connected UV component to its corresponding vanilla `*_planks` texture once.
- Plank armor now uses larger component-local plank plates with restrained joins/breaks, avoiding dense tiling and chaotic global stripes.
- Log/stem/bamboo-block armor remains on vanilla-source baseline for now; do not apply plank logic to logs.
- Added audit image `docs/reports/ROUND46_PLANK_COMPONENT_MAPPING_AUDIT_20260703.png`.
- Added report `docs/reference/ROUND46_PLANK_COMPONENT_MAPPING_ALL_FAMILIES_20260703.md`.
- Refreshed release jar/source zip after validation.

## Validation executed this turn

1. `python3 scripts/generate_wood_worn_textures.py` — PASS, 72 files regenerated.
2. `python3 scripts/generate_equipment_resources.py` — PASS, `equipment resources in sync — files=1125`.
3. `python3 scripts/validate_equipment_families_json.py` — PASS, `families=56, items=312`.
4. `python3 scripts/validate_dream_equipment_assets.py` — PASS, `items=312, materials=56`.
5. `python3 scripts/validate_set_effects_json.py` — PASS, `passive=24, brittle=4`.
6. `python3 scripts/audit_equipment_balance.py` — PASS.
7. `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — PASS, `BUILD SUCCESSFUL`.

## Client visual retest checklist

1. Check all 12 plank armor families in game.
2. Compare light plank sets: birch, cherry, pale oak.
3. Compare dark/colored plank sets: dark oak, crimson, warped.
4. Confirm plank sets read as larger plank plates, not leather recolors or noisy stripes.
5. Confirm log/stem/bamboo-block sets are unchanged enough and still acceptable for now.
6. Confirm no black/floating bands in transparent UV areas.

## Recommended next round

- If plank families pass, design a separate component-local log/stem style instead of reusing plank logic.
- If a single plank family has palette issues, tune per-family sampling/contrast in `generate_wood_worn_textures.py`.

## Current turn status — cherry component-local plank test — 2026-07-03

- Implemented a focused cherry-only test after the vanilla-source full-layer fill still felt off compared with a placed cherry planks block.
- Added component-local plank mapping in `scripts/generate_wood_worn_textures.py`.
- `PIECE_AWARE_PLANK_FAMILIES = {"cherry"}` keeps this intentionally narrow.
- For cherry, opaque equipment-layer pixels are split into connected components; each component maps once to the vanilla `cherry_planks` texture, giving larger plank panels instead of dense full-layer tiling.
- Added only a few component-local vertical plank joins and restrained horizontal plate breaks.
- Other plank families remain on the vanilla-source baseline pending cherry approval.
- Added audit image `docs/reports/ROUND45_CHERRY_PLANK_COMPONENT_SAMPLE_20260703.png`.
- Added report `docs/reference/ROUND45_CHERRY_COMPONENT_LOCAL_PLANK_TEST_20260703.md`.
- Refreshed release jar/source zip after validation.

## Validation executed this turn

1. `python3 scripts/generate_wood_worn_textures.py` — PASS, 72 files regenerated.
2. `python3 scripts/generate_equipment_resources.py` — PASS, `equipment resources in sync — files=1125`.
3. `python3 scripts/validate_equipment_families_json.py` — PASS, `families=56, items=312`.
4. `python3 scripts/validate_dream_equipment_assets.py` — PASS, `items=312, materials=56`.
5. `python3 scripts/validate_set_effects_json.py` — PASS, `passive=24, brittle=4`.
6. `python3 scripts/audit_equipment_balance.py` — PASS.
7. `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — PASS, `BUILD SUCCESSFUL`.

## Client visual retest checklist

1. Test cherry armor specifically.
2. Compare with a placed cherry planks block.
3. Confirm it reads as larger cherry plank plates, not chaotic stripes and not flat leather.
4. Confirm no transparent-UV black/floating bands.

## Recommended next round

- If cherry is accepted, expand `PIECE_AWARE_PLANK_FAMILIES` to all plank families.
- Then create a separate component-local log/stem mapping for log armor rather than applying plank logic to logs.

## Current turn status — wood worn-layer vanilla source baseline — 2026-07-03

- User correctly pointed out the high-contrast generated stripes were too chaotic and lacked vanilla source-material elements.
- Reset the worn-layer approach to step 1: reuse corresponding vanilla plank/log/stem/bamboo block textures directly, then optimize later only if needed.
- Retuned `scripts/generate_wood_worn_textures.py` to remove synthetic global stripes/joins/bark bands.
- Generator now preserves current MC 26.1 equipment UV/alpha masks and fills only non-transparent pixels with the vanilla source block texture plus light mask shading.
- Regenerated the same 72 wood/log-like worn layer files.
- Added audit image `docs/reports/ROUND44_WOOD_WORN_LAYER_VANILLA_SOURCE_AUDIT_20260703.png`.
- Added report `docs/reference/ROUND44_WOOD_WORN_LAYER_VANILLA_SOURCE_BASELINE_20260703.md`.
- Refreshed release jar/source zip after validation.

## Validation executed this turn

1. `python3 scripts/generate_wood_worn_textures.py` — PASS, 72 files regenerated.
2. `python3 scripts/generate_equipment_resources.py` — PASS, `equipment resources in sync — files=1125`.
3. `python3 scripts/validate_equipment_families_json.py` — PASS, `families=56, items=312`.
4. `python3 scripts/validate_dream_equipment_assets.py` — PASS, `items=312, materials=56`.
5. `python3 scripts/validate_set_effects_json.py` — PASS, `passive=24, brittle=4`.
6. `python3 scripts/audit_equipment_balance.py` — PASS.
7. `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — PASS, `BUILD SUCCESSFUL`.

## Client visual retest checklist

1. Recheck cherry plank armor: it should now read as vanilla cherry planks sampled inside the armor mask, not artificial stripes.
2. Recheck all other plank armor variants for vanilla material readability.
3. Recheck log/stem/bamboo-block variants for source-material readability.
4. Confirm no black/floating bands in transparent UV areas.
5. Confirm item icons are unchanged.

## Recommended next round

- Do not add synthetic board/bark overlays yet.
- If this vanilla-source baseline is accepted but too flat, tune in tiny steps: per-family contrast multiplier, sampling scale, or palette mix only.

## Current turn status — visible wood worn-layer contrast — 2026-07-03

- Client screenshot showed cherry plank armor still appeared like flat pink leather, meaning Round 42's internal repaint was too subtle at normal player-render scale.
- Retuned `scripts/generate_wood_worn_textures.py` for stronger visible board/bark details while preserving current 26.1 equipment UV/alpha masks.
- Plank armor now has stronger horizontal seams, staggered vertical joins, alternating board-row tint, and clearer clipped binding/shadow bands.
- Log/stem/bamboo-block armor now has stronger vertical bark/stem channels and darker clipped edge/bark treatment.
- Regenerated the same 72 worn-layer files.
- Added audit image `docs/reports/ROUND43_WOOD_WORN_LAYER_VISIBLE_AUDIT_20260703.png`.
- Added report `docs/reference/ROUND43_VISIBLE_WOOD_WORN_LAYER_CONTRAST_20260703.md`.
- Refreshed release jar/source zip after validation.

## Validation executed this turn

1. `python3 scripts/generate_wood_worn_textures.py` — PASS, 72 files regenerated.
2. `python3 scripts/generate_equipment_resources.py` — PASS, `equipment resources in sync — files=1125`.
3. `python3 scripts/validate_equipment_families_json.py` — PASS, `families=56, items=312`.
4. `python3 scripts/validate_dream_equipment_assets.py` — PASS, `items=312, materials=56`.
5. `python3 scripts/validate_set_effects_json.py` — PASS, `passive=24, brittle=4`.
6. `python3 scripts/audit_equipment_balance.py` — PASS.
7. `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — PASS, `BUILD SUCCESSFUL`.

## Client visual retest checklist

1. Recheck cherry plank armor specifically; seams/board rows should now be visible in third-person/inventory-world view.
2. Check other plank families for too-strong or too-weak seams.
3. Check log/stem/bamboo-block armor for visible vertical bark/stem grain.
4. Confirm no black/floating bands appear in transparent UV areas.
5. Confirm item icons are unchanged.

## Recommended next round

- If cherry still reads too flat, increase plank seam strength further or add a dedicated cherry contrast multiplier.
- If some dark log families become too noisy, add per-family contrast multipliers to the worn texture generator.

## Current turn status — wood/log worn layer internal repaint — 2026-07-03

- User clarified the desired art task: do not redraw new armor shapes; preserve current 26.1 equipment UV/masks and replace the interior of the existing wood/log worn layers.
- Re-read current texture/spec reports before drawing: current equipment layers are `humanoid` 64×32, `humanoid_leggings` 64×32, and `humanoid_baby` 64×64 under `textures/entity/equipment/`.
- Added `scripts/generate_wood_worn_textures.py`.
- Regenerated 72 worn layer textures for 24 wood-like families × 3 current equipment layers.
- Plank families now use vanilla plank texture sampling with clipped board seams and sparse joins.
- Log/stem/bamboo-block families now use vanilla log/stem/block texture sampling with clipped vertical bark/stem grain and darker edges.
- Existing alpha/UV masks are preserved; generation writes only non-transparent interior pixels.
- Added final audit image `docs/reports/ROUND42_WOOD_WORN_LAYER_FINAL_AUDIT_20260703.png`.
- Added report `docs/reference/ROUND42_WOOD_LOG_WORN_LAYER_INTERNAL_REPAINT_20260703.md`.
- Refreshed release jar/source zip after validation.

## Validation executed this turn

1. `python3 scripts/generate_wood_worn_textures.py` — PASS, 72 files regenerated.
2. `python3 scripts/generate_equipment_resources.py` — PASS, `equipment resources in sync — files=1125`.
3. `python3 scripts/validate_equipment_families_json.py` — PASS, `families=56, items=312`.
4. `python3 scripts/validate_dream_equipment_assets.py` — PASS, `items=312, materials=56`.
5. `python3 scripts/validate_set_effects_json.py` — PASS, `passive=24, brittle=4`.
6. `python3 scripts/audit_equipment_balance.py` — PASS.
7. `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — PASS, `BUILD SUCCESSFUL`.

## Client visual retest checklist

1. Check all plank armor variants worn on adult player models.
2. Check all log/stem/bamboo-block armor variants worn on adult player models.
3. Check baby humanoid rendering where applicable.
4. Confirm no black/floating bands appear in transparent UV areas.
5. Confirm item icons were not changed by this worn-layer-only pass.

## Recommended next round

- If any family feels too noisy/dark/light, tune `scripts/generate_wood_worn_textures.py` and regenerate the 72 worn layers; do not hand-edit individual equipment layers unless a single material has a specific palette issue.

## Current turn status — redstone wire evaluator mixin — 2026-07-03

- Client reported that the redstone pulse effect itself works, but redstone dust lines still do not activate.
- Kept the short-lived redstone step/equip pulse design.
- Added `RedstoneWireEvaluatorMixin` targeting `RedstoneWireEvaluator#getBlockSignal`, so vanilla wire power recalculation directly includes Dream Equipment virtual pulse sources.
- Registered the mixin in `dream_equipment.mixins.json`.
- Updated asset validator to require the evaluator mixin.
- Added report `docs/reference/ROUND41_REDSTONE_WIRE_EVALUATOR_MIXIN_20260703.md`.
- Refreshed release jar/source zip after validation.

## Validation executed this turn

1. `python3 scripts/generate_equipment_resources.py` — PASS, `equipment resources in sync — files=1125`.
2. `python3 scripts/validate_equipment_families_json.py` — PASS, `families=56, items=312`.
3. `python3 scripts/validate_dream_equipment_assets.py` — PASS, `items=312, materials=56`.
4. `python3 scripts/validate_set_effects_json.py` — PASS, `passive=24, brittle=4`.
5. `python3 scripts/audit_equipment_balance.py` — PASS.
6. `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — PASS, `BUILD SUCCESSFUL`.

## Client redstone retest checklist

1. Place a redstone dust line beside the player.
2. Equip redstone boots; adjacent dust should receive the pulse and propagate along the line.
3. Step/move along/near the line; each new block position should pulse the line.
4. Confirm the line turns off after pulse expiry.
5. Compare boots-only pulse with full-set pulse.

## Recommended next round

- If redstone wire still fails, implement the documented fallback: directly pulse nearby redstone wire block states for the configured duration, with expiry/recalculation safeguards so external redstone sources are not overwritten.

## Current turn status — redstone step pulse mechanic — 2026-07-03

- User approved changing away from the continuous virtual redstone-block model.
- Reworked redstone equipment into a short-lived step/equip pulse mechanic.
- Redstone boots pulse at strength 7 for 8 ticks; full redstone set pulses at strength 15 for 12 ticks.
- Added JSON-owned `boots_pulse_ticks` and `full_set_pulse_ticks` to `set_effects.json`.
- `DreamEquipmentRedstonePower` now tracks active pulses with expiry rather than permanent active sources.
- Tooltip text now says redstone pulse instead of continuous redstone signal.
- Added report `docs/reference/ROUND40_REDSTONE_STEP_PULSE_MECHANIC_20260703.md`.
- Refreshed release jar/source zip after validation.

## Validation executed this turn

1. `python3 scripts/generate_equipment_resources.py --write` — PASS.
2. `python3 scripts/generate_equipment_resources.py` — PASS, `equipment resources in sync — files=1125`.
3. `python3 scripts/validate_equipment_families_json.py` — PASS, `families=56, items=312`.
4. `python3 scripts/validate_dream_equipment_assets.py` — PASS, `items=312, materials=56`.
5. `python3 scripts/validate_set_effects_json.py` — PASS, `passive=24, brittle=4`.
6. `python3 scripts/audit_equipment_balance.py` — PASS.
7. `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — PASS, `BUILD SUCCESSFUL`.

## Client redstone pulse retest checklist

1. Equip redstone boots beside redstone dust; dust should briefly pulse.
2. Step/move beside dust/repeaters/lamps; each new block position should emit a pulse.
3. Remove boots while a pulse is active; signal should expire after the configured short duration, not persist.
4. Compare boots-only pulse and full-set pulse.
5. Test logout/dimension change/death for no permanent stale signal.

## Recommended next round

- Tune only `boots_pulse_ticks` / `full_set_pulse_ticks` in JSON if the pulse feels too short or too long.
- Avoid returning to continuous redstone-block emulation unless there is a concrete redstone requirement that pulses cannot satisfy.

## Current turn status — redstone virtual source rework — 2026-07-03

- Investigated the redstone equipment mechanic after user feedback that the block-below signal model was unreliable and conceptually awkward.
- Replaced player-scan-on-query behavior with a server-tick rebuilt virtual redstone source registry in `DreamEquipmentRedstonePower`.
- Virtual source position is now the player's feet-space (`player.blockPosition()`), closer to a redstone block beside floor-level dust/repeaters than the previous `below()` source.
- Removed old redstone notification bookkeeping from `DreamEquipmentSetEffects`.
- Added `RedStoneWireBlockMixin` so redstone dust power recalculation directly considers virtual redstone equipment sources.
- Active source maps are rebuilt every server tick; stale sources should clear when boots are removed, players move, logout, change state, or signal strength changes.
- Added report `docs/reference/ROUND39_REDSTONE_VIRTUAL_SOURCE_REWORK_20260703.md`.
- Refreshed release jar/source zip after validation.

## Validation executed this turn

1. `python3 scripts/generate_equipment_resources.py` — PASS, `equipment resources in sync — files=1125`.
2. `python3 scripts/validate_equipment_families_json.py` — PASS, `families=56, items=312`.
3. `python3 scripts/validate_dream_equipment_assets.py` — PASS, `items=312, materials=56`.
4. `python3 scripts/validate_set_effects_json.py` — PASS, `passive=24, brittle=4`.
5. `python3 scripts/audit_equipment_balance.py` — PASS.
6. `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — PASS, `BUILD SUCCESSFUL`.

## Client redstone retest checklist

1. Place redstone dust beside the player, equip redstone boots, confirm dust powers.
2. Remove boots, confirm dust turns off quickly.
3. Walk away, confirm old dust turns off and new nearby dust updates.
4. Compare boots-only signal and full-set signal.
5. Test repeaters, redstone lamps, and comparable adjacent components beside the player's feet-space.
6. Test logout/dimension change/death if possible to confirm no stale signal remains.

## Recommended next round

- If redstone dust still has edge cases, the next option is to replace the dynamic source entirely with a deliberately limited mechanic, e.g. redstone boots only pulse/activate nearby components on step, rather than pretending to be a continuous redstone block.
- Do not add more broad `SignalGetter` patches without a concrete failing component; redstone should remain narrowly targeted and test-driven.

## Current turn status — cherry icon fix and fuel values — 2026-07-03

- Fixed client-reported broken cherry wood armor inventory icons.
- Regenerated `cherry_helmet`, `cherry_chestplate`, `cherry_leggings`, and `cherry_boots` item textures as complete 128×128 silhouettes using the accepted oak armor silhouette and vanilla cherry planks palette.
- Added data-driven fuel values for coal armor and all wood/plank/log/stem/bamboo-block armor.
- New JSON field: `fuel_burn_time_per_material`.
- New Java mechanism: `DreamEquipmentFuelValues` registers fuels through Fabric `FuelValueEvents.BUILD`.
- Fuel calculation follows recipe material count: helmet 5, chestplate 8, leggings 7, boots 4.
- Wood/log-like armor uses 300 ticks per material; coal armor uses 1600 ticks per material.
- Added report `docs/reference/ROUND38_CHERRY_TEXTURE_AND_FUEL_VALUES_20260703.md`.
- Refreshed release jar/source zip after validation.

## Validation executed this turn

1. `python3 scripts/generate_equipment_resources.py --write` — PASS.
2. `python3 scripts/generate_equipment_resources.py` — PASS, `equipment resources in sync — files=1125`.
3. `python3 scripts/validate_equipment_families_json.py` — PASS, `families=56, items=312`.
4. `python3 scripts/validate_dream_equipment_assets.py` — PASS, `items=312, materials=56`.
5. `python3 scripts/validate_set_effects_json.py` — PASS, `passive=24, brittle=4`.
6. `python3 scripts/audit_equipment_balance.py` — PASS.
7. `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — PASS, `BUILD SUCCESSFUL`.

## Client retest checklist

1. Check cherry helmet/chestplate/leggings/boots inventory icons; no piece should look cut off or incomplete.
2. Put coal armor pieces into a furnace and confirm relative burn times match 5/8/7/4 coal material counts.
3. Put plank armor and log/stem/bamboo-block armor pieces into a furnace and confirm they burn.
4. Confirm stone/gem/glass/redstone/lapis/etc. equipment did not become fuel accidentally.

## Recommended next round

- If another material family has broken icons, compare its texture dimensions/alpha silhouette against the accepted 128×128 armor templates before changing mechanics.
- If fuel values need tuning, adjust only `fuel_burn_time_per_material` in JSON unless the recipe pattern itself changes.

## Current turn status — repair ingredient expansion — 2026-07-03

- Responded to client feedback that some equipment still could not be repaired with expected materials.
- Kept Java repair mechanics unchanged: every family still points to one generated repair tag.
- Added optional JSON-owned `repair_ingredients` arrays in `equipment_families.json`; generator falls back to `ingredient` if absent.
- Expanded repair tags for common expectation gaps:
  - slime ball + slime block for slime armor
  - bone + bone meal for bone equipment
  - glass + glass pane for glass equipment
  - item/block forms for emerald, lapis, redstone, quartz, amethyst, and coal where appropriate
  - vanilla item tags for log/stem/bamboo-block armor repair, e.g. `#minecraft:oak_logs`, `#minecraft:bamboo_blocks`, `#minecraft:crimson_stems`
- Updated generator and family validator for the new optional field.
- Added report `docs/reference/ROUND37_REPAIR_INGREDIENT_EXPANSION_20260703.md`.
- Refreshed release jar/source zip after validation.

## Validation executed this turn

1. `python3 scripts/generate_equipment_resources.py --write` — PASS.
2. `python3 scripts/generate_equipment_resources.py` — PASS, `equipment resources in sync — files=1125`.
3. `python3 scripts/validate_equipment_families_json.py` — PASS, `families=56, items=312`.
4. `python3 scripts/validate_dream_equipment_assets.py` — PASS, `items=312, materials=56`.
5. `python3 scripts/validate_set_effects_json.py` — PASS, `passive=24, brittle=4`.
6. `python3 scripts/audit_equipment_balance.py` — PASS.
7. `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — PASS, `BUILD SUCCESSFUL`.

## Client repair retest checklist

1. Slime armor: slime ball and slime block.
2. Bone armor/weapons: bone and bone meal.
3. Glass armor/weapons: glass and glass pane.
4. Log/stem/bamboo-block armor: stripped logs/wood/hyphae/bamboo variants covered by vanilla tags.
5. Emerald/lapis/redstone/quartz/amethyst/coal equipment: item and block-form repair materials where configured.

## Recommended next round

- If any family still fails anvil repair, report the exact item + exact attempted repair material; the new `repair_ingredients` path should allow correcting it as a JSON-only change plus resource regeneration.
- Consider adding a small tooltip line for repair materials if repair expectations remain unclear.

## Current turn status — environment setup and report brief — 2026-07-03

- Pulled/read the standalone Dream Equipment repository and root `AGENT_BRIEF.md`.
- Attempted requested `python3 scripts/generate_agent_brief.py --write`; script is absent in this repository, so no generated brief script was run.
- Confirmed requested `docs/reports/CURRENT_AGENT_BRIEF.md` was absent before this pass; created it from current docs plus fresh validation/build output.
- Added `docs/DOCUMENTATION_INDEX.md` because no documentation index was present.
- Recorded missing requested docs `docs/JSON_EXTENSION_SPEC_1_1_3.md` and `docs/EXTENDING_HERBCRAFT.md` as documentation gaps; no Herbcraft-specific content was invented inside this standalone project.
- Set up Java 25 validation/build environment with Temurin `25.0.3+9-LTS` at `/tmp/herbcraft-jdk25/jdk-25`.
- Ran generator drift check, all validators, balance audit, and Gradle build successfully.
- Refreshed `release_output/dream-equipment-0.1.0.jar` and source zip after documentation updates.
- No gameplay Java code or generated gameplay/resource content changed this pass.

## Validation executed this turn

1. `python3 scripts/generate_equipment_resources.py` — PASS, `equipment resources in sync — files=1125`.
2. `python3 scripts/validate_equipment_families_json.py` — PASS, `families=56, items=312`.
3. `python3 scripts/validate_dream_equipment_assets.py` — PASS, `items=312, materials=56`.
4. `python3 scripts/validate_set_effects_json.py` — PASS, `passive=24, brittle=4`.
5. `python3 scripts/audit_equipment_balance.py` — PASS.
6. `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — PASS, `BUILD SUCCESSFUL`.

## Client-only checks still required

1. Launch MC `26.1.2` with Fabric Loader `0.19.3` and Fabric API `0.152.1+26.1.2`.
2. Confirm all 312 custom items appear and localize correctly.
3. Test representative recipes and recipe book display/unlocks.
4. Verify item icons and worn armor rendering for logs/stems/bamboo, rocks, turtle shell pieces, and custom tools/weapons.
5. Test redstone boots/full redstone set with dust/repeaters and signal shutoff after movement/removal.
6. Test lapis enchanting refund, amethyst sonic-boom immunity, turtle helmet set integration, bone shatter, slime decay/bounce, paper wet decay, stone armor physics, and tooltip durability values.

## Recommended next round

- Resolve documentation gaps if the missing Herbcraft/JSON extension docs are actually expected for this standalone repository, or explicitly remove those references from future setup instructions.
- Then proceed with live-client QA against the current 312-item build before changing balance/content again.

## Current turn status — expansion + deeper set mechanics — 2026-07-02

- Expanded the mod from 42 items to 95 items.
- New material families:
  - lapis tools + armor
  - redstone tools + armor
  - quartz tools + armor
  - amethyst tools + armor
  - prismarine tools + armor
  - slime armor
  - coal armor
- Expanded/deepened mechanics:
  - cactus retaliation is per armor piece, not full-set-only
  - paper full set takes wet/rain durability wear
  - slime full set gets mobility/fall utility
  - added set effects for lapis/redstone/quartz/amethyst/prismarine/slime/coal
- Added report `docs/reference/ROUND5_EXPANSION_AND_DEEPER_MECHANICS_20260702.md`.
- Build and validator pass.

## Client test checklist

1. Launch with MC 26.1.2 + Fabric Loader 0.19.3 + Fabric API 0.152.1.
2. Confirm all 95 items appear and localize correctly.
3. Craft representative recipes from every family.
4. Test every full-set effect for flicker and balance.
5. Test cactus per-piece retaliation.
6. Test paper armor wet durability wear.
7. Test glass shatter and obsidian/slime/prismarine set effects.

## Recommended next round

After live test, choose one:

1. Balance/polish pass: tune stats/effect duration/intensity and fix broken visuals.
2. Add config toggles for set effects or families if 95 items feels too broad.
3. Add remaining material families:
   - copper if desired despite modern vanilla
   - honey/slime variants
   - ender/chorus/echo/geode themed sets
4. Add advancements/recipe book unlock polish.

## External style reference

- User supplied Vanilla+ / VKL+ Modrinth link as a style/scope reference: https://modrinth.com/mod/vanilla-plus-data-pack
- Reference notes recorded in `docs/reference/VANILLA_PLUS_REFERENCE_NOTES_20260702.md`.
- Important boundary: Modrinth reports Vanilla+ as All Rights Reserved, so use it for visual/design reference only unless explicit reuse permission is provided. Redraw original Dream Equipment textures.

## Current turn status — tool scope correction + spears — 2026-07-02

- Replaced emerald tool icons with user-supplied templates.
- Added spears for emerald/lapis/redstone/quartz/amethyst/prismarine/glass/obsidian.
- Corrected quartz to weapon-only: sword, axe, spear.
- Added glass and obsidian weapon-only tools: sword, axe, spear.
- Removed quartz pickaxe/shovel/hoe resources and recipes.
- Current validator count: 104 items / 17 materials.

## Next client checks for tools

1. Check emerald tool icons match uploaded templates.
2. Check spear rendering and 26.1 combat behavior.
3. Confirm quartz utility recipes are gone.
4. Confirm glass/obsidian weapon-only direction feels right.

## Current turn status — texture/tag/equipment-standard correction — 2026-07-02

- Recolored the uploaded emerald tool template style across all relevant material tools/weapons.
- Researched vanilla 26.1 equipment resources and regenerated worn armor layers using the correct `equipment/*.json` + `humanoid` / `humanoid_baby` / `humanoid_leggings` 64×32 layout.
- Fixed custom spears to use separate render icon and in-hand model/texture via vanilla-style `display_context` item definitions.
- Added vanilla item tags for `swords`, `axes`, `pickaxes`, `shovels`, `hoes`, and `spears` for animation/combat mod recognition.
- Build and validator pass.

## Next client checks for this correction

1. Check non-emerald tools now match the template style in their material colors.
2. Check worn armor textures align correctly on adult and baby humanoid models.
3. Check first-person animation mods recognize weapons/tools through vanilla tags.
4. Check spear inventory icon vs held/in-hand render are correct.

## Current turn status — animation tag aliases + outline recolor fix — 2026-07-02

- Added c/fabric/forge tag aliases and aggregate `tools` / `weapons` / `melee_weapons` tags in addition to vanilla tags.
- Improved recolor logic so non-emerald tools no longer retain green edge pixels from emerald templates.
- Added report `docs/reference/ROUND8_ANIMATION_TAG_AND_TOOL_OUTLINE_FIX_20260702.md`.
- Build and validator pass.

## Client checks

1. Re-test first-person animation mod recognition for sword/axe/pickaxe/shovel/hoe.
2. Check non-emerald tool icons for leftover green pixels.

## Current turn status — handheld/class/name/outline fix — 2026-07-02

- Implemented the cause-analysis fixes:
  - tool/weapon models use `minecraft:item/handheld`
  - axes/shovels/hoes use `AxeItem` / `ShovelItem` / `HoeItem`
  - cobblestone Chinese names use `圆石`, not `原石`
  - dark emerald edge pixels are recolored for non-emerald tool templates
- Added report `docs/reference/ROUND10_HANDHELD_CLASS_NAME_AND_OUTLINE_FIX_20260702.md`.
- Build and validator pass.

## Client checks

1. Re-test first-person animation mod recognition.
2. Test axe strip / shovel flatten / hoe till behavior.
3. Check held transforms now look like vanilla handheld tools.
4. Check non-emerald tools for green edge remnants.
5. Check 圆石 names.

## Current turn status — wood/stone diversity audit — 2026-07-02

- Investigated user feedback that wood/stone/cobblestone equipment lacks diversity and render icons are wrong.
- Current generic wood/stone/cobblestone-style count is only 12 items: wooden×4, stone×4, cobblestone×4.
- Vanilla 26.1.2 has 12 plank variants; full per-plank armor would add 48 items.
- Vanilla 26.1.2 has 19 stone-like material items; excluding existing stone/cobblestone/obsidian leaves up to 16 additional stone-like armor families.
- Root cause: current icons are procedural/generic fills, not derived from actual raw material/block textures; worn layers are UV-correct but still visually generic.
- Report: `docs/reference/ROUND11_WOOD_STONE_VARIANT_AUDIT_AND_PLAN_20260702.md`.

## Next implementation recommendation

- Implement wood diversity first: 12 plank-style armor families, with icons and worn layers generated from actual plank texture palettes/overlays.
- Decision needed for existing `wooden_*`: keep generic alongside variants, treat it as oak, or migrate/rename to oak. Recommended: keep generic for compatibility and add explicit variants.
- After wood, implement a curated stone variant batch: mossy_cobblestone, cobbled_deepslate, blackstone, sandstone, red_sandstone, end_stone, tuff, calcite.

## Current turn status — wood variant armor implementation — 2026-07-02

- User chose option A: keep generic `wooden_*` and add explicit variants.
- Added 12 plank-based armor families: oak, spruce, birch, jungle, acacia, dark oak, mangrove, cherry, pale oak, bamboo, crimson, warped.
- Added 48 items, increasing total to 152 items / 29 materials.
- Icons and worn-layer material cues are generated from actual vanilla plank textures.
- Build and validator pass.

## Next implementation recommendation

- Client-test wood variant icons and worn layers first.
- Then implement curated stone variant batch: mossy_cobblestone, cobbled_deepslate, blackstone, sandstone, red_sandstone, end_stone, tuff, calcite.

## Current turn status — wood/stone/cobblestone render fix — 2026-07-02

- Fixed the wooden armor black/floating horizontal-line issue by regenerating worn layers with alpha-safe overlays.
- Regenerated wood/plank icons from vanilla leather armor item templates + actual plank textures.
- Regenerated stone/cobblestone icons from vanilla iron armor item templates + actual stone/cobblestone textures.
- Added report `docs/reference/ROUND13_WOOD_STONE_RENDER_FIX_20260702.md`.
- Build and validator pass.

## Next client checks

1. Re-test wooden/plank armor worn rendering; black bands should be gone.
2. Check wood/stone/cobblestone item icons against expected correct armor silhouettes.
3. If acceptable, proceed to curated stone variant batch.

## Current turn status — curated stone variant armor implementation — 2026-07-02

- Added 8 curated stone-like armor families: mossy cobblestone, cobbled deepslate, blackstone, sandstone, red sandstone, end stone, tuff, calcite.
- Added 32 items, increasing total to 184 items / 37 materials.
- Icons/layers are generated from real vanilla block textures.
- Added first-pass set effects for these variants.
- Build and validator pass.

## Next client checks

1. Check the 8 stone variants in inventory and worn on player.
2. Check recipes and set effects.
3. Tune or remove any overpowered effects after testing.

## Current turn status — physics-style mechanics pass — 2026-07-02

- Added material-property-based behavior instead of only generic strong set buffs:
  - emerald set: Hero of the Village for trade discount flavor
  - slime set: durability decay every tick, slime-ball return on break, 10% damage cancel
  - slime boots: cancel and bounce falls of 12 blocks or less
  - glass/calcite/quartz/amethyst: heavy-hit shatter chances
  - heavy armor slowness remains for obsidian/deepslate/blackstone
- Redstone boots real signal emission is not faked; next pass should implement a redstone-power query/mixin after defining exact signal position/range.
- Build and validator pass.

## Next mechanic target

- Implement redstone boots true signal output: choose whether signal is emitted at player block, block below, or adjacent blocks, then add the required world/block redstone power integration.

## Current turn status — set effects data-driven decoupling — 2026-07-02

- Added `data/dream_equipment/set_effects.json` and moved set-effect values out of Java.
- Added `DreamEquipmentSetEffectRules` loader and `validate_set_effects_json.py`.
- Refactored `DreamEquipmentSetEffects` to use JSON-owned passive effects, cactus retaliation, slime behavior, wet durability, and brittle shatter rules.
- Build and validators pass.

## Next decoupling targets

1. Add `materials.json` for registration-time material stats and family declarations.
2. Generate recipes/assets from material-family data instead of ad hoc scripts.
3. Decide whether set-effect JSON needs runtime `/reload` support or startup-only is enough for now.
4. Implement redstone boots real redstone signal as a separate mechanic after signal-position rules are decided.

## Current turn status — data-driven family registration, round 1/2 — 2026-07-02

- Added `equipment_families.json` owning all family declarations, armor stats, tool stats, ingredients, and included pieces/tools.
- Added `DreamEquipmentFamilyRules` loader.
- Rewrote `DreamEquipmentItems` to register dynamically from the JSON instead of hardcoded Java material fields.
- Added `validate_equipment_families_json.py`.
- Build and validators pass.

## Round 2/2 target

- Add a deterministic resource generator that reads `equipment_families.json` and regenerates item definitions, models, recipes, repair tags, tool tags, and lang keys.
- Add sync/drift validator so generated resource files cannot silently diverge from the JSON.
- After that, material family additions should be JSON + generator driven instead of manual file edits.

## Current turn status — resource generator and drift check, round 2/2 — 2026-07-02

- Added `scripts/generate_equipment_resources.py`.
- Generator reads `equipment_families.json` and manages 687 resource files: item definitions, item models, recipes, equipment definitions, repair tags, tool tags, aggregate tags, and lang keys.
- Running generator without `--write` is now a drift check.
- Full decoupling target for current content is complete: registration and set-effect values are JSON-driven, and resources can be regenerated/checked from family JSON.
- Build and validators pass.

## Recommended next task

- Implement redstone boots real redstone signal output as a separate mechanic, or add tooltip generation from `set_effects.json` / `equipment_families.json` so players can see effects in game.

## Current turn status — data-driven tooltips — 2026-07-02

- Added client entrypoint and tooltip callback.
- Tooltips now show stats and effects based on `equipment_families.json` and `set_effects.json`.
- Armor shows material, armor, durability multiplier, toughness/knockback if relevant, enchantability, and set-effect/drawback lines.
- Tools show material, type, durability, speed, attack bonus, and enchantability.
- Build and validators pass.

## Next recommended tasks

1. Client-test tooltip readability and wording.
2. Move tooltip sentence templates into lang keys if bilingual polish is needed.
3. Implement redstone boots real redstone signal output.

## Current turn status — redstone signal + localized tooltips — 2026-07-02

- Redstone boots now output signal 7 from the block below the player; full redstone set outputs signal 15.
- Implemented with `SignalGetterMixin` and `DreamEquipmentRedstonePower`, with neighbor updates while active.
- Tooltip templates/material names now use lang keys generated from JSON and `Component.translatable`.
- Build and validators pass.

## Client checks

1. Confirm game starts with the new mixin.
2. Test redstone dust/repeater next to the block below player with redstone boots/full set.
3. Confirm signal turns off after moving away/removing boots.
4. Confirm zh/en tooltip templates display correctly.

## Current turn status — redstone/slime/icon fix pass — 2026-07-02

- Expanded redstone signal handling so redstone dust should query nearby player redstone sources through `getBestNeighborSignal`.
- Slime armor now uses slime blocks, has higher durability, and returns modest slime balls on decay break.
- Wood/plank/stone/cobblestone inventory icons regenerated from emerald armor templates with material palettes.
- Build and validators pass.

## Client checks

1. Retest redstone dust with redstone boots/full set.
2. Confirm signal turns off after moving/removing boots.
3. Confirm slime recipes now use slime blocks and durability feels better.
4. Check bamboo/wood/stone/cobblestone icons.
5. If redstone dust still fails, next pass must mixin directly into `RedStoneWireBlock` power calculation.

## Current turn status — redstone/slime/icon/tools/effect rebalance — 2026-07-02

- Redstone dust fix attempt: added best-neighbor/neighbor-signal signal paths and old/new position updates.
- Slime armor now costs slime blocks and has higher durability/adjusted returns.
- Wood/plank/stone/cobblestone icons regenerated from emerald armor templates with material palettes.
- Added curated tools/weapons for several stone/end/bone/cactus families.
- Removed or contextualized several boring/unreasonable placeholder effects.
- Current count: 212 items / 37 materials.
- Build and validators pass.

## Client checks

1. Redstone dust/repeater detection with redstone boots/full set.
2. Slime armor recipes/durability/return feel.
3. Wood/bamboo/stone/cobblestone item icons.
4. New curated weapons/tools and animation recognition.
5. Rebalanced effects.

## If redstone still fails

- Target `RedStoneWireBlock` power calculation directly.

## Current turn status — A+B+C+D material fix batch — 2026-07-02

- Wood/plank icons are now muted vanilla leather reskins, not shiny emerald-template variants.
- Glass armor follows supplied glass pane reference for item and worn textures.
- Redstone signal detection expanded again through neighbor query paths.
- Slime armor cost/durability rebalanced around slime blocks.
- Blackstone tools/weapons removed; blackstone armor remains.
- Added curated tools/weapons for suitable stone/end/bone/cactus materials.
- Added granite/diorite/andesite/basalt/smooth basalt/dripstone/netherrack armor families.
- Further pruned unreasonable placeholder effects.
- Current count: 236 items / 44 materials.

## Client checks

1. Wood/plank icons, especially bamboo.
2. Glass item and worn armor look.
3. Redstone dust/repeater detection.
4. Slime cost and durability.
5. Blackstone tools removed.
6. New tools/weapons and new stone-like armor families.

## Current turn status — physics rebalance and redstone retry — 2026-07-02

- Retried redstone dust support via best-neighbor/neighbor-signal paths.
- Rebalanced slime armor cost/durability.
- Regenerated wood/glass visuals per user direction.
- Added C+D material tool/effect changes and stone physics rules.
- Build and validators pass.

## Client checks

1. Redstone dust/repeater signal.
2. Slime cost/durability/returns.
3. Wood/glass visuals.
4. Obsidian weapon break chance.
5. Stone armor physics and mossy repair.

## Current turn status — narrow brittle rules and density rebalance — 2026-07-02

- Fixed over-broad brittle display by separating armor-set and weapon/tool brittle tooltips.
- Obsidian weapon shatter no longer drops obsidian.
- Stone armor physics retuned by material density/fragility, including mossy cobblestone and netherrack.
- Validators/build pass.

## Client checks

1. Calcite tools/weapons should not show armor shatter lines.
2. Obsidian weapons should break without dropping obsidian.
3. Stone armor density differences should feel coherent.

## Current turn status — user-suggested mechanics implementation — 2026-07-02

- Armadillo shell boots: Speed III on sand/red sand/gravel/suspicious variants.
- Prismarine pickaxe: underwater Haste II and Heart of the Sea recipe requirement.
- Prismarine armor recipes: include nautilus shells.
- Redstone recipes: redstone block + redstone dust mix.
- Paper armor wet/rain damage: 1 durability per 10 ticks.
- Build and validators pass.

## Client checks

1. Armadillo terrain speed.
2. Prismarine pickaxe underwater haste and recipe.
3. Prismarine armor nautilus recipes.
4. Redstone recipe costs.
5. Paper wet decay speed.

## Current turn status — bone/chainmail/turtle/log armor batch — 2026-07-02

- Removed old generic `wooden_*` armor.
- Added all log/stem/bamboo-block armor variants separately from plank variants.
- Added turtle shell full set with Resistance II + Slowness + Water Breathing.
- Bone shatter returns bone meal; bone weapons can shatter.
- Full vanilla chainmail approximates Projectile Protection II by restoring part of projectile damage.
- Current count: 284 items / 56 materials.
- Build and validators pass.

## Client checks

1. Confirm `wooden_*` is gone and plank/log variants remain.
2. Test turtle shell full set effects.
3. Test bone weapon/armor shatter drops bone meal.
4. Test full chainmail against arrows/projectiles.

## Current turn status — lapis enchanting support — 2026-07-02

- Wearing any lapis armor piece refunds enchanting-table lapis cost after successful enchant.
- Refund is paid by damaging lapis armor durability.
- No full set required.
- Tooltip line added for lapis armor.
- Build and validators pass.

## Client checks

1. Enchant with one lapis armor piece and confirm lapis refund.
2. Confirm lapis armor durability decreases.
3. Confirm no refund with no lapis armor.

## Current turn status — amethyst sonic boom immunity — 2026-07-02

- Added `damage_immunities` to `set_effects.json`.
- Full amethyst armor now cancels Warden sonic boom damage.
- Tooltip displays the immunity.
- Build and validators pass.

## Client checks

1. Wear full amethyst armor and test Warden sonic boom.
2. Confirm other damage types still apply.
3. Confirm tooltip shows immunity line.

## Current turn status — turtle helmet integration and log icon fix — 2026-07-02

- Removed custom `turtle_shell_helmet`; vanilla turtle helmet is now part of turtle shell set.
- Regenerated turtle shell chest/legs/boots textures from vanilla turtle references.
- Regenerated log/stem/bamboo-block armor icons as cleaner vanilla leather-style reskins.
- Build and validators pass.

## Client checks

1. Custom turtle shell helmet should be gone.
2. Vanilla turtle helmet + custom turtle chest/legs/boots should trigger set effects.
3. Log armor icons should no longer look broken.

## Current turn status — log icon fix and rock tools completion — 2026-07-02

- Fixed log/stem/bamboo-block armor item icons using accepted emerald armor templates.
- Generated missing rock-family tool/weapon textures.
- Current count: 302 items / 56 materials.
- Build and validators pass.

## Client checks

1. Log/stem/bamboo-block helmet/leggings/boots icons.
2. Granite/diorite/andesite/basalt/smooth basalt/dripstone/netherrack tools.

## Current turn status — pickaxe silhouette and rock tool expansion — 2026-07-02

- Regenerated all custom pickaxes from vanilla diamond pickaxe silhouette.
- Added granite/diorite/andesite shovel+hoe.
- Added mossy cobblestone, sandstone, red sandstone, and tuff shovels.
- Current count: 312 items / 56 materials.
- Build and validators pass.

## Client checks

1. Compare custom pickaxes to vanilla pickaxe in inventory.
2. Check newly added rock shovels/hoes.

## Current turn status — emerald armor recipe rebalance — 2026-07-02

- Emerald armor recipes now mainly use emerald blocks and secondarily emeralds.
- Full emerald armor set cost is 11 emerald blocks + 8 emeralds.
- Build and validators pass.

## Client checks

1. Confirm emerald armor recipes in recipe book.
2. Confirm crafting works with emerald blocks + emeralds.
3. Confirm cost feels appropriate for Luck + Hero of the Village effects.

## Current turn status — durability and mining tier audit — 2026-07-02

- Rebalanced tool durability and mining tiers for brittle/stone/high-value materials.
- Armor tooltip now displays actual max durability per piece.
- Added `scripts/audit_equipment_balance.py`.
- Build and validators pass.

## Client checks

1. Compare armor tooltip durability with actual durability bar/max damage.
2. Check stone-like tools cannot mine unintended high-tier blocks.
3. Check obsidian weapons feel high-damage but short-lived.

---

## ★ 玻璃装备半透明调研完成（2026-07-06）

详细报告：`docs/reports/ROUND57_GLASS_TRANSLUCENCY_RESEARCH.md`

### 核心结论

| 层 | 半透明支持 | 所需工作 |
|---|---|---|
| item 贴图（背包/手持） | ✅ 原生支持，PNG 有中间 alpha 即生效 | 修改贴图 PNG |
| 穿戴层（worn）真半透明 | ❌ 管线固定 CUTOUT，需 Mixin | 注入 EquipmentLayerRenderer 改用 armorTranslucent |
| 穿戴层 伪玻璃效果 | ✅ 可用镂空边框（CUTOUT） | 修改贴图，仅保留边框像素 |

### 推荐实施顺序

1. **下一轮 P0**：item 贴图半透明（零 Java 改动，效果立竿见影）
2. **下一轮 P1**：穿戴贴图镂空边框（伪玻璃，无 artifact 风险）
3. **后续可选**：穿戴层真半透明 Mixin（需充分测试排序问题）

### 颜色方案（已确定）
- 主色填充：`#a8d4e8` alpha=110
- 高光线：`#d8eff8` alpha=180
- 边框/棱线：`#5f9aaa` alpha=255
- 阴影边：`#3a7080` alpha=255

