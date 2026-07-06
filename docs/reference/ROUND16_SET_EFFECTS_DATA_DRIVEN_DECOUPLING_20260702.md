# Round 16 Set Effects Data-Driven Decoupling — 2026-07-02

## Scope

The user requested decoupling and data-driven behavior. This round starts with the most coupled system: set effects.

## What changed

### Added JSON rules

New file:

```text
src/main/resources/data/dream_equipment/set_effects.json
```

It owns:

- whether set effects are enabled
- passive full-set effects
- effect id / duration / amplifier / condition
- cactus retaliation damage per armor piece
- slime armor decay, damage-cancel chance, safe fall distance, bounce values, fall-heal ratio, slime-ball return counts
- wet durability rules such as paper armor decay in rain/water
- brittle set damage thresholds and shatter chances

### Added loader

New class:

```text
DreamEquipmentSetEffectRules
```

It loads `set_effects.json` at mod initialization and exposes `current()` rules to gameplay code. If loading fails, it falls back to safe built-in defaults.

### Decoupled set-effect logic

`DreamEquipmentSetEffects` no longer hardcodes most effect values and per-material passive effects. It now:

- iterates `passive_effects` from JSON
- resolves mob effects from namespaced ids such as `minecraft:luck`
- applies conditions (`always`, `in_water`, `wet`, `dry`)
- reads cactus/slime/brittle/wet-durability values from JSON

### Added validator

New script:

```text
scripts/validate_set_effects_json.py
```

It validates:

- referenced materials exist as equipment materials
- effect ids are namespaced
- conditions are valid
- durations and amplifiers are valid
- slime fields are non-negative and return counts include all armor pieces
- brittle chances are 0..1

## What remains hardcoded

This pass intentionally does not yet data-drive item registration/material stats. Those are registration-time values and need a separate `materials.json`/bootstrap strategy.

Still hardcoded for now:

- item/material registration families
- armor defense/durability/enchantability/toughness values
- tool material values
- exact redstone-signal implementation, still pending

## Validation

Executed:

```bash
python3 scripts/validate_dream_equipment_assets.py
python3 scripts/validate_set_effects_json.py
JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks
```

Results:

- Asset validator: PASS — 184 items, 37 materials.
- Set-effect JSON validator: PASS — 28 passive effects, 4 brittle entries.
- Build: PASS.

## Next decoupling targets

1. `materials.json` for registration-time material stats and family declarations.
2. `recipes/material_families` generator so resource generation is repeatable.
3. `set_effects.json` runtime reload support if desired.
4. Redstone boots power system as a separately designed mechanic.
