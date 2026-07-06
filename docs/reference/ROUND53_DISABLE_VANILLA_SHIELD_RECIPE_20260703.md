# Round 53 Disable Vanilla Shield Recipe — 2026-07-03

## Scope

Disabled the vanilla `minecraft:shield` crafting recipe because it conflicts with Dream Equipment plank shield recipes.

The client test showed the current custom shields work, but vanilla's broad shield recipe competes with custom plank shields because vanilla accepts generic wooden material inputs. The user requested disabling the vanilla recipe.

## Change

Added an override at:

```text
src/main/resources/data/minecraft/recipe/shield.json
```

The override keeps the same recipe id as vanilla:

```text
minecraft:shield
```

but changes it to require `minecraft:barrier` in every slot:

```json
{
  "type": "minecraft:crafting_shaped",
  "category": "equipment",
  "pattern": [
    "BBB",
    "BBB",
    "BBB"
  ],
  "key": {
    "B": "minecraft:barrier"
  },
  "result": {
    "id": "minecraft:shield"
  }
}
```

This effectively disables survival crafting of the vanilla shield while leaving the vanilla item itself available for worlds/loot/commands/compatibility.

## Why this approach

- It avoids changing/removing the vanilla shield item.
- It avoids recipe conflicts with custom plank shields.
- It is a data/resource override only, not a Java hardcode.
- It can be reverted cleanly by deleting the override.

## Not changed

The vanilla shield decoration recipe was not disabled:

```text
data/minecraft/recipe/shield_decoration.json
```

That recipe targets `minecraft:shield` specifically and does not conflict with custom shield recipes.

## Validator update

Updated:

```text
scripts/validate_dream_equipment_assets.py
```

The validator now checks that the vanilla shield recipe override exists and contains `minecraft:barrier`.

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
- Asset validator: PASS — includes vanilla shield recipe override check.
- Set-effect validator: PASS — includes shield effect checks.
- Balance audit: PASS — 368 entries including all shields.
- Gradle build: BUILD SUCCESSFUL.

## Client-only checks

1. Confirm crafting with vanilla shield recipe shape no longer produces `minecraft:shield`.
2. Confirm Dream Equipment plank shield recipes still produce the intended custom shields.
3. Confirm recipe book no longer offers a normal vanilla shield recipe in survival progression.
4. Confirm existing vanilla shields in worlds/inventory remain valid items.
