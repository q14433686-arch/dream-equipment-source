# CHANGELOG

## 0.1.0 — 2026-07-06 — 石质/矿物穿戴贴图批量重做（Round 57）

### Changed

- 新增 `scripts/generate_rock_worn_textures.py`：22 个石质/矿物装备家族的穿戴贴图确定性重新生成脚本，类比 `generate_wood_worn_textures.py`。
- 重新生成 66 个穿戴贴图文件（humanoid / humanoid_leggings / humanoid_baby，22 个家族各 3 层）。
- **P0 严重修复**：obsidian（B 通道从偏高 57 修正到近黑）、lapis（蓝色提深，补金色高光点）、quartz（偏暖黄修正为冷白）。
- **P1 特征修复**：redstone（保留暗红/亮红强对比电路图案）、amethyst（从洋红修正为蓝紫均衡）。
- **P2 材质感修复**：cobblestone（石块分割缝）、cobbled_deepslate（同上）、blackstone（紫色层纹）、diorite（黑白斑驳）、granite（粉色矿点）、mossy_cobblestone（石块缝+苔绿）。
- **P3 全面刷新**：stone、andesite、basalt、smooth_basalt、netherrack、sandstone、red_sandstone、end_stone、tuff、calcite、dripstone_block 均从原版 block 材质重新映射。
- basalt vs smooth_basalt 增加区分度（smooth_basalt 整体微亮 +4 三通道）。
- 所有修改严格保留原 UV alpha 形状，仅替换非透明像素颜色。

### Validation

- `python3 scripts/generate_equipment_resources.py` — PASS, files=1369.
- `python3 scripts/generate_rock_worn_textures.py` — PASS, families=22.
- `python3 scripts/validate_equipment_families_json.py` — PASS, families=60, items=372.
- `python3 scripts/validate_dream_equipment_assets.py` — PASS, items=312, materials=56.
- `python3 scripts/validate_set_effects_json.py` — PASS, passive=24, brittle=4.
- `python3 scripts/audit_equipment_balance.py` — PASS.
- `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — BUILD SUCCESSFUL.

### Final colour fidelity (all 🟢, ΔE ≤ 20 vs vanilla block palette)

obsidian ΔE=13.3 | lapis ΔE=6.3 | quartz ΔE=15.6 | redstone ΔE=14.5 | amethyst ΔE=6.4 | cobblestone ΔE=17.3 | mossy_cobblestone ΔE=16.9 | all others ΔE < 15.

### Client-only

1. 穿戴 obsidian 套装确认近黑色（不再偏蓝紫）。
2. 穿戴 lapis 套装确认深蓝，有金色亮斑。
3. 穿戴 quartz 套装确认冷白（不再偏暖黄）。
4. 穿戴 redstone 套装确认暗红底+亮红电路线对比感。
5. 穿戴 amethyst 套装确认蓝紫（不再偏洋红）。
6. 穿戴 cobblestone 套装确认有石块分割缝。
7. 穿戴 blackstone 套装确认有深色层纹。
8. 穿戴 basalt vs smooth_basalt 两套可视觉区分。



## 0.1.0 — 2026-07-06 — 穿戴贴图审计准备

### Analysed (no files changed)

- 完成全量穿戴贴图诊断：22 个石质/矿物家族的 humanoid worn 贴图颜色保真度分析。
- 确认 UV 形状模板全部正确（与原版 iron 一致），无需修改形状。
- 识别 P0 严重偏离：obsidian（B 通道严重偏高）、lapis（蓝色过亮）、quartz（偏暖黄，原版冷白）。
- 识别 P1 偏差：redstone（缺深暗红对比）、amethyst（偏洋红）。
- 识别 P2 材质感不足：cobblestone、blackstone、diorite、granite。
- 从 MC 26.1.2 客户端 jar 提取 22 种材质 block 调色板作为下一轮修正参考。
- 编写下一轮执行规划：`docs/reports/ROUND56_WORN_TEXTURE_REWORK_PLAN.md`。
- 生成审计图像：ROUND56_WORN_TEXTURE_AUDIT_PRE.png、ROUND56_WORN_VS_SOURCE_AUDIT.png、ROUND56_WORN_DETAIL_AUDIT.png。
- 未修改任何 worn 贴图、Java 源码、JSON 数据文件。
- 更新 NEXT_TASK.md，将穿戴贴图重做标注为下一轮 ★ 优先任务。

### Validation

- 本次为分析准备工作，未修改任何资源文件，不需要重新验证。
- 所有验证器（环境搭建轮已执行）状态：PASS。

### Client-only

- 无，本次未改动任何游戏资源。


## 0.1.0 — 2026-07-06 — Environment setup and report brief (Round 56)

### Changed

- Re-ran full environment setup on a fresh clone of `q14433686-arch/dream-equipment-source-current`.
- Installed Temurin 25.0.3+9-LTS at `/tmp/herbcraft-jdk25/jdk-25.0.3+9`.
- Re-created `release_output/` directory (absent in fresh clone); copied jar and built source zip.
- Updated `docs/reports/CURRENT_AGENT_BRIEF.md` to Round 56.
- Updated `CURRENT_BASELINE.md` to 2026-07-06.
- Updated `NEXT_TASK.md` with Round 56 turn status and carry-forward client checklist.
- No gameplay Java or generated gameplay/resource content changed.

### Validation

- `python3 scripts/generate_equipment_resources.py` — PASS, `equipment resources in sync — files=1369`.
- `python3 scripts/validate_equipment_families_json.py` — PASS, `families=60, items=372`.
- `python3 scripts/validate_dream_equipment_assets.py` — PASS, `items=312, materials=56`.
- `python3 scripts/validate_set_effects_json.py` — PASS, `passive=24, brittle=4`.
- `python3 scripts/audit_equipment_balance.py` — PASS, armor durability formula and guardrail values OK.
- `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — BUILD SUCCESSFUL (Gradle 9.4.1, Loom 1.16.3).

### Client-only

- No new client checks added this pass. Carry-forward client checks from Round 55 apply (vanilla material shields, 372 items visibility, recipes, redstone behavior, etc.).


## 0.1.0 — 2026-07-03 — Vanilla material shields

### Added

- Added shield-only families for vanilla material shields: copper, golden, diamond, and netherite.
- Added `copper_shield`, `golden_shield`, `diamond_shield`, and `netherite_shield`.
- Current totals are now 60 families / 372 custom items / 60 shields.
- Added repair ingredients for copper/gold/diamond/netherite shield families.
- Marked `netherite_shield` fire-resistant during item registration.
- Extended shield texture particle/source mapping for copper/gold/diamond/netherite materials.
- Added `docs/reference/ROUND55_VANILLA_MATERIAL_SHIELDS_20260703.md`.

### Validation

- `python3 scripts/generate_equipment_resources.py` — PASS, 1369 generated resources in sync.
- `python3 scripts/generate_wood_worn_textures.py` — PASS, 72 worn layer files regenerated.
- `python3 scripts/generate_shield_textures.py` — PASS, 60 shield base textures generated.
- `python3 scripts/validate_equipment_families_json.py` — PASS, 60 families / 372 items.
- `python3 scripts/validate_dream_equipment_assets.py` — PASS, includes shield resources/textures.
- `python3 scripts/validate_set_effects_json.py` — PASS, includes shield effect checks.
- `python3 scripts/audit_equipment_balance.py` — PASS, 372 entries including all shields.
- `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — BUILD SUCCESSFUL.

### Client-only

- Test the four new shields for visibility, recipes, repair, blocking, textures, and netherite fire resistance/balance.

## 0.1.0 — 2026-07-03 — Project cover art

### Added

- Added selected minimal 2D Dream Equipment cover art.
- Added documentation cover at `docs/assets/dream_equipment_cover.png`.
- Added packaged resource copy at `src/main/resources/assets/dream_equipment/cover.png`.
- Updated `README.md` to display the cover near the top.
- Updated asset validator to require the cover files and basic dimensions.
- Added `docs/reference/ROUND54_PROJECT_COVER_ART_20260703.md`.

### Validation

- `python3 scripts/generate_equipment_resources.py` — PASS, 1349 generated resources in sync.
- `python3 scripts/generate_wood_worn_textures.py` — PASS, 72 worn layer files regenerated.
- `python3 scripts/generate_shield_textures.py` — PASS, 56 shield base textures generated.
- `python3 scripts/validate_equipment_families_json.py` — PASS, 56 families / 368 items.
- `python3 scripts/validate_dream_equipment_assets.py` — PASS, includes cover image checks.
- `python3 scripts/validate_set_effects_json.py` — PASS, includes shield effect checks.
- `python3 scripts/audit_equipment_balance.py` — PASS, 368 entries including all shields.
- `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — BUILD SUCCESSFUL.

### Client-only

- No gameplay check required. Optional: confirm README/Modrinth-style preview displays the cover correctly.

## 0.1.0 — 2026-07-03 — Disable vanilla shield recipe

### Changed

