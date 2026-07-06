# Round 35 Durability and Mining Tier Audit — 2026-07-02

## Scope

Audited all added equipment for durability and mining-tier reasonableness, adjusted clearly unreasonable values, and changed tooltip display so armor durability shows actual max durability instead of the internal durability multiplier.

## Main balance changes

### Tool durability / mining tier changes

Changed values in `equipment_families.json`:

- `glass` tools: durability lowered to 64, mining tier lowered to stone-like. Glass weapons are brittle/novelty and should not be 384-durability iron-tier tools.
- `quartz` tools: durability lowered to 220, mining tier lowered to stone-like. Quartz is hard but brittle and should not behave like a durable iron-tier material.
- `bone` tools: durability lowered to 160. Bone is light and brittle; it should not outlast stone variants by much.
- `cactus` spear: durability lowered to 80.
- `calcite` tools: durability lowered to 100.
- `netherrack` spear: durability lowered to 64 and kept weak/wood-like.
- `amethyst` tools: durability lowered to 640 and mining tier lowered from diamond-like to iron-like. Amethyst is valuable/magical but accessible and brittle; it should not be full diamond-tier utility.
- `end_stone` tools: durability lowered to 520 and mining tier lowered from diamond-like to iron-like. End stone is late-game but should not become a diamond-tier progression bypass.
- `granite`, `diorite`, `andesite`, `tuff`, `mossy_cobblestone`, `cobbled_deepslate`, `basalt`, `smooth_basalt`, `dripstone_block`: retuned as stone-tier variants with durability based on material density/role.
- `obsidian` weapons remain 120 durability with diamond-like damage and diamond-tier weapon material, per user direction.
- `emerald` remains diamond-tier-ish because its armor recipes were made expensive with emerald blocks.
- `prismarine` remains iron-tier with high durability because its pickaxe now requires Heart of the Sea and armor recipes include nautilus shells.
- `redstone` remains gold-like: low durability, high speed/enchantability.
- `lapis` remains iron-tier but durability adjusted to 420, emphasizing enchantment economy rather than raw durability.

## Tooltip display fix

Previously armor tooltip displayed durability multiplier, e.g. `耐久倍率`. That is not the actual in-game max durability shown by the item.

Now armor tooltip displays actual max durability using the vanilla 26.1 armor formula:

```text
helmet     = 11 × durability_multiplier
chestplate = 16 × durability_multiplier
leggings   = 15 × durability_multiplier
boots      = 13 × durability_multiplier
```

Updated tooltip lang text:

- zh_cn: `护甲：%s  耐久：%s`
- en_us: `Armor: %s  Durability: %s`

`DreamEquipmentTooltips` now computes actual armor durability per piece through `armorDurability(piece, multiplier)`.

Tool tooltip already displays actual tool durability directly from `equipment_families.json`, which is the same value used by `ToolMaterial` registration.

## Added audit script

New script:

```text
scripts/audit_equipment_balance.py
```

It prints a durability/mining-tier summary and checks:

- armor durability display uses actual max durability formula, not multiplier text
- tooltip source computes actual armor durability
- specific guardrail values for brittle/stone/obsidian materials
- mining tier tags are known
- durability values are positive

## Current audited tool summary

Important examples after rebalance:

- emerald: durability 1248, diamond tier, speed 7.5, attack bonus 2.5
- obsidian: durability 120, diamond tier, speed 8.0, attack bonus 3.0, 5% break chance on hit
- glass: durability 64, stone tier, speed 5.0, attack bonus 2.0
- quartz: durability 220, stone tier, speed 5.8, attack bonus 1.8
- amethyst: durability 640, iron tier, speed 6.8, attack bonus 2.2
- end stone: durability 520, iron tier, speed 5.8, attack bonus 2.0
- prismarine: durability 720, iron tier, speed 7.0, attack bonus 2.4
- redstone: durability 96, gold-like tier, speed 11.0, attack bonus 0.5

## Validation

Executed:

```bash
python3 scripts/audit_equipment_balance.py
python3 scripts/validate_equipment_families_json.py
python3 scripts/validate_dream_equipment_assets.py
python3 scripts/validate_set_effects_json.py
JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks
```

Results:

- balance audit: PASS
- equipment families: PASS — 56 families / 312 items
- assets: PASS — 312 items / 56 materials
- set effects: PASS — 24 passive effects / 4 brittle entries
- build: PASS

## Client-only checks

- Hover armor pieces and confirm tooltip durability equals actual max durability bar value.
- Confirm tool durability feels reasonable in survival testing.
- Confirm reduced mining tiers do not allow stone-like tools to mine unintended high-tier ores.
- Confirm obsidian weapons are high-damage but short-lived and brittle.
