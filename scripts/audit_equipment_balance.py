#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RES=ROOT/'src/main/resources'
MOD='dream_equipment'
BASE_DUR={'helmet':11,'chestplate':16,'leggings':15,'boots':13}
TIERS={
    'minecraft:incorrect_for_wooden_tool':'wood/gold-like',
    'minecraft:incorrect_for_gold_tool':'gold-like',
    'minecraft:incorrect_for_stone_tool':'stone',
    'minecraft:incorrect_for_iron_tool':'iron',
    'minecraft:incorrect_for_diamond_tool':'diamond',
}
families=json.loads((RES/f'data/{MOD}/equipment_families.json').read_text())['families']
errors=[]
rows=[]
for f in families:
    fid=f['id']
    a=f.get('armor')
    if a:
        for piece in a['pieces']:
            expected=BASE_DUR[piece]*a['durability_multiplier']
            rows.append((fid,piece,'armor',expected,a['defense'].get(piece,0),a['toughness'],a['enchantment_value']))
            if expected <= 0: errors.append(f'{fid}_{piece} durability <=0')
    sh=f.get('shield')
    if sh and sh.get('enabled', True):
        dur=sh.get('durability', 0)
        rows.append((fid,'shield','shield',dur))
        if dur <= 0: errors.append(f'{fid}_shield durability <=0')
    t=f.get('tools')
    if t:
        tier=t['incorrect_blocks_for_drops']
        if tier not in TIERS: errors.append(f'{fid} unknown mining tier tag {tier}')
        for typ in t['types']:
            dur=t['durability']
            rows.append((fid,typ,'tool',dur,t['speed'],t['attack_damage_bonus'],t['enchantment_value'],TIERS.get(tier,tier)))
            if dur <= 0: errors.append(f'{fid}_{typ} durability <=0')
# Consistency: tooltip must display actual armor durability, not multiplier.
zh=json.loads((RES/f'assets/{MOD}/lang/zh_cn.json').read_text())
en=json.loads((RES/f'assets/{MOD}/lang/en_us.json').read_text())
if '耐久倍率' in zh.get('tooltip.dream_equipment.armor',''): errors.append('zh armor tooltip still says durability multiplier')
if 'multiplier' in en.get('tooltip.dream_equipment.armor','').lower(): errors.append('en armor tooltip still says durability multiplier')
source=(ROOT/'src/main/java/com/dreamequipment/client/DreamEquipmentTooltips.java').read_text()
if 'armorDurability(piece, armor.durabilityMultiplier())' not in source: errors.append('tooltip source does not compute actual armor durability')
# Specific balance guardrails introduced this pass.
byid={f['id']:f for f in families}
checks={
    'obsidian':120,
    'glass':64,
    'bone':160,
    'calcite':100,
    'netherrack':64,
    'amethyst':640,
    'granite':260,
    'diorite':250,
    'andesite':280,
}
for fid,dur in checks.items():
    if fid in byid and byid[fid].get('tools') and byid[fid]['tools']['durability'] != dur:
        errors.append(f'{fid} tool durability expected {dur}, got {byid[fid]["tools"]["durability"]}')
# Print useful summary.
print('Equipment balance audit')
print(f'families={len(families)} entries={len(rows)}')
print('\nShield families:')
for f in families:
    sh=f.get('shield')
    if sh and sh.get('enabled', True):
        print(f"- {f['id']}: shield durability={sh.get('durability')}")
print('\nTool families:')
for f in families:
    if f.get('tools'):
        t=f['tools']
        print(f"- {f['id']}: types={','.join(t['types'])} durability={t['durability']} speed={t['speed']} attack_bonus={t['attack_damage_bonus']} enchant={t['enchantment_value']} tier={TIERS.get(t['incorrect_blocks_for_drops'],t['incorrect_blocks_for_drops'])}")
print('\nArmor durability formula: helmet=11×mult, chestplate=16×mult, leggings=15×mult, boots=13×mult')
if errors:
    print('\nERRORS:')
    print('\n'.join(errors))
    raise SystemExit(1)
print('\nBalance audit OK — actual armor durability formula matches tooltip display formula; tool/shield durability values are JSON-owned.')
