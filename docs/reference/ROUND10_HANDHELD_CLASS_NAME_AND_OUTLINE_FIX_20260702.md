# Round 10 Handheld Model, Tool Class, Name, and Outline Fix — 2026-07-02

## Scope

This round implements the fixes from the previous cause-analysis pass.

## Fixes applied

### 1. Tool/weapon model parent corrected

All non-spear tools/weapons now use the vanilla handheld model parent:

```json
"parent": "minecraft:item/handheld"
```

Affected suffixes:

- `_sword`
- `_axe`
- `_pickaxe`
- `_shovel`
- `_hoe`

This matches vanilla 26.1.2 diamond/iron/etc. tool models and Fabric's 26.1.2 tool documentation. It should improve held rendering and may help first-person animation mods that expect vanilla handheld model conventions.

### 2. Axe/shovel/hoe registration corrected

Axes, shovels, and hoes now use their dedicated vanilla classes:

- `AxeItem`
- `ShovelItem`
- `HoeItem`

instead of being plain `Item` instances with only properties. This restores vanilla-like right-click tool behavior and makes the item classes closer to what compatibility mods may expect.

Pickaxes remain plain `Item` with `.pickaxe(...)`, because no standalone `PickaxeItem` class exists in this MC 26.1.2 mapped jar. Swords likewise follow the Fabric 26.1.2 docs pattern of generic `Item` + `.sword(...)`.

### 3. Cobblestone Chinese name fixed

Changed cobblestone armor names from `原石` to `圆石`:

- `圆石头盔`
- `圆石胸甲`
- `圆石护腿`
- `圆石靴子`

### 4. Tool recolor fixed again

The tool recolor pass now detects saturated green/cyan blade/head pixels by hue/saturation and recolors dark emerald edge pixels too. It preserves:

- true neutral/black outline pixels
- brown wooden handle pixels

This should remove the leftover emerald-green edge artifacts on non-emerald tools.

## Validator additions

`validate_dream_equipment_assets.py` now also checks:

- non-spear tool/weapon models use `minecraft:item/handheld`
- cobblestone zh_cn names do not contain `原石`
- `DreamEquipmentItems.java` contains `new AxeItem`, `new ShovelItem`, and `new HoeItem`

## Validation

Executed:

```bash
python3 scripts/validate_dream_equipment_assets.py
JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks
```

Results:

- Asset/source validator: PASS — 104 items, 17 materials.
- Build: PASS.

## Client-only checks

- Re-test the first-person animation mod.
- Confirm axes can strip logs, shovels can flatten, hoes can till.
- Confirm held model transforms now look vanilla-tool-like.
- Confirm no non-emerald tool still has green edge pixels.
- Confirm cobblestone armor displays as `圆石...`.
