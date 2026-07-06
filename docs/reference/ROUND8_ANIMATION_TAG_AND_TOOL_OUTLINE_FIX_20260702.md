# Round 8 Animation Tag and Tool Outline Fix — 2026-07-02

## User feedback

- First-person animation mod recognized spears, but not swords/axes/other tools.
- Non-emerald tool recolors still kept emerald-green edge/outline pixels.

## Fixes

### Broader item tags

The previous pass added vanilla `minecraft` tags, but some animation/combat mods do not check only those tags. This pass adds broader compatibility tags while keeping `replace=false` everywhere.

Now generated/validated:

- `data/minecraft/tags/item/swords.json`
- `data/minecraft/tags/item/axes.json`
- `data/minecraft/tags/item/pickaxes.json`
- `data/minecraft/tags/item/shovels.json`
- `data/minecraft/tags/item/hoes.json`
- `data/minecraft/tags/item/spears.json`

Also added common/Fabric/Forge-style aliases:

- `data/c/tags/item/<type>.json`
- `data/c/tags/item/tools/<type>.json`
- `data/fabric/tags/item/<type>.json`
- `data/fabric/tags/item/tools/<type>.json`
- `data/forge/tags/item/<type>.json`
- `data/forge/tags/item/tools/<type>.json`

For aggregate checks:

- `data/c/tags/item/tools.json`
- `data/c/tags/item/weapons.json`
- `data/c/tags/item/melee_weapons.json`
- same aggregate aliases under `fabric` and `forge`

Expected compatibility improvement: animation mods that inspect common weapon/tool tags should now identify swords/axes/pickaxes/shovels/hoes as well as spears.

### Tool outline recolor

The recolor logic was too conservative and left dark emerald-green outline pixels from the uploaded templates. The new recolor pass detects the full green/cyan blade/head region, including darker edge pixels, and remaps them to material-specific dark/base/highlight colors.

This preserves:

- brown wooden handles
- black/neutral hard outlines
- the uploaded template silhouette

But no longer leaves green edge pixels on lapis/redstone/quartz/amethyst/prismarine/glass/obsidian tools.

## Validation

Executed:

```bash
python3 scripts/validate_dream_equipment_assets.py
JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks
```

Results:

- Asset validator: PASS — 104 items, 17 materials.
- Validator now checks vanilla/common/fabric/forge tags and aggregate tags.
- Build: PASS.

## Client-only checks

- Confirm first-person animation mod recognizes swords/axes/pickaxes/shovels/hoes now.
- Confirm material tool outlines no longer retain emerald-green pixels.
