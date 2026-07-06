#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'src/main/resources/data/dream_equipment/set_effects.json'
data=json.loads(path.read_text(encoding='utf-8'))
errors=[]
materials=set()
for p in (ROOT/'src/main/resources/assets/dream_equipment/equipment').glob('*.json'):
    materials.add(p.stem)
allowed_conditions={'always','in_water','wet','dry'}
if not isinstance(data.get('enabled'), bool): errors.append('enabled must be bool')
for i,r in enumerate(data.get('passive_effects', [])):
    if r.get('material') not in materials: errors.append(f'passive[{i}] unknown material {r.get("material")}')
    if ':' not in r.get('effect',''): errors.append(f'passive[{i}] effect must be namespaced')
    if r.get('condition','always') not in allowed_conditions: errors.append(f'passive[{i}] invalid condition')
    if int(r.get('duration_ticks',0)) <= 0: errors.append(f'passive[{i}] duration must be >0')
    if int(r.get('amplifier',0)) < 0: errors.append(f'passive[{i}] amplifier must be >=0')
cactus=data.get('cactus_retaliation',{})
if float(cactus.get('damage_per_piece',0)) < 0: errors.append('cactus damage_per_piece must be >=0')
slime=data.get('slime',{})
for k in ['durability_damage_per_tick','boots_safe_fall_distance','bounce_min_velocity','bounce_distance_divisor','fall_heal_ratio','damage_cancel_chance']:
    if float(slime.get(k,0)) < 0: errors.append(f'slime {k} must be >=0')
for piece in ['helmet','chestplate','leggings','boots']:
    if piece not in slime.get('return_slime_balls',{}): errors.append(f'slime return missing {piece}')
for i,r in enumerate(data.get('wet_durability', [])):
    if r.get('material') not in materials: errors.append(f'wet_durability[{i}] unknown material')
    if int(r.get('interval_ticks',0)) <= 0: errors.append(f'wet_durability[{i}] interval must be >0')
    if int(r.get('damage',0)) <= 0: errors.append(f'wet_durability[{i}] damage must be >0')

redstone=data.get('redstone_signal',{})
if not isinstance(redstone.get('enabled', True), bool): errors.append('redstone_signal.enabled must be bool')
for k in ['boots_signal','full_set_signal']:
    v=int(redstone.get(k,0))
    if not (0 <= v <= 15): errors.append(f'redstone_signal.{k} must be 0..15')
for k in ['boots_pulse_ticks','full_set_pulse_ticks']:
    v=int(redstone.get(k,0))
    if v <= 0: errors.append(f'redstone_signal.{k} must be >0')

for i,r in enumerate(data.get('brittle_sets', [])):
    if r.get('material') not in materials: errors.append(f'brittle[{i}] unknown material')
    if float(r.get('damage_threshold',0)) <= 0: errors.append(f'brittle[{i}] threshold must be >0')
    chance=float(r.get('shatter_chance',-1))
    if not (0 <= chance <= 1): errors.append(f'brittle[{i}] chance must be 0..1')

for i,r in enumerate(data.get('wet_repair', [])):
    if r.get('material') not in materials: errors.append(f'wet_repair[{i}] unknown material')
    if int(r.get('interval_ticks',0)) <= 0: errors.append(f'wet_repair[{i}] interval must be >0')
    if int(r.get('repair',0)) <= 0: errors.append(f'wet_repair[{i}] repair must be >0')
for i,r in enumerate(data.get('brittle_weapons', [])):
    if r.get('material') not in materials: errors.append(f'brittle_weapons[{i}] unknown material')
    chance=float(r.get('break_chance',-1))
    if not (0 <= chance <= 1): errors.append(f'brittle_weapons[{i}] break_chance must be 0..1')
for i,r in enumerate(data.get('stone_armor_physics', [])):
    if r.get('material') not in materials: errors.append(f'stone_armor_physics[{i}] unknown material')
    for k in ['cancel_chance_per_piece','shatter_damage_threshold','slowness_per_piece']:
        if float(r.get(k,-1)) < 0: errors.append(f'stone_armor_physics[{i}].{k} must be >=0')


armadillo=data.get('armadillo_boots',{})
if not isinstance(armadillo.get('enabled', True), bool): errors.append('armadillo_boots.enabled must be bool')
if not armadillo.get('blocks'): errors.append('armadillo_boots.blocks must not be empty')
for b in armadillo.get('blocks', []):
    if ':' not in b: errors.append(f'armadillo block {b} must be namespaced')
if ':' not in armadillo.get('effect','minecraft:speed'): errors.append('armadillo effect must be namespaced')
if int(armadillo.get('duration_ticks',0)) <= 0: errors.append('armadillo duration must be >0')
if int(armadillo.get('amplifier',0)) < 0: errors.append('armadillo amplifier must be >=0')
for i,r in enumerate(data.get('held_effects', [])):
    if ':' not in r.get('item',''): errors.append(f'held_effects[{i}] item must be namespaced')
    if ':' not in r.get('effect',''): errors.append(f'held_effects[{i}] effect must be namespaced')
    if r.get('condition','always') not in {'always','in_water','wet','dry'}: errors.append(f'held_effects[{i}] invalid condition')
    if int(r.get('duration_ticks',0)) <= 0: errors.append(f'held_effects[{i}] duration must be >0')


