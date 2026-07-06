# Round 2 Texture Replacement Report — 2026-07-02

## User request

Use the provided template textures for emerald armor:

- `641123.png` / “23” → emerald helmet
- `641158.png` / “58” → emerald chestplate / armor
- `641193.png` / “93” → emerald leggings
- `641228.png` / “28” → emerald boots

Also make cobblestone and other material armor follow their block texture/material look.

## Changes made

### Emerald armor item textures

Replaced the generated emerald armor item icons with the uploaded user templates:

- `assets/dream_equipment/textures/item/emerald_helmet.png`
- `assets/dream_equipment/textures/item/emerald_chestplate.png`
- `assets/dream_equipment/textures/item/emerald_leggings.png`
- `assets/dream_equipment/textures/item/emerald_boots.png`

The uploaded files are kept at their original 128×128 resolution.

### Wood / stone / cobblestone armor item textures

Regenerated the non-emerald armor item icons by preserving the armor silhouettes and applying material/block-style fills:

- wooden armor: plank-like horizontal grain and brown palette
- stone armor: smooth stone gray gradient/crack highlights
- cobblestone armor: rough cobble-cell pattern with dark mortar lines

These are original generated textures, not copied Vanilla+ assets.

## Validation

Executed:

```bash
python3 scripts/validate_dream_equipment_assets.py
JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks
```

Results:

- Asset validator: PASS — 21 items, 4 materials.
- Build: PASS.
- Jar contains the replaced emerald armor texture path.

## Client-only checks

- Confirm the four emerald armor icons match the intended templates in inventory.
- Confirm wood/stone/cobblestone armor icons read like their source block materials.
- Confirm worn armor layer visuals are acceptable; this turn changed item icons, not bespoke model-layer templates from VKL+.
