# Round 40 Redstone Step Pulse Mechanic — 2026-07-03

## Scope

Changed redstone equipment from a continuous virtual redstone-block source into a short-lived step/equip pulse mechanic.

This follows the design decision made after the virtual redstone-block approach remained conceptually risky: continuous player-based redstone sources are difficult to make completely consistent with vanilla redstone dust, movement, equipment changes, logout, dimension changes, and neighbor update timing.

## Design change

Previous model:

```text
while wearing redstone boots/full set, behave like a continuous virtual redstone block at the player's feet-space
```

New model:

```text
when the player equips redstone boots/full set, changes signal strength, or steps into a new block position, emit a short redstone pulse at the player's feet-space
```

The pulse expires automatically after a small configured duration, so stale permanent redstone signals are avoided by design.

## JSON-owned values

`set_effects.json` now has pulse timing values under `redstone_signal`:

```json
"redstone_signal": {
  "enabled": true,
  "boots_signal": 7,
  "full_set_signal": 15,
  "boots_pulse_ticks": 8,
  "full_set_pulse_ticks": 12
}
```

Meaning:

- Redstone boots emit a signal strength 7 pulse lasting 8 ticks.
- Full redstone set emits a signal strength 15 pulse lasting 12 ticks.

## Implementation details

`DreamEquipmentRedstonePower` now owns:

```text
ACTIVE_PULSES: Map<ServerLevel, Map<BlockPos, Pulse>>
LAST_PLAYER_SOURCE: Map<UUID, SourceState>
```

Each server tick:

1. Expire old pulses and notify redstone around expired positions.
2. Scan online players.
3. Compute redstone equipment signal from JSON values.
4. If the player's active source state changed — new position, newly equipped, removed/re-equipped, or boot/full-set strength changed — add a pulse at `player.blockPosition()`.
5. Notify redstone around the pulse position.
6. Remove last-player state for inactive/offline players.

`SignalGetterMixin` and `RedStoneWireBlockMixin` still query the active pulse map, but there is no permanent source to get stuck.

## Why this is safer

- Removing boots does not need to actively clear a continuous source; any active pulse expires naturally.
- Walking away leaves only a short pulse behind, not an indefinite signal.
- Logout/dimension-change/death cannot leave a permanent active source because active redstone output is time-limited.
- Redstone dust recalculation can still see active pulses through `RedStoneWireBlockMixin#getBlockSignal`.

## Tooltip update

Updated localized tooltip text:

- zh_cn: `红石脉冲：靴子 %s 强度/%s tick，整套 %s 强度/%s tick`
- en_us: `Redstone pulse: boots %s power/%s ticks, full set %s power/%s ticks`

## Files changed

- `src/main/java/com/dreamequipment/DreamEquipmentRedstonePower.java`
- `src/main/java/com/dreamequipment/DreamEquipmentSetEffectRules.java`
- `src/main/java/com/dreamequipment/client/DreamEquipmentTooltips.java`
- `src/main/resources/data/dream_equipment/set_effects.json`
- `scripts/generate_equipment_resources.py`
- `scripts/validate_set_effects_json.py`
- `scripts/validate_dream_equipment_assets.py`
- generated lang files

## Validation

Executed:

```bash
python3 scripts/generate_equipment_resources.py --write
python3 scripts/generate_equipment_resources.py
python3 scripts/validate_equipment_families_json.py
python3 scripts/validate_dream_equipment_assets.py
python3 scripts/validate_set_effects_json.py
python3 scripts/audit_equipment_balance.py
JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks
```

Results:

- Generator write/check: PASS — 1125 generated resources in sync.
- Equipment family validator: PASS — 56 families / 312 items.
- Asset validator: PASS — 312 items / 56 materials.
- Set-effect validator: PASS — 24 passive entries / 4 brittle entries.
- Balance audit: PASS.
- Gradle build: BUILD SUCCESSFUL.

## Client-only checks

1. Equip redstone boots beside dust: dust should briefly pulse, not remain permanently powered.
2. Walk from one block to another beside dust/repeaters: each step should emit a pulse.
3. Remove boots while a pulse is active: any signal should disappear after the configured short duration.
4. Compare boots-only pulse and full-set pulse strength/duration.
5. Confirm redstone lamps/repeaters next to the player's feet-space can see the pulse.
6. Confirm no stale signal remains after logout/dimension change/death.

## Future tuning

If pulse duration feels too short or too long, tune only these JSON values:

```json
"boots_pulse_ticks": 8,
"full_set_pulse_ticks": 12
```

No Java change is required unless the trigger model itself changes.
