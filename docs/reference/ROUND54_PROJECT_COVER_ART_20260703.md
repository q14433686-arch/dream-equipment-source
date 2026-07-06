# Round 54 Project Cover Art — 2026-07-03

## Scope

Added the selected 2D minimal/logo-style Dream Equipment cover image as the official project cover asset.

The user selected the cover featuring:

- central shield/chestplate emblem
- crossed spear and pickaxe
- surrounding material icons
- title text `DREAM EQUIPMENT`
- Chinese subtitle `圆梦装备`

## Files added

The uploaded image was added in two places:

```text
docs/assets/dream_equipment_cover.png
src/main/resources/assets/dream_equipment/cover.png
```

Purpose:

- `docs/assets/dream_equipment_cover.png` — README/documentation/release presentation cover.
- `src/main/resources/assets/dream_equipment/cover.png` — packaged mod resource copy for distribution/archive completeness.

Image metadata:

```text
size: 1376×768
format: PNG
```

## README update

`README.md` now displays the cover near the top:

```markdown
![Dream Equipment cover](docs/assets/dream_equipment_cover.png)
```

It also notes the resource mirror path.

## Validator update

Updated:

```text
scripts/validate_dream_equipment_assets.py
```

The validator now checks:

- `docs/assets/dream_equipment_cover.png` exists.
- `src/main/resources/assets/dream_equipment/cover.png` exists.
- cover image dimensions are not unexpectedly small.

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
- Asset validator: PASS — includes cover image checks.
- Set-effect validator: PASS — includes shield effect checks.
- Balance audit: PASS — 368 entries including all shields.
- Gradle build: BUILD SUCCESSFUL.

## Output refresh

Because a packaged resource file was added, the release jar and source zip were refreshed:

```text
release_output/dream-equipment-0.1.0.jar
release_output/dream-equipment-source-current-20260703.zip
```

## Client-only checks

No gameplay client check is required for the cover image. Optional checks:

1. Confirm README cover renders correctly on GitHub/Modrinth-like pages.
2. Confirm packaged resource `assets/dream_equipment/cover.png` is present in the jar.
