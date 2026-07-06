#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RES=ROOT/'src/main/resources'
MOD='dream_equipment'
errors=[]
for src in ['src/main/java/com/dreamequipment/DreamEquipmentItems.java', 'src/main/java/com/dreamequipment/DreamEquipmentSetEffects.java', 'src/main/java/com/dreamequipment/DreamEquipmentFuelValues.java', 'src/main/java/com/dreamequipment/DreamEquipmentRedstonePower.java', 'src/main/java/com/dreamequipment/DreamEquipmentShieldEffects.java', 'src/main/java/com/dreamequipment/DreamEquipmentShieldEffectRules.java', 'src/main/java/com/dreamequipment/DreamEquipmentDataComponents.java', 'src/main/java/com/dreamequipment/mixin/ShieldSpecialRendererMixin.java', 'src/main/java/com/dreamequipment/mixin/RedStoneWireBlockMixin.java', 'src/main/java/com/dreamequipment/mixin/RedstoneWireEvaluatorMixin.java']:
    if not (ROOT/src).exists(): errors.append(f'missing {src}')

def require(p):
    if not p.exists(): errors.append(f'missing {p.relative_to(ROOT)}')

# The concrete item universe is resource-owned: every item texture must have model, item definition, recipe, and lang.
item_texture_dir=RES/f'assets/{MOD}/textures/item'
items=sorted(p.stem for p in item_texture_dir.glob('*.png') if not p.stem.endswith('_in_hand'))
# Exclude none for now; all item textures are registered game items.
for item in items:
    require(RES/f'assets/{MOD}/items/{item}.json')
    require(RES/f'assets/{MOD}/models/item/{item}.json')
    require(RES/f'data/{MOD}/recipe/{item}.json')

materials=sorted(p.stem for p in (RES/f'assets/{MOD}/equipment').glob('*.json'))
for mat in materials:
    require(RES/f'assets/{MOD}/textures/entity/equipment/humanoid/{mat}.png')
    require(RES/f'assets/{MOD}/textures/entity/equipment/humanoid_baby/{mat}.png')
    require(RES/f'assets/{MOD}/textures/entity/equipment/humanoid_leggings/{mat}_leggings.png')
    suffix='equipment' if mat == 'emerald' else 'armor'
    require(RES/f'data/{MOD}/tags/item/repairs_{mat}_{suffix}.json')

for lang in ['zh_cn','en_us']:
    p=RES/f'assets/{MOD}/lang/{lang}.json'; require(p)
    data=json.loads(p.read_text(encoding='utf-8'))
    for item in items:
        k=f'item.{MOD}.{item}'
        if k not in data: errors.append(f'{lang} missing {k}')




# Vanilla shield recipe is intentionally disabled to avoid conflicts with Dream Equipment plank shield recipes.
vanilla_shield_recipe=RES/'data/minecraft/recipe/shield.json'
require(vanilla_shield_recipe)
if vanilla_shield_recipe.exists():
    recipe_text=vanilla_shield_recipe.read_text(encoding='utf-8')
    if 'minecraft:barrier' not in recipe_text:
        errors.append('minecraft shield recipe override should require minecraft:barrier to disable vanilla shield crafting')