- Overrode `minecraft:shield` recipe at `data/minecraft/recipe/shield.json` to require `minecraft:barrier`, effectively disabling vanilla shield crafting in survival.
- This resolves recipe conflicts between vanilla's broad wooden-material shield recipe and Dream Equipment plank shield recipes.
- Existing vanilla shield items remain valid; only normal survival crafting is disabled.
- Added validator guard for the vanilla shield recipe override.
- Added `docs/reference/ROUND53_DISABLE_VANILLA_SHIELD_RECIPE_20260703.md`.

### Validation

- `python3 scripts/generate_equipment_resources.py` — PASS, 1349 generated resources in sync.
- `python3 scripts/generate_wood_worn_textures.py` — PASS, 72 worn layer files regenerated.
- `python3 scripts/generate_shield_textures.py` — PASS, 56 shield base textures generated.
- `python3 scripts/validate_equipment_families_json.py` — PASS, 56 families / 368 items.
- `python3 scripts/validate_dream_equipment_assets.py` — PASS, includes vanilla shield recipe override check.
- `python3 scripts/validate_set_effects_json.py` — PASS, includes shield effect checks.
- `python3 scripts/audit_equipment_balance.py` — PASS, 368 entries including all shields.
- `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — BUILD SUCCESSFUL.

### Client-only

- Confirm vanilla shield recipe no longer crafts in survival and Dream Equipment shield recipes still work.

## 0.1.0 — 2026-07-03 — Custom shield base textures

### Added

- Added material-adapted shield base textures for all 56 Dream Equipment shields.
- Added `DreamEquipmentDataComponents` with synchronized/persistent `dream_equipment:shield_base_texture`.
- Added `ShieldSpecialRendererMixin` to select a custom shield base sprite for Dream Equipment shields while preserving vanilla shield geometry and special-renderer behavior.
- Added `scripts/generate_shield_textures.py`, generating 56 shield base textures from vanilla `shield_base_nopattern.png` plus family source material textures.
- Added audit image `docs/reports/ROUND52_CUSTOM_SHIELD_TEXTURE_AUDIT_20260703.png`.
- Added `docs/reference/ROUND52_CUSTOM_SHIELD_BASE_TEXTURES_20260703.md`.

### Validation

- `python3 scripts/generate_equipment_resources.py` — PASS, 1349 generated resources in sync.
- `python3 scripts/generate_wood_worn_textures.py` — PASS, 72 worn layer files regenerated.
- `python3 scripts/generate_shield_textures.py` — PASS, 56 shield base textures generated.
- `python3 scripts/validate_equipment_families_json.py` — PASS, 56 families / 368 items.
- `python3 scripts/validate_dream_equipment_assets.py` — PASS, includes shield texture/mixin/component checks.
- `python3 scripts/validate_set_effects_json.py` — PASS, includes shield effect checks.
- `python3 scripts/audit_equipment_balance.py` — PASS, 368 entries including all shields.
- `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — BUILD SUCCESSFUL.

### Client-only

- Confirm custom shield base textures render in normal/blocking poses and no shield atlas missing-texture errors appear.

## 0.1.0 — 2026-07-03 — Shield effects data-driven pass 2

### Added

- Added second batch of shield effects for obsidian, prismarine, amethyst, bone, coal, and quartz shields.
- `obsidian_shield`: applies Slowness while blocking and refunds durability loss against fire/explosions.
- `prismarine_shield`: refunds durability loss for successful blocks in water.
- `amethyst_shield`: blocks Warden sonic boom at shield durability cost.
- `bone_shield`: refunds durability loss when blocking undead-like attackers.
- `coal_shield`: refunds durability loss against fire damage.
- `quartz_shield`: refunds durability loss against projectiles.
- Added tooltip lines and validation for these new shield effects.
- Added `docs/reference/ROUND51_SHIELD_EFFECTS_DATA_DRIVEN_PASS2_20260703.md`.

### Validation

- `python3 scripts/generate_equipment_resources.py` — PASS, 1349 generated resources in sync.
- `python3 scripts/generate_wood_worn_textures.py` — PASS, 72 worn layer files regenerated.
- `python3 scripts/validate_equipment_families_json.py` — PASS, 56 families / 368 items.
- `python3 scripts/validate_dream_equipment_assets.py` — PASS, texture-backed item/material checks plus shield resources/effects.
- `python3 scripts/validate_set_effects_json.py` — PASS, including shield effect checks.
- `python3 scripts/audit_equipment_balance.py` — PASS, 368 entries including all shields.
- `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — BUILD SUCCESSFUL.

### Client-only

- Test obsidian/prismarine/amethyst/bone/coal/quartz shield effects and confirm first-pass effects still work.

## 0.1.0 — 2026-07-03 — Shield effects data-driven pass 1

### Added

- Added `shield_effects` to `set_effects.json` for data-driven shield effect values.
- Added `DreamEquipmentShieldEffectRules` and `DreamEquipmentShieldEffects`.
- Added first shield gameplay effects:
  - `cactus_shield`: retaliates on successful melee block.
  - `glass_shield`: can shatter after blocking high damage.
  - `redstone_shield`: emits a short redstone pulse on successful block.
  - `slime_shield`: bounces living attackers on successful block.
  - `paper_shield`: loses durability while blocking in water/rain.
- Added shield effect tooltip lines.
- Updated set-effect and asset validators for shield effects.
- Added `docs/reference/ROUND50_SHIELD_EFFECTS_DATA_DRIVEN_PASS1_20260703.md`.

### Validation

- `python3 scripts/generate_equipment_resources.py` — PASS, 1349 generated resources in sync.
- `python3 scripts/generate_wood_worn_textures.py` — PASS, 72 worn layer files regenerated.
- `python3 scripts/validate_equipment_families_json.py` — PASS, 56 families / 368 items.
- `python3 scripts/validate_dream_equipment_assets.py` — PASS, texture-backed item/material checks plus shield resources/effects.
- `python3 scripts/validate_set_effects_json.py` — PASS, including shield effect checks.
- `python3 scripts/audit_equipment_balance.py` — PASS, 368 entries including all shields.
- `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — BUILD SUCCESSFUL.

### Client-only

- Test cactus/glass/redstone/slime/paper shield effects and tooltip lines in live client.

## 0.1.0 — 2026-07-03 — Shield completion for all families

### Added

- Expanded shields from the 8-item prototype batch to all 56 current material families.
- Custom item count is now 368.
- Added JSON-owned shield durability values for every family.
- Generator now manages 1349 files and emits 56 shield item definitions, 56 shield base models, 56 shield blocking models, and 56 shield recipes.
- Improved generated shield model particle texture mapping for non-block ingredients such as emerald, lapis, redstone, quartz, amethyst shard, prismarine shard, bone, paper, armadillo scute, and turtle scute.
- Existing wood/log-like fuel logic now applies to shields as 6 material slots × material burn time.
- Added `docs/reference/ROUND49_SHIELD_COMPLETION_ALL_FAMILIES_20260703.md`.

### Validation

- `python3 scripts/generate_equipment_resources.py` — PASS, 1349 generated resources in sync.
- `python3 scripts/generate_wood_worn_textures.py` — PASS, 72 worn layer files regenerated.
- `python3 scripts/validate_equipment_families_json.py` — PASS, 56 families / 368 items.
- `python3 scripts/validate_dream_equipment_assets.py` — PASS, texture-backed item/material checks plus shield resources.
- `python3 scripts/validate_set_effects_json.py` — PASS, 24 passive entries / 4 brittle entries.
- `python3 scripts/audit_equipment_balance.py` — PASS, 368 entries including all shields.
- `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — BUILD SUCCESSFUL.

### Client-only

- Test representative shields from every material category for visibility, recipes, offhand/blocking behavior, durability, repair, fuel, and missing model/texture warnings.

## 0.1.0 — 2026-07-03 — Shield prototype batch

### Added

- Added first behavior-focused custom shield prototype batch: `oak_shield`, `cherry_shield`, `bamboo_shield`, `emerald_shield`, `redstone_shield`, `amethyst_shield`, `prismarine_shield`, and `obsidian_shield`.
- Added optional JSON-owned `shield` declarations with durability values in `equipment_families.json`.
- Registered shields as `ShieldItem` with vanilla-like `BLOCKS_ATTACKS`, offhand equippable-unswappable behavior, banner pattern data, repair tags, and shield break/block sounds.
- Extended resource generator for shield item definitions, base/blocking models, recipes, and lang keys.
- Wood/plank prototype shields with `fuel_burn_time_per_material` now register furnace fuel time as 6 material slots × material burn time.
- Updated validators and balance audit for shield prototype resources/durability.
- Added `docs/reference/ROUND48_SHIELD_PROTOTYPE_BATCH_20260703.md`.

### Validation

- `python3 scripts/generate_equipment_resources.py` — PASS, 1157 generated resources in sync.
- `python3 scripts/generate_wood_worn_textures.py` — PASS, 72 worn layer files regenerated.
- `python3 scripts/validate_equipment_families_json.py` — PASS, 56 families / 320 items.
- `python3 scripts/validate_dream_equipment_assets.py` — PASS, 312 texture-backed items / 56 materials plus shield resources.
- `python3 scripts/validate_set_effects_json.py` — PASS, 24 passive entries / 4 brittle entries.
- `python3 scripts/audit_equipment_balance.py` — PASS, 320 entries including shield prototypes.
- `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — BUILD SUCCESSFUL.

