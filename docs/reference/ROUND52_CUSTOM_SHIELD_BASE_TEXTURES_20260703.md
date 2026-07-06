# Round 52 Custom Shield Base Textures — 2026-07-03

## Scope

Added material-adapted shield base textures based on vanilla shield resources.

The previous shield implementation used vanilla shield behavior and special rendering, but all shields shared the vanilla shield base sprite. This pass keeps vanilla shield geometry and special renderer behavior, but adds a small client mixin and item data component so each Dream Equipment shield can select a custom shield base texture.

## Vanilla resource/rendering research

Checked MC 26.1.2 resources/classes before implementation:

- `assets/minecraft/items/shield.json`
- `assets/minecraft/models/item/shield.json`
- `assets/minecraft/models/item/shield_blocking.json`
- `assets/minecraft/textures/entity/shield/shield_base_nopattern.png`
- `assets/minecraft/atlases/shield_patterns.json`
- `net.minecraft.client.renderer.special.ShieldSpecialRenderer`
- `net.minecraft.client.renderer.Sheets`
- `net.minecraft.client.model.object.equipment.ShieldModel`

Findings:

- Vanilla shields are rendered by `ShieldSpecialRenderer` using the shield pattern atlas.
- Vanilla chooses between `Sheets.SHIELD_BASE` and `Sheets.SHIELD_BASE_NO_PATTERN`.
- `assets/minecraft/atlases/shield_patterns.json` uses a directory source over `textures/entity/shield`, so additional textures placed under that path can be included in the atlas.
- The vanilla shield geometry/base model can be kept; only the base sprite needs material-specific selection.

## Implementation

### Custom data component

Added:

```text
src/main/java/com/dreamequipment/DreamEquipmentDataComponents.java
```

Registered component:

```text
dream_equipment:shield_base_texture
```

Type:

```text
DataComponentType<Identifier>
```

It is persistent and network-synchronized.

### Shield item registration

Each Dream Equipment shield now receives:

```text
DreamEquipmentDataComponents.SHIELD_BASE_TEXTURE
```

Value example:

```text
minecraft:entity/shield/dream_equipment/oak_shield_base_nopattern
```

The texture namespace is intentionally `minecraft` because vanilla's shield atlas is sourced from `assets/minecraft/textures/entity/shield/`.

### Client mixin

Added:

```text
src/main/java/com/dreamequipment/mixin/ShieldSpecialRendererMixin.java
```

Registered as a client mixin in:

```text
src/main/resources/dream_equipment.mixins.json
```

It modifies the local `SpriteId` selected in `ShieldSpecialRenderer#submit(...)`. If the item stack component contains a Dream Equipment shield base texture, the mixin returns:

```text
new SpriteId(Sheets.SHIELD_SHEET, customTexture)
```

Otherwise vanilla behavior is preserved.

## Texture generation

Added:

```text
scripts/generate_shield_textures.py
```

It generates 56 custom shield base textures under:

```text
src/main/resources/assets/minecraft/textures/entity/shield/dream_equipment/
```

Texture file pattern:

```text
<family>_shield_base_nopattern.png
```

Generation approach:

- Start from vanilla `shield_base_nopattern.png`.
- Preserve vanilla shield rim/handle/geometry pixels.
- Replace the vanilla wood panel pixels with the family source material texture.
- Source materials are derived from the family ingredient, with mappings for item ingredients such as emerald, lapis, redstone, quartz, amethyst shard, prismarine shard, bone, paper, armadillo scute, and turtle scute.

## Audit image

Generated:

```text
docs/reports/ROUND52_CUSTOM_SHIELD_TEXTURE_AUDIT_20260703.png
```

It previews representative custom shield base textures.

## Files changed

- `src/main/java/com/dreamequipment/DreamEquipmentDataComponents.java`
- `src/main/java/com/dreamequipment/DreamEquipment.java`
- `src/main/java/com/dreamequipment/DreamEquipmentItems.java`
- `src/main/java/com/dreamequipment/mixin/ShieldSpecialRendererMixin.java`
- `src/main/resources/dream_equipment.mixins.json`
- `scripts/generate_shield_textures.py`
- `scripts/validate_dream_equipment_assets.py`
- 56 generated shield base textures under `assets/minecraft/textures/entity/shield/dream_equipment/`

## Validation

Executed:

```bash
python3 scripts/generate_equipment_resources.py
python3 scripts/generate_wood_worn_textures.py
python3 scripts/generate_shield_textures.py
python3 scripts/validate_equipment_families_json.py
python3 scripts/validate_dream_equipment_assets.py
python3 scripts/validate_set_effects_json.py
python3 scripts/audit_equipment_balance.py
JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks
```

Results:

- Equipment resource generator drift check: PASS — 1349 generated resources in sync.
- Wood/log worn texture generator: PASS — 72 worn layer files regenerated.
- Shield texture generator: PASS — 56 shield base textures generated.
- Equipment family validator: PASS — 56 families / 368 items.
- Asset validator: PASS — includes shield texture/mixin/component checks.
- Set-effect validator: PASS — includes shield effect checks.
- Balance audit: PASS — 368 entries including all shields.
- Gradle build: BUILD SUCCESSFUL.

## Client-only checks

1. Confirm each custom shield uses a material-adapted base texture, not vanilla wood shield texture.
2. Test both normal and blocking shield poses.
3. Confirm enchanted glint still renders correctly.
4. Confirm banner decoration behavior, if used, still behaves acceptably.
5. Watch logs for atlas/missing texture errors under `minecraft:entity/shield/dream_equipment/*`.
6. Confirm multiplayer/server join is stable with the new synchronized item component.

## Notes

This is a targeted client rendering extension, but it is intentionally narrow:

- no custom shield geometry
- no custom renderer replacement
- no changes to vanilla banner pattern logic except replacing the selected base sprite for Dream Equipment shields

If any renderer conflicts appear, this feature can be isolated to the `ShieldSpecialRendererMixin` and the `shield_base_texture` component.
