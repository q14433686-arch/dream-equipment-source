#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / 'src/main/resources'
MOD = 'dream_equipment'
FAMILY_JSON = RES / f'data/{MOD}/equipment_families.json'

ZH_PIECES = {'helmet':'头盔','chestplate':'胸甲','leggings':'护腿','boots':'靴子'}
EN_PIECES = {'helmet':'Helmet','chestplate':'Chestplate','leggings':'Leggings','boots':'Boots'}
TOOL_ZH = {'sword':'剑','pickaxe':'镐','axe':'斧','shovel':'锹','hoe':'锄','spear':'矛'}
TOOL_EN = {'sword':'Sword','pickaxe':'Pickaxe','axe':'Axe','shovel':'Shovel','hoe':'Hoe','spear':'Spear'}
ARMOR_PATTERNS = {
    'helmet': ['MMM','M M'],
    'chestplate': ['M M','MMM','MMM'],
    'leggings': ['MMM','M M','M M'],
    'boots': ['M M','M M'],
}
TOOL_PATTERNS = {
    'sword': ['M','M','S'],
    'pickaxe': ['MMM',' S ',' S '],
    'axe': ['MM','MS',' S'],
    'shovel': ['M','S','S'],
    'hoe': ['MM',' S',' S'],
    'spear': ['  M',' S ','S  '],
}
TOOL_TAGS = {'swords':'sword','axes':'axe','pickaxes':'pickaxe','shovels':'shovel','hoes':'hoe','spears':'spear'}
AGGREGATE_TAGS = {
    'tools': ['sword','axe','pickaxe','shovel','hoe','spear'],
    'weapons': ['sword','axe','spear'],
    'melee_weapons': ['sword','axe','spear'],
}

def ordered(obj):
    return json.dumps(obj, ensure_ascii=False, indent=2) + '\n'

def load_families():
    return json.loads(FAMILY_JSON.read_text(encoding='utf-8'))['families']

def write_or_check(path, content, write, diffs):
    path = ROOT / path
    if write:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
    else:
        if not path.exists():
            diffs.append(f'missing {path.relative_to(ROOT)}')
        elif path.read_text(encoding='utf-8') != content:
            diffs.append(f'out-of-date {path.relative_to(ROOT)}')

def item_def(model):
    return {'model': {'type': 'minecraft:model', 'model': model}}

def spear_item_def(name):
    return {
        'model': {
            'type': 'minecraft:select',
            'cases': [{
                'model': {'type':'minecraft:model','model':f'{MOD}:item/{name}'},
                'when': ['gui','ground','fixed','on_shelf']
            }],
            'fallback': {'type':'minecraft:model','model':f'{MOD}:item/{name}_in_hand'},
            'property': 'minecraft:display_context'
        },
        'swap_animation_scale': 1.95
    }

def shield_item_def(name):
    return {
        'model': {
            'type': 'minecraft:condition',
            'on_false': {
                'type': 'minecraft:special',
                'base': f'{MOD}:item/{name}',
                'model': {'type': 'minecraft:shield'}
            },
            'on_true': {
                'type': 'minecraft:special',
                'base': f'{MOD}:item/{name}_blocking',
                'model': {'type': 'minecraft:shield'}
            },
            'property': 'minecraft:using_item',
            'transformation': {
                'left_rotation': [0.0, 0.0, 0.0, 1.0],
                'right_rotation': [0.0, 0.0, 0.0, 1.0],
                'scale': [1.0, -1.0, -1.0],
                'translation': [0.0, 0.0, 0.0]
            }
        }
    }


def shield_model(particle):
    return {
        'gui_light': 'front',
        'textures': {'particle': particle},
        'display': {
            'thirdperson_righthand': {'rotation': [0, 90, 0], 'translation': [10, 6, -4], 'scale': [1, 1, 1]},
            'thirdperson_lefthand': {'rotation': [0, 90, 0], 'translation': [10, 6, 12], 'scale': [1, 1, 1]},
            'firstperson_righthand': {'rotation': [0, 180, 5], 'translation': [-10, 1.75, -10], 'scale': [1.25, 1.25, 1.25]},
            'firstperson_lefthand': {'rotation': [0, 180, 5], 'translation': [10, 0, -10], 'scale': [1.25, 1.25, 1.25]},
            'gui': {'rotation': [15, -25, -5], 'translation': [2, 3, 0], 'scale': [0.65, 0.65, 0.65]},
            'fixed': {'rotation': [0, 180, 0], 'translation': [-4.5, 4.5, -5], 'scale': [0.55, 0.55, 0.55]},
            'on_shelf': {'rotation': [0, 0, 0], 'translation': [11, 18.5, 8.7], 'scale': [1.4, 1.4, 1.4]},
            'ground': {'rotation': [0, 0, 0], 'translation': [2, 4, 2], 'scale': [0.25, 0.25, 0.25]}
        }
    }


