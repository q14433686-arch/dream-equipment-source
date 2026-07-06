# Round 2 Equipment Implementation Report — 2026-07-02

## Scope

Implemented the first playable content batch for the standalone `dream-equipment` Fabric mod, using Vanilla+ / VKL+ as style and balance reference only. No Vanilla+ texture pixels were copied; textures are original generated project assets.

## Added equipment

### Emerald set

Tools:

- `dream_equipment:emerald_sword`
- `dream_equipment:emerald_pickaxe`
- `dream_equipment:emerald_axe`
- `dream_equipment:emerald_shovel`
- `dream_equipment:emerald_hoe`

Armor:

- `dream_equipment:emerald_helmet`
- `dream_equipment:emerald_chestplate`
- `dream_equipment:emerald_leggings`
- `dream_equipment:emerald_boots`

Balance intent: dream/prestige tier, diamond-like but not netherite. Durability 1248 for tools; armor defense 3/7/6/3 with 1.5 toughness.

### Wooden armor

- `dream_equipment:wooden_helmet`
- `dream_equipment:wooden_chestplate`
- `dream_equipment:wooden_leggings`
- `dream_equipment:wooden_boots`

Balance intent: weak early novelty/transition armor. Defense 1/2/2/1.

### Stone armor

- `dream_equipment:stone_helmet`
- `dream_equipment:stone_chestplate`
- `dream_equipment:stone_leggings`
- `dream_equipment:stone_boots`

Balance intent: stronger than wood, below iron. Defense 1/4/3/1.

### Cobblestone armor

- `dream_equipment:cobblestone_helmet`
- `dream_equipment:cobblestone_chestplate`
- `dream_equipment:cobblestone_leggings`
- `dream_equipment:cobblestone_boots`

Balance intent: rougher/cheaper stone-like armor. Defense 1/3/3/1.

## Resources added

For all 21 items:

- item definitions under `assets/dream_equipment/items/`
- item models under `assets/dream_equipment/models/item/`
- generated original 16×16 item textures under `assets/dream_equipment/textures/item/`
- crafting recipes under `data/dream_equipment/recipe/`
- zh_cn and en_us language keys

For all 4 armor materials:

- equipment definitions under `assets/dream_equipment/equipment/`
- humanoid, humanoid_baby, and humanoid_leggings equipment textures
- repair item tags

## Java implementation

Added `DreamEquipmentItems`:

- registers all tools and armor with real Minecraft/Fabric item registration
- uses 26.1 `Item.Properties().sword/pickaxe/axe/shovel/hoe(...)` methods
- uses 26.1 `humanoidArmor(...)` armor material path
- adds equipment to Combat and tools to Tools & Utilities creative tabs

## Validation

Executed:

```bash
JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks
python3 scripts/validate_dream_equipment_assets.py
```

Results:

- Build: PASS
- Asset/resource validator: PASS — 21 items, 4 materials
- Jar spot-check confirmed key classes/resources are included.

## Client-only checks still required

- Game startup with Fabric API 0.152.1+26.1.2.
- All 21 items appear in creative tabs.
- Item names show in zh_cn/en_us.
- Recipes unlock/craft correctly.
- Armor renders with the intended material colors on player model.
- Emerald tool mining/combat stats feel correct.
- Balance tuning after playtest.
