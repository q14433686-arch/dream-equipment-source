# Round 6 Tool Scope and User Texture Integration — 2026-07-02

## User request

The user supplied emerald tool textures and clarified equipment/tool scope:

- `479478.png` → emerald axe
- `479477.png` → emerald pickaxe
- `479479.png` → emerald shovel
- `479480.png` → emerald hoe
- `479475.png` → emerald sword
- `Held_Diamond_Spear_JE2_BE1.webp` → use vanilla diamond spear as base and recolor for spears

The user also clarified that material toolsets need judgment. For example, quartz/glass/obsidian should not blindly receive every utility tool; they make more sense as weapons such as spear, axe, and sword.

## Changes made

### Emerald tools

Replaced all five emerald tool item icons with the user-provided templates:

- `emerald_axe.png`
- `emerald_pickaxe.png`
- `emerald_shovel.png`
- `emerald_hoe.png`
- `emerald_sword.png`

### Spears

Added spear items and recipes for:

- `emerald_spear`
- `lapis_spear`
- `redstone_spear`
- `quartz_spear`
- `amethyst_spear`
- `prismarine_spear`
- `glass_spear`
- `obsidian_spear`

The spear texture source is the uploaded diamond spear image, recolored per material. These are real 26.1 spear-property items using `Item.Properties().spear(...)`.

### Tool scope correction

Changed quartz from a full toolset to weapon-only:

- kept/registered: `quartz_sword`, `quartz_axe`, `quartz_spear`
- removed resource recipes/models/textures for: `quartz_pickaxe`, `quartz_shovel`, `quartz_hoe`

Added weapon-only tools for glass and obsidian:

- `glass_sword`, `glass_axe`, `glass_spear`
- `obsidian_sword`, `obsidian_axe`, `obsidian_spear`

## Current content count

After this round:

- Items: 104
- Armor/equipment materials: 17
- Recipes: 104

## Validation

Executed:

```bash
python3 scripts/validate_dream_equipment_assets.py
JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks
```

Results:

- Asset validator: PASS — 104 items, 17 materials.
- Build: PASS.

## Client-only checks

- Confirm uploaded emerald tool textures render correctly.
- Confirm spear items behave correctly in 26.1 combat.
- Confirm quartz no longer exposes inappropriate pickaxe/shovel/hoe routes.
- Confirm glass/obsidian weapon-only selection feels sensible.
