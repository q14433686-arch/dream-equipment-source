# Round 18 Resource Generator and Drift Check — 2026-07-02

## Scope

This is round 2 of 2 for the requested full decoupling/data-driven work.

Round 1 moved registration-time family/material data into `equipment_families.json` and made Java registration read that JSON. This round adds deterministic resource generation from the same JSON.

## Added generator

New script:

```text
scripts/generate_equipment_resources.py
```

It reads:

```text
src/main/resources/data/dream_equipment/equipment_families.json
```

and generates/checks:

- item definitions: `assets/dream_equipment/items/*.json`
- item models: `assets/dream_equipment/models/item/*.json`
- spear render/in-hand split item definitions and models
- equipment definitions: `assets/dream_equipment/equipment/*.json`
- recipes: `data/dream_equipment/recipe/*.json`
- repair tags: `data/dream_equipment/tags/item/repairs_*.json`
- vanilla/common/fabric/forge tool tags
- aggregate `tools`, `weapons`, `melee_weapons` tags
- zh_cn and en_us item lang keys

## Usage

Write/regenerate resources:

```bash
python3 scripts/generate_equipment_resources.py --write
```

Drift check only:

```bash
python3 scripts/generate_equipment_resources.py
```

If any generated file differs from what the JSON says, the check mode exits non-zero and lists out-of-date/missing files.

## Data-driven naming override

`equipment_families.json` now supports armor language overrides. It is currently used for:

```json
"armadillo_shell": {
  "zh_overrides": { "boots": "犰狳壳鞋" },
  "en_overrides": { "boots": "Armadillo Shell Shoes" }
}
```

This preserves the user-requested `犰狳壳鞋` name instead of mechanically producing `犰狳壳靴子`.

## Generated output status

Generator output count:

- 687 managed resource files
- 37 equipment families
- 184 concrete registered items

## Validation

Executed:

```bash
python3 scripts/generate_equipment_resources.py --write
python3 scripts/generate_equipment_resources.py
python3 scripts/validate_equipment_families_json.py
python3 scripts/validate_dream_equipment_assets.py
python3 scripts/validate_set_effects_json.py
JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks
```

Results:

- Generator write: PASS — 687 files written.
- Generator drift check: PASS — resources in sync.
- `equipment_families` validator: PASS — 37 families, 184 items.
- asset validator: PASS — 184 items, 37 materials.
- set-effect validator: PASS — 28 passive effects, 4 brittle entries.
- build: PASS.

## Completed decoupling state

After rounds 16–18:

- `set_effects.json` owns set-effect behavior values.
- `equipment_families.json` owns equipment families and registration-time stats.
- Java registration loops over JSON family data.
- Generated resource files can be refreshed and checked deterministically.

Future additions should generally be:

1. edit `equipment_families.json`
2. run `python3 scripts/generate_equipment_resources.py --write`
3. add/update textures where needed
4. run validators/build

## Remaining future work

- Texture generation is still partly script/manual and not fully described in `equipment_families.json`.
- Runtime `/reload` support is not implemented; these JSON files are startup-loaded for now.
- Redstone boots real redstone signal output is still a separate mechanic task.