# Shield prototype resources are special-renderer based and do not require item textures.
family_json=RES/f'data/{MOD}/equipment_families.json'
if family_json.exists():
    family_data=json.loads(family_json.read_text(encoding='utf-8'))
    shield_items=[]
    for fam in family_data.get('families', []):
        shield=fam.get('shield')
        if shield and shield.get('enabled', True):
            shield_items.append(f"{fam.get('id')}_shield")
            if int(shield.get('durability', 0)) <= 0:
                errors.append(f"{fam.get('id')} shield durability must be >0")
    shield_texture_generator=ROOT/'scripts/generate_shield_textures.py'
    require(shield_texture_generator)
    for item in shield_items:
        require(RES/f'assets/{MOD}/items/{item}.json')
        require(RES/f'assets/{MOD}/models/item/{item}.json')
        require(RES/f'assets/{MOD}/models/item/{item}_blocking.json')
        require(RES/f'data/{MOD}/recipe/{item}.json')
        require(RES/f'assets/minecraft/textures/entity/shield/{MOD}/{item}_base_nopattern.png')
    if shield_items:
        source=ROOT/'src/main/java/com/dreamequipment/DreamEquipmentItems.java'
        components_source=ROOT/'src/main/java/com/dreamequipment/DreamEquipmentDataComponents.java'
        shield_mixin=ROOT/'src/main/java/com/dreamequipment/mixin/ShieldSpecialRendererMixin.java'
        require(components_source)
        require(shield_mixin)
        if source.exists():
            src=source.read_text(encoding='utf-8')
            for needle in ['new ShieldItem', 'DataComponents.BLOCKS_ATTACKS', 'equippableUnswappable', 'BannerPatternLayers.EMPTY', 'SHIELD_BASE_TEXTURE']:
                if needle not in src:
                    errors.append(f'DreamEquipmentItems.java missing shield marker {needle}')
        if components_source.exists():
            comp_src=components_source.read_text(encoding='utf-8')
            for needle in ['DATA_COMPONENT_TYPE', 'shield_base_texture', 'Identifier.CODEC']:
                if needle not in comp_src:
                    errors.append(f'DreamEquipmentDataComponents.java missing {needle}')
        if shield_mixin.exists():
            mix_src=shield_mixin.read_text(encoding='utf-8')
            for needle in ['ShieldSpecialRenderer', 'SHIELD_BASE_TEXTURE', 'Sheets.SHIELD_SHEET']:
                if needle not in mix_src:
                    errors.append(f'ShieldSpecialRendererMixin.java missing {needle}')
    shield_effects_source=ROOT/'src/main/java/com/dreamequipment/DreamEquipmentShieldEffects.java'
    shield_rules_source=ROOT/'src/main/java/com/dreamequipment/DreamEquipmentShieldEffectRules.java'
    require(shield_effects_source)
    require(shield_rules_source)
    if shield_effects_source.exists():
        shield_src=shield_effects_source.read_text(encoding='utf-8')
        for needle in ['ServerLivingEntityEvents.AFTER_DAMAGE', 'shieldMaterial', 'emitPulse', 'paper']:
            if needle not in shield_src:
                errors.append(f'DreamEquipmentShieldEffects.java missing {needle}')
    if shield_rules_source.exists() and 'shield_effects' not in shield_rules_source.read_text(encoding='utf-8'):
        errors.append('DreamEquipmentShieldEffectRules.java should load shield_effects')


# Project cover art used for README/release presentation.
require(ROOT/'docs/assets/dream_equipment_cover.png')
require(RES/f'assets/{MOD}/cover.png')
try:
    from PIL import Image
    for cover_path in [ROOT/'docs/assets/dream_equipment_cover.png', RES/f'assets/{MOD}/cover.png']:
        if cover_path.exists():
            with Image.open(cover_path) as im:
                if im.size[0] < 1000 or im.size[1] < 500:
                    errors.append(f'{cover_path.relative_to(ROOT)} cover image is unexpectedly small: {im.size}')
except Exception as ex:
    errors.append(f'cover image validation failed: {ex}')

# Current MC 26.1 equipment-layer spec and wood/log worn-layer generation guardrails.
wood_like_families=['oak','spruce','birch','jungle','acacia','dark_oak','mangrove','cherry','pale_oak','bamboo','crimson','warped','oak_log','spruce_log','birch_log','jungle_log','acacia_log','dark_oak_log','mangrove_log','cherry_log','pale_oak_log','bamboo_block','crimson_stem','warped_stem']
wood_worn_generator=ROOT/'scripts/generate_wood_worn_textures.py'
require(wood_worn_generator)
if wood_worn_generator.exists():
    generator_src=wood_worn_generator.read_text(encoding='utf-8')
    for needle in ['humanoid_baby', '64, 32', '64, 64', 'preserves the existing alpha/UV mask']:
        if needle not in generator_src:
            errors.append(f'generate_wood_worn_textures.py missing spec marker {needle}')
