# Round 33 Pickaxe Silhouette and Rock Tool Expansion — 2026-07-02

## Scope

Addressed user feedback that custom pickaxe inventory textures differed subtly from vanilla pickaxe shape, and that several rock variants should have shovel/hoe/tool coverage where material logic permits.

## Pickaxe texture fix

All custom pickaxe item textures were regenerated from the vanilla `diamond_pickaxe.png` silhouette, recolored per material.

This affects all existing custom pickaxes, including but not limited to:

- emerald
- lapis
- redstone
- amethyst
- prismarine
- mossy cobblestone
- cobbled deepslate
- end stone
- granite
- diorite
- andesite
- basalt

The same vanilla-template approach was also used for newly added shovels/hoes.

## Added rock tools

Added additional tools based on material logic:

- granite: added shovel and hoe, now has sword/pickaxe/axe/shovel/hoe/spear
- diorite: added shovel and hoe, now has sword/pickaxe/axe/shovel/hoe/spear
- andesite: added shovel and hoe, now has sword/pickaxe/axe/shovel/hoe/spear
- mossy cobblestone: added shovel
- sandstone: added shovel
- red sandstone: added shovel
- tuff: added shovel

Rationale:

- granite/diorite/andesite are common hard stone families and can support fuller stone-tool-like coverage
- sandstone/red sandstone are softer sedimentary materials, so shovel is reasonable, but hoe/full tools are not broadly added
- tuff is workable rough stone, so shovel was added but not full utility coverage
- mossy cobblestone receives shovel as a utility extension while remaining thematically rough

## Content totals

After this round:

- families: 56
- items: 312
- equipment materials: 56
- generator-managed files: 1125

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

- generator drift check: PASS — 1125 files
- equipment families: PASS — 56 families / 312 items
- assets: PASS — 312 items / 56 materials
- set effects: PASS
- build: PASS

## Client-only checks

- Compare custom pickaxes to vanilla pickaxe shape in inventory; silhouettes should now match.
- Check newly added shovels/hoes appear and use correct vanilla-like silhouettes.
- Test tool behavior for newly added AxeItem/ShovelItem/HoeItem registrations where applicable.