### Client-only

- Test prototype shields for creative-tab visibility, recipes, offhand/blocking behavior, durability loss, repair, fuel for wood shields, shield disable behavior, and vanilla special-renderer visual acceptability.

## 0.1.0 — 2026-07-03 — Shield feasibility audit

### Added

- Added `docs/reference/ROUND47_SHIELD_FEASIBILITY_AUDIT_20260703.md`.
- Audited vanilla 26.1.2 `ShieldItem`, shield item definition/model/recipe resources, `BlocksAttacks`, and `ShieldSpecialRenderer`.

### Findings

- Custom shields can likely reuse vanilla `ShieldItem` and component-driven blocking behavior.
- Vanilla shield behavior is driven by `DataComponents.BLOCKS_ATTACKS`, offhand equippable data, durability, repair tags, banner pattern data, and break sound.
- Vanilla shield rendering is special-renderer based and uses fixed shield base sprites plus banner pattern overlays, so material-specific shield base textures are not trivial without custom client rendering/mixins.
- Recommended next step is a small behavior-first shield prototype batch rather than adding shields for every material immediately.

### Validation

- `python3 scripts/generate_equipment_resources.py` — PASS, 1125 generated resources in sync.
- `python3 scripts/validate_equipment_families_json.py` — PASS, 56 families / 312 items.
- `python3 scripts/validate_dream_equipment_assets.py` — PASS, 312 items / 56 materials.
- `python3 scripts/validate_set_effects_json.py` — PASS, 24 passive entries / 4 brittle entries.
- `python3 scripts/audit_equipment_balance.py` — PASS.
- `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — BUILD SUCCESSFUL.

### Client-only

- No shield implementation was added in this pass. Client-only shield behavior checks are deferred to the future prototype batch.

## 0.1.0 — 2026-07-03 — Plank component mapping for all plank families

### Changed

- Applied the accepted cherry component-local plank worn-layer style to all plank armor families.
- `scripts/generate_wood_worn_textures.py` now sets `PIECE_AWARE_PLANK_FAMILIES = set(PLANK_TEXTURES.keys())`.
- All plank armor worn layers now map each connected armor UV component to the corresponding vanilla `*_planks` texture once, with a few large component-local plank joins/plate breaks.
- Log/stem/bamboo-block armor families remain on the vanilla-source baseline pending a separate log-specific art direction.
- Added audit image `docs/reports/ROUND46_PLANK_COMPONENT_MAPPING_AUDIT_20260703.png`.
- Added `docs/reference/ROUND46_PLANK_COMPONENT_MAPPING_ALL_FAMILIES_20260703.md`.

### Validation

- `python3 scripts/generate_wood_worn_textures.py` — PASS, 72 worn layer files regenerated.
- `python3 scripts/generate_equipment_resources.py` — PASS, 1125 generated resources in sync.
- `python3 scripts/validate_equipment_families_json.py` — PASS, 56 families / 312 items.
- `python3 scripts/validate_dream_equipment_assets.py` — PASS, 312 items / 56 materials.
- `python3 scripts/validate_set_effects_json.py` — PASS, 24 passive entries / 4 brittle entries.
- `python3 scripts/audit_equipment_balance.py` — PASS.
- `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — BUILD SUCCESSFUL.

### Client-only

- Check all plank armor families in game for larger plank-plate readability and no transparent-UV artifacts.

## 0.1.0 — 2026-07-03 — Cherry component-local plank test

### Changed

- Added a narrow component-local plank mapping test for `cherry` worn armor only.
- The generator now splits cherry armor UV opaque pixels into connected components and maps each component to the vanilla `cherry_planks` texture once, instead of densely tiling the texture across the whole equipment layer.
- Added only a few large component-local plank joins/plate breaks, avoiding the previous chaotic global stripe approach.
- Left other plank families on the vanilla-source baseline until cherry direction is accepted.
- Added audit image `docs/reports/ROUND45_CHERRY_PLANK_COMPONENT_SAMPLE_20260703.png`.
- Added `docs/reference/ROUND45_CHERRY_COMPONENT_LOCAL_PLANK_TEST_20260703.md`.

### Validation

- `python3 scripts/generate_wood_worn_textures.py` — PASS, 72 worn layer files regenerated.
- `python3 scripts/generate_equipment_resources.py` — PASS, 1125 generated resources in sync.
- `python3 scripts/validate_equipment_families_json.py` — PASS, 56 families / 312 items.
- `python3 scripts/validate_dream_equipment_assets.py` — PASS, 312 items / 56 materials.
- `python3 scripts/validate_set_effects_json.py` — PASS, 24 passive entries / 4 brittle entries.
- `python3 scripts/audit_equipment_balance.py` — PASS.
- `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — BUILD SUCCESSFUL.

### Client-only

- Recheck cherry armor before applying the component-local plank approach to all plank families.

## 0.1.0 — 2026-07-03 — Wood worn-layer vanilla source baseline

### Changed

- Reverted the over-designed synthetic board/bark worn-layer approach.
- Retuned `scripts/generate_wood_worn_textures.py` to reuse corresponding vanilla block textures directly inside the existing equipment UV/alpha masks.
- Plank armor now samples vanilla `*_planks` textures with only light armor-mask shading.
- Log/stem/bamboo-block armor now samples vanilla log/stem/bamboo-block textures with only light armor-mask shading.
- Removed artificial global board stripes, heavy generated joins, and synthetic bark bands from the generator.
- Regenerated 72 wood/log-like worn equipment layer files.
- Added audit image `docs/reports/ROUND44_WOOD_WORN_LAYER_VANILLA_SOURCE_AUDIT_20260703.png`.
- Added `docs/reference/ROUND44_WOOD_WORN_LAYER_VANILLA_SOURCE_BASELINE_20260703.md`.

### Validation

- `python3 scripts/generate_wood_worn_textures.py` — PASS, 72 worn layer files regenerated.
- `python3 scripts/generate_equipment_resources.py` — PASS, 1125 generated resources in sync.
- `python3 scripts/validate_equipment_families_json.py` — PASS, 56 families / 312 items.
- `python3 scripts/validate_dream_equipment_assets.py` — PASS, 312 items / 56 materials.
- `python3 scripts/validate_set_effects_json.py` — PASS, 24 passive entries / 4 brittle entries.
- `python3 scripts/audit_equipment_balance.py` — PASS.
- `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — BUILD SUCCESSFUL.

### Client-only

- Recheck wood/log-like worn armor as vanilla-source material fills before adding any optimization overlays.

## 0.1.0 — 2026-07-03 — Visible wood worn-layer contrast

### Changed

- Retuned `scripts/generate_wood_worn_textures.py` after client screenshot showed cherry plank armor still read as flat pink leather in game.
- Increased plank-armor visibility with stronger horizontal seams, staggered vertical joins, alternating board-row tint, and clearer clipped binding/shadow bands.
- Increased log/stem/bamboo-block armor visibility with stronger vertical bark/stem grain and darker bark channels.
- Preserved current MC 26.1 equipment-layer alpha/UV masks and changed only non-transparent interior pixels.
- Added audit image `docs/reports/ROUND43_WOOD_WORN_LAYER_VISIBLE_AUDIT_20260703.png`.
- Added `docs/reference/ROUND43_VISIBLE_WOOD_WORN_LAYER_CONTRAST_20260703.md`.

### Validation

- `python3 scripts/generate_wood_worn_textures.py` — PASS, 72 worn layer files regenerated.
- `python3 scripts/generate_equipment_resources.py` — PASS, 1125 generated resources in sync.
- `python3 scripts/validate_equipment_families_json.py` — PASS, 56 families / 312 items.
- `python3 scripts/validate_dream_equipment_assets.py` — PASS, 312 items / 56 materials.
- `python3 scripts/validate_set_effects_json.py` — PASS, 24 passive entries / 4 brittle entries.
- `python3 scripts/audit_equipment_balance.py` — PASS.
- `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — BUILD SUCCESSFUL.

### Client-only

- Recheck cherry plank armor and other wood/log-like worn armor in game; details should now be visible at player-render scale.

## 0.1.0 — 2026-07-03 — Wood/log worn layer internal repaint

### Changed

- Regenerated worn equipment textures for all plank armor and log/stem/bamboo-block armor families.
- Confirmed current MC 26.1 equipment texture spec before drawing: `humanoid` 64×32, `humanoid_leggings` 64×32, `humanoid_baby` 64×64.
- Preserved existing equipment-layer alpha/UV masks and replaced only non-transparent interior pixels.
- Plank armor interiors now sample vanilla plank textures and add clipped board seams/sparse joins/binding shadows.
- Log/stem/bamboo-block armor interiors now sample vanilla log/stem/block textures and add clipped vertical bark/stem grain, darker edges, and subtle exposed-material flecks.
- Added `scripts/generate_wood_worn_textures.py` for deterministic regeneration of these worn layers.
- Added asset-validator checks for current wood/log worn-layer dimensions and generator spec markers.
- Added audit image `docs/reports/ROUND42_WOOD_WORN_LAYER_FINAL_AUDIT_20260703.png`.
- Added `docs/reference/ROUND42_WOOD_LOG_WORN_LAYER_INTERNAL_REPAINT_20260703.md`.

### Validation

- `python3 scripts/generate_wood_worn_textures.py` — PASS, 72 worn layer files regenerated.
- `python3 scripts/generate_equipment_resources.py` — PASS, 1125 generated resources in sync.
- `python3 scripts/validate_equipment_families_json.py` — PASS, 56 families / 312 items.
- `python3 scripts/validate_dream_equipment_assets.py` — PASS, 312 items / 56 materials.
- `python3 scripts/validate_set_effects_json.py` — PASS, 24 passive entries / 4 brittle entries.
- `python3 scripts/audit_equipment_balance.py` — PASS.
- `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — BUILD SUCCESSFUL.

