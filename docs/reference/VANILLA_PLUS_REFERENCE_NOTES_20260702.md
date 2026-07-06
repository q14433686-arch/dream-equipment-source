# Vanilla+ / VKL+ Reference Notes — 2026-07-02

Source link supplied by user:

- https://modrinth.com/mod/vanilla-plus-data-pack

## Role in this project

Vanilla+ is a reference for style, scope, and balance direction only. This project remains a standalone Fabric mod with real registered items.

## License / asset boundary

Modrinth API reports the project license as `LicenseRef-All-Rights-Reserved`. Therefore:

- Do not copy or include Vanilla+ texture pixels directly.
- Do not redistribute their resource pack assets inside this project.
- Allowed workflow unless explicit permission is provided: use the screenshots/resource pack as visual reference and redraw original textures in a vanilla-compatible style.

If the user later provides explicit permission or a compatible license from the author, this boundary can be revisited.

## Useful reference points

Vanilla+ includes custom armor/tool tiers such as lapis, resin, redstone, quartz, emerald, amethyst, nether star, turtle armor, robes, and related tools/weapons. For the first Dream Equipment content pass, the most relevant design cues are:

- Emerald gear: positioned around diamond-level in Vanilla+; good reference for "dream but still vanilla-like" green gear.
- Quartz/redstone/lapis style: useful examples for turning vanilla materials into complete equipment families.
- Vanilla-style silhouettes: item icons should look like Mojang-adjacent material swaps, not hyper-detailed modded gear.
- Datapack limitation lesson: Vanilla+ uses datapack/resource-pack tricks, while Dream Equipment should implement real mod items, real armor/tool materials, recipes, models, and language keys.

## Suggested Dream Equipment interpretation

Initial content should not blindly mirror Vanilla+. Suggested standalone identity:

1. Emerald set — prestige gear, roughly between iron and diamond or diamond-like depending user preference.
2. Wooden armor — early novelty/protection, weak durability and defense.
3. Stone/cobblestone armor — stronger than wood, weaker than iron, heavy-looking gray visuals.
4. Optional later material sets — lapis/redstone/quartz/amethyst if user wants a broader Vanilla+-like scope.

## Texture approach

Use original 16x16/armor-layer art generated for this project:

- Palette reference only: emerald green, stone gray, wood brown.
- Preserve vanilla tool/armor silhouettes.
- Add small material-specific highlights: emerald facets, cobblestone cracks, wood plank grain.
- Avoid one-to-one pixel layout duplication from Vanilla+ screenshots/resources.
