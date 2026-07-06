# Round 41 Redstone Wire Evaluator Mixin — 2026-07-03

## Scope

Client feedback after the step-pulse rework: the pulse effect itself worked, but redstone wire lines still did not activate reliably.

This pass keeps the short-lived redstone pulse design and adds a more direct hook into vanilla redstone wire power evaluation.

## Root cause

The previous pass injected into `RedStoneWireBlock#getBlockSignal` and broad `SignalGetter` query methods. However, vanilla 26.1.2 redstone wire updates route through `RedstoneWireEvaluator` / `DefaultRedstoneWireEvaluator` / `ExperimentalRedstoneWireEvaluator` during wire power recalculation.

Even if a virtual pulse exists, a redstone wire line may fail to update unless the evaluator's block-signal calculation sees that pulse while computing the wire's target power.

## Change

Added:

```text
src/main/java/com/dreamequipment/mixin/RedstoneWireEvaluatorMixin.java
```

This injects into:

```text
RedstoneWireEvaluator#getBlockSignal(Level, BlockPos)
```

and raises the returned block signal to include `DreamEquipmentRedstonePower.bestNeighborSignalAt(level, pos)`.

The existing `RedStoneWireBlockMixin` remains in place, but this new evaluator-level mixin targets the exact path vanilla wire lines use when deciding their own `POWER` value.

## Files changed

- `src/main/java/com/dreamequipment/mixin/RedstoneWireEvaluatorMixin.java`
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

1. Put a redstone dust line beside the player.
2. Equip redstone boots; the adjacent dust should receive the pulse and the line should propagate it.
3. Step along a dust line; each new block position should pulse the line.
4. Confirm the line turns off after pulse expiry.
5. Compare boot-only pulse and full-set pulse.

## If this still fails

The next fallback should not be another broad signal-query patch. Instead, directly pulse nearby redstone wire block states for the configured pulse duration, with careful expiry/recalculation safeguards to avoid breaking external redstone sources.
