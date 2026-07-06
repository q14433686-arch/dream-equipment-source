# Round 21 User Feedback Audit and Rebalance Plan — 2026-07-02

## Scope

User reported five issues and requested a separate deliberation round before changing more content:

1. Bamboo and other wooden armor inventory icons are still wrong.
2. Redstone boots/full redstone set output is not detected by redstone dust.
3. Slime armor is too cheap.
4. End stone and some other materials do not have their own tools/weapons.
5. Some effects are boring/unreasonable, and many item families still have no meaningful set identity.

This is an audit/planning pass only. No code/resource mechanics are intentionally changed in this pass.

## 1. Wood / stone / cobblestone inventory icons are still wrong

### Current state

- We now have 12 plank-variant armor families plus generic `wooden_*`.
- Current inventory icons are generated from vanilla leather/iron icon templates with block-texture fills.
- The user still considers the result wrong.

### Cause

The icon pipeline is technically valid but artistically mismatched:

- vanilla leather/iron icon silhouettes do not match the VKL+/provided emerald armor icon style the user wants
- plank texture fills are too literal and can look noisy or visually unclear at 16×16
- bamboo/crimson/warped need hand-tuned palettes and shape cues, not only block-texture sampling

### Next fix direction

Use the user-provided emerald armor item icons as the universal armor-item silhouette templates:

- `helmet` template = uploaded emerald helmet
- `chestplate` template = uploaded emerald chestplate
- `leggings` template = uploaded emerald leggings
- `boots` template = uploaded emerald boots

Then recolor/material-fill these templates per material:

- wood variants: simplified plank palette + subtle grain, not raw noisy plank texture
- stone/cobble variants: simplified crack/stone pattern based on real block palette
- bamboo: yellow-green bamboo-strip palette, not generic oak-like wood
- crimson/warped: fungus plank palettes with strong red/cyan identity

This should make all armor inventory icons stylistically consistent with the correct emerald set.

## 2. Redstone signal not detected by redstone dust

### Current state

Current implementation:

- `SignalGetterMixin` injects `getSignal` and `getDirectSignal`.
- The signal is returned for the block below a player wearing redstone boots/full set.
- Neighbor updates are triggered around the player every 2 ticks.

### Observed failure

User tested: redstone dust does not detect the signal.

### Likely causes

Redstone dust logic does not simply call the same method path in all cases.

Local bytecode inspection shows `RedStoneWireBlock` computes target power using:

- `Level.getBestNeighborSignal(pos)`
- internal wire-specific signal source gating through `shouldSignal`
- block state conductor/direct-signal logic

The current `SignalGetter` default-method mixin may not affect the exact `Level.getBestNeighborSignal` / redstone-wire calculation path used by redstone dust, or it may return signal in a path that redstone wire ignores because the source block is not considered a conventional signal source at that calculation stage.

### Next fix direction

Do not rely only on generic `SignalGetter#getSignal`.

Implement a redstone-specific compatibility pass:

1. Add/inject into `SignalGetter#getBestNeighborSignal` or the concrete redstone wire calculation path.
2. Add a mixin targeting `RedStoneWireBlock` power calculation, merging nearby player redstone-boot signal into the computed dust power.
3. Add a mixin targeting `DiodeBlock` / repeater input signal if repeaters still fail.
4. Keep JSON values:
   - boots signal = 7
   - full set signal = 15
5. Define exact source positions:
   - current best rule: player block below = source block
   - redstone dust adjacent to that source should receive signal

This should be done as a focused redstone mechanic pass, because redstone has many edge-case query paths.

## 3. Slime armor is too cheap

### Current state

`slime` family currently uses:

```json
"ingredient": "minecraft:slime_ball"
```

With vanilla armor recipes, full set cost is 24 slime balls.

The set is now strong mechanically:

- continuous durability decay
- partial slime-ball return on break
- 10% damage cancel
- boots cancel/bounce ≤12 block falls
- jump/slow-falling utility

### Cause

The cost was set before the mechanics became this strong. After adding damage cancel and fall/bounce utility, slime balls are too cheap.

### Next fix direction

Change slime armor economics, likely through `equipment_families.json`:

Option A — simple and strict:

```json
"ingredient": "minecraft:slime_block"
```

This raises full-set cost to 24 slime blocks = 216 slime balls.

But with every-tick durability loss, 24 slime blocks may be too expensive unless durability is also increased.

Recommended balanced option:

- ingredient: `minecraft:slime_block`
- increase slime armor durability multiplier significantly, e.g. from 9 to 40–60
- increase return slime balls modestly, e.g. helmet 4, chestplate 8, leggings 7, boots 4
- keep 10% damage cancel for now
- test live feel