### Client-only

- Check plank armor and log/stem/bamboo-block armor worn rendering on adult and baby humanoid models.
- Confirm no black/floating bands appear and item icons remain unchanged.

## 0.1.0 — 2026-07-03 — Redstone wire evaluator mixin

### Fixed

- Added `RedstoneWireEvaluatorMixin` so vanilla redstone wire power recalculation directly sees Dream Equipment redstone pulses.
- This targets `RedstoneWireEvaluator#getBlockSignal`, the path used by vanilla wire evaluators when computing a dust line's `POWER` value.
- Registered the new mixin in `dream_equipment.mixins.json`.
- Added `docs/reference/ROUND41_REDSTONE_WIRE_EVALUATOR_MIXIN_20260703.md`.

### Validation

- `python3 scripts/generate_equipment_resources.py` — PASS, 1125 generated resources in sync.
- `python3 scripts/validate_equipment_families_json.py` — PASS, 56 families / 312 items.
- `python3 scripts/validate_dream_equipment_assets.py` — PASS, 312 items / 56 materials.
- `python3 scripts/validate_set_effects_json.py` — PASS, 24 passive entries / 4 brittle entries.
- `python3 scripts/audit_equipment_balance.py` — PASS.
- `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — BUILD SUCCESSFUL.

### Client-only

- Retest redstone dust lines beside the player with redstone boots/full set; adjacent dust should receive the pulse and line propagation should occur.

## 0.1.0 — 2026-07-03 — Redstone step pulse mechanic

### Changed

- Changed redstone equipment from a continuous virtual redstone-block source into a short-lived step/equip pulse mechanic.
- Redstone boots now emit a signal strength 7 pulse for 8 ticks when equipped, when signal state changes, or when the player steps into a new block position.
- Full redstone set now emits a signal strength 15 pulse for 12 ticks.
- Added JSON-owned `boots_pulse_ticks` and `full_set_pulse_ticks` under `redstone_signal` in `set_effects.json`.
- `DreamEquipmentRedstonePower` now tracks `ACTIVE_PULSES` and `LAST_PLAYER_SOURCE` instead of permanent active sources.
- Updated redstone tooltip localization to describe pulses rather than continuous block-like output.
- Added `docs/reference/ROUND40_REDSTONE_STEP_PULSE_MECHANIC_20260703.md`.

### Validation

- `python3 scripts/generate_equipment_resources.py --write` — PASS.
- `python3 scripts/generate_equipment_resources.py` — PASS, 1125 generated resources in sync.
- `python3 scripts/validate_equipment_families_json.py` — PASS, 56 families / 312 items.
- `python3 scripts/validate_dream_equipment_assets.py` — PASS, 312 items / 56 materials.
- `python3 scripts/validate_set_effects_json.py` — PASS, 24 passive entries / 4 brittle entries.
- `python3 scripts/audit_equipment_balance.py` — PASS.
- `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — BUILD SUCCESSFUL.

### Client-only

- Retest redstone boots/full set as short pulses: equip pulse, step pulse, expiry after removing boots, repeaters/dust/lamps seeing the pulse, and no stale signal after logout/dimension change/death.

## 0.1.0 — 2026-07-03 — Redstone virtual source rework

### Changed

- Reworked redstone equipment power from player-scan-on-query to a server-tick rebuilt virtual source registry.
- Redstone equipment now creates a virtual redstone-block source at the player's feet-space (`player.blockPosition()`), not the floor block below the player.
- Removed old per-player redstone notification bookkeeping from `DreamEquipmentSetEffects`; redstone update ownership moved to `DreamEquipmentRedstonePower`.
- Added `RedStoneWireBlockMixin` to include virtual redstone sources directly during redstone dust `getBlockSignal` recalculation.
- Changed source cleanup so stale redstone sources are removed whenever active source maps are rebuilt.
- Added broader neighbor notifications around added/removed/moved/strength-changed virtual sources.
- Added `docs/reference/ROUND39_REDSTONE_VIRTUAL_SOURCE_REWORK_20260703.md`.

### Validation

- `python3 scripts/generate_equipment_resources.py` — PASS, 1125 generated resources in sync.
- `python3 scripts/validate_equipment_families_json.py` — PASS, 56 families / 312 items.
- `python3 scripts/validate_dream_equipment_assets.py` — PASS, 312 items / 56 materials.
- `python3 scripts/validate_set_effects_json.py` — PASS, 24 passive entries / 4 brittle entries.
- `python3 scripts/audit_equipment_balance.py` — PASS.
- `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — BUILD SUCCESSFUL.

### Client-only

- Retest redstone dust/repeaters/lamps beside the player with redstone boots and full redstone set.
- Confirm dust turns off after moving away, removing boots, changing dimension, logout, or death.

## 0.1.0 — 2026-07-03 — Cherry texture fix and fuel values

### Fixed

- Regenerated cherry wood armor inventory icons from the accepted full oak armor silhouettes and vanilla 26.1.2 cherry planks palette.
- Fixed incomplete/fragmented cherry helmet, leggings, and boots item icons; all four cherry armor item textures are now 128×128 complete silhouettes.

### Added

- Added JSON-owned `fuel_burn_time_per_material` for coal armor and all wood/plank/log/stem/bamboo-block armor families.
- Added `DreamEquipmentFuelValues` using Fabric `FuelValueEvents.BUILD` to register furnace fuel values.
- Fuel time is computed as `base material burn time × armor recipe material count`: helmet 5, chestplate 8, leggings 7, boots 4.
- Wood/plank/log/stem/bamboo-block armor uses 300 ticks per material. Coal armor uses 1600 ticks per material.
- Added `docs/reference/ROUND38_CHERRY_TEXTURE_AND_FUEL_VALUES_20260703.md`.

### Validation

- `python3 scripts/generate_equipment_resources.py --write` — PASS.
- `python3 scripts/generate_equipment_resources.py` — PASS, 1125 generated resources in sync.
- `python3 scripts/validate_equipment_families_json.py` — PASS, 56 families / 312 items.
- `python3 scripts/validate_dream_equipment_assets.py` — PASS, 312 items / 56 materials.
- `python3 scripts/validate_set_effects_json.py` — PASS, 24 passive entries / 4 brittle entries.
- `python3 scripts/audit_equipment_balance.py` — PASS.
- `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — BUILD SUCCESSFUL.

### Client-only

- Recheck cherry armor inventory icons in game.
- Recheck furnace fuel behavior for coal armor and all plank/log/stem/bamboo-block armor.
- Confirm non-fuel material equipment did not become fuel unexpectedly.

## 0.1.0 — 2026-07-03 — Repair ingredient expansion

### Changed

- Added optional JSON-owned `repair_ingredients` arrays to selected equipment families.
- Expanded repair tags for materials whose recipes/mechanics imply more than one natural repair material.
- Log/stem/bamboo-block armor repair now uses vanilla item tags such as `#minecraft:oak_logs`, `#minecraft:bamboo_blocks`, `#minecraft:crimson_stems`, and `#minecraft:warped_stems`, allowing tagged stripped/wood/hyphae variants where vanilla includes them.
- Slime armor can now be repaired with slime balls as well as slime blocks.
- Bone equipment can now be repaired with bone meal as well as bones.
- Glass equipment can now be repaired with glass panes as well as glass blocks.
- Emerald, lapis, redstone, quartz, amethyst, and coal families now accept item/block-form repair ingredients where appropriate.
- Updated `scripts/generate_equipment_resources.py` so repair tags are generated from `repair_ingredients` when present, falling back to the original single `ingredient`.
- Updated `scripts/validate_equipment_families_json.py` to validate optional repair ingredient arrays and `#namespace:tag` syntax.
- Added `docs/reference/ROUND37_REPAIR_INGREDIENT_EXPANSION_20260703.md`.

### Validation

