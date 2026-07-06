# Round 12 Wood Variant Armor Implementation — 2026-07-02

## Decision

User chose option A from the wood/stone audit:

- Keep the existing generic `wooden_*` armor set for compatibility.
- Add explicit armor sets for each vanilla plank variant alongside it.

## Added wood armor variants

Added 12 plank-based armor families, 48 items total:

1. `oak_helmet`, `oak_chestplate`, `oak_leggings`, `oak_boots`
2. `spruce_helmet`, `spruce_chestplate`, `spruce_leggings`, `spruce_boots`
3. `birch_helmet`, `birch_chestplate`, `birch_leggings`, `birch_boots`
4. `jungle_helmet`, `jungle_chestplate`, `jungle_leggings`, `jungle_boots`
5. `acacia_helmet`, `acacia_chestplate`, `acacia_leggings`, `acacia_boots`
6. `dark_oak_helmet`, `dark_oak_chestplate`, `dark_oak_leggings`, `dark_oak_boots`
7. `mangrove_helmet`, `mangrove_chestplate`, `mangrove_leggings`, `mangrove_boots`
8. `cherry_helmet`, `cherry_chestplate`, `cherry_leggings`, `cherry_boots`
9. `pale_oak_helmet`, `pale_oak_chestplate`, `pale_oak_leggings`, `pale_oak_boots`
10. `bamboo_helmet`, `bamboo_chestplate`, `bamboo_leggings`, `bamboo_boots`
11. `crimson_helmet`, `crimson_chestplate`, `crimson_leggings`, `crimson_boots`
12. `warped_helmet`, `warped_chestplate`, `warped_leggings`, `warped_boots`

## Texture approach

Unlike the earlier generic wooden armor, these variants are generated from actual vanilla plank block textures from the MC 26.1.2 jar:

- `oak_planks.png`
- `spruce_planks.png`
- `birch_planks.png`
- `jungle_planks.png`
- `acacia_planks.png`
- `dark_oak_planks.png`
- `mangrove_planks.png`
- `cherry_planks.png`
- `pale_oak_planks.png`
- `bamboo_planks.png`
- `crimson_planks.png`
- `warped_planks.png`

Item icons preserve the armor silhouette but fill it with the real plank color/pattern. Worn layers use the correct 26.1 equipment UV layout and overlay plank-grain material cues.

## Mechanics

The new plank variants currently share weak wooden armor stats:

- defense: 1 / 2 / 2 / 1
- low durability multiplier
- leather equip sound

No special effects were added yet. This keeps wood variants primarily visual for the first client test. Crimson/warped/bamboo special behavior can be added later if desired.

## Content totals

After this round:

- Items: 152
- Armor/equipment materials: 29
- Added this round: 48 items / 12 materials

## Validation

Executed:

```bash
python3 scripts/validate_dream_equipment_assets.py
JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks
```

Results:

- Asset validator: PASS — 152 items, 29 materials.
- Build: PASS.

## Client-only checks

- Confirm all 12 wood variant sets appear in creative tabs.
- Confirm recipes use the matching plank type.
- Confirm icons visually match source plank colors/patterns.
- Confirm worn layers render without UV issues and look wood-like enough.
- Decide if generic `wooden_*` should remain visible long term or become deprecated/hidden later.
