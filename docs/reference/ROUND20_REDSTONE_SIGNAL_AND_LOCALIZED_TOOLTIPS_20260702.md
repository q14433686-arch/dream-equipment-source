# Round 20 Redstone Signal + Localized Data-Driven Tooltips — 2026-07-02

## Scope

User chose A+B:

- A: redstone boots / redstone set should output real redstone signal.
- B: tooltip polish/localization after the data-driven tooltip pass.

## Redstone signal implementation

### Data

`set_effects.json` now contains:

```json
"redstone_signal": {
  "enabled": true,
  "boots_signal": 7,
  "full_set_signal": 15
}
```

### Java

Added:

- `DreamEquipmentRedstonePower`
- `SignalGetterMixin`
- `dream_equipment.mixins.json`

`SignalGetterMixin` injects into 26.1 `SignalGetter#getSignal` and `SignalGetter#getDirectSignal`. If a server player is standing on a block while wearing redstone boots/full redstone set, that block can report an additional redstone signal.

Current rule:

- wearing `redstone_boots`: block below the player outputs signal strength 7
- wearing full redstone armor: block below the player outputs signal strength 15

`DreamEquipmentSetEffects` also notifies neighboring blocks around the player every 2 ticks while a redstone signal is active so redstone dust/components can update.

## Tooltip localization polish

### Data source

Tooltips still read from:

- `equipment_families.json`
- `set_effects.json`

### Lang templates

The resource generator now writes material translation keys and tooltip sentence templates into:

- `zh_cn.json`
- `en_us.json`

Examples:

- `material.dream_equipment.emerald`
- `tooltip.dream_equipment.material`
- `tooltip.dream_equipment.armor`
- `tooltip.dream_equipment.effect`
- `tooltip.dream_equipment.redstone_signal`

`DreamEquipmentTooltips` now uses `Component.translatable(...)` instead of hardcoded Chinese literal sentences for headers/templates/tool names/material names. Vanilla effect display names use vanilla translation keys such as `effect.minecraft.luck`.

## Validation

Executed:

```bash
python3 scripts/generate_equipment_resources.py
python3 scripts/validate_equipment_families_json.py
python3 scripts/validate_dream_equipment_assets.py
python3 scripts/validate_set_effects_json.py
JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks
```

Results:

- Generator drift check: PASS.
- `equipment_families` validator: PASS — 37 families, 184 items.
- asset validator: PASS — 184 items, 37 materials.
- set-effect validator: PASS — 28 passive effects, 4 brittle entries.
- build: PASS.

## Client-only checks

- Confirm game starts with the new mixin.
- Put redstone dust/repeater next to the block under a player wearing redstone boots; signal should be 7.
- Wear full redstone armor; signal should be 15.
- Move away; redstone should update off.
- Confirm tooltips display in zh/en templates and show redstone signal info on redstone boots.

## Known limitation

This is the first redstone-power implementation. It powers the block below the player through signal query injection. If some specific redstone component does not react, a follow-up may need to target that component's exact signal query/update path.
