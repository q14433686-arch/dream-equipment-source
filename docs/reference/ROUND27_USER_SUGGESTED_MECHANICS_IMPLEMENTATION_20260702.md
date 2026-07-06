# Round 27 User-Suggested Mechanics Implementation — 2026-07-02

## Scope

Implemented the concrete mechanics proposed by the user after the previous pass:

- armadillo shell boots should give Speed III on sand/red sand/gravel-style blocks
- prismarine pickaxe should gain underwater mining speed
- prismarine armor recipes should use nautilus shells
- prismarine pickaxe recipe should require Heart of the Sea
- redstone recipes should be made more expensive with redstone blocks + redstone dust
- paper armor water/rain durability loss should be much faster

## Changes

### Armadillo shell boots

`set_effects.json` now has:

```json
"armadillo_boots": {
  "enabled": true,
  "blocks": [
    "minecraft:sand",
    "minecraft:red_sand",
    "minecraft:gravel",
    "minecraft:suspicious_sand",
    "minecraft:suspicious_gravel"
  ],
  "effect": "minecraft:speed",
  "duration_ticks": 80,
  "amplifier": 2
}
```

`DreamEquipmentSetEffects` applies this when the player wears `armadillo_shell_boots` and stands on one of those blocks.

### Prismarine pickaxe underwater haste

`set_effects.json` now has a held item rule:

```json
"held_effects": [
  {
    "item": "dream_equipment:prismarine_pickaxe",
    "condition": "in_water",
    "effect": "minecraft:haste",
    "duration_ticks": 120,
    "amplifier": 1
  }
]
```

This gives Haste II while holding the prismarine pickaxe underwater.

### Prismarine recipes

`equipment_families.json` recipe overrides now make:

- `prismarine_pickaxe` require `minecraft:heart_of_the_sea`
- prismarine armor recipes include `minecraft:nautilus_shell`

### Redstone recipes

`equipment_families.json` recipe overrides now make redstone gear use a mix of:

- `minecraft:redstone_block`
- `minecraft:redstone`

instead of being made only from redstone dust.

### Paper wet durability

`set_effects.json` now changes paper armor wet/rain durability loss to:

- every 10 ticks
- 1 durability damage

This is much faster and should make paper armor properly weak to water/rain.

## Tooltip support

Tooltip generation was updated so:

- armadillo shell boots describe their sand/red sand/gravel speed effect
- held item effects such as prismarine pickaxe underwater Haste display on the tool

## Validation

Executed:

```bash
python3 scripts/generate_equipment_resources.py
python3 scripts/validate_equipment_families_json.py
python3 scripts/validate_set_effects_json.py
python3 scripts/validate_dream_equipment_assets.py
JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks
```

Results:

- generator drift check: PASS
- equipment families: PASS — 44 families / 236 items
- set effects: PASS
- assets: PASS — 236 items / 44 materials
- build: PASS

## Client-only checks

- Armadillo shell boots give Speed III on sand/red sand/gravel/suspicious sand/suspicious gravel.
- Prismarine pickaxe gives Haste II underwater.
- Prismarine pickaxe recipe requires Heart of the Sea.
- Prismarine armor recipes include nautilus shells.
- Redstone recipes use redstone blocks + dust.
- Paper armor decays quickly when wet/rained on.