for i,r in enumerate(data.get('damage_immunities', [])):
    if r.get('material') not in materials: errors.append(f'damage_immunities[{i}] unknown material')
    if ':' not in r.get('damage_type',''): errors.append(f'damage_immunities[{i}] damage_type must be namespaced')


shield_effects=data.get('shield_effects', {})
if shield_effects:
    cactus=shield_effects.get('cactus', {})
    if not isinstance(cactus.get('enabled', True), bool): errors.append('shield_effects.cactus.enabled must be bool')
    if float(cactus.get('retaliate_damage', 0)) < 0: errors.append('shield_effects.cactus.retaliate_damage must be >=0')
    if int(cactus.get('cooldown_ticks', 0)) < 0: errors.append('shield_effects.cactus.cooldown_ticks must be >=0')
    glass=shield_effects.get('glass', {})
    if not isinstance(glass.get('enabled', True), bool): errors.append('shield_effects.glass.enabled must be bool')
    if float(glass.get('shatter_threshold', 0)) < 0: errors.append('shield_effects.glass.shatter_threshold must be >=0')
    chance=float(glass.get('shatter_chance', 0))
    if not (0 <= chance <= 1): errors.append('shield_effects.glass.shatter_chance must be 0..1')
    redstone=shield_effects.get('redstone', {})
    if not isinstance(redstone.get('enabled', True), bool): errors.append('shield_effects.redstone.enabled must be bool')
    if not (0 <= int(redstone.get('pulse_signal', 0)) <= 15): errors.append('shield_effects.redstone.pulse_signal must be 0..15')
    if int(redstone.get('pulse_ticks', 0)) <= 0: errors.append('shield_effects.redstone.pulse_ticks must be >0')
    slime=shield_effects.get('slime', {})
    if not isinstance(slime.get('enabled', True), bool): errors.append('shield_effects.slime.enabled must be bool')
    if float(slime.get('knockback_strength', 0)) < 0: errors.append('shield_effects.slime.knockback_strength must be >=0')
    if float(slime.get('vertical_boost', 0)) < 0: errors.append('shield_effects.slime.vertical_boost must be >=0')
    paper=shield_effects.get('paper', {})
    if not isinstance(paper.get('enabled', True), bool): errors.append('shield_effects.paper.enabled must be bool')
    if int(paper.get('wet_damage_interval', 0)) <= 0: errors.append('shield_effects.paper.wet_damage_interval must be >0')
    if int(paper.get('wet_damage', 0)) <= 0: errors.append('shield_effects.paper.wet_damage must be >0')

    obsidian=shield_effects.get('obsidian', {})
    if not isinstance(obsidian.get('enabled', True), bool): errors.append('shield_effects.obsidian.enabled must be bool')
    if int(obsidian.get('refund_damage', 0)) < 0: errors.append('shield_effects.obsidian.refund_damage must be >=0')
    if int(obsidian.get('slowness_duration_ticks', 0)) <= 0: errors.append('shield_effects.obsidian.slowness_duration_ticks must be >0')
    if int(obsidian.get('slowness_amplifier', 0)) < 0: errors.append('shield_effects.obsidian.slowness_amplifier must be >=0')
    prismarine=shield_effects.get('prismarine', {})
    if not isinstance(prismarine.get('enabled', True), bool): errors.append('shield_effects.prismarine.enabled must be bool')
    if int(prismarine.get('water_refund_damage', 0)) < 0: errors.append('shield_effects.prismarine.water_refund_damage must be >=0')
    amethyst=shield_effects.get('amethyst', {})
    if not isinstance(amethyst.get('enabled', True), bool): errors.append('shield_effects.amethyst.enabled must be bool')
    if int(amethyst.get('sonic_boom_damage_cost', 0)) < 0: errors.append('shield_effects.amethyst.sonic_boom_damage_cost must be >=0')
    bone=shield_effects.get('bone', {})
    if not isinstance(bone.get('enabled', True), bool): errors.append('shield_effects.bone.enabled must be bool')
    if int(bone.get('undead_refund_damage', 0)) < 0: errors.append('shield_effects.bone.undead_refund_damage must be >=0')
    coal=shield_effects.get('coal', {})
    if not isinstance(coal.get('enabled', True), bool): errors.append('shield_effects.coal.enabled must be bool')
    if int(coal.get('fire_refund_damage', 0)) < 0: errors.append('shield_effects.coal.fire_refund_damage must be >=0')
    quartz=shield_effects.get('quartz', {})
    if not isinstance(quartz.get('enabled', True), bool): errors.append('shield_effects.quartz.enabled must be bool')
    if int(quartz.get('projectile_refund_damage', 0)) < 0: errors.append('shield_effects.quartz.projectile_refund_damage must be >=0')

if errors:
    print('\n'.join(errors)); raise SystemExit(1)
print(f'set_effects JSON OK — passive={len(data.get("passive_effects", []))}, brittle={len(data.get("brittle_sets", []))}')
