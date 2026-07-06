# Round 47 Shield Feasibility Audit — 2026-07-03

## Scope

Audited Minecraft 26.1.2 shield item registration, resources, renderer behavior, recipes, and data components to decide whether Dream Equipment should add custom material shields.

This is an audit/planning pass only. No shield items were registered in this pass.

## Vanilla 26.1.2 findings

### Vanilla item/API

The vanilla item class exists:

```text
net.minecraft.world.item.ShieldItem
```

`ShieldItem` is currently a small subclass of `Item`. Its visible custom logic is name handling for patterned/dyed shields through `DataComponents.BASE_COLOR`.

Vanilla `Items.SHIELD` is registered roughly as:

```text
new ShieldItem(
  new Item.Properties()
    .durability(336)
    .component(DataComponents.BANNER_PATTERNS, BannerPatternLayers.EMPTY)
    .repairable(ItemTags.WOODEN_TOOL_MATERIALS)
    .equippableUnswappable(EquipmentSlot.OFFHAND)
    .delayedComponent(DataComponents.BLOCKS_ATTACKS, vanilla shield BlocksAttacks)
    .component(DataComponents.BREAK_SOUND, SoundEvents.SHIELD_BREAK)
)
```

The vanilla shield block behavior is component-driven through:

```text
DataComponents.BLOCKS_ATTACKS
net.minecraft.world.item.component.BlocksAttacks
```

The vanilla block configuration uses:

- `blockDelaySeconds`: `0.25`
- `disableCooldownScale`: `1.0`
- one `DamageReduction` entry with 90-degree angle coverage
- item durability damage function
- bypass tag: `DamageTypeTags.BYPASSES_SHIELD`
- block sound: `SoundEvents.SHIELD_BLOCK`
- disable/break sound: `SoundEvents.SHIELD_BREAK`

### Vanilla resources

The item definition is special-renderer based:

```text
assets/minecraft/items/shield.json
```

It uses a `minecraft:condition` on `minecraft:using_item`:

- not blocking: special shield model with base `minecraft:item/shield`
- blocking: special shield model with base `minecraft:item/shield_blocking`

Models:

```text
assets/minecraft/models/item/shield.json
assets/minecraft/models/item/shield_blocking.json
```

Shield textures and patterns live under:

```text
assets/minecraft/textures/entity/shield/
assets/minecraft/atlases/shield_patterns.json
```

Vanilla recipes:

```text
data/minecraft/recipe/shield.json
data/minecraft/recipe/shield_decoration.json
```

### Renderer limitation

The vanilla `ShieldSpecialRenderer` chooses between fixed vanilla atlas sprites:

```text
Sheets.SHIELD_BASE
Sheets.SHIELD_BASE_NO_PATTERN
```

Then it overlays banner patterns from `DataComponents.BANNER_PATTERNS` and `DataComponents.BASE_COLOR`.

Important implication:

- A custom `ShieldItem` can use vanilla blocking mechanics and vanilla special shield rendering.
- But material-specific base textures are not trivial with only item JSON, because the special renderer does not select a base texture per custom item id.
- Without a client renderer/mixin/model extension, custom material shields using `minecraft:shield` special model will visually look like vanilla shield base plus optional banner-style color/pattern components.

## Implementation risk assessment

### Low-risk path

Implement custom shields as `ShieldItem` with the same data components as vanilla:

- stable blocking behavior
- offhand equipment behavior
- durability/repair support
- recipes/lang/tags generated from JSON
- vanilla-like item definition with `minecraft:shield` special renderer

Risk: visuals may not be material-specific enough unless using banner/base-color tricks.

### Medium-risk path

Use `BASE_COLOR` and possibly predefined banner patterns to approximate material identity:

- cherry/oak/bamboo shields could use dye colors close to material
- redstone shield could use red base color
- lapis shield could use blue base color
- emerald shield could use green/lime base color

Risk: still reads as recolored vanilla shield, not as material-specific equipment. It also does not preserve exact plank/log/stone material texture.

### High-risk path

Add custom material-specific shield rendering:

- custom client special renderer or mixin into `ShieldSpecialRenderer`
- custom atlas sprite selection per item id
- custom entity/shield base textures per material

Risk: higher conflict potential, more client-only rendering maintenance, more likely to break across versions or with renderer mods/resource packs.

## Recommended design decision

Do not add shields by brute force yet.

