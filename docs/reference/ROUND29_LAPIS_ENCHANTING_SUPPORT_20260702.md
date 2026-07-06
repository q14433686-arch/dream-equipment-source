# Round 29 Lapis Enchanting Support — 2026-07-02

## Scope

Implemented the previously deferred lapis equipment enchanting mechanic.

## Behavior

When a player successfully enchants through the vanilla enchanting table while wearing any lapis armor piece:

- the vanilla lapis lazuli cost is refunded after the enchant succeeds
- lapis armor takes extra durability damage as the conversion cost
- no full set is required

Current durability cost:

- 12 durability per lapis lazuli refunded
- damage is distributed across worn lapis armor pieces

This implements the intended “almost fully offset lapis cost through lapis equipment durability” behavior while keeping the vanilla enchanting flow stable.

## Implementation

Added:

- `DreamEquipmentEnchantingSupport`
- `EnchantmentMenuAccessor`
- `EnchantmentMenuMixin`

Mixin target:

- `EnchantmentMenu#clickMenuButton`

The mixin runs after a successful vanilla enchantment transaction, refunds the lapis amount that vanilla consumed, and damages worn lapis armor.

## Tooltip

Lapis armor tooltip now includes:

- zh_cn: `附魔：返还青金石消耗，但额外损耗青金石装备耐久`
- en_us: `Enchanting: refunds lapis cost, but damages lapis equipment`

## Validation

Executed:

```bash
python3 scripts/generate_equipment_resources.py --write
python3 scripts/generate_equipment_resources.py
python3 scripts/validate_equipment_families_json.py
python3 scripts/validate_set_effects_json.py
python3 scripts/validate_dream_equipment_assets.py
JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks
```

Results:

- generator write/check: PASS
- equipment families: PASS — 56 families / 284 items
- set effects: PASS — 24 passive effects / 4 brittle entries
- assets: PASS — 284 items / 56 materials
- build: PASS

## Client-only checks

- Wear one lapis armor piece.
- Put lapis into enchanting table.
- Enchant an item.
- Confirm lapis is refunded after successful enchant.
- Confirm worn lapis armor durability decreases.
- Confirm no refund occurs with no lapis armor.
