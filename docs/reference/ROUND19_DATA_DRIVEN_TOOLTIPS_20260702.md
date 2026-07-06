# Round 19 Data-Driven Tooltips — 2026-07-02

## Scope

Implemented the recommended tooltip stage after decoupling. Tooltips are generated at runtime from the same JSON tables that drive registration and set-effect logic.

## Added client entrypoint

Updated `fabric.mod.json` with a client entrypoint:

```json
"client": ["com.dreamequipment.client.DreamEquipmentClient"]
```

New class:

```text
src/main/java/com/dreamequipment/client/DreamEquipmentClient.java
```

It loads the JSON tables on the client and registers tooltip callbacks.

## Added tooltip implementation

New class:

```text
src/main/java/com/dreamequipment/client/DreamEquipmentTooltips.java
```

Uses Fabric's `ItemTooltipCallback`.

## Data sources

Tooltips read from:

```text
data/dream_equipment/equipment_families.json
```

and:

```text
data/dream_equipment/set_effects.json
```

## Tooltip content

For armor:

- material name
- armor value for that piece
- durability multiplier
- toughness / knockback resistance if non-zero
- enchantability
- set effects / drawbacks / brittleness / wet weakness where applicable

For tools:

- material name
- tool type
- durability
- mining speed
- attack damage bonus
- enchantability

For set mechanics:

- passive effects with condition labels
- cactus per-piece retaliation
- slime set durability decay / slime-ball return / damage cancel / slime boots fall bounce
- armadillo shell boots fall mitigation
- paper wet/rain durability weakness
- brittle set shatter chance and damage threshold

## Notes

The tooltip text is currently Chinese literal text assembled from JSON values. It is already data-driven in terms of content and values, but future polish could move the sentence templates themselves into lang keys.

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

- Hover armor pieces and confirm material/stat/effect text appears.
- Hover tools and confirm tool stats appear.
- Confirm tooltip text is not too long or visually cluttered.
- Confirm Chinese wording is acceptable; later pass can add lang-template localization if desired.