Because the mod's art direction has recently required careful texture iteration, and vanilla shield rendering is special-renderer based, the safest approach is a two-stage implementation:

### Stage 1 — behavior-first prototype

Add a very small shield batch using vanilla special shield rendering, to confirm mechanics:

Recommended first prototype set:

- `oak_shield`
- `cherry_shield`
- `bamboo_shield`
- `emerald_shield`
- `redstone_shield`
- `amethyst_shield`
- `prismarine_shield`
- `obsidian_shield`

Goals:

- confirm registration and blocking behavior
- confirm recipes and repair materials
- confirm durability values
- confirm creative-tab visibility
- confirm no crashes from special shield item definitions
- confirm whether vanilla renderer appearance is acceptable enough

### Stage 2 — art/render decision

Only after Stage 1 works:

1. Decide whether recolored vanilla shield is acceptable.
2. If not, evaluate custom shield rendering separately.
3. Avoid adding all 56 material shields until the rendering path is accepted.

## JSON/schema recommendation

Extend `equipment_families.json` with an optional `shield` object:

```json
"shield": {
  "enabled": true,
  "durability": 336,
  "recipe_pattern": [
    "MIM",
    "MMM",
    " M "
  ],
  "recipe_key": {
    "M": "minecraft:oak_planks",
    "I": "minecraft:iron_ingot"
  }
}
```

Minimal fields for first implementation:

- `enabled`
- `durability`

The generator can initially derive the recipe from `ingredient` plus `minecraft:iron_ingot`, mirroring the vanilla shield recipe shape.

## Java implementation notes for a future pass

Add to `DreamEquipmentItems`:

- register shield if `family.shield()` exists/enabled
- use `new ShieldItem(properties)`
- properties should mirror vanilla:
  - `.durability(shieldDurability)`
  - `.component(DataComponents.BANNER_PATTERNS, BannerPatternLayers.EMPTY)`
  - `.repairable(repairTag(material))`
  - `.equippableUnswappable(EquipmentSlot.OFFHAND)`
  - `.delayedComponent(DataComponents.BLOCKS_ATTACKS, ...)`
  - `.component(DataComponents.BREAK_SOUND, SoundEvents.SHIELD_BREAK)`

Need either:

- recreate the vanilla `BlocksAttacks` value in Dream Equipment Java, or
- find a safe way to reuse vanilla shield's component value after registries/components are initialized.

Given the bytecode audit, recreating the vanilla `BlocksAttacks` value is feasible but should be done carefully in a dedicated helper to avoid hardcoding unrelated shield behavior in multiple places.

## Resource-generator notes for a future pass

For each shield:

- item definition should be based on vanilla `assets/minecraft/items/shield.json`, with namespace-adjusted base model paths if custom base models are used.
- models can initially mirror vanilla `shield.json` and `shield_blocking.json`.
- recipe should mirror vanilla shield shape.
- lang keys should be generated like other items.
- repair tags can reuse the family repair tag.
- optional common tags can be added if a shield tag convention is desired.

## Recommended next implementation pass

If proceeding, implement Stage 1 prototype only:

```text
Round 48 — Shield Prototype Batch
```

Suggested batch:

```text
oak_shield
cherry_shield
bamboo_shield
emerald_shield
redstone_shield
amethyst_shield
prismarine_shield
obsidian_shield
```

Do not implement all plank shields or all material shields until the first shield batch is validated in client.

## Validation executed this pass

This audit used local MC 26.1.2 deobfuscated classes and client resources:

- `net.minecraft.world.item.ShieldItem`
- `net.minecraft.world.item.Items`
- `net.minecraft.world.item.component.BlocksAttacks`
- `net.minecraft.client.renderer.special.ShieldSpecialRenderer`
- vanilla shield item definition/model/recipe/atlas resources

Project validators/build were executed after the documentation update:

- `python3 scripts/generate_equipment_resources.py`
- `python3 scripts/validate_equipment_families_json.py`
- `python3 scripts/validate_dream_equipment_assets.py`
- `python3 scripts/validate_set_effects_json.py`
- `python3 scripts/audit_equipment_balance.py`
- `JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks`

All passed.

## Client-only checks for future shield implementation

- startup with shield items registered
- blocking animation in first/third person
- offhand equip behavior
- durability loss on block
- repair in anvil
- recipe book/crafting
- shield disable behavior from axes or other disabling attacks
- banner decoration compatibility if supported
- visual acceptability of vanilla special-renderer output
