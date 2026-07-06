# Round 44 Wood Worn Layer Vanilla Source Baseline — 2026-07-03

## Scope

Reverted the over-designed wood/log worn-layer art direction and reset the approach to the user's requested first step:

> Reuse the corresponding vanilla plank/log/stem/bamboo block texture inside the current equipment UV mask first, then discuss optimization later.

This pass changes worn-layer textures only. It does not change item icons, recipes, stats, registration, fuel values, repair tags, or set effects.

## Change

Retuned `scripts/generate_wood_worn_textures.py` to remove synthetic board/bark overlays from the previous rounds.

The generator now:

- Preserves the existing MC 26.1 equipment layer dimensions and UV/alpha masks.
- Samples the corresponding vanilla block texture directly:
  - plank armor uses `*_planks` block textures;
  - log/stem/bamboo-block armor uses `*_log`, `*_stem`, or `bamboo_block` block textures.
- Replaces only non-transparent pixels.
- Applies only a small amount of the existing armor-mask shading so the worn model still has depth.
- Draws no extra generated seams, bands, artificial joins, or noise.

## Current equipment spec preserved

```text
humanoid           64×32
humanoid_leggings 64×32
humanoid_baby      64×64
```

Texture paths:

```text
assets/dream_equipment/textures/entity/equipment/humanoid/<material>.png
assets/dream_equipment/textures/entity/equipment/humanoid_leggings/<material>_leggings.png
assets/dream_equipment/textures/entity/equipment/humanoid_baby/<material>.png
```

## Affected families

Plank families:

- `oak`, `spruce`, `birch`, `jungle`, `acacia`, `dark_oak`, `mangrove`, `cherry`, `pale_oak`, `bamboo`, `crimson`, `warped`

Log/stem/bamboo-block families:

- `oak_log`, `spruce_log`, `birch_log`, `jungle_log`, `acacia_log`, `dark_oak_log`, `mangrove_log`, `cherry_log`, `pale_oak_log`, `bamboo_block`, `crimson_stem`, `warped_stem`

Total regenerated files:

```text
24 families × 3 equipment layers = 72 files
```

## Audit image

Generated audit image:

```text
docs/reports/ROUND44_WOOD_WORN_LAYER_VANILLA_SOURCE_AUDIT_20260703.png
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

1. Recheck cherry plank armor; it should now be based on the vanilla cherry planks texture rather than artificial board stripes.
2. Recheck other plank armor variants for vanilla material readability.
3. Recheck log/stem/bamboo-block armor variants for vanilla source-material readability.
4. Confirm no black/floating bands in transparent UV areas.
5. Confirm item icons remain unchanged.

## Next art step

Only after this vanilla-source baseline is accepted should we add optimization, and then preferably in small targeted steps:

1. If a material is too flat, add a very small contrast multiplier.
2. If a material loses identity, adjust sampling scale or palette mix.
3. Avoid synthetic global stripes unless specifically requested.
