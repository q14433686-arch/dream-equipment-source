# Documentation Index

Last updated: 2026-07-06 (Round 57)

## Root workflow/status documents

- `AGENT_BRIEF.md` — repository-specific onboarding rules and current priority boundaries.
- `CURRENT_BASELINE.md` — current project baseline, target environment, implemented content, and latest validation/output status.
- `NEXT_TASK.md` — chronological working notes, client-test checklist, and recommended next actions.
- `CHANGELOG.md` — release-style change history and validation notes.
- `README.md` — user-facing project overview and build/environment notes.

## Generated/current reports

- `docs/reports/CURRENT_AGENT_BRIEF.md` — current agent-readable report generated/maintained from the latest baseline/task/changelog/build-validation state. Updated Round 56 (2026-07-06).

## Reference reports

Reference reports are stored in `docs/reference/` and record each implementation/audit pass. The latest report is:

- `docs/reference/ROUND55_VANILLA_MATERIAL_SHIELDS_20260703.md` — copper/golden/diamond/netherite shield-only families.

Recent previous reports:

- `docs/reference/ROUND54_PROJECT_COVER_ART_20260703.md` — selected project cover art added to docs/resources and README.
- `docs/reference/ROUND53_DISABLE_VANILLA_SHIELD_RECIPE_20260703.md` — vanilla shield recipe override to avoid conflicts with Dream Equipment shield recipes.
- `docs/reference/ROUND52_CUSTOM_SHIELD_BASE_TEXTURES_20260703.md` — material-adapted custom shield base textures and shield renderer mixin.
- `docs/reference/ROUND48_SHIELD_PROTOTYPE_BATCH_20260703.md` — first behavior-focused custom shield prototype batch.
- `docs/reference/ROUND47_SHIELD_FEASIBILITY_AUDIT_20260703.md` — shield item/API/resource feasibility audit and prototype recommendation.
- `docs/reference/ROUND46_PLANK_COMPONENT_MAPPING_ALL_FAMILIES_20260703.md` — accepted component-local plank mapping applied to all plank armor worn layers.

- `docs/reference/ROUND45_CHERRY_COMPONENT_LOCAL_PLANK_TEST_20260703.md` — cherry-only component-local plank mapping test for worn equipment layers.
- `docs/reference/ROUND44_WOOD_WORN_LAYER_VANILLA_SOURCE_BASELINE_20260703.md` — vanilla-source material fill baseline for wood/log worn equipment layers.

- `docs/reference/ROUND43_VISIBLE_WOOD_WORN_LAYER_CONTRAST_20260703.md` — stronger visible board/bark contrast attempt for wood/log worn equipment layers.
- `docs/reference/ROUND42_WOOD_LOG_WORN_LAYER_INTERNAL_REPAINT_20260703.md` — current-spec wood/log worn equipment layer internal repaint.

- `docs/reference/ROUND41_REDSTONE_WIRE_EVALUATOR_MIXIN_20260703.md` — redstone wire evaluator hook for dust-line pulse propagation.
- `docs/reference/ROUND40_REDSTONE_STEP_PULSE_MECHANIC_20260703.md` — redstone equipment changed from continuous virtual source to JSON-tuned step/equip pulse mechanic.

- `docs/reference/ROUND39_REDSTONE_VIRTUAL_SOURCE_REWORK_20260703.md` — redstone equipment virtual-source registry and dust recalculation rework.
- `docs/reference/ROUND38_CHERRY_TEXTURE_AND_FUEL_VALUES_20260703.md` — cherry armor item icon fix plus JSON-driven furnace fuel values for coal and wood/log-like armor.
- `docs/reference/ROUND37_REPAIR_INGREDIENT_EXPANSION_20260703.md` — JSON-owned multi-material repair ingredients and broader generated repair tags.
- `docs/reference/ROUND36_ENVIRONMENT_SETUP_AND_REPORT_BRIEF_20260703.md` — environment setup, report brief creation, validation/build, and release-output refresh.

Earlier rounds include equipment implementation, texture corrections, data-driven JSON decoupling, resource generation, tooltip/redstone mechanics, balance passes, and durability/mining-tier audit reports (`ROUND2` through `ROUND35`).

## Data-driven configuration files

- `src/main/resources/data/dream_equipment/equipment_families.json` — JSON-owned equipment family declarations, item inclusion, stats, ingredients, recipe overrides, and localization metadata.
- `src/main/resources/data/dream_equipment/set_effects.json` — JSON-owned set-effect values and rule tables for passive effects, brittle behavior, wet durability/repair, redstone signal values, held effects, and damage immunities.

## Scripts and validators

- `scripts/generate_equipment_resources.py` — deterministic resource generator and drift checker. Run with `--write` to update generated resources; run without flags to verify sync.
- `scripts/validate_equipment_families_json.py` — validates equipment family JSON structure/content.
- `scripts/validate_dream_equipment_assets.py` — validates generated assets/resources against declared items/materials.
- `scripts/validate_set_effects_json.py` — validates set-effect JSON structure/content.
- `scripts/audit_equipment_balance.py` — audits durability/mining-tier guardrails and tooltip durability formula assumptions.

## Known documentation gaps

The following documents were requested by the 2026-07-03 setup instructions but are not present in this standalone Dream Equipment repository as of this pass:

- `docs/JSON_EXTENSION_SPEC_1_1_3.md`
- `docs/EXTENDING_HERBCRAFT.md`

Because this repository is explicitly standalone and separate from `yansheng-source`/Herbcraft references, no Herbcraft-specific spec content was invented in this pass.