Longer-term generator improvement:

- support multi-ingredient recipes so slime armor can use `slime_block + leather` or `slime_block + string`, not only one material key.

## 4. End stone and other materials lack tools/weapons

### Current state

Families without tools include:

- wooden / stone / cobblestone
- cactus
- armadillo shell
- bone
- paper
- slime
- coal
- all wood variants
- mossy_cobblestone
- cobbled_deepslate
- blackstone
- sandstone
- red_sandstone
- end_stone
- tuff
- calcite

Some of these should not have full toolsets, but several should have at least weapons.

### Next fix direction

Add curated tools/weapons based on material logic, not full sets for everything.

Recommended additions:

#### End stone

- sword
- axe
- spear
- pickaxe

Reason: hard/end-game stone, useful but not full everyday toolset unless desired.

#### Blackstone / Cobbled deepslate

- sword
- axe
- pickaxe
- spear

Reason: heavy, hard stone materials; pickaxe and heavy weapons make sense.

#### Sandstone / Red sandstone

- sword or spear only, possibly axe omitted

Reason: brittle sedimentary stone; not good for pickaxe/shovel/hoe.

#### Tuff

- pickaxe
- axe
- spear

Reason: rough stone; moderate utility.

#### Calcite

- spear
- sword only, brittle

Reason: brittle mineral; should not be a robust utility tool.

#### Bone

- dagger/sword/spear style tools would make sense, but only if we add non-vanilla weapon categories later. With current categories, sword + spear is reasonable.

#### Cactus

- spear only or no tool; cactus spear is thematically reasonable.

#### Wood variants

The generic vanilla wood tools already exist; adding 12 wood-variant toolsets would bloat content. Do not add unless the user explicitly wants decorative wood tool variants.

## 5. Effects boring/unreasonable / many no-effect families

### Problem

Some effects were added quickly as placeholder fantasy utility:

- sandstone speed
- calcite night vision
- mossy cobblestone regeneration
- tuff haste

These are mechanically useful but not always physically grounded.

Many families have no effects at all, especially the 12 plank variants.

### Better design principle

Not every set needs a strong effect. Effects should be grouped by material properties:

#### Wood / plank variants

- mostly visual variety
- low defense, flammable in future if implemented
- no strong buffs
- optional small differences only:
  - bamboo: lighter movement/jump but lower durability
  - crimson: slightly fire-resistant or nether-safe, not full immunity
  - warped: slight fall/ender flavor, very minor

#### Heavy stones

- deepslate / blackstone / obsidian: strong protection + slowness
- this is already a good direction

#### Brittle hard materials

- glass / calcite / quartz / amethyst: high-ish mitigation but lower durability and shatter chance
- this is the right direction; tune values rather than add more buffs

#### Soft/elastic materials

- slime: special movement/defense, high upkeep cost
- current direction is good, but cost/durability must be rebalanced

#### Organic/prickly materials

- cactus: per-piece retaliation is appropriate
- bone: maybe undead/skeleton flavor, not necessarily night vision
- mossy: should not be strong regeneration; maybe tiny healing only when wet/raining, or no effect

#### Redstone

- redstone signal is the main identity
- speed may be acceptable but should maybe be weaker or tied to movement/boots, not full-set generic buff

### Next effect rebalance proposal

1. Remove or weaken strong generic buffs from common materials.
2. Keep no-effect sets as valid if their role is visual/cheap armor.
3. Move all set effect decisions through `set_effects.json`, not Java.
4. Add tooltip text that describes weaknesses as much as strengths.

## Proposed next implementation order

### Round A — Fix redstone signal and slime cost

- Target redstone dust/repeater query path specifically.
- Change slime ingredient/cost/durability through `equipment_families.json`.
- Keep changes small and testable.

### Round B — Fix inventory icon pipeline

- Use provided emerald armor templates as universal item-icon silhouette.
- Generate wood/stone/cobble icons from material palettes with cleaner hand-tuned fills.
- Avoid raw noisy block texture fills at 16×16.

### Round C — Tool/weapon expansion

- Add end_stone, blackstone, cobbled_deepslate, tuff, calcite, sandstone weapons/tools as curated lists.
- Do not add full toolsets blindly.

### Round D — Effect rebalance

- Revisit every set in `set_effects.json`.
- Decide which sets should intentionally have no effect.
- Convert placeholder effects into material-logic effects.

## Immediate recommendation

Start next with Round A:

1. redstone dust detection fix
2. slime armor cost/durability rebalance

These are the most concrete gameplay bugs from the user report.