- `python3 scripts/generate_equipment_resources.py --write` — PASS.
- `python3 scripts/generate_equipment_resources.py` — PASS, 1125 generated resources in sync.
- `python3 scripts/validate_equipment_families_json.py` — PASS, 56 families / 312 items.
- `python3 scripts/validate_dream_equipment_assets.py` — PASS, 312 items / 56 materials.
- `python3 scripts/validate_set_effects_json.py` — PASS, 24 passive entries / 4 brittle entries.
- `python3 scripts/audit_equipment_balance.py` — PASS.
- `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — BUILD SUCCESSFUL.

### Client-only

- Live anvil repair should be rechecked for slime ball/block, bone/bone meal, glass pane, tagged log/stem/bamboo variants, and item/block-form gem/redstone repair ingredients.

## 0.1.0 — 2026-07-03 — Environment setup and current agent report

### Added

- Added `docs/reports/CURRENT_AGENT_BRIEF.md` with the current environment/setup/build/validation summary.
- Added `docs/reference/ROUND36_ENVIRONMENT_SETUP_AND_REPORT_BRIEF_20260703.md`.
- Added `docs/DOCUMENTATION_INDEX.md` for current workflow, report, JSON, and validator documentation entry points.

### Changed

- Updated `CURRENT_BASELINE.md` for the 2026-07-03 environment setup state and current output files.
- Updated `NEXT_TASK.md` with this turn's validation results, client-only checklist, and documentation-gap notes.
- Refreshed `release_output/dream-equipment-0.1.0.jar` and `release_output/dream-equipment-source-current-20260703.zip`.

### Notes

- Requested `scripts/generate_agent_brief.py --write` could not be run because that script is not present in this repository.
- Requested `docs/JSON_EXTENSION_SPEC_1_1_3.md` and `docs/EXTENDING_HERBCRAFT.md` are not present in this standalone Dream Equipment repository; this pass records the gap without inventing unrelated Herbcraft-specific content.
- No gameplay Java code or generated gameplay/resource content was changed.

### Validation

- `python3 scripts/generate_equipment_resources.py` — PASS, 1125 generated resources in sync.
- `python3 scripts/validate_equipment_families_json.py` — PASS, 56 families / 312 items.
- `python3 scripts/validate_dream_equipment_assets.py` — PASS, 312 items / 56 materials.
- `python3 scripts/validate_set_effects_json.py` — PASS, 24 passive entries / 4 brittle entries.
- `python3 scripts/audit_equipment_balance.py` — PASS.
- `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — BUILD SUCCESSFUL.

### Client-only

- Live client/world validation is still required for item visibility/localization, recipes, rendering, redstone signal behavior, enchanting refund, sonic-boom immunity, turtle helmet integration, brittle/decay mechanics, and tooltip durability values.

## 0.1.0 — 2026-07-02 — Durability and mining tier audit

### Changed

- Rebalanced clearly unreasonable tool durability and mining-tier values.
- Glass/quartz/calcite/bone/cactus/netherrack tools are now shorter-lived and/or lower tier.
- Amethyst and end stone tools are no longer diamond-tier progression bypasses.
- Granite/diorite/andesite/tuff/mossy/cobbled deepslate/basalt/smooth basalt/dripstone tools are tuned as stone-tier variants with different durability.
- Armor tooltip now displays actual max durability per piece instead of durability multiplier.
- Added `scripts/audit_equipment_balance.py`.
- Added `docs/reference/ROUND35_DURABILITY_AND_MINING_TIER_AUDIT_20260702.md`.

### Validation

- `python3 scripts/audit_equipment_balance.py` — PASS.
- `python3 scripts/validate_equipment_families_json.py` — PASS.
- `python3 scripts/validate_dream_equipment_assets.py` — PASS.
- `python3 scripts/validate_set_effects_json.py` — PASS.
- Gradle build — BUILD SUCCESSFUL.

## 0.1.0 — 2026-07-02 — Emerald armor recipe rebalance

### Changed

- Emerald armor recipes now use emerald blocks as the primary ingredient and emeralds as secondary ingredients.
- Full emerald armor set now costs 11 emerald blocks + 8 emeralds, or 107 emeralds total.
- Added `docs/reference/ROUND34_EMERALD_ARMOR_RECIPE_REBALANCE_20260702.md`.

### Validation

- `python3 scripts/generate_equipment_resources.py --write` — PASS.
- `python3 scripts/generate_equipment_resources.py` — PASS.
- `python3 scripts/validate_equipment_families_json.py` — PASS.
- `python3 scripts/validate_dream_equipment_assets.py` — PASS.
- `python3 scripts/validate_set_effects_json.py` — PASS.
- Gradle build — BUILD SUCCESSFUL.

## 0.1.0 — 2026-07-02 — Pickaxe silhouette and rock tool expansion

### Fixed

- Regenerated all custom pickaxe textures from the vanilla diamond pickaxe silhouette to remove subtle inventory-shape mismatch.

### Added

- Added additional rock tools where material logic supports them:
  - granite shovel/hoe
  - diorite shovel/hoe
  - andesite shovel/hoe
  - mossy cobblestone shovel
  - sandstone shovel
  - red sandstone shovel
  - tuff shovel
- Generated vanilla-template textures for the new shovels/hoes.
- Added `docs/reference/ROUND33_PICKAXE_SILHOUETTE_AND_ROCK_TOOL_EXPANSION_20260702.md`.

### Validation

- `python3 scripts/generate_equipment_resources.py` — PASS, 1125 files in sync.
- `python3 scripts/validate_equipment_families_json.py` — PASS, 56 families + 312 items.
- `python3 scripts/validate_dream_equipment_assets.py` — PASS, 312 items + 56 materials.
- `python3 scripts/validate_set_effects_json.py` — PASS.
- Gradle build — BUILD SUCCESSFUL.

## 0.1.0 — 2026-07-02 — Log icon fix and rock tools completion

### Fixed

- Regenerated all log/stem/bamboo-block armor inventory icons from the accepted emerald armor templates, fixing incomplete helmet/leggings/boots icons.
- Generated missing textures for newly added granite, diorite, andesite, basalt, smooth basalt, dripstone, and netherrack tools/weapons.
- Added `docs/reference/ROUND32_LOG_ICON_AND_ROCK_TOOL_COMPLETION_20260702.md`.

### Validation

- `python3 scripts/generate_equipment_resources.py` — PASS, 1095 files in sync.
- `python3 scripts/validate_equipment_families_json.py` — PASS, 56 families + 302 items.
- `python3 scripts/validate_dream_equipment_assets.py` — PASS, 302 items + 56 materials.
- `python3 scripts/validate_set_effects_json.py` — PASS.
- Gradle build — BUILD SUCCESSFUL.

## 0.1.0 — 2026-07-02 — Turtle helmet integration and log icon fix

### Fixed

- Removed custom `turtle_shell_helmet`; vanilla `minecraft:turtle_helmet` now counts as the turtle shell set helmet.
- Regenerated turtle shell chestplate/leggings/boots item and worn textures from vanilla turtle shell/scute references.
- Regenerated log/stem/bamboo-block armor inventory icons as cleaner vanilla leather-style reskins without broken/incomplete shapes.
- Added tooltip support for vanilla `minecraft:turtle_helmet` as part of the Dream Equipment turtle shell set.
- Added `docs/reference/ROUND31_TURTLE_HELMET_AND_LOG_ICON_FIX_20260702.md`.

### Validation

- `python3 scripts/generate_equipment_resources.py` — PASS, 1031 files in sync.
- `python3 scripts/validate_equipment_families_json.py` — PASS, 56 families + 283 items.
- `python3 scripts/validate_set_effects_json.py` — PASS.
- `python3 scripts/validate_dream_equipment_assets.py` — PASS, 283 items + 56 materials.
- Gradle build — BUILD SUCCESSFUL.

## 0.1.0 — 2026-07-02 — Amethyst sonic boom immunity

### Added

- Added `damage_immunities` support in `set_effects.json`.
- Full amethyst armor set now cancels `minecraft:sonic_boom` damage, making it immune to Warden sonic boom attacks.
- Added tooltip line for damage immunities.
- Added `docs/reference/ROUND30_AMETHYST_SONIC_BOOM_IMMUNITY_20260702.md`.

### Validation

- `python3 scripts/generate_equipment_resources.py --write` — PASS.
- `python3 scripts/generate_equipment_resources.py` — PASS.
- `python3 scripts/validate_equipment_families_json.py` — PASS.
- `python3 scripts/validate_dream_equipment_assets.py` — PASS.
- `python3 scripts/validate_set_effects_json.py` — PASS.
- Gradle build — BUILD SUCCESSFUL.

## 0.1.0 — 2026-07-02 — Lapis enchanting support

### Added

- Added `DreamEquipmentEnchantingSupport`.
- Added `EnchantmentMenuAccessor` and `EnchantmentMenuMixin`.
- Wearing any lapis armor piece now refunds vanilla enchanting-table lapis cost after a successful enchant, while damaging lapis armor durability.
- Added lapis armor tooltip line describing the enchanting refund/durability tradeoff.
- Added `docs/reference/ROUND29_LAPIS_ENCHANTING_SUPPORT_20260702.md`.

### Validation

- `python3 scripts/generate_equipment_resources.py --write` — PASS.
- `python3 scripts/generate_equipment_resources.py` — PASS.
- `python3 scripts/validate_equipment_families_json.py` — PASS.
- `python3 scripts/validate_set_effects_json.py` — PASS.
- `python3 scripts/validate_dream_equipment_assets.py` — PASS.
- Gradle build — BUILD SUCCESSFUL.

## 0.1.0 — 2026-07-02 — Bone shatter, chainmail projectile protection, turtle shell set, log armor

### Added

