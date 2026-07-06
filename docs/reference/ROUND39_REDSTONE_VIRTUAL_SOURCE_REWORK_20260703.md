# Round 39 Redstone Virtual Source Rework — 2026-07-03

## Scope

Reworked the redstone equipment power mechanic after client feedback that the previous implementation was conceptually awkward and unreliable:

- redstone signal could stay active after leaving/removing boots,
- redstone dust could fail to update or fail to see the virtual source,
- the implementation tried to make a player-scanned block-below signal behave like a redstone block, which was not a good fit for redstone dust placement.

## Root cause

The old implementation queried player equipment directly inside `SignalGetterMixin` and treated `player.blockPosition().below()` as the powered block. That produced two problems:

1. **Wrong virtual source position for dust beside the player.**
   Redstone dust on the floor beside a player is usually at the player's feet Y-level, while `player.blockPosition().below()` is the floor block below. That makes the virtual source diagonal to the dust instead of directly adjacent in redstone terms.

2. **Notification/state cleanup was event-like instead of stateful.**
   The old notifier remembered per-player previous positions in `DreamEquipmentSetEffects`. If a player changed dimension, left, became spectator/creative, moved during an edge case, or equipment state changed without the right update path, wire block states could fail to recalculate.

## New model

Redstone equipment now uses a stateful virtual redstone-block source registry.

- `DreamEquipmentRedstonePower` rebuilds the active virtual source map every server tick.
- Active source position is now `player.blockPosition()` — the player's feet-space — instead of the block below the player.
- Signal values still come from JSON-owned `set_effects.json`:
  - boots: `boots_signal`
  - full set: `full_set_signal`
- When active sources are added, removed, moved, or signal strength changes, neighboring redstone blocks/wires are notified around the old and new source positions.
- If no player currently provides a source, no stale source remains in the registry.

## Implementation changes

### `DreamEquipmentRedstonePower`

Changed from player-scan-on-query to a server-tick rebuilt source map:

```text
Map<ServerLevel, Map<BlockPos, Integer>> ACTIVE_SOURCES
```

Every server tick:

1. Read all online players.
2. Compute redstone signal from equipped redstone boots/full set.
3. Put a virtual source at `player.blockPosition()`.
4. Compare previous and next source maps.
5. Notify redstone updates around changed/removed/added positions.
6. Replace active source map.

### `RedStoneWireBlockMixin`

Added a direct mixin into `RedStoneWireBlock#getBlockSignal` so redstone dust power recalculation explicitly includes the virtual redstone source neighbors.

This supplements the existing `SignalGetterMixin` and makes dust updates less dependent on indirect vanilla query paths.

### `DreamEquipmentSetEffects`

Removed old redstone notification bookkeeping from set-effect ticking. Redstone source updates are now owned by `DreamEquipmentRedstonePower`, matching the architecture rule that Java owns mechanics/sync/registration/event behavior while JSON owns signal values.

## Current behavior target

Redstone equipment should behave like a virtual redstone block occupying the player's feet-space:

- Redstone boots emit the configured boot signal.
- Full redstone armor emits the configured full-set signal.
- Dust/repeaters beside the player should update when the source appears, moves, disappears, or changes strength.
- Removing boots/full set should clear the virtual source on the next server tick and notify surrounding redstone.
- Walking away should notify the previous and new source areas so dust can turn off behind the player.

## Files changed

- `src/main/java/com/dreamequipment/DreamEquipmentRedstonePower.java`
- `src/main/java/com/dreamequipment/DreamEquipment.java`
- `src/main/java/com/dreamequipment/DreamEquipmentSetEffects.java`
- `src/main/java/com/dreamequipment/mixin/RedStoneWireBlockMixin.java`
- `src/main/resources/dream_equipment.mixins.json`
- `scripts/validate_dream_equipment_assets.py`

## Validation

Executed:

```bash
python3 scripts/generate_equipment_resources.py
python3 scripts/validate_equipment_families_json.py
python3 scripts/validate_dream_equipment_assets.py
python3 scripts/validate_set_effects_json.py
python3 scripts/audit_equipment_balance.py
JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks
```

Results:

- Generator drift check: PASS — 1125 generated resources in sync.
- Equipment family validator: PASS — 56 families / 312 items.
- Asset validator: PASS — 312 items / 56 materials.
- Set-effect validator: PASS — 24 passive entries / 4 brittle entries.
- Balance audit: PASS.
- Gradle build: BUILD SUCCESSFUL.

## Client-only checks

1. Put redstone dust beside the player and equip redstone boots; dust should power.
2. Remove redstone boots; dust should turn off within one tick/update.
3. Walk away while wearing boots; dust behind the player should turn off and dust near the new position should update.
4. Compare boot-only signal and full-set signal.
5. Test repeaters/comparators/lamps adjacent to the player's feet-space.
6. Test dimension change/logout/death if possible to confirm no stale source remains.

## Notes

This pass intentionally keeps the mechanic as a virtual redstone-block source rather than placing/removing real blocks. It avoids griefing/world-state mutation while giving redstone components a stable, queryable source.
