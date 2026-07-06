#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RES=ROOT/'src/main/resources'
MOD='dream_equipment'
path=RES/f'data/{MOD}/equipment_families.json'
data=json.loads(path.read_text(encoding='utf-8'))
errors=[]
families=data.get('families', [])
ids=[]
valid_pieces={'helmet','chestplate','leggings','boots'}
valid_tools={'sword','pickaxe','axe','shovel','hoe','spear'}
valid_sounds={'chain','diamond','gold','iron','leather','netherite','wolf','turtle','copper'}

def namespaced_or_tag(value):
    if not isinstance(value, str):
        return False
    if value.startswith('#'):
        value = value[1:]
    return ':' in value and not value.endswith(':') and not value.startswith(':')

expected_items=[]
for i,f in enumerate(families):
    fid=f.get('id')
    if not fid: errors.append(f'family[{i}] missing id'); continue
    if fid in ids: errors.append(f'duplicate family id {fid}')
    ids.append(fid)
    if not namespaced_or_tag(f.get('ingredient','')): errors.append(f'{fid} ingredient must be namespaced or tag-like namespaced')
    if int(f.get('fuel_burn_time_per_material', 0)) < 0: errors.append(f'{fid} fuel_burn_time_per_material must be >=0')
    repair_ingredients=f.get('repair_ingredients')
    if repair_ingredients is not None:
        if not isinstance(repair_ingredients, list) or not repair_ingredients:
            errors.append(f'{fid} repair_ingredients must be a non-empty list when present')
        else:
            for value in repair_ingredients:
                if not namespaced_or_tag(value):
                    errors.append(f'{fid} invalid repair ingredient {value}')
    armor=f.get('armor')
    if armor:
        pieces=armor.get('pieces', [])
        if not pieces: errors.append(f'{fid} armor has no pieces')
        for piece in pieces:
            if piece not in valid_pieces: errors.append(f'{fid} invalid armor piece {piece}')
            expected_items.append(f'{fid}_{piece}')
        if armor.get('equip_sound','iron') not in valid_sounds: errors.append(f'{fid} invalid equip_sound')
        for k in ['durability_multiplier','enchantment_value']:
            if int(armor.get(k,0)) < 0: errors.append(f'{fid} {k} must be >=0')
        defense=armor.get('defense',{})
        for piece in valid_pieces:
            if int(defense.get(piece,0)) < 0: errors.append(f'{fid} defense {piece} must be >=0')
    tools=f.get('tools')
    if tools:
        types=tools.get('types', [])
        if not types: errors.append(f'{fid} tools has no types')
        for t in types:
            if t not in valid_tools: errors.append(f'{fid} invalid tool {t}')
            expected_items.append(f'{fid}_{t}')
        if not namespaced_or_tag(tools.get('incorrect_blocks_for_drops','')): errors.append(f'{fid} incorrect_blocks_for_drops must be namespaced')
        for k in ['durability','enchantment_value']:
            if int(tools.get(k,0)) < 0: errors.append(f'{fid} tool {k} must be >=0')
    shield=f.get('shield')
    if shield and shield.get('enabled', True):
        expected_items.append(f'{fid}_shield')
        if int(shield.get('durability', 0)) <= 0: errors.append(f'{fid} shield durability must be >0')
# Cross-check concrete resources.
for item in expected_items:
    resource_paths=[RES/f'assets/{MOD}/items/{item}.json', RES/f'assets/{MOD}/models/item/{item}.json', RES/f'data/{MOD}/recipe/{item}.json']
    if item.endswith('_shield'):
        resource_paths.append(RES/f'assets/{MOD}/models/item/{item}_blocking.json')
    else:
        resource_paths.append(RES/f'assets/{MOD}/textures/item/{item}.png')
    for p in resource_paths:
        if not p.exists(): errors.append(f'missing resource for {item}: {p.relative_to(ROOT)}')
# Counts are intentionally derived from JSON so new family additions do not require validator edits.
if errors:
    print('\n'.join(errors)); raise SystemExit(1)
print(f'equipment_families JSON OK — families={len(families)}, items={len(expected_items)}')
