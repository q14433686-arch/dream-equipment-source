# Round 45 Cherry Component-Local Plank Test — 2026-07-03

## Scope

Focused follow-up for the cherry plank armor worn texture after client screenshots showed that simple full-layer vanilla texture fill still did not read like cherry planks on the player model.

This is intentionally a narrow art test for `cherry` plank armor only. It does not change item icons, recipes, stats, effects, registration, fuel values, repair tags, or non-cherry wood families beyond regenerating the existing baseline.

## Problem

A straight tiled fill of `minecraft:cherry_planks` across the whole armor UV preserved the vanilla source texture, but on the worn model it still produced a noisy/flat leather-like read. The cherry plank block has large low-frequency plank panels, but the armor UV was sampling too densely and not respecting armor-piece components.

## New approach

Added a component-local plank mapping path to `scripts/generate_wood_worn_textures.py` for selected test families:

```python
PIECE_AWARE_PLANK_FAMILIES = {"cherry"}
```

For cherry worn layers:

1. Preserve the current MC 26.1 equipment layer alpha/UV mask.
2. Split opaque armor pixels into connected components.
3. Map each component's bounding box to the 16×16 vanilla `cherry_planks` texture once.
4. Add only a few large component-local vertical plank joins and one restrained horizontal plate break for tall UV chunks.
5. Avoid dense global stripes across the whole layer.

This keeps the source material as vanilla cherry planks, but makes the sampling scale closer to large armor plates instead of a repeated wallpaper texture.

## Files changed

- `scripts/generate_wood_worn_textures.py`
- Cherry worn textures under:
  - `textures/entity/equipment/humanoid/cherry.png`
  - `textures/entity/equipment/humanoid_leggings/cherry_leggings.png`
  - `textures/entity/equipment/humanoid_baby/cherry.png`
- Regenerated wood/log worn layer outputs through the generator.

## Audit image

```text
docs/reports/ROUND45_CHERRY_PLANK_COMPONENT_SAMPLE_20260703.png
```

## Validation

Executed:

```bash
python3 scripts/generate_wood_worn_textures.py
python3 scripts/generate_equipment_resources.py
python3 scripts/validate_equipment_families_json.py
python3 scripts/validate_dream_equipment_assets.py
python3 scripts/validate_set_effects_json.py
python3 scripts/audit_equipment_balance.py
JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks
```

Results:

- Wood/log worn texture generator: PASS — 72 files regenerated.
- Equipment resource generator drift check: PASS — 1125 generated resources in sync.
- Equipment family validator: PASS — 56 families / 312 items.
- Asset validator: PASS — 312 items / 56 materials.
- Set-effect validator: PASS — 24 passive entries / 4 brittle entries.
- Balance audit: PASS.
- Gradle build: BUILD SUCCESSFUL.

## Client-only checks

1. Recheck cherry armor only before applying this approach to all plank families.
2. Compare it directly against a placed cherry planks block.
3. Confirm the armor reads as larger cherry plank plates instead of dense stripes or flat leather.
4. Confirm no transparent-UV black/floating bands appear.

## Next step

If this cherry direction is accepted, expand `PIECE_AWARE_PLANK_FAMILIES` to all plank families and then separately design a component-local log/stem mapping for log armor.
