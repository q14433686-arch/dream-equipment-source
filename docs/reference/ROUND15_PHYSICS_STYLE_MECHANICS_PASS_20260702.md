# Round 15 Physics-Style Mechanics Pass — 2026-07-02

## User direction

The user clarified that not every armor set should have a strong fantasy effect. Mechanics should follow material properties and Minecraft style:

- heavy armor should slow movement
- hard but brittle materials should have high protection but low durability / shatter chance
- slime armor should consume durability continuously and return small amounts of slime, provide occasional damage immunity, and slime boots should behave like slime-block landing protection
- emerald armor should provide trade price reduction
- redstone boots should provide redstone signal strength (requires a dedicated redstone-power implementation, see notes)

## Implemented this round

### Emerald set trade flavor

Full emerald set now grants:

- `Luck I`
- `Hero of the Village I`

The latter is used as a vanilla-style first implementation of trade discount behavior. This is not a custom merchant-price hook yet, but it should trigger vanilla discount behavior where Hero of the Village is respected.

### Slime armor deeper mechanics

Full slime set now has multiple material-style mechanics:

1. Continuous durability loss:
   - while a full slime set is worn, each slime armor piece loses 1 durability every game tick.

2. Partial slime-ball return on break:
   - when a slime armor piece breaks from this continuous decay, it is removed and gives back a small number of slime balls.
   - helmet: 2 slime balls
   - chestplate: 3 slime balls
   - leggings: 3 slime balls
   - boots: 2 slime balls

3. 10% damage immunity:
   - while wearing the full slime set, incoming damage has a 10% chance to be canceled.

4. Slime boots landing behavior:
   - wearing slime boots cancels fall damage from falls of 12 blocks or less.
   - the wearer bounces upward after landing, like a simplified slime-block bounce.

The older full-set Jump Boost + Slow Falling and partial post-fall recovery remain.

### Brittle high-hardness materials

Hard/brittle full sets now have shatter checks on heavy hits:

- glass full set: if damage ≥ 6, 25% chance to shatter one random glass armor piece
- calcite full set: if damage ≥ 5, 20% chance to shatter one random calcite armor piece
- quartz full set: if damage ≥ 7, 10% chance to shatter one random quartz armor piece
- amethyst full set: if damage ≥ 8, 8% chance to shatter one random amethyst armor piece

This moves those materials closer to “good protection / brittle failure” behavior without adding custom damage types yet.

### Heavy armor penalties

Heavy armor behavior already exists and remains:

- obsidian full set: Resistance + Fire Resistance + Slowness
- cobbled deepslate full set: Resistance + Slowness
- blackstone full set: Fire Resistance + Slowness

This matches the heavy-material direction.

## Not fully implemented yet

### Redstone boots emitting redstone signal

A wearable item cannot emit real redstone power through data tags or simple tick effects. True signal output requires a world/block power integration, likely a mixin into redstone signal queries or a helper block/entity approach.

This pass does not fake the feature with particles/effects. Recommended next implementation:

1. decide exact behavior: signal at player block position, block below player, or adjacent blocks?
2. add a redstone-signal provider/mixin for level/block power queries
3. redstone boots contribute configured signal strength, e.g. 7 or 15
4. test with redstone dust, repeaters, observers/comparators if applicable

## Validation

Executed:

```bash
python3 scripts/validate_dream_equipment_assets.py
JAVA_HOME=/tmp/herbcraft-jdk25/jdk-25 bash ./gradlew --no-daemon build --rerun-tasks
```

Results:

- Asset/source validator: PASS — 184 items, 37 materials.
- Build: PASS.

## Client-only checks

- Verify emerald set discounts through Hero of the Village behavior.
- Verify slime full set durability drops every tick and returns slime balls on break.
- Verify slime full set 10% damage cancel can trigger.
- Verify slime boots cancel ≤12 block fall damage and bounce.
- Verify brittle sets shatter at acceptable rates.
- Verify heavy armor slowness feels acceptable.
