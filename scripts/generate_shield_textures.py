#!/usr/bin/env python3
"""Generate custom shield base textures from vanilla shield resources.

The vanilla 26.1 shield special renderer uses the shield pattern atlas. We add
material-specific base textures under assets/minecraft/textures/entity/shield/
dream_equipment/ so they are included by vanilla's shield atlas directory source,
then a small client mixin selects the texture via a custom item data component.
"""
from __future__ import annotations

import io
import json
import zipfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "src/main/resources"
MC_CLIENT_JAR = Path.home() / ".gradle/caches/fabric-loom/26.1.2/minecraft-client.jar"
FAMILY_JSON = RES / "data/dream_equipment/equipment_families.json"
OUT_DIR = RES / "assets/minecraft/textures/entity/shield/dream_equipment"

BLOCK_OVERRIDES = {
    "minecraft:emerald": "emerald_block",
    "minecraft:lapis_lazuli": "lapis_block",
    "minecraft:redstone": "redstone_block",
    "minecraft:quartz": "quartz_block_side",
    "minecraft:amethyst_shard": "amethyst_block",
    "minecraft:prismarine_shard": "prismarine",
    "minecraft:slime_block": "slime_block",
    "minecraft:coal": "coal_block",
    "minecraft:charcoal": "coal_block",
    "minecraft:bone": "bone_block_side",
    "minecraft:paper": "white_wool",
    "minecraft:glass": "glass",
    "minecraft:cactus": "cactus_side",
    "minecraft:armadillo_scute": "brown_wool",
    "minecraft:turtle_scute": "turtle_egg",
}


def load_from_jar(path: str) -> Image.Image:
    with zipfile.ZipFile(MC_CLIENT_JAR) as zf:
        return Image.open(io.BytesIO(zf.read(path))).convert("RGBA")


def load_block_texture(block_name: str) -> Image.Image:
    return load_from_jar(f"assets/minecraft/textures/block/{block_name}.png")


def block_texture_for_ingredient(ingredient: str) -> str:
    if ingredient in BLOCK_OVERRIDES:
        return BLOCK_OVERRIDES[ingredient]
    if ingredient.startswith("minecraft:"):
        return ingredient.split(":", 1)[1]
    return "dark_oak_planks"


def luminance(rgb: tuple[int, int, int]) -> float:
    return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]


def clamp(v: float) -> int:
    return max(0, min(255, int(round(v))))


def mix(a: tuple[int, int, int], b: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    return tuple(clamp(a[i] * (1 - t) + b[i] * t) for i in range(3))


def shade(c: tuple[int, int, int], factor: float) -> tuple[int, int, int]:
    return tuple(clamp(v * factor) for v in c)


def sample(texture: Image.Image, x: int, y: int) -> tuple[int, int, int]:
    w, h = texture.size
    r, g, b, a = texture.getpixel((x % w, y % h))
    if a == 0:
        # Transparent source materials such as glass: blend toward pale cyan.
        return (170, 215, 225)
    return (r, g, b)


def is_vanilla_wood_pixel(r: int, g: int, b: int, a: int) -> bool:
    if a == 0:
        return False
    # Vanilla shield wood is brown/yellow; gray rim/handle should be preserved.
    return r > 55 and g > 35 and b < 95 and (r - b) > 24 and (g - b) > 8


def generate(base: Image.Image, material: Image.Image, family: str) -> Image.Image:
    out = Image.new("RGBA", base.size, (0, 0, 0, 0))
    seed = sum(ord(c) for c in family)
    for y in range(base.height):
        for x in range(base.width):
            r, g, b, a = base.getpixel((x, y))
            if a == 0:
                continue
            if is_vanilla_wood_pixel(r, g, b, a):
                raw = sample(material, x * 2 + seed, y * 2 + seed // 3)
                vanilla_lum = luminance((r, g, b))
                factor = 0.62 + (vanilla_lum / 255.0) * 0.78
                c = shade(raw, factor)
                # Preserve vanilla shield carved vertical-board rhythm on front/back.
                if x % 4 == 0 and y < 42:
                    c = mix(c, (38, 30, 26), 0.18)
                out.putpixel((x, y), (*c, a))
            else:
                out.putpixel((x, y), (r, g, b, a))
    return out


def main() -> None:
    if not MC_CLIENT_JAR.exists():
        raise SystemExit(f"Missing Minecraft client jar: {MC_CLIENT_JAR}")
    base = load_from_jar("assets/minecraft/textures/entity/shield/shield_base_nopattern.png")
    families = json.loads(FAMILY_JSON.read_text(encoding="utf-8"))["families"]
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    count = 0
    for fam in families:
        shield = fam.get("shield")
        if not (shield and shield.get("enabled", True)):
            continue
        family = fam["id"]
        block_name = block_texture_for_ingredient(fam["ingredient"])
        try:
            material = load_block_texture(block_name)
        except KeyError:
            material = load_block_texture("dark_oak_planks")
        image = generate(base, material, family)
        image.save(OUT_DIR / f"{family}_shield_base_nopattern.png")
        count += 1
    print(f"Generated Dream Equipment shield base textures: files={count}")


if __name__ == "__main__":
    main()
