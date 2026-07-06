# Round 9 Cause Analysis Before Next Fix — 2026-07-02

## User feedback to investigate

1. First-person animation mod recognizes spears but not swords/axes/other tools.
2. Non-emerald tools still show emerald-green edge/outline pixels.
3. Some equipment render images are wrong.
4. One Chinese name is wrong: cobblestone was translated as `原石`, should be `圆石`.
5. This round should identify causes first; fixes are deferred to the next round.

## Findings

### 1. Animation mod recognition: tags are probably not the only issue

Current project already has many item tags, including:

- `data/minecraft/tags/item/swords.json`
- `data/minecraft/tags/item/axes.json`
- `data/minecraft/tags/item/pickaxes.json`
- `data/minecraft/tags/item/shovels.json`
- `data/minecraft/tags/item/hoes.json`
- `data/minecraft/tags/item/spears.json`
- common/fabric/forge aliases and aggregate tool/weapon tags

But the user's test says spears are recognized while other tools are not. This strongly suggests the animation mod is not relying only on the tags we added.

Local vanilla/Fabric checks show two important differences:

#### A. Vanilla tool item models use `minecraft:item/handheld`

Vanilla 26.1.2 models:

```json
{
  "parent": "minecraft:item/handheld",
  "textures": {
    "layer0": "minecraft:item/diamond_sword"
  }
}
```

Our generated sword/axe/pickaxe/shovel/hoe models currently use:

```json
{
  "parent": "minecraft:item/generated",
  "textures": {
    "layer0": "dream_equipment:item/emerald_sword"
  }
}
```

This is wrong for tools/weapons. Fabric's 26.1.2 tool documentation explicitly says tool models should use `item/handheld`, not `item/generated`.

Probable impact:

- first-person transforms can look wrong
- animation mods that check model/display assumptions may fail to classify them correctly
- held render will be flat/generated-style rather than vanilla tool-style

#### B. Axe/shovel/hoe are registered as plain `Item`, not specialized classes

Fabric 26.1.2 docs say swords can be generic `Item` with `.sword(...)`, but axes/shovels/hoes should be `AxeItem`, `ShovelItem`, or `HoeItem` because those classes implement right-click tool actions.

Current project uses generic `Item` for all tools with `Item.Properties().axe/pickaxe/shovel/hoe(...)`.

Probable impact:

- axe strip / shovel flatten / hoe till behavior may be absent or incomplete
- mods that use class checks or vanilla-like behavior checks may not identify them as expected

#### C. Spears work because they are closer to vanilla 26.1 spear structure

Spears now use `Item.Properties().spear(...)` plus a vanilla-style `display_context` item definition split between inventory render and in-hand model. This likely explains why spear recognition works when other tools do not.

### 2. Green edge/outline issue: recolor mask is still insufficient

The uploaded emerald tool templates contain multiple green ranges:

- bright emerald fill
- cyan/white highlight
- medium green shading
- very dark green edge/outline pixels

Previous recolor passes changed the obvious bright green/cyan areas, but some dark green outline pixels are close enough to neutral/dark colors that they were preserved.

Root cause:

- recolor logic treated very dark pixels as outlines to preserve
- some of those very dark pixels are actually emerald-tinted outlines, not neutral black outlines

Correct next fix:

- derive a material mask from hue/saturation rather than only brightness
- preserve only true neutral black/brown handle pixels
- recolor all saturated green/cyan pixels, including dark edge pixels
- for non-emerald tools, regenerate from mask rather than repeatedly recoloring already-recolored files

### 3. Equipment render images: two separate problems

The phrase "render image" can refer to two different places:

#### A. Item/GUI render icons

For normal tools, our item models are currently `item/generated`. For handheld tools this is wrong; they should use `item/handheld`. This affects held/render behavior.

For spears, vanilla 26.1 uses two models:

- inventory / GUI / ground / fixed / shelf: `diamond_spear`
- held/in-hand contexts: `diamond_spear_in_hand`

We now know this split is correct and should keep it.

#### B. Worn armor layer textures

Current version armor uses:

- `assets/<namespace>/equipment/<material>.json`
- `humanoid`
- `humanoid_baby`
- `humanoid_leggings`
- 64×32 textures under `textures/entity/equipment/...`

Earlier hand-drawn armor layer rectangles were wrong. The current best approach is to recolor vanilla 26.1 equipment UV templates, not draw rectangles manually.

However, some visual mismatch can still remain if every material is recolored from the diamond template. Cactus/paper/glass/slime may need distinct layer templates, not just recolored diamond armor.

### 4. Naming issue: cobblestone Chinese name

Confirmed in `zh_cn.json`:

```json
"item.dream_equipment.cobblestone_helmet": "原石头盔"
"item.dream_equipment.cobblestone_chestplate": "原石胸甲"
"item.dream_equipment.cobblestone_leggings": "原石护腿"
"item.dream_equipment.cobblestone_boots": "原石靴子"
```

User wants `圆石`, not `原石`.

Correct next fix:

- change to `圆石头盔`, `圆石胸甲`, `圆石护腿`, `圆石靴子`
- also audit any docs/report text using `原石套` and rename to `圆石套` where it specifically means cobblestone

## Next-round fix plan

1. Change all non-spear tool/weapon item models from `minecraft:item/generated` to `minecraft:item/handheld`.
2. Register axes/shovels/hoes using `AxeItem`, `ShovelItem`, `HoeItem` instead of generic `Item` where applicable.
3. Investigate whether pickaxe also has a dedicated class in 26.1 mappings; if absent, keep `Item.Properties().pickaxe(...)`.
4. Rebuild tool texture recolor using hue/saturation mask so dark emerald edges become material-specific outlines.
5. Keep vanilla-style spear render/in-hand split.
6. Rework worn armor layers material-by-material if recolored diamond UV is not visually enough.
7. Fix cobblestone zh name from `原石` to `圆石`.
8. Rebuild, validate, and ask for a client retest with the exact first-person animation mod.

## Information still needed

For maximum accuracy, ask the user which first-person animation mod is being used. Different mods may check different things:

- vanilla item tags
- common tags
- item model parent / display context
- item components
- Java class type
- Better Combat-style fallback compatibility files
- hardcoded item IDs