try:
    from PIL import Image
    for fam in wood_like_families:
        layer_specs=[('humanoid', f'{fam}.png', (64,32)), ('humanoid_leggings', f'{fam}_leggings.png', (64,32)), ('humanoid_baby', f'{fam}.png', (64,64))]
        for sub, filename, expected_size in layer_specs:
            p=RES/f'assets/{MOD}/textures/entity/equipment/{sub}/{filename}'
            require(p)
            if p.exists():
                with Image.open(p) as im:
                    if im.size != expected_size:
                        errors.append(f'{p.relative_to(ROOT)} size {im.size}, expected {expected_size}')
except Exception as ex:
    errors.append(f'wood worn layer image validation failed: {ex}')

# Minimum scope guard: this project should now contain the broad expansion batch.
if len(items) < 104: errors.append(f'expected at least 104 items, found {len(items)}')
if len(materials) < 17: errors.append(f'expected at least 17 armor materials, found {len(materials)}')
for required in ['cactus_helmet','armadillo_shell_boots','emerald_spear','lapis_sword','redstone_chestplate','quartz_spear','glass_spear','obsidian_sword','amethyst_pickaxe','prismarine_boots','slime_leggings','coal_helmet']:
    if required not in items: errors.append(f'missing expected item {required}')

# Vanilla handheld model parent for non-spear tools/weapons.
for suffix in ['sword','axe','pickaxe','shovel','hoe']:
    for item in [i for i in items if i.endswith('_' + suffix)]:
        model_path=RES/f'assets/{MOD}/models/item/{item}.json'
        if model_path.exists():
            data=json.loads(model_path.read_text(encoding='utf-8'))
            if data.get('parent') != 'minecraft:item/handheld':
                errors.append(f'{model_path.relative_to(ROOT)} should use minecraft:item/handheld')

# Cobblestone Chinese name must be 圆石, not 原石.
zh_path=RES/f'assets/{MOD}/lang/zh_cn.json'
if zh_path.exists():
    zh=json.loads(zh_path.read_text(encoding='utf-8'))
    for k,v in zh.items():
        if k.startswith(f'item.{MOD}.cobblestone_') and '原石' in v:
            errors.append(f'{k} uses 原石; should use 圆石')



# Redstone equipment should use a stateful virtual-source registry rather than one-off player scans.
redstone_source=ROOT/'src/main/java/com/dreamequipment/DreamEquipmentRedstonePower.java'
redstone_wire_mixin=ROOT/'src/main/java/com/dreamequipment/mixin/RedStoneWireBlockMixin.java'
mixin_json=RES/'dream_equipment.mixins.json'
if redstone_source.exists():
    redstone_src=redstone_source.read_text(encoding='utf-8')
    for needle in ['ACTIVE_PULSES', 'LAST_PLAYER_SOURCE', 'ServerTickEvents.END_SERVER_TICK', 'player.blockPosition()', 'notifyRedstoneAround']:
        if needle not in redstone_src:
            errors.append(f'DreamEquipmentRedstonePower.java missing {needle}')
if redstone_source.exists() and 'player.blockPosition().below()' in redstone_source.read_text(encoding='utf-8'):
    errors.append('DreamEquipmentRedstonePower.java should not use blockPosition().below() as the redstone source')
if redstone_wire_mixin.exists() and 'getBlockSignal' not in redstone_wire_mixin.read_text(encoding='utf-8'):
    errors.append('RedStoneWireBlockMixin.java should inject getBlockSignal')
