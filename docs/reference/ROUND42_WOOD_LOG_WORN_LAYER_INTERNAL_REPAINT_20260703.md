# Round 42 Wood/Log Worn Layer Internal Repaint — 2026-07-03

## Scope

Reworked the worn equipment textures for all plank-style and log/stem/bamboo-block armor families after reviewing the current MC 26.1 equipment texture specification and the project's prior texture reports.

This pass changes worn-layer art only. It does not change item ids, recipes, stats, set effects, registration, item icons, or fuel/repair behavior.

## Current texture spec confirmed

The project uses the MC 26.1 equipment system, not legacy `layer_1` / `layer_2` armor textures.

Equipment definitions:

```text
assets/dream_equipment/equipment/<material>.json
```

Texture layer keys:

```text
humanoid
humanoid_baby
humanoid_leggings
```

Texture paths:

```text
assets/dream_equipment/textures/entity/equipment/humanoid/<material>.png
assets/dream_equipment/textures/entity/equipment/humanoid_baby/<material>.png
assets/dream_equipment/textures/entity/equipment/humanoid_leggings/<material>_leggings.png
```

Expected dimensions:

```text
humanoid           64×32
humanoid_leggings 64×32
humanoid_baby      64×64
```

Important rendering rule from earlier fixes: texture accents must be clipped to non-transparent armor pixels. Nothing should be drawn into transparent UV space, because earlier unclipped seam lines caused black/floating bands in game.

## Art direction

The previous wood/log worn layers were valid UV-wise but read too much like recolored leather armor.

This pass preserves the accepted current alpha/UV mask and replaces only the interior non-transparent pixels:

- Plank armor interiors use the corresponding vanilla plank texture as the material source.
- Log/stem/bamboo-block armor interiors use the corresponding vanilla log/stem/block texture as the material source.
- Existing equipment-layer silhouettes and alpha are preserved.
- All generated board seams, bark grain, dark edges, and bindings are clipped to the existing mask.

## Plank armor treatment

Affected families:

- `oak`, `spruce`, `birch`, `jungle`, `acacia`, `dark_oak`, `mangrove`, `cherry`, `pale_oak`, `bamboo`, `crimson`, `warped`

Visual treatment:

- Samples each family's vanilla `*_planks` block texture.
- Reduces raw block noise so tiny 64×32 UV areas remain readable.
- Adds horizontal board seams and sparse vertical joins, clipped to armor pixels.
- Preserves original mask shading rank so UV highlights/shadows still read correctly.
- Adds subtle dark binding/shadow bands without drawing outside the mask.

## Log/stem/bamboo-block armor treatment

Affected families:

- `oak_log`, `spruce_log`, `birch_log`, `jungle_log`, `acacia_log`, `dark_oak_log`, `mangrove_log`, `cherry_log`, `pale_oak_log`, `bamboo_block`, `crimson_stem`, `warped_stem`

Visual treatment:

- Samples each family's vanilla log/stem/bamboo-block texture.
- Uses more vertical bark/stem grain instead of leather-like horizontal coloring.
- Darkens the alpha edge more strongly than plank armor for a heavier bark-plate feel.
- Adds rare light flecks/exposed wood chips, clipped to armor pixels.
- Keeps texture density conservative to avoid noisy worn armor in-game.

## Generator added

New script:

```text
scripts/generate_wood_worn_textures.py
```

The script documents and enforces the current equipment texture spec. It regenerates 72 worn layer files:

```text
24 families × 3 equipment layers = 72 files
```

It deliberately does not manage item icons.

## Audit image

Generated audit image:

```text
docs/reports/ROUND42_WOOD_WORN_LAYER_FINAL_AUDIT_20260703.png
```

This shows all regenerated wood/log-like families across:

- `humanoid`
- `humanoid_leggings`
- `humanoid_baby`

## Files changed

- `scripts/generate_wood_worn_textures.py`
- `scripts/validate_dream_equipment_assets.py`
- 72 worn equipment textures under:
  - `src/main/resources/assets/dream_equipment/textures/entity/equipment/humanoid/`
  - `src/main/resources/assets/dream_equipment/textures/entity/equipment/humanoid_leggings/`
  - `src/main/resources/assets/dream_equipment/textures/entity/equipment/humanoid_baby/`
- Documentation/status files.

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
- Asset validator: PASS — 312 items / 56 materials, including wood/log worn-layer size/spec checks.
- Set-effect validator: PASS — 24 passive entries / 4 brittle entries.
- Balance audit: PASS.
- Gradle build: BUILD SUCCESSFUL.

## Client-only checks

1. Check plank armor worn on player and baby humanoid models; it should read as wood boards rather than leather recolor.
2. Check log/stem/bamboo-block armor worn on player and baby humanoid models; it should read as bark/stem plates rather than leather recolor.
3. Confirm no black/floating bands appear around transparent UV areas.
4. Confirm armor alignment remains correct for helmet/chest/legs/boots.
5. Confirm item icons are unchanged by this worn-layer-only pass.
