# Round 46 Plank Component Mapping for All Plank Families — 2026-07-03

## Scope

Applied the accepted cherry component-local plank worn-layer style to all plank armor families.

This pass changes plank worn-layer textures only. It does not change item icons, recipes, stats, set effects, fuel values, repair tags, registration, or log/stem/bamboo-block armor art.

## Change

After the cherry-only test was accepted, `scripts/generate_wood_worn_textures.py` was updated from:

```python
PIECE_AWARE_PLANK_FAMILIES = {"cherry"}
```

to:

```python
PIECE_AWARE_PLANK_FAMILIES = set(PLANK_TEXTURES.keys())
```

All plank armor families now use the same component-local vanilla plank mapping:

1. Preserve the current MC 26.1 equipment layer alpha/UV mask.
2. Split opaque equipment pixels into connected components.
3. Map each component to the corresponding vanilla `*_planks` texture once.
4. Add a few large component-local plank joins and restrained plate breaks.
5. Avoid dense full-layer tiling and avoid global artificial stripes.

## Affected plank families

- `oak`
- `spruce`
- `birch`
- `jungle`
- `acacia`
- `dark_oak`
- `mangrove`
- `cherry`
- `pale_oak`
- `bamboo`
- `crimson`
- `warped`

Each family has three current-spec equipment layers regenerated:

```text
humanoid           64×32
humanoid_leggings 64×32
humanoid_baby      64×64
```

## Unchanged in this pass

Log/stem/bamboo-block armor families remain on the vanilla-source baseline pending a separate accepted log-specific component-local style.

## Audit image

```text
docs/reports/ROUND46_PLANK_COMPONENT_MAPPING_AUDIT_20260703.png
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

1. Check all plank armor families in game, especially light families (`birch`, `cherry`, `pale_oak`) and dark families (`dark_oak`, `crimson`, `warped`).
2. Confirm all plank sets read as larger plank plates rather than flat leather or chaotic stripes.
3. Confirm log/stem/bamboo-block armor remains acceptable as-is for now.
4. Confirm no transparent-UV black/floating bands appear.
5. Confirm item icons are unchanged.
