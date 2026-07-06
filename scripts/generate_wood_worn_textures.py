#!/usr/bin/env python3
"""Generate wood/plank and log/stem worn equipment textures.

The current MC 26.1 equipment spec uses:
- assets/<namespace>/equipment/<material>.json
- textures/entity/equipment/humanoid/<material>.png          64x32
- textures/entity/equipment/humanoid_leggings/<material>.png 64x32
- textures/entity/equipment/humanoid_baby/<material>.png     64x64

This script deliberately preserves the existing alpha/UV mask and replaces only
non-transparent interior pixels. No lines are drawn outside the mask.
"""
from __future__ import annotations

import io
import math
import statistics
import zipfile
from pathlib import Path
from typing import Iterable

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "src/main/resources"
MOD = "dream_equipment"
MC_CLIENT_JAR = Path.home() / ".gradle/caches/fabric-loom/26.1.2/minecraft-client.jar"

PLANK_TEXTURES = {
    "oak": "oak_planks",
    "spruce": "spruce_planks",
    "birch": "birch_planks",
    "jungle": "jungle_planks",
    "acacia": "acacia_planks",
    "dark_oak": "dark_oak_planks",
    "mangrove": "mangrove_planks",
    "cherry": "cherry_planks",
    "pale_oak": "pale_oak_planks",
    "bamboo": "bamboo_planks",
    "crimson": "crimson_planks",
    "warped": "warped_planks",
}

LOG_TEXTURES = {
    "oak_log": "oak_log",
    "spruce_log": "spruce_log",
    "birch_log": "birch_log",
    "jungle_log": "jungle_log",
    "acacia_log": "acacia_log",
    "dark_oak_log": "dark_oak_log",
    "mangrove_log": "mangrove_log",
    "cherry_log": "cherry_log",
    "pale_oak_log": "pale_oak_log",
    "bamboo_block": "bamboo_block",
    "crimson_stem": "crimson_stem",
    "warped_stem": "warped_stem",
}

# Families being tested with low-frequency, component-local plank panels.
# Keep this list narrow until the art direction is accepted in client.
PIECE_AWARE_PLANK_FAMILIES = set(PLANK_TEXTURES.keys())

LAYER_PATHS = [
    ("humanoid", "{family}.png"),
    ("humanoid_leggings", "{family}_leggings.png"),
    ("humanoid_baby", "{family}.png"),
]


def load_vanilla_texture(block_name: str) -> Image.Image:
    with zipfile.ZipFile(MC_CLIENT_JAR) as zf:
        data = zf.read(f"assets/minecraft/textures/block/{block_name}.png")
    return Image.open(io.BytesIO(data)).convert("RGBA")


def luminance(rgb: tuple[int, int, int]) -> float:
    r, g, b = rgb
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def clamp(v: float) -> int:
    return max(0, min(255, int(round(v))))


