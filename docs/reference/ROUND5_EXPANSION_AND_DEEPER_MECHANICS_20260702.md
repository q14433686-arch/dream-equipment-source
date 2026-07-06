# Round 5 Expansion + Expanded/Deepened Mechanics — 2026-07-02

## Scope

User requested expansion plus expanded/deepened mechanics. This round adds multiple new material families and broadens set-effect behavior while keeping mechanics vanilla-effect-based and safe for first live testing.

## New equipment families

### Lapis / 青金石

Added full toolset and armor set:

- `lapis_sword`, `lapis_pickaxe`, `lapis_axe`, `lapis_shovel`, `lapis_hoe`
- `lapis_helmet`, `lapis_chestplate`, `lapis_leggings`, `lapis_boots`

Set effect: full set grants Haste.

### Redstone / 红石

Added full toolset and armor set:

- `redstone_sword`, `redstone_pickaxe`, `redstone_axe`, `redstone_shovel`, `redstone_hoe`
- `redstone_helmet`, `redstone_chestplate`, `redstone_leggings`, `redstone_boots`

Set effect: full set grants Speed.

### Quartz / 石英

Added full toolset and armor set:

- `quartz_sword`, `quartz_pickaxe`, `quartz_axe`, `quartz_shovel`, `quartz_hoe`
- `quartz_helmet`, `quartz_chestplate`, `quartz_leggings`, `quartz_boots`

Set effect: full set grants Resistance.

### Amethyst / 紫水晶

Added full toolset and armor set:

- `amethyst_sword`, `amethyst_pickaxe`, `amethyst_axe`, `amethyst_shovel`, `amethyst_hoe`
- `amethyst_helmet`, `amethyst_chestplate`, `amethyst_leggings`, `amethyst_boots`

Set effect: full set grants Regeneration.

### Prismarine / 海晶石

Added full toolset and armor set:

- `prismarine_sword`, `prismarine_pickaxe`, `prismarine_axe`, `prismarine_shovel`, `prismarine_hoe`
- `prismarine_helmet`, `prismarine_chestplate`, `prismarine_leggings`, `prismarine_boots`

Set effects: full set grants Water Breathing, and Dolphin's Grace while in water.

### Slime / 史莱姆

Added armor set:

- `slime_helmet`, `slime_chestplate`, `slime_leggings`, `slime_boots`

Set effects: full set grants Jump Boost + Slow Falling; fall damage is partially offset after damage.

### Coal / 煤炭

Added armor set:

- `coal_helmet`, `coal_chestplate`, `coal_leggings`, `coal_boots`

Set effect: full set grants Fire Resistance.

## Deepened mechanics

Existing effects were expanded:

- Cactus retaliation is now per-piece instead of full-set-only: each cactus armor piece contributes 0.5 thorns-style retaliation damage, up to 2.0 for the full set.
- Paper full set now loses durability while wet/rained on in addition to Weakness + Slowness.
- Slime full set has both passive mobility effects and partial fall-damage recovery.

Existing first-pass effects remain:

- Emerald full set: Luck.
- Armadillo shell boots: partial fall-damage recovery.
- Bone full set: Night Vision.
- Glass full set: heavy-hit shatter chance.
- Obsidian full set: Fire Resistance + Resistance + Slowness.

## Content totals

After this round:

- Items: 95
- Armor/equipment materials: 17
- Recipes: 95
- Item textures: 95

## Validation

Executed:

```bash
python3 scripts/validate_dream_equipment_assets.py
JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks
```

Results:

- Asset validator: PASS — 95 items, 17 materials.
- Build: PASS.

## Client-only checks

- Confirm all 95 items appear and localize correctly.
- Test all new toolsets' mining/combat feel.
- Test all set effects for flicker, balance, and edge cases.
- Check whether 95 items is still a reasonable scope or whether any should be moved to config/disabled by default later.