- Added turtle shell full armor set with Resistance II, Slowness I, and Water Breathing.
- Added 12 log/stem/bamboo-block armor families: oak_log, spruce_log, birch_log, jungle_log, acacia_log, dark_oak_log, mangrove_log, cherry_log, pale_oak_log, bamboo_block, crimson_stem, warped_stem.
- Added vanilla chainmail full-set projectile mitigation approximation.
- Added `docs/reference/ROUND28_BONE_CHAIN_TURTLE_LOG_ARMOR_20260702.md`.

### Changed

- Removed old generic `wooden_*` armor family and resources. Plank variants remain.
- Bone weapons can shatter and return bone meal.
- Bone armor shatter returns bone meal rather than bone.
- Obsidian weapon shatter still returns no material.

### Validation

- `python3 scripts/generate_equipment_resources.py` — PASS, 1034 files in sync.
- `python3 scripts/validate_equipment_families_json.py` — PASS, 56 families + 284 items.
- `python3 scripts/validate_set_effects_json.py` — PASS.
- `python3 scripts/validate_dream_equipment_assets.py` — PASS, 284 items + 56 materials.
- Gradle build — BUILD SUCCESSFUL.

## 0.1.0 — 2026-07-02 — User-suggested mechanics implementation

### Changed

- Armadillo shell boots now grant Speed III on sand, red sand, gravel, suspicious sand, and suspicious gravel.
- Prismarine pickaxe now grants Haste II while held underwater.
- Prismarine pickaxe recipe now requires Heart of the Sea.
- Prismarine armor recipes now include nautilus shells.
- Redstone gear recipes now mix redstone blocks and redstone dust.
- Paper armor wet/rain durability loss increased to 1 durability every 10 ticks.
- Tooltips now include armadillo terrain speed and held item effects.
- Added `docs/reference/ROUND27_USER_SUGGESTED_MECHANICS_IMPLEMENTATION_20260702.md`.

### Validation

- `python3 scripts/generate_equipment_resources.py` — PASS.
- `python3 scripts/validate_equipment_families_json.py` — PASS.
- `python3 scripts/validate_set_effects_json.py` — PASS.
- `python3 scripts/validate_dream_equipment_assets.py` — PASS.
- Gradle build — BUILD SUCCESSFUL.

## 0.1.0 — 2026-07-02 — Narrow brittle rules and density rebalance

### Changed

- Tooltips now separate armor-set brittle rules from tool/weapon brittle rules, so calcite tools/weapons no longer present armor shatter logic.
- Obsidian weapon shatter no longer returns obsidian material.
- Retuned `stone_armor_physics` by material density/fragility, including mossy cobblestone and netherrack.
- Added validation for `wet_repair`, `brittle_weapons`, and `stone_armor_physics`.
- Added `docs/reference/ROUND26_NARROW_BRITTLE_AND_DENSITY_REBALANCE_20260702.md`.

### Validation

- `python3 scripts/generate_equipment_resources.py --write` — PASS.
- `python3 scripts/generate_equipment_resources.py` — PASS.
- `python3 scripts/validate_equipment_families_json.py` — PASS.
- `python3 scripts/validate_set_effects_json.py` — PASS.
- `python3 scripts/validate_dream_equipment_assets.py` — PASS.
- Gradle build — BUILD SUCCESSFUL.

## 0.1.0 — 2026-07-02 — Physics rebalance and redstone retry

### Changed

- Retried redstone boot detection with best-neighbor and neighbor-signal query support plus old/new position updates.
- Rebalanced slime armor to slime-block cost, higher durability, and adjusted slime-ball returns.
- Changed wood/plank icons to muted vanilla leather-style reskins; glass visuals now use the supplied glass pane reference without unsafe semi-transparent armor alpha.
- Removed blackstone tools/weapons and added curated tools/weapons for sensible materials.
- Added granite/diorite/andesite/basalt/smooth basalt/dripstone/netherrack armor variants.
- Added JSON-driven wet repair, brittle weapon, and stone armor physics rules.
- Obsidian weapons now have 120 durability, diamond-like damage, and 5% break chance on hit.
- Added `docs/reference/ROUND25_PHYSICS_REBALANCE_AND_REDSTONE_RETRY_20260702.md`.

### Validation

- `python3 scripts/validate_equipment_families_json.py` — PASS, 44 families + 236 items.
- `python3 scripts/validate_set_effects_json.py` — PASS.
- `python3 scripts/validate_dream_equipment_assets.py` — PASS, 236 items + 44 materials.
- Gradle build — BUILD SUCCESSFUL.

## 0.1.0 — 2026-07-02 — A+B+C+D material fix batch

### Changed

- Wood/plank armor inventory icons changed to muted vanilla leather-armor reskins without emerald-style highlights.
- Glass armor item and worn textures regenerated from the supplied glass pane reference.
- Redstone signal support expanded through best-neighbor and neighbor-signal query paths.
- Slime armor rebalanced to use slime blocks with higher durability and partial slime-ball returns.
- Blackstone tools/weapons removed because vanilla already supports blackstone stone-tool recipes.
- Added curated weapons/tools for cactus, bone, mossy cobblestone, cobbled deepslate, sandstone, red sandstone, end stone, tuff, and calcite.
- Added granite, diorite, andesite, basalt, smooth basalt, dripstone block, and netherrack armor families.
- Further pruned/rebalanced arbitrary strong set buffs.
- Added `docs/reference/ROUND24_ABCD_MATERIAL_FIXES_20260702.md`.

### Validation

- `python3 scripts/generate_equipment_resources.py` — PASS, 866 files in sync.
- `python3 scripts/validate_equipment_families_json.py` — PASS, 44 families + 236 items.
- `python3 scripts/validate_set_effects_json.py` — PASS, 21 passive effects + 4 brittle entries.
- `python3 scripts/validate_dream_equipment_assets.py` — PASS, 236 items + 44 materials.
- `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — BUILD SUCCESSFUL.

## 0.1.0 — 2026-07-02 — Redstone/slime/icon/tools/effect rebalance

### Changed

- Expanded redstone signal handling with best-neighbor/neighbor-signal paths so redstone dust can detect redstone boots/full set.
- Rebalanced slime armor: ingredient is now slime blocks, durability multiplier is 50, and slime-ball return values are adjusted.
- Regenerated wooden/plank/stone/cobblestone inventory icons from emerald armor templates with material-specific palettes.
- Added curated tools/weapons for mossy cobblestone, cobbled deepslate, blackstone, sandstone, red sandstone, end stone, tuff, calcite, bone, and cactus.
- Rebalanced placeholder effects: removed redstone speed, coal fire resistance, calcite night vision; mossy regeneration is wet-only; sandstone speed is dry-only.
- Added `docs/reference/ROUND23_REDSTONE_SLIME_ICON_TOOLS_EFFECT_REBALANCE_20260702.md`.

### Validation

- `python3 scripts/generate_equipment_resources.py` — PASS, 781 files in sync.
- `python3 scripts/validate_equipment_families_json.py` — PASS, 37 families + 212 items.
- `python3 scripts/validate_set_effects_json.py` — PASS, 25 passive effects + 4 brittle entries.
- `python3 scripts/validate_dream_equipment_assets.py` — PASS, 212 items + 37 materials.
- `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — BUILD SUCCESSFUL.

## 0.1.0 — 2026-07-02 — Redstone dust fix attempt, slime rebalance, wood/stone icon fix

### Changed

- Expanded redstone signal mixin coverage to include `getBestNeighborSignal` and `hasNeighborSignal`, so adjacent redstone dust can see redstone-boot source blocks.
- Redstone notification now tracks old/new player source positions to help dust turn off after movement/removal.
- Slime armor ingredient changed from slime balls to slime blocks; durability multiplier increased to 50; slime-ball return values increased modestly.
- Regenerated wooden/plank/stone/cobblestone inventory icons from the accepted emerald armor templates with material-specific palettes/patterns instead of raw noisy block fills.
- Added `docs/reference/ROUND22_REDSTONE_SLIME_AND_ICON_FIX_20260702.md`.

### Validation

- `python3 scripts/generate_equipment_resources.py` — PASS.
- `python3 scripts/validate_equipment_families_json.py` — PASS.
- `python3 scripts/validate_set_effects_json.py` — PASS.
- `python3 scripts/validate_dream_equipment_assets.py` — PASS.
- `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — BUILD SUCCESSFUL.

## 0.1.0 — 2026-07-02 — Redstone signal + localized data-driven tooltips

### Added

- Added `redstone_signal` section to `set_effects.json`.
- Added `DreamEquipmentRedstonePower`, `SignalGetterMixin`, and `dream_equipment.mixins.json`.
- Redstone boots now make the block below the player output signal 7; full redstone set outputs signal 15.
- Added neighbor updates while redstone signal is active so nearby components can refresh.
- Added translatable tooltip templates and material translation keys generated from `equipment_families.json`.
- Refactored `DreamEquipmentTooltips` to use `Component.translatable(...)` templates instead of hardcoded Chinese sentence literals.
- Added `docs/reference/ROUND20_REDSTONE_SIGNAL_AND_LOCALIZED_TOOLTIPS_20260702.md`.

### Validation

- `python3 scripts/generate_equipment_resources.py` — PASS.
- `python3 scripts/validate_equipment_families_json.py` — PASS.
- `python3 scripts/validate_dream_equipment_assets.py` — PASS.
- `python3 scripts/validate_set_effects_json.py` — PASS.
- `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — BUILD SUCCESSFUL.

