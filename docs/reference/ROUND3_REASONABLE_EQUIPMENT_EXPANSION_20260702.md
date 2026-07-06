# Round 3 Reasonable Equipment Expansion — 2026-07-02

## Scope

Added a broader set of reasonable vanilla-material equipment after the user requested items such as armadillo shell shoes and cactus armor.

## Added items

### Cactus armor set / 仙人掌套

- `dream_equipment:cactus_helmet`
- `dream_equipment:cactus_chestplate`
- `dream_equipment:cactus_leggings`
- `dream_equipment:cactus_boots`

Ingredient: `minecraft:cactus`.

Balance intent: low-to-mid desert novelty armor, weak but flavorful. This round only adds the base armor; special thorn/contact mechanics can be added later after client test.

### Armadillo shell shoes / 犰狳壳鞋

- `dream_equipment:armadillo_shell_boots`

Ingredient: `minecraft:armadillo_scute`.

Balance intent: a reasonable single armor piece made from scutes/shells, slightly stronger than leather boots.

### Bone armor set / 骨套

- `dream_equipment:bone_helmet`
- `dream_equipment:bone_chestplate`
- `dream_equipment:bone_leggings`
- `dream_equipment:bone_boots`

Ingredient: `minecraft:bone`.

Balance intent: skeleton-themed early/mid armor, roughly between stone and chainmail feel.

### Paper armor set / 纸套

- `dream_equipment:paper_helmet`
- `dream_equipment:paper_chestplate`
- `dream_equipment:paper_leggings`
- `dream_equipment:paper_boots`

Ingredient: `minecraft:paper`.

Balance intent: joke/novelty armor, very weak but enchantable.

### Glass armor set / 玻璃套

- `dream_equipment:glass_helmet`
- `dream_equipment:glass_chestplate`
- `dream_equipment:glass_leggings`
- `dream_equipment:glass_boots`

Ingredient: `minecraft:glass`.

Balance intent: fragile novelty armor with moderate visual identity. This round does not add shattering mechanics.

### Obsidian armor set / 黑曜石套

- `dream_equipment:obsidian_helmet`
- `dream_equipment:obsidian_chestplate`
- `dream_equipment:obsidian_leggings`
- `dream_equipment:obsidian_boots`

Ingredient: `minecraft:obsidian`.

Balance intent: heavy late-game armor, strong defense/toughness but low enchantability. This round does not add movement penalties.

## Resources added

For every new item:

- item definition
- item model
- generated material-style item texture
- recipe
- zh_cn/en_us lang key

For every new material:

- equipment definition
- humanoid/humanoid_baby/humanoid_leggings armor layer textures
- repair tag

## Validation

Executed:

```bash
python3 scripts/validate_dream_equipment_assets.py
JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks
```

Results:

- Asset validator: PASS — 42 items, 10 materials.
- Build: PASS.

## Client-only checks

- Confirm all 42 items appear and localize correctly.
- Confirm cactus/armadillo/bone/paper/glass/obsidian recipes work.
- Confirm worn armor textures look acceptable.
- Tune balance after playtest.