def shield_particle_texture(ingredient):
    direct = {
        'minecraft:emerald': 'minecraft:block/emerald_block',
        'minecraft:copper_ingot': 'minecraft:block/copper_block',
        'minecraft:gold_ingot': 'minecraft:block/gold_block',
        'minecraft:diamond': 'minecraft:block/diamond_block',
        'minecraft:netherite_ingot': 'minecraft:block/netherite_block',
        'minecraft:lapis_lazuli': 'minecraft:block/lapis_block',
        'minecraft:redstone': 'minecraft:block/redstone_block',
        'minecraft:quartz': 'minecraft:block/quartz_block_side',
        'minecraft:amethyst_shard': 'minecraft:block/amethyst_block',
        'minecraft:prismarine_shard': 'minecraft:block/prismarine',
        'minecraft:coal': 'minecraft:block/coal_block',
        'minecraft:charcoal': 'minecraft:block/coal_block',
        'minecraft:bone': 'minecraft:block/bone_block_side',
        'minecraft:paper': 'minecraft:block/white_wool',
        'minecraft:armadillo_scute': 'minecraft:block/brown_wool',
        'minecraft:turtle_scute': 'minecraft:block/turtle_egg',
    }
    if ingredient in direct:
        return direct[ingredient]
    if ingredient.startswith('minecraft:'):
        return 'minecraft:block/' + ingredient.split(':', 1)[1]
    return 'minecraft:block/dark_oak_planks'


def shield_blocking_model(particle):
    return {
        'gui_light': 'front',
        'textures': {'particle': particle},
        'display': {
            'thirdperson_righthand': {'rotation': [45, 155, 0], 'translation': [-3.49, 11, -2], 'scale': [1, 1, 1]},
            'thirdperson_lefthand': {'rotation': [45, 155, 0], 'translation': [11.51, 7, 2.5], 'scale': [1, 1, 1]},
            'firstperson_righthand': {'rotation': [0, 180, -5], 'translation': [-15, 3.25, -11], 'scale': [1.25, 1.25, 1.25]},
            'firstperson_lefthand': {'rotation': [0, 180, -5], 'translation': [5, 5, -11], 'scale': [1.25, 1.25, 1.25]},
            'gui': {'rotation': [15, -25, -5], 'translation': [2, 3, 0], 'scale': [0.65, 0.65, 0.65]}
        }
    }


def model(parent, texture):
    return {'parent': parent, 'textures': {'layer0': texture}}

def shaped_recipe(pattern, key, result, category='equipment'):
    return {'type':'minecraft:crafting_shaped','category':category,'pattern':pattern,'key':key,'result':{'id':result,'count':1}}

def repair_values(fam):
    values = fam.get('repair_ingredients')
    if values is None:
        values = [fam['ingredient']]
    return values

def managed_item_ids(families):
    ids=[]
    for fam in families:
        fid=fam['id']
        armor=fam.get('armor')
        if armor:
            for piece in armor['pieces']:
                ids.append(f'{fid}_{piece}')
        tools=fam.get('tools')
        if tools:
            for tool in tools['types']:
                ids.append(f'{fid}_{tool}')
        shield=fam.get('shield')
        if shield and shield.get('enabled', True):
            ids.append(f'{fid}_shield')
    return ids