### Client-only

- Redstone power mixin behavior must be tested in a live world with dust/repeaters.

## 0.1.0 — 2026-07-02 — Data-driven tooltips

### Added

- Added client entrypoint `com.dreamequipment.client.DreamEquipmentClient`.
- Added `DreamEquipmentTooltips` using Fabric `ItemTooltipCallback`.
- Tooltips now read from `equipment_families.json` and `set_effects.json` to display material stats, tool stats, armor stats, set effects, drawbacks, brittle/shatter rules, slime behavior, cactus retaliation, and wet weaknesses.
- Added `docs/reference/ROUND19_DATA_DRIVEN_TOOLTIPS_20260702.md`.

### Validation

- `python3 scripts/generate_equipment_resources.py` — PASS, no drift.
- `python3 scripts/validate_equipment_families_json.py` — PASS.
- `python3 scripts/validate_dream_equipment_assets.py` — PASS.
- `python3 scripts/validate_set_effects_json.py` — PASS.
- `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — BUILD SUCCESSFUL.

## 0.1.0 — 2026-07-02 — Equipment resource generator and drift check

### Added

- Added `scripts/generate_equipment_resources.py`.
- Generator reads `equipment_families.json` and writes/checks item definitions, item models, equipment definitions, recipes, repair tags, tool tags, aggregate tags, and lang keys.
- Added check mode: running without `--write` verifies generated resources are in sync.
- Added armor lang overrides in `equipment_families.json`, currently preserving `犰狳壳鞋`.
- Added `docs/reference/ROUND18_RESOURCE_GENERATOR_AND_DRIFT_CHECK_20260702.md`.

### Validation

- `python3 scripts/generate_equipment_resources.py --write` — PASS, 687 files managed.
- `python3 scripts/generate_equipment_resources.py` — PASS, no drift.
- `python3 scripts/validate_equipment_families_json.py` — PASS, 37 families + 184 items.
- `python3 scripts/validate_dream_equipment_assets.py` — PASS, 184 items + 37 materials.
- `python3 scripts/validate_set_effects_json.py` — PASS.
- `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — BUILD SUCCESSFUL.

## 0.1.0 — 2026-07-02 — Data-driven equipment family registration

### Added

- Added `data/dream_equipment/equipment_families.json` with 37 equipment family declarations and 184 expected items.
- Added `DreamEquipmentFamilyRules` startup loader.
- Added `scripts/validate_equipment_families_json.py`.
- Added `docs/reference/ROUND17_EQUIPMENT_FAMILIES_DATA_DRIVEN_REGISTRATION_20260702.md`.

### Changed

- Rewrote `DreamEquipmentItems` to dynamically register armor/tools from `equipment_families.json` instead of hardcoded Java material tables.
- Java now owns registration mechanics; JSON owns material families and registration-time material values.
- Existing item ids remain stable.

### Validation

- `python3 scripts/validate_equipment_families_json.py` — PASS, 37 families + 184 items.
- `python3 scripts/validate_dream_equipment_assets.py` — PASS, 184 items + 37 materials.
- `python3 scripts/validate_set_effects_json.py` — PASS.
- `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — BUILD SUCCESSFUL.

## 0.1.0 — 2026-07-02 — Set effects data-driven decoupling

### Added

- Added `data/dream_equipment/set_effects.json` to own set-effect values and rules.
- Added `DreamEquipmentSetEffectRules` loader with fallback defaults.
- Added `scripts/validate_set_effects_json.py`.
- Added `docs/reference/ROUND16_SET_EFFECTS_DATA_DRIVEN_DECOUPLING_20260702.md`.

### Changed

- `DreamEquipmentSetEffects` now reads passive effects, cactus retaliation, slime rules, wet durability, and brittle shatter rules from JSON instead of hardcoding most values.

### Validation

- `python3 scripts/validate_dream_equipment_assets.py` — PASS, 184 items + 37 materials.
- `python3 scripts/validate_set_effects_json.py` — PASS, 28 passive effects + 4 brittle entries.
- `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — BUILD SUCCESSFUL.

## 0.1.0 — 2026-07-02 — Physics-style armor mechanics pass

### Added

- Emerald full set now also grants Hero of the Village as a vanilla-style trade discount implementation.
- Slime full set now loses durability every game tick while worn, returns small slime-ball amounts when pieces break from this decay, and has a 10% chance to cancel incoming damage.
- Slime boots now cancel fall damage from falls of 12 blocks or less and bounce the player upward.
- Glass/calcite/quartz/amethyst full sets now have material-appropriate heavy-hit shatter chances.
- Added `docs/reference/ROUND15_PHYSICS_STYLE_MECHANICS_PASS_20260702.md`.

### Notes

- Redstone boots as true redstone signal output are not faked. They require a dedicated redstone-power/mixin implementation and are documented for the next mechanic pass.

### Validation

- `python3 scripts/validate_dream_equipment_assets.py` — PASS, 184 items + 37 materials.
- `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — BUILD SUCCESSFUL.

## 0.1.0 — 2026-07-02 — Curated stone variant armor

### Added

- Added mossy cobblestone, cobbled deepslate, blackstone, sandstone, red sandstone, end stone, tuff, and calcite armor families.
- Added 32 items, recipes, item definitions, models, item textures, equipment definitions, worn layer textures, repair tags, and lang keys.
- Added first-pass set effects for the curated stone variants.
- Added `docs/reference/ROUND14_CURATED_STONE_VARIANT_ARMOR_20260702.md`.

### Validation

- `python3 scripts/validate_dream_equipment_assets.py` — PASS, 184 items + 37 materials.
- `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — BUILD SUCCESSFUL.

## 0.1.0 — 2026-07-02 — Wood/stone/cobblestone render fix

### Fixed

- Fixed wooden/plank armor worn-layer black horizontal bands by removing the non-alpha-clipped seam drawing and regenerating layers from vanilla 26.1 equipment templates.
- Regenerated generic wooden, all plank-variant, stone, and cobblestone item icons from vanilla leather/iron armor item templates with material block texture fills.
- Regenerated wood/plank worn layers from vanilla leather equipment UV templates and stone/cobblestone layers from vanilla iron equipment UV templates.
- Added `docs/reference/ROUND13_WOOD_STONE_RENDER_FIX_20260702.md`.

### Validation

- `python3 scripts/validate_dream_equipment_assets.py` — PASS, 152 items + 29 materials.
- `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — BUILD SUCCESSFUL.

## 0.1.0 — 2026-07-02 — Wood variant armor sets

### Added

- Added 12 plank-based armor families while keeping the existing generic `wooden_*` set.
- New variants: oak, spruce, birch, jungle, acacia, dark oak, mangrove, cherry, pale oak, bamboo, crimson, warped.
- Added 48 new armor items, recipes, item definitions, item models, item textures, equipment definitions, worn layer textures, repair tags, and lang keys.
- Generated item icons and equipment layers from actual vanilla MC 26.1.2 plank block textures.
- Added `docs/reference/ROUND12_WOOD_VARIANT_ARMOR_IMPLEMENTATION_20260702.md`.

### Validation

- `python3 scripts/validate_dream_equipment_assets.py` — PASS, 152 items + 29 materials.
- `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — BUILD SUCCESSFUL.

## 0.1.0 — 2026-07-02 — Wood/stone diversity audit and next plan

### Added

- Added `docs/reference/ROUND11_WOOD_STONE_VARIANT_AUDIT_AND_PLAN_20260702.md`.

### Findings

- Current wood/stone/cobblestone-style equipment is only 12 items: 4 generic wooden, 4 stone, 4 cobblestone.
- Vanilla 26.1.2 has 12 plank variants, meaning a full per-plank armor pass would add 48 wood-variant armor items.
- Vanilla 26.1.2 has at least 19 stone-like material items; excluding existing stone/cobblestone/obsidian leaves up to 16 additional stone-like armor families.
- Current render icons are wrong because they are generic/generated pattern fills, not true raw-material/block-texture-derived visuals.
- Existing worn layers are UV-correct after prior pass, but visually too generic because they are recolored diamond layers rather than material-specific overlays.
- Confirmed cobblestone Chinese should remain `圆石`, not `原石`.

### Validation

- Investigation/docs-only pass; no gameplay/resource implementation changed this turn. Source zip should be refreshed to include the new report.

## 0.1.0 — 2026-07-02 — Handheld/class/name/outline fix

### Fixed

- Changed all non-spear tool/weapon item models from `minecraft:item/generated` to `minecraft:item/handheld`, matching vanilla 26.1.2 tool model convention.
- Registered axes, shovels, and hoes using `AxeItem`, `ShovelItem`, and `HoeItem` instead of plain `Item`, restoring vanilla-like tool classes/actions.
- Fixed cobblestone zh_cn names from `原石...` to `圆石...`.
- Improved tool recolor masking so dark emerald edge pixels are recolored for non-emerald materials while true black outlines and brown handles are preserved.
- Added `docs/reference/ROUND10_HANDHELD_CLASS_NAME_AND_OUTLINE_FIX_20260702.md`.

