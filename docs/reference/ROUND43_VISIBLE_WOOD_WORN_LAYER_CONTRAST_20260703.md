# Round 43 Visible Wood Worn Layer Contrast — 2026-07-03

## Scope

Follow-up to Round 42 after client screenshot showed cherry plank armor still reading like a flat pink leather recolor in game.

The issue was not the current MC 26.1 equipment-layer spec or UV path; those were correct. The issue was that the first internal repaint was too subtle at actual player-render scale. The board/bark details were visible in texture audits but not visible enough in a normal third-person/inventory-world view.

## Change

Retuned `scripts/generate_wood_worn_textures.py` to make the internal material language more visible while still preserving the current equipment-layer alpha/UV masks.

### Plank armor changes

- Stronger horizontal plank seams.
- More visible staggered vertical plank joins.
- Alternating board-row tint so adjacent planks differ more clearly.
- Stronger clipped binding/shadow bands.
- Still samples the corresponding vanilla `*_planks` texture.

### Log/stem/bamboo-block armor changes

- Stronger vertical bark/stem grain.
- More visible dark bark channels.
- Slightly stronger exposed-material flecks.
- Stronger dark edge treatment remains clipped to the existing mask.
- Still samples the corresponding vanilla log/stem/bamboo-block texture.

## Important constraint preserved

This pass still does **not** redraw armor shapes and does **not** draw outside the current UV/alpha mask.

The current equipment spec remains:

```text
humanoid           64×32
humanoid_leggings 64×32
humanoid_baby      64×64
```

Changed content is only non-transparent interior pixels of wood/plank/log/stem/bamboo-block worn equipment layers.

## Audit image

Updated audit image:

```text
docs/reports/ROUND43_WOOD_WORN_LAYER_VISIBLE_AUDIT_20260703.png
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

1. Recheck cherry plank armor worn in game; board seams should now be visible at normal player-render scale.
2. Check other plank families for overly strong/weak seams.
3. Check log/stem/bamboo-block armor for visible vertical bark/stem grain.
4. Confirm no floating black lines appear in transparent UV areas.
5. Confirm item icons remain unchanged.