def build_outputs():
    families=load_families()
    outputs={}
    ids=managed_item_ids(families)
    # Preserve non-item lang keys.
    lang_base={}
    for lang in ['zh_cn','en_us']:
        p=RES / f'assets/{MOD}/lang/{lang}.json'
        if p.exists():
            lang_base[lang]={k:v for k,v in json.loads(p.read_text(encoding='utf-8')).items() if not k.startswith(f'item.{MOD}.')}
        else:
            lang_base[lang]={}
    zh=dict(lang_base.get('zh_cn',{})); en=dict(lang_base.get('en_us',{}))
    tag_values={tag:[] for tag in TOOL_TAGS}
    aggregate_values={tag:[] for tag in AGGREGATE_TAGS}

    for fam in families:
        fid=fam['id']; ingredient=fam['ingredient']
        recipe_overrides=fam.get('recipe_overrides', {})
        zh[f'material.{MOD}.{fid}'] = fam['zh_name']
        en[f'material.{MOD}.{fid}'] = fam['en_name']
        repair_suffix='equipment' if fid == 'emerald' else 'armor'
        if fam.get('armor'):
            armor=fam['armor']
            # equipment definition
            equip={
                'layers': {
                    'humanoid': [{'texture': f'{MOD}:{fid}'}],
                    'humanoid_baby': [{'texture': f'{MOD}:{fid}'}],
                    'humanoid_leggings': [{'texture': f'{MOD}:{fid}_leggings'}]
                }
            }
            outputs[f'src/main/resources/assets/{MOD}/equipment/{fid}.json']=ordered(equip)
            outputs[f'src/main/resources/data/{MOD}/tags/item/repairs_{fid}_{repair_suffix}.json']=ordered({'replace':False,'values':repair_values(fam)})
            zh_overrides=armor.get('zh_overrides', {})
            en_overrides=armor.get('en_overrides', {})
            for piece in armor['pieces']:
                item=f'{fid}_{piece}'
                outputs[f'src/main/resources/assets/{MOD}/items/{item}.json']=ordered(item_def(f'{MOD}:item/{item}'))
                outputs[f'src/main/resources/assets/{MOD}/models/item/{item}.json']=ordered(model('minecraft:item/generated', f'{MOD}:item/{item}'))
                
                if item in recipe_overrides:
                    override=recipe_overrides[item]
                    outputs[f'src/main/resources/data/{MOD}/recipe/{item}.json']=ordered(shaped_recipe(override['pattern'], override['key'], f'{MOD}:{item}', override.get('category','equipment')))
                else:
                    outputs[f'src/main/resources/data/{MOD}/recipe/{item}.json']=ordered(shaped_recipe(ARMOR_PATTERNS[piece], {'M': ingredient}, f'{MOD}:{item}'))
                zh[f'item.{MOD}.{item}']=zh_overrides.get(piece, fam['zh_name'] + ZH_PIECES[piece])
                en[f'item.{MOD}.{item}']=en_overrides.get(piece, fam['en_name'] + ' ' + EN_PIECES[piece])
        if fam.get('tools'):
            tools=fam['tools']
            # tools use same repair tag convention as armor, even if no armor exists.
            outputs[f'src/main/resources/data/{MOD}/tags/item/repairs_{fid}_{repair_suffix}.json']=ordered({'replace':False,'values':repair_values(fam)})
            for tool in tools['types']:
                item=f'{fid}_{tool}'
                outputs[f'src/main/resources/assets/{MOD}/items/{item}.json']=ordered(spear_item_def(item) if tool == 'spear' else item_def(f'{MOD}:item/{item}'))
                if tool == 'spear':
                    outputs[f'src/main/resources/assets/{MOD}/models/item/{item}.json']=ordered(model('minecraft:item/generated', f'{MOD}:item/{item}'))
                    outputs[f'src/main/resources/assets/{MOD}/models/item/{item}_in_hand.json']=ordered(model('minecraft:item/spear_in_hand', f'{MOD}:item/{item}_in_hand'))
                else:
                    outputs[f'src/main/resources/assets/{MOD}/models/item/{item}.json']=ordered(model('minecraft:item/handheld', f'{MOD}:item/{item}'))
                # Valid recipe categories in 1.21+/26.x are equipment, building, misc, redstone (tools is invalid).
                cat='equipment'
                
                if item in recipe_overrides:
                    override=recipe_overrides[item]
                    # Guard against legacy invalid category values in JSON (e.g. \"tools\").
                    override_cat = override.get('category', cat)
                    if override_cat == 'tools':
                        override_cat = 'equipment'
                    outputs[f'src/main/resources/data/{MOD}/recipe/{item}.json']=ordered(shaped_recipe(override['pattern'], override['key'], f'{MOD}:{item}', override_cat))
                else:
                    outputs[f'src/main/resources/data/{MOD}/recipe/{item}.json']=ordered(shaped_recipe(TOOL_PATTERNS[tool], {'M': ingredient, 'S':'minecraft:stick'}, f'{MOD}:{item}', cat))
                zh[f'item.{MOD}.{item}']=fam['zh_name'] + TOOL_ZH[tool]
                en[f'item.{MOD}.{item}']=fam['en_name'] + ' ' + TOOL_EN[tool]
                for tag,suffix in TOOL_TAGS.items():
                    if tool == suffix:
                        tag_values[tag].append(f'{MOD}:{item}')
                for tag, suffixes in AGGREGATE_TAGS.items():
                    if tool in suffixes:
                        aggregate_values[tag].append(f'{MOD}:{item}')
        if fam.get('shield') and fam['shield'].get('enabled', True):
            outputs[f'src/main/resources/data/{MOD}/tags/item/repairs_{fid}_{repair_suffix}.json']=ordered({'replace':False,'values':repair_values(fam)})
            item=f'{fid}_shield'
            particle=shield_particle_texture(ingredient)
            # Special shield renderer uses vanilla shield atlases; these base models provide transforms/particle only.
            outputs[f'src/main/resources/assets/{MOD}/items/{item}.json']=ordered(shield_item_def(item))
            outputs[f'src/main/resources/assets/{MOD}/models/item/{item}.json']=ordered(shield_model(particle))
            outputs[f'src/main/resources/assets/{MOD}/models/item/{item}_blocking.json']=ordered(shield_blocking_model(particle))
            if item in recipe_overrides:
                override=recipe_overrides[item]
                outputs[f'src/main/resources/data/{MOD}/recipe/{item}.json']=ordered(shaped_recipe(override['pattern'], override['key'], f'{MOD}:{item}', override.get('category','equipment')))
            else:
                outputs[f'src/main/resources/data/{MOD}/recipe/{item}.json']=ordered(shaped_recipe(['MIM','MMM',' M '], {'M': ingredient, 'I': 'minecraft:iron_ingot'}, f'{MOD}:{item}'))
            zh[f'item.{MOD}.{item}']=fam['zh_name'] + '盾牌'
            en[f'item.{MOD}.{item}']=fam['en_name'] + ' Shield'

    zh.update({
        'tooltip.dream_equipment.header': '圆梦装备',
        'tooltip.dream_equipment.material': '材料：%s',
        'tooltip.dream_equipment.armor': '护甲：%s  耐久：%s',
        'tooltip.dream_equipment.toughness': '韧性：%s  击退抗性：%s',
        'tooltip.dream_equipment.enchantability': '附魔能力：%s',
        'tooltip.dream_equipment.tool': '类型：%s  耐久：%s',
        'tooltip.dream_equipment.tool_stats': '速度：%s  攻击加成：%s',
        'tooltip.dream_equipment.shield': '盾牌：耐久 %s',
        'tooltip.dream_equipment.effects_header': '效果说明：',
        'tooltip.dream_equipment.effect': '套装：%s%s %s',
        'tooltip.dream_equipment.condition.always': '获得 ',
        'tooltip.dream_equipment.condition.in_water': '水中获得 ',
        'tooltip.dream_equipment.condition.wet': '潮湿时获得 ',
        'tooltip.dream_equipment.condition.dry': '干燥时获得 ',
        'tooltip.dream_equipment.cactus': '每件：受击反伤 %s 点',
        'tooltip.dream_equipment.slime_decay': '套装：每刻消耗耐久，损坏返还少量粘液球',
        'tooltip.dream_equipment.slime_cancel': '套装：%s 概率免伤',
        'tooltip.dream_equipment.slime_boots': '靴子：≤%s 格摔落免伤并弹跳',
        'tooltip.dream_equipment.armadillo': '鞋子：返还部分摔落伤害',
        'tooltip.dream_equipment.wet_weakness': '弱点：遇水/雨每 %s tick 损耗 %s 耐久',
        'tooltip.dream_equipment.brittle': '脆性：受 ≥%s 伤害时 %s 概率碎裂一件',
        'tooltip.dream_equipment.redstone_signal': '红石脉冲：靴子 %s 强度/%s tick，整套 %s 强度/%s tick',
        'tooltip.dream_equipment.lapis_enchanting': '附魔：返还青金石消耗，但额外损耗青金石装备耐久',
        'tooltip.dream_equipment.wet_repair': '潮湿修复：每 %s tick 修复 %s 耐久',
        'tooltip.dream_equipment.stone_physics': '石质：整套约 %s 免伤；≥%s 伤害碎裂；缓慢系数 %s',
        'tooltip.dream_equipment.brittle_weapon': '武器脆性：命中后 %s 概率直接碎裂',
        'tooltip.dream_equipment.damage_immunity': '免疫：%s',
        'damage_type.minecraft.sonic_boom': '监守者声波',
        'tooltip.dream_equipment.armadillo_terrain': '鞋子：在沙子/红沙/沙砾上获得 速度 III',
        'tooltip.dream_equipment.held_effect': '手持：%s%s %s',
        'tooltip.dream_equipment.tool.sword': '剑',
        'tooltip.dream_equipment.tool.pickaxe': '镐',
        'tooltip.dream_equipment.tool.axe': '斧',
        'tooltip.dream_equipment.tool.shovel': '锹',
        'tooltip.dream_equipment.tool.hoe': '锄',
        'tooltip.dream_equipment.shield_cactus': '盾牌：成功格挡近战时反刺 %s 伤害（冷却 %s tick）',
        'tooltip.dream_equipment.shield_glass': '盾牌脆性：格挡 ≥%s 伤害时 %s 概率碎裂',
        'tooltip.dream_equipment.shield_redstone': '盾牌：成功格挡时发出强度 %s / %s tick 红石脉冲',
        'tooltip.dream_equipment.shield_slime': '盾牌：成功格挡时弹开攻击者（强度 %s）',
        'tooltip.dream_equipment.shield_paper': '盾牌弱点：潮湿举盾每 %s tick 损耗 %s 耐久',
        'tooltip.dream_equipment.shield_obsidian': '盾牌：举盾缓慢；格挡火焰/爆炸时返还 %s 耐久损耗',
        'tooltip.dream_equipment.shield_prismarine': '盾牌：水中成功格挡返还 %s 耐久损耗',
        'tooltip.dream_equipment.shield_amethyst': '盾牌：可格挡监守者声波，消耗 %s 耐久',
        'tooltip.dream_equipment.shield_bone': '盾牌：格挡亡灵攻击时返还 %s 耐久损耗',
        'tooltip.dream_equipment.shield_coal': '盾牌：格挡火焰伤害时返还 %s 耐久损耗',
        'tooltip.dream_equipment.shield_quartz': '盾牌：格挡弹射物时返还 %s 耐久损耗',
        'tooltip.dream_equipment.tool.spear': '矛'
    })
    en.update({
        'tooltip.dream_equipment.header': 'Dream Equipment',
        'tooltip.dream_equipment.material': 'Material: %s',
        'tooltip.dream_equipment.armor': 'Armor: %s  Durability: %s',
        'tooltip.dream_equipment.toughness': 'Toughness: %s  Knockback resistance: %s',
        'tooltip.dream_equipment.enchantability': 'Enchantability: %s',
        'tooltip.dream_equipment.tool': 'Type: %s  Durability: %s',
        'tooltip.dream_equipment.tool_stats': 'Speed: %s  Attack bonus: %s',
        'tooltip.dream_equipment.shield': 'Shield: durability %s',
        'tooltip.dream_equipment.effects_header': 'Effects:',
        'tooltip.dream_equipment.effect': 'Set: %s%s %s',
        'tooltip.dream_equipment.condition.always': 'gain ',
        'tooltip.dream_equipment.condition.in_water': 'in water gain ',
        'tooltip.dream_equipment.condition.wet': 'when wet gain ',
        'tooltip.dream_equipment.condition.dry': 'when dry gain ',
        'tooltip.dream_equipment.cactus': 'Per piece: retaliates for %s damage',
        'tooltip.dream_equipment.slime_decay': 'Set: loses durability every tick; returns some slime balls on break',
        'tooltip.dream_equipment.slime_cancel': 'Set: %s chance to ignore damage',
        'tooltip.dream_equipment.slime_boots': 'Boots: ≤%s block falls deal no damage and bounce',
        'tooltip.dream_equipment.armadillo': 'Shoes: restores part of fall damage taken',
        'tooltip.dream_equipment.wet_weakness': 'Weakness: rain/water deals %s durability damage every %s ticks',
        'tooltip.dream_equipment.brittle': 'Brittle: taking ≥%s damage has %s chance to shatter one piece',
        'tooltip.dream_equipment.redstone_signal': 'Redstone pulse: boots %s power/%s ticks, full set %s power/%s ticks',
        'tooltip.dream_equipment.lapis_enchanting': 'Enchanting: refunds lapis cost, but damages lapis equipment',
        'tooltip.dream_equipment.wet_repair': 'Wet repair: restores %s durability every %s ticks',
        'tooltip.dream_equipment.stone_physics': 'Stone: full set ~%s damage ignore; shatters at ≥%s damage; slowness factor %s',
        'tooltip.dream_equipment.brittle_weapon': 'Brittle weapon: %s chance to shatter on hit',
        'tooltip.dream_equipment.damage_immunity': 'Immune to: %s',
        'damage_type.minecraft.sonic_boom': 'Sonic Boom',
        'tooltip.dream_equipment.armadillo_terrain': 'Shoes: gain Speed III on sand, red sand, or gravel',
        'tooltip.dream_equipment.held_effect': 'Held: %s%s %s',
        'tooltip.dream_equipment.tool.sword': 'Sword',
        'tooltip.dream_equipment.tool.pickaxe': 'Pickaxe',
        'tooltip.dream_equipment.tool.axe': 'Axe',
        'tooltip.dream_equipment.tool.shovel': 'Shovel',
        'tooltip.dream_equipment.tool.hoe': 'Hoe',
        'tooltip.dream_equipment.shield_cactus': 'Shield: retaliates for %s damage on melee block (cooldown %s ticks)',
        'tooltip.dream_equipment.shield_glass': 'Shield brittle: blocking ≥%s damage has %s chance to shatter',
        'tooltip.dream_equipment.shield_redstone': 'Shield: emits redstone pulse %s power / %s ticks on block',
        'tooltip.dream_equipment.shield_slime': 'Shield: bounces attackers on block (strength %s)',
        'tooltip.dream_equipment.shield_paper': 'Shield weakness: when wet and blocking, loses %s durability every %s ticks',
        'tooltip.dream_equipment.shield_obsidian': 'Shield: slows while blocking; refunds %s durability loss against fire/explosions',
        'tooltip.dream_equipment.shield_prismarine': 'Shield: in water, successful blocks refund %s durability loss',
        'tooltip.dream_equipment.shield_amethyst': 'Shield: blocks Warden sonic boom, costing %s durability',
        'tooltip.dream_equipment.shield_bone': 'Shield: blocking undead attacks refunds %s durability loss',
        'tooltip.dream_equipment.shield_coal': 'Shield: blocking fire damage refunds %s durability loss',
        'tooltip.dream_equipment.shield_quartz': 'Shield: blocking projectiles refunds %s durability loss',
        'tooltip.dream_equipment.tool.spear': 'Spear'
    })
    outputs[f'src/main/resources/assets/{MOD}/lang/zh_cn.json']=ordered(dict(sorted(zh.items())))
    outputs[f'src/main/resources/assets/{MOD}/lang/en_us.json']=ordered(dict(sorted(en.items())))
    # Tags for tool recognition.
    for tag, values in tag_values.items():
        for ns in ['minecraft','c','fabric','forge']:
            outputs[f'src/main/resources/data/{ns}/tags/item/{tag}.json']=ordered({'replace':False,'values':values})
            if ns != 'minecraft':
                outputs[f'src/main/resources/data/{ns}/tags/item/tools/{tag}.json']=ordered({'replace':False,'values':values})
    for tag, values in aggregate_values.items():
        for ns in ['c','fabric','forge']:
            outputs[f'src/main/resources/data/{ns}/tags/item/{tag}.json']=ordered({'replace':False,'values':values})
    return outputs

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true')
    args=ap.parse_args()
    outputs=build_outputs()
    diffs=[]
    for path, content in sorted(outputs.items()):
        write_or_check(path, content, args.write, diffs)
    if args.write:
        print(f'Wrote equipment resources: files={len(outputs)}')
    elif diffs:
        print('\n'.join(diffs[:200]))
        if len(diffs)>200: print(f'... and {len(diffs)-200} more')
        raise SystemExit(1)
    else:
        print(f'equipment resources in sync — files={len(outputs)}')

if __name__ == '__main__':
    main()