if mixin_json.exists():
    mixin_text=mixin_json.read_text(encoding='utf-8')
    if 'RedStoneWireBlockMixin' not in mixin_text:
        errors.append('dream_equipment.mixins.json missing RedStoneWireBlockMixin')
    if 'RedstoneWireEvaluatorMixin' not in mixin_text:
        errors.append('dream_equipment.mixins.json missing RedstoneWireEvaluatorMixin')
    if 'ShieldSpecialRendererMixin' not in mixin_text:
        errors.append('dream_equipment.mixins.json missing ShieldSpecialRendererMixin')

# Fuel registration should remain data-driven through equipment_families.json.
fuel_source=ROOT/'src/main/java/com/dreamequipment/DreamEquipmentFuelValues.java'
family_json=RES/f'data/{MOD}/equipment_families.json'
if fuel_source.exists():
    fuel_src=fuel_source.read_text(encoding='utf-8')
    for needle in ['FuelValueEvents.BUILD', 'fuelBurnTimePerMaterial()', 'armorMaterialCount(piece)']:
        if needle not in fuel_src:
            errors.append(f'DreamEquipmentFuelValues.java missing {needle}')
if family_json.exists():
    fam_data=json.loads(family_json.read_text(encoding='utf-8'))
    fuel_fams={f.get('id') for f in fam_data.get('families', []) if int(f.get('fuel_burn_time_per_material', 0)) > 0}
    for required in ['coal','oak','spruce','birch','jungle','acacia','dark_oak','mangrove','cherry','pale_oak','bamboo','crimson','warped','oak_log','spruce_log','birch_log','jungle_log','acacia_log','dark_oak_log','mangrove_log','cherry_log','pale_oak_log','bamboo_block','crimson_stem','warped_stem']:
        if required not in fuel_fams:
            errors.append(f'{required} should declare positive fuel_burn_time_per_material')

# Source sanity: axe/shovel/hoe must use the specialized vanilla item classes.
items_source=ROOT/'src/main/java/com/dreamequipment/DreamEquipmentItems.java'
if items_source.exists():
    src=items_source.read_text(encoding='utf-8')
    for needle in ['new AxeItem', 'new ShovelItem', 'new HoeItem']:
        if needle not in src:
            errors.append(f'DreamEquipmentItems.java missing {needle}')

# Spear models must follow vanilla 26.1 render-vs-in-hand split.
spears=[item for item in items if item.endswith('_spear')]
for spear in spears:
    require(RES/f'assets/{MOD}/models/item/{spear}_in_hand.json')
    require(RES/f'assets/{MOD}/textures/item/{spear}_in_hand.png')
    item_def=RES/f'assets/{MOD}/items/{spear}.json'
    if item_def.exists() and 'display_context' not in item_def.read_text(encoding='utf-8'):
        errors.append(f'{item_def.relative_to(ROOT)} does not use display_context split for spear')

# Vanilla/common item tags for animation/combat compatibility.
def check_tag_file(tag_path):
    require(tag_path)
    if tag_path.exists():
        data=json.loads(tag_path.read_text(encoding='utf-8'))
        if data.get('replace') is not False:
            errors.append(f'{tag_path.relative_to(ROOT)} must use replace=false')
        if not data.get('values'):
            errors.append(f'{tag_path.relative_to(ROOT)} has no values')

for tag in ['swords','axes','pickaxes','shovels','hoes','spears']:
    for ns in ['minecraft', 'c', 'fabric', 'forge']:
        paths=[RES/f'data/{ns}/tags/item/{tag}.json']
        if ns in ['c', 'fabric', 'forge']:
            paths.append(RES/f'data/{ns}/tags/item/tools/{tag}.json')
        for tag_path in paths:
            check_tag_file(tag_path)
for tag in ['tools', 'weapons', 'melee_weapons']:
    for ns in ['c', 'fabric', 'forge']:
        check_tag_file(RES/f'data/{ns}/tags/item/{tag}.json')

if errors:
    print('\n'.join(errors)); raise SystemExit(1)
print(f'Dream Equipment assets OK — items={len(items)}, materials={len(materials)}')