def mix(a: tuple[int, int, int], b: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    return tuple(clamp(a[i] * (1.0 - t) + b[i] * t) for i in range(3))


def shade(c: tuple[int, int, int], factor: float) -> tuple[int, int, int]:
    return tuple(clamp(v * factor) for v in c)


def palette(texture: Image.Image) -> list[tuple[int, int, int]]:
    colors = [(r, g, b) for r, g, b, a in texture.getdata() if a > 0]
    return sorted(colors, key=luminance)


def quantile_color(colors: list[tuple[int, int, int]], q: float) -> tuple[int, int, int]:
    if not colors:
        return (128, 128, 128)
    idx = max(0, min(len(colors) - 1, int(round((len(colors) - 1) * q))))
    return colors[idx]


def average_color(colors: Iterable[tuple[int, int, int]]) -> tuple[int, int, int]:
    values = list(colors)
    if not values:
        return (128, 128, 128)
    return tuple(clamp(statistics.mean(c[i] for c in values)) for i in range(3))


def sample(texture: Image.Image, x: int, y: int) -> tuple[int, int, int]:
    w, h = texture.size
    r, g, b, _ = texture.getpixel((x % w, y % h))
    return (r, g, b)


def is_edge(mask: Image.Image, x: int, y: int) -> bool:
    if mask.getpixel((x, y))[3] == 0:
        return False
    w, h = mask.size
    for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
        if nx < 0 or ny < 0 or nx >= w or ny >= h or mask.getpixel((nx, ny))[3] == 0:
            return True
    return False


def source_rank(mask: Image.Image, x: int, y: int, mn: float, mx: float) -> float:
    r, g, b, _ = mask.getpixel((x, y))
    return (luminance((r, g, b)) - mn) / max(1.0, mx - mn)


def component_bounds(mask: Image.Image) -> dict[tuple[int, int], tuple[int, int, int, int]]:
    """Return per-pixel connected-component bounds for opaque armor pixels."""
    w, h = mask.size
    seen: set[tuple[int, int]] = set()
    bounds: dict[tuple[int, int], tuple[int, int, int, int]] = {}
    for sy in range(h):
        for sx in range(w):
            if (sx, sy) in seen or mask.getpixel((sx, sy))[3] == 0:
                continue
            stack = [(sx, sy)]
            seen.add((sx, sy))
            pixels: list[tuple[int, int]] = []
            while stack:
                x, y = stack.pop()
                pixels.append((x, y))
                for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                    if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in seen and mask.getpixel((nx, ny))[3] > 0:
                        seen.add((nx, ny))
                        stack.append((nx, ny))
            xs = [x for x, _ in pixels]
            ys = [y for _, y in pixels]
            bbox = (min(xs), min(ys), max(xs), max(ys))
            for pixel in pixels:
                bounds[pixel] = bbox
    return bounds


def plank_piece_rgb(texture: Image.Image, pal: list[tuple[int, int, int]], base: tuple[int, int, int], x: int, y: int, rank: float, bbox: tuple[int, int, int, int]) -> tuple[int, int, int]:
    """Low-frequency vanilla-plank fill with a few large panel seams.

    This is intended for the cherry test pass: use the original block texture as
    the source, but map a whole armor UV component to the 16x16 block once rather
    than tiling dense horizontal stripes across the body.
    """
    min_x, min_y, max_x, max_y = bbox
    bw = max(1, max_x - min_x + 1)
    bh = max(1, max_y - min_y + 1)
    lx = x - min_x
    ly = y - min_y
    tx = round(lx / max(1, bw - 1) * 15)
    ty = round(ly / max(1, bh - 1) * 15)
    raw = sample(texture, tx, ty)
    c = mix(base, raw, 0.92)
    c = shade(c, 0.86 + rank * 0.22)
    dark = quantile_color(pal, 0.11)
    light = quantile_color(pal, 0.86)

    # A few large vertical board joins, not repeated horizontal banding.
    seam = False
    if bw >= 12:
        seam_positions = {bw // 3, (2 * bw) // 3}
        seam = any(abs(lx - pos) <= 0 for pos in seam_positions)
    if seam:
        c = mix(c, dark, 0.58)
    elif bw >= 12 and any(abs(lx - pos) == 1 for pos in {bw // 3, (2 * bw) // 3}):
        c = mix(c, light, 0.10)

    # One restrained horizontal plate break only for tall UV chunks.
    if bh >= 14 and abs(ly - bh // 2) == 0 and bw >= 8:
        c = mix(c, dark, 0.34)
    return c


def plank_rgb(texture: Image.Image, pal: list[tuple[int, int, int]], base: tuple[int, int, int], x: int, y: int, rank: float, seed: int) -> tuple[int, int, int]:
    # Step 1 art rule: reuse the corresponding vanilla plank block texture directly.
    # No synthetic board bands or joins here; the vanilla block texture already owns
    # the material language. Keep only a small amount of existing armor UV shading.
    raw = sample(texture, x * 2 + seed, y * 2 + seed // 2)
    c = mix(base, raw, 0.86)
    return shade(c, 0.82 + rank * 0.30)


def log_rgb(texture: Image.Image, pal: list[tuple[int, int, int]], base: tuple[int, int, int], x: int, y: int, rank: float, seed: int) -> tuple[int, int, int]:
    # Step 1 art rule: reuse the corresponding vanilla log/stem/bamboo block texture
    # directly. Do not add extra generated bark bands yet; first establish the raw
    # source-material look inside the current equipment UV mask.
    raw = sample(texture, x * 2 + seed, y * 2 + seed)
    c = mix(base, raw, 0.90)
    return shade(c, 0.80 + rank * 0.28)


def regenerate_layer(path: Path, texture: Image.Image, style: str, seed: int, family: str) -> None:
    mask = Image.open(path).convert("RGBA")
    if mask.size not in {(64, 32), (64, 64)}:
        raise SystemExit(f"Unexpected equipment texture size for {path.relative_to(ROOT)}: {mask.size}")
    pal = palette(texture)
    base = average_color(pal[int(len(pal) * 0.20): int(len(pal) * 0.78)] or pal)
    edge_dark = quantile_color(pal, 0.05)

    opaque = [(r, g, b) for r, g, b, a in mask.getdata() if a > 0]
    lum_values = [luminance(c) for c in opaque]
    mn, mx = (min(lum_values), max(lum_values)) if lum_values else (0.0, 255.0)

    out = Image.new("RGBA", mask.size, (0, 0, 0, 0))
    bounds = component_bounds(mask) if style == "plank" and family in PIECE_AWARE_PLANK_FAMILIES else {}
    for y in range(mask.height):
        for x in range(mask.width):
            _, _, _, a = mask.getpixel((x, y))
            if a == 0:
                continue
            rank = source_rank(mask, x, y, mn, mx)
            if style == "plank":
                if family in PIECE_AWARE_PLANK_FAMILIES:
                    rgb = plank_piece_rgb(texture, pal, base, x, y, rank, bounds[(x, y)])
                else:
                    rgb = plank_rgb(texture, pal, base, x, y, rank, seed)
                if is_edge(mask, x, y):
                    rgb = mix(rgb, edge_dark, 0.50)
            else:
                rgb = log_rgb(texture, pal, base, x, y, rank, seed)
                if is_edge(mask, x, y):
                    rgb = mix(rgb, edge_dark, 0.63)
            out.putpixel((x, y), (*rgb, a))
    out.save(path)


def main() -> None:
    if not MC_CLIENT_JAR.exists():
        raise SystemExit(f"Missing Minecraft client jar: {MC_CLIENT_JAR}")
    count = 0
    for style, mapping in (("plank", PLANK_TEXTURES), ("log", LOG_TEXTURES)):
        for index, (family, texture_name) in enumerate(mapping.items()):
            texture = load_vanilla_texture(texture_name)
            for layer_index, (layer_dir, pattern) in enumerate(LAYER_PATHS):
                path = RES / f"assets/{MOD}/textures/entity/equipment/{layer_dir}" / pattern.format(family=family)
                if not path.exists():
                    raise SystemExit(f"Missing equipment layer: {path.relative_to(ROOT)}")
                regenerate_layer(path, texture, style, seed=(index + 1) * 23 + (layer_index + 1) * 7, family=family)
                count += 1
    print(f"Regenerated wood/plank/log worn equipment texture interiors: files={count}")


if __name__ == "__main__":
    main()