### Validation

- `python3 scripts/validate_dream_equipment_assets.py` — PASS, including handheld parent, class-source, and cobblestone-name checks.
- `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — BUILD SUCCESSFUL.

## 0.1.0 — 2026-07-02 — Animation tag aliases + tool outline recolor fix

### Fixed

- Added broader common/Fabric/Forge item tag aliases for swords, axes, pickaxes, shovels, hoes, spears, aggregate tools, weapons, and melee weapons so first-person animation/combat mods that do not check only `minecraft:*` tags can recognize items.
- Improved material recolor logic for uploaded tool templates so non-emerald tools no longer keep green edge/outline pixels.
- Added `docs/reference/ROUND8_ANIMATION_TAG_AND_TOOL_OUTLINE_FIX_20260702.md`.

### Validation

- `python3 scripts/validate_dream_equipment_assets.py` — PASS, including expanded tag checks.
- `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — BUILD SUCCESSFUL.

## 0.1.0 — 2026-07-02 — Texture/tag/equipment-standard correction

### Fixed

- Recolored the uploaded emerald tool templates for all relevant material tools/weapons instead of only emerald.
- Regenerated worn armor equipment layer textures from vanilla 26.1.2 equipment UV templates (`humanoid`, `humanoid_baby`, `humanoid_leggings`, 64×32), fixing the incorrect custom layer layout.
- Corrected custom spear resources to match vanilla 26.1: GUI/render icon and in-hand texture are separate via `display_context` item definitions.
- Added vanilla item tags under `data/minecraft/tags/item/` for swords, axes, pickaxes, shovels, hoes, and spears so animation/combat mods can identify the items.
- Added `docs/reference/ROUND7_TEXTURE_TAG_AND_EQUIPMENT_STANDARD_FIX_20260702.md`.

### Validation

- `python3 scripts/validate_dream_equipment_assets.py` — PASS, including spear split and vanilla tag checks.
- `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — BUILD SUCCESSFUL.

## 0.1.0 — 2026-07-02 — Tool scope correction + emerald templates + spears

### Changed

- Replaced emerald sword/axe/pickaxe/shovel/hoe item textures with the user-provided templates.
- Added spear items for emerald, lapis, redstone, quartz, amethyst, prismarine, glass, and obsidian, using recolored spear art based on the supplied diamond spear image.
- Changed quartz from full utility toolset to weapon-only: sword, axe, spear. Removed quartz pickaxe/shovel/hoe resources and recipes.
- Added glass sword/axe/spear and obsidian sword/axe/spear as weapon-only material expansions.
- Added `docs/reference/ROUND6_TOOL_SCOPE_AND_USER_TEXTURES_20260702.md`.

### Validation

- `python3 scripts/validate_dream_equipment_assets.py` — PASS, 104 items + 17 materials.
- `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — BUILD SUCCESSFUL.

## 0.1.0 — 2026-07-02 — Expansion + deeper set mechanics

### Added

- Added lapis tools and armor.
- Added redstone tools and armor.
- Added quartz tools and armor.
- Added amethyst tools and armor.
- Added prismarine tools and armor.
- Added slime armor.
- Added coal armor.
- Expanded total item count to 95 and armor/equipment material count to 17.
- Added generated item textures, models, item definitions, recipes, equipment definitions, armor layer textures, repair tags, and lang keys for all new items.
- Added set effects for lapis, redstone, quartz, amethyst, prismarine, slime, and coal.
- Deepened existing mechanics: cactus retaliation is per-piece, paper full set wears in wet/rain conditions, slime full set has fall/mobility utility.
- Added `docs/reference/ROUND5_EXPANSION_AND_DEEPER_MECHANICS_20260702.md`.

### Validation

- `python3 scripts/validate_dream_equipment_assets.py` — PASS, 95 items + 17 materials.
- `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — BUILD SUCCESSFUL.

### Client-only

- All new items/effects require live testing for visuals, recipes, effect behavior, and balance.

## 0.1.0 — 2026-07-02 — First set effects

### Added

- Added `DreamEquipmentSetEffects` and registered it from the mod initializer.
- Emerald full set now grants Luck.
- Cactus full set now retaliates with low thorns-style damage when hit by a living attacker.
- Armadillo shell boots now partially offset fall damage by healing back 35% after a fall.
- Bone full set now grants Night Vision.
- Paper full set now grants Slow Falling while dry, but Weakness + Slowness in water/rain.
- Glass full set can shatter one random piece when the wearer takes a heavy hit.
- Obsidian full set grants Fire Resistance + Resistance, with Slowness as weight penalty.
- Added `docs/reference/ROUND4_SET_EFFECTS_REPORT_20260702.md`.

### Validation

- `python3 scripts/validate_dream_equipment_assets.py` — PASS, 42 items + 10 materials.
- `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — BUILD SUCCESSFUL.
- Jar contains `DreamEquipmentSetEffects.class`.

### Client-only

- All set effects require live client/world testing for feel, balance, and edge cases.

## 0.1.0 — 2026-07-02 — Reasonable material equipment expansion

### Added

- Added cactus armor set: helmet, chestplate, leggings, boots.
- Added armadillo shell boots / 犰狳壳鞋.
- Added bone armor set: helmet, chestplate, leggings, boots.
- Added paper armor set: helmet, chestplate, leggings, boots.
- Added glass armor set: helmet, chestplate, leggings, boots.
- Added obsidian armor set: helmet, chestplate, leggings, boots.
- Added item definitions, item models, generated material-style item textures, recipes, equipment definitions, armor layer textures, repair tags, and lang keys for the new items.
- Updated `scripts/validate_dream_equipment_assets.py` to cover 42 items / 10 materials.
- Added `docs/reference/ROUND3_REASONABLE_EQUIPMENT_EXPANSION_20260702.md`.

### Validation

- `python3 scripts/validate_dream_equipment_assets.py` — PASS, 42 items + 10 materials.
- `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — BUILD SUCCESSFUL.
- Jar spot-check confirmed cactus, armadillo shell, and obsidian resources are packed.

### Client-only

- Startup, creative tab visibility, crafting, armor rendering, and stat/balance feel still require live client testing.

## 0.1.0 — 2026-07-02 — User emerald armor templates + block-style material icons

### Changed

- Replaced emerald armor item textures with the user-provided templates:
  - `641123.png` → `emerald_helmet.png`
  - `641158.png` → `emerald_chestplate.png`
  - `641193.png` → `emerald_leggings.png`
  - `641228.png` → `emerald_boots.png`
- Regenerated wooden, stone, and cobblestone armor item icons so they preserve armor silhouettes but use block/material-style fills.
- Added `docs/reference/ROUND2_TEXTURE_REPLACEMENT_REPORT_20260702.md`.

### Validation

- `python3 scripts/validate_dream_equipment_assets.py` — PASS.
- `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — BUILD SUCCESSFUL.

## 0.1.0 — 2026-07-02 — First equipment batch: emerald, wood, stone, cobblestone

### Added

- Added `DreamEquipmentItems` item registration.
- Added emerald tools: sword, pickaxe, axe, shovel, hoe.
- Added emerald armor: helmet, chestplate, leggings, boots.
- Added wooden armor: helmet, chestplate, leggings, boots.
- Added stone armor: helmet, chestplate, leggings, boots.
- Added cobblestone armor: helmet, chestplate, leggings, boots.
- Added item definitions, item models, generated original item textures, recipes, equipment definitions, armor layer textures, repair tags, and zh_cn/en_us language keys.
- Added `scripts/validate_dream_equipment_assets.py`.
- Added `docs/reference/ROUND2_EQUIPMENT_IMPLEMENTATION_REPORT_20260702.md`.

### Validation

- `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks` — BUILD SUCCESSFUL.
- `python3 scripts/validate_dream_equipment_assets.py` — PASS, 21 items + 4 materials.
- Jar spot-check confirmed key class/resources are packed.

### Client-only

- Startup, creative tab visibility, crafting, armor rendering, and stat/balance feel still require live client testing.

## 0.1.0 — 2026-07-02 — Standalone project scaffold

### Added

- Created standalone Fabric mod project `dream-equipment` / `dream_equipment` outside the reference `yansheng-source` repository.
- Added Gradle/Loom setup for MC 26.1.2, Fabric Loader 0.19.3, Fabric API 0.152.1+26.1.2, and Java 25.
- Added mod entrypoint, fabric.mod.json, icon, zh_cn/en_us lang files, and workflow docs.

### Notes

- No custom equipment has been implemented yet. This is the clean base for later rounds.

## 0.1.0 — 2026-07-02 — Vanilla+ reference recorded

### Added

- Added `docs/reference/VANILLA_PLUS_REFERENCE_NOTES_20260702.md` after the user supplied the Vanilla+ / VKL+ Modrinth link as a texture/style reference.

### Notes

- Vanilla+ is treated as visual/design reference only. Modrinth reports it as All Rights Reserved, so Dream Equipment textures should be original redraws unless explicit permission is provided.
