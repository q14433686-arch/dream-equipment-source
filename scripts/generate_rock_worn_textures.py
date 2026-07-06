#!/usr/bin/env python3
"""Generate stone/rock/mineral worn equipment textures.

Strategy:
- Preserve existing UV alpha mask exactly (shape unchanged).
- Sample each non-transparent pixel's colour from the corresponding vanilla
  block texture, mapped by the pixel's relative position within its UV region.
- Apply per-family colour correction where the source block avg deviates
  significantly from what was previously generated.
- Apply a simple 3-level shading pass (edge darkening, face shading) to give
  depth without adding extra colours beyond the block palette.
- Write humanoid, humanoid_leggings, and humanoid_baby layers.

Run:
    python3 scripts/generate_rock_worn_textures.py            # check mode
    python3 scripts/generate_rock_worn_textures.py --write    # write mode
"""
from __future__ import annotations

import argparse
import io
import math
import statistics
import zipfile
from pathlib import Path
from typing import Any

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "src/main/resources"
MOD = "dream_equipment"
MC_CLIENT_JAR = Path.home() / ".gradle/caches/fabric-loom/26.1.2/minecraft-client.jar"

LAYER_DIRS = ["humanoid", "humanoid_leggings", "humanoid_baby"]

# ---------------------------------------------------------------------------
# Per-family config
# ---------------------------------------------------------------------------
# block_texture : name inside assets/minecraft/textures/block/
# correction    : (dr, dg, db) added to sampled colour before clamping
# edge_q        : quantile (0-1) of palette used for edge/outline pixels
# dark_q        : quantile used for the darkest interior shading level
# light_q       : quantile used for the lightest interior shading level
# feature       : optional special-case handler name
# ---------------------------------------------------------------------------
FAMILY_CONFIG: dict[str, dict[str, Any]] = {
    # ── P0: severe colour deviation ─────────────────────────────────────
    "obsidian": {
        "block_texture": "obsidian",
        # Current worn B≈81, source B≈24 → pull strongly toward true near-black
        "correction": (+2, +1, -19),
        "edge_q": 0.0,
        "dark_q": 0.05,
        "light_q": 0.75,
    },
    "lapis": {
        "block_texture": "lapis_block",
        # Current B≈183 vs source B≈140 → reduce blue, add gold highlight
        "correction": (+3, 0, +13),
        "edge_q": 0.0,
        "dark_q": 0.05,
        "light_q": 0.85,
        "feature": "lapis_gold_highlight",
    },
    "quartz": {
        "block_texture": "quartz_block_side",
        # Current warm-yellow #ddd2bd vs cold-white #ebe5de → reduce R-B gap
        "correction": (-10, -9, -15),
        "edge_q": 0.15,
        "dark_q": 0.30,
        "light_q": 0.95,
    },
    # ── P1: moderate deviation / lost material character ─────────────────
    "redstone": {
        "block_texture": "redstone_block",
        # Preserve the strong dark-red / bright-red contrast of redstone_block
        "correction": (+1, +1, -19),
        "edge_q": 0.0,
        "dark_q": 0.02,
        "light_q": 0.90,
        "feature": "redstone_circuit",
    },
    "amethyst": {
        "block_texture": "amethyst_block",
        # Target avg #8561bf — calibrated iteratively
        "correction": (+15, +4, +17),
        "edge_q": 0.05,
        "dark_q": 0.10,
        "light_q": 0.88,
    },
    # ── P2: colour OK, need material texture character ────────────────────
    "cobblestone": {
        "block_texture": "cobblestone",
        "correction": (+16, +16, +16),
        "edge_q": 0.05,
        "dark_q": 0.10,
        "light_q": 0.85,
        "feature": "cobble_seams",
    },
    "blackstone": {
        "block_texture": "blackstone",
        "correction": (0, 0, 0),
        "edge_q": 0.00,
        "dark_q": 0.05,
        "light_q": 0.80,
        "feature": "blackstone_veins",
    },
    "diorite": {
        "block_texture": "diorite",
        "correction": (0, 0, 0),
        "edge_q": 0.10,
        "dark_q": 0.20,
        "light_q": 0.95,
        "feature": "diorite_speckle",
    },
    "granite": {
        "block_texture": "granite",
        "correction": (0, 0, 0),
        "edge_q": 0.05,
        "dark_q": 0.15,
        "light_q": 0.85,
        "feature": "granite_speckle",
    },
    # ── P3: refresh from source block for consistency ─────────────────────
    "stone": {
        "block_texture": "stone",
        "correction": (0, 0, 0),
        "edge_q": 0.05,
        "dark_q": 0.15,
        "light_q": 0.85,
    },
    "cobbled_deepslate": {
        "block_texture": "cobbled_deepslate",
        "correction": (0, 0, 0),
        "edge_q": 0.05,
        "dark_q": 0.10,
        "light_q": 0.85,
        "feature": "cobble_seams",
    },
    "sandstone": {
        "block_texture": "sandstone",
        "correction": (0, 0, 0),
        "edge_q": 0.10,
        "dark_q": 0.20,
        "light_q": 0.92,
    },
    "red_sandstone": {
        "block_texture": "red_sandstone",
        "correction": (0, 0, 0),
        "edge_q": 0.05,
        "dark_q": 0.15,
        "light_q": 0.88,
    },
    "end_stone": {
        "block_texture": "end_stone",
        "correction": (0, 0, 0),
        "edge_q": 0.10,
        "dark_q": 0.20,
        "light_q": 0.90,
    },
    "tuff": {
        "block_texture": "tuff",
        "correction": (0, 0, 0),
        "edge_q": 0.05,
        "dark_q": 0.15,
        "light_q": 0.88,
    },
    "calcite": {
        "block_texture": "calcite",
        "correction": (0, 0, 0),
        "edge_q": 0.10,
        "dark_q": 0.25,
        "light_q": 0.95,
    },
    "andesite": {
        "block_texture": "andesite",
        "correction": (0, 0, 0),
        "edge_q": 0.05,
        "dark_q": 0.15,
        "light_q": 0.85,
    },
    "basalt": {
        "block_texture": "basalt_side",
        "correction": (0, 0, 0),
        "edge_q": 0.00,
        "dark_q": 0.05,
        "light_q": 0.80,
        "feature": "basalt_stripes",
    },
    "smooth_basalt": {
        "block_texture": "smooth_basalt",
        # Slightly lighter/warmer than basalt for distinction
        "correction": (+4, +4, +4),
        "edge_q": 0.02,
        "dark_q": 0.08,
        "light_q": 0.82,
    },
    "dripstone_block": {
        "block_texture": "dripstone_block",
        "correction": (0, 0, 0),
        "edge_q": 0.05,
        "dark_q": 0.10,
        "light_q": 0.85,
    },
    "netherrack": {
        "block_texture": "netherrack",
        "correction": (0, 0, 0),
        "edge_q": 0.00,
        "dark_q": 0.05,
        "light_q": 0.85,
        "feature": "netherrack_pits",
    },
    "mossy_cobblestone": {
        "block_texture": "mossy_cobblestone",
        "correction": (+15, +13, +21),
        "edge_q": 0.05,
        "dark_q": 0.10,
        "light_q": 0.88,
        "feature": "cobble_seams",
    },
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def clamp(v: float) -> int:
    return max(0, min(255, int(round(v))))


def luminance(r: int, g: int, b: int) -> float:
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def mix(
    a: tuple[int, int, int], b: tuple[int, int, int], t: float
) -> tuple[int, int, int]:
    return (
        clamp(a[0] * (1 - t) + b[0] * t),
        clamp(a[1] * (1 - t) + b[1] * t),
        clamp(a[2] * (1 - t) + b[2] * t),
    )


def shade(c: tuple[int, int, int], factor: float) -> tuple[int, int, int]:
    return (clamp(c[0] * factor), clamp(c[1] * factor), clamp(c[2] * factor))


def load_block_texture(name: str) -> Image.Image:
    with zipfile.ZipFile(MC_CLIENT_JAR) as zf:
        data = zf.read(f"assets/minecraft/textures/block/{name}.png")
    return Image.open(io.BytesIO(data)).convert("RGBA")


def build_palette(
    img: Image.Image,
) -> list[tuple[int, int, int]]:
    """Return opaque pixels sorted by luminance."""
    colors = [
        (r, g, b)
        for r, g, b, a in img.convert("RGBA").get_flattened_data()
        if a > 0
    ]
    return sorted(colors, key=lambda c: luminance(*c))


def quantile_color(
    palette: list[tuple[int, int, int]], q: float
) -> tuple[int, int, int]:
    if not palette:
        return (128, 128, 128)
    idx = max(0, min(len(palette) - 1, int(round((len(palette) - 1) * q))))
    return palette[idx]


def sample_block(
    block: Image.Image, x: int, y: int
) -> tuple[int, int, int]:
    bw, bh = block.size
    r, g, b, _ = block.getpixel((x % bw, y % bh))
    return (r, g, b)


def is_edge(mask: Image.Image, x: int, y: int) -> bool:
    if mask.getpixel((x, y))[3] == 0:
        return False
    w, h = mask.size
    for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
        if nx < 0 or ny < 0 or nx >= w or ny >= h or mask.getpixel((nx, ny))[3] == 0:
            return True
    return False


def region_bounds(mask: Image.Image) -> tuple[int, int, int, int]:
    """Bounding box of all opaque pixels in the mask."""
    arr_data = [(x, y) for y in range(mask.height) for x in range(mask.width)
                if mask.getpixel((x, y))[3] > 0]
    if not arr_data:
        return (0, 0, mask.width - 1, mask.height - 1)
    xs = [p[0] for p in arr_data]
    ys = [p[1] for p in arr_data]
    return (min(xs), min(ys), max(xs), max(ys))


def uv_rel(x: int, y: int, bounds: tuple[int, int, int, int]) -> tuple[float, float]:
    """Normalised position of (x, y) within the opaque bounding box."""
    x0, y0, x1, y1 = bounds
    rx = (x - x0) / max(1, x1 - x0)
    ry = (y - y0) / max(1, y1 - y0)
    return rx, ry


# ---------------------------------------------------------------------------
# UV region identification
# The humanoid worn texture UV has several distinct panels.
# We identify which panel each pixel belongs to so we can map it to a
# coherent section of the block texture rather than a global tile.
#
# Panels (from iron.png observation):
#   HEAD_FRONT   y 0-7   x 8-15
#   HELMET_WRAP  y 8-15  x 0-31
#   ARM_TOP      y 16-19 x 8-47
#   BODY_FRONT   y 20-25 x 16-55
#   WAIST        y 26-31 x 0-39
#
# humanoid_leggings UV (from iron leggings observation):
#   WAIST_TOP    y 16-19 x 4-7
#   LEFT_LEG     y 20-31 x 0-15
#   RIGHT_LEG    y 27-31 x 16-39
# ---------------------------------------------------------------------------

def block_uv_for_pixel(
    x: int,
    y: int,
    block_w: int,
    block_h: int,
    layer_dir: str,
) -> tuple[int, int]:
    """Map a worn-texture pixel (x, y) to a block texture coordinate."""
    # Each UV panel maps independently to the 16×16 block.
    # We compute a normalised (u, v) in [0,1]² per panel, then scale.
    if layer_dir in ("humanoid", "humanoid_baby"):
        if y <= 7:
            # HEAD_FRONT: x 8-15, y 0-7  →  map to block top-left quadrant
            u = (x - 8) / 7.0
            v = y / 7.0
        elif y <= 15:
            # HELMET_WRAP: x 0-31, y 8-15
            u = x / 31.0
            v = (y - 8) / 7.0
        elif y <= 19:
            # ARM_TOP: x 8-47, y 16-19  →  map to block top strip
            u = (x - 8) / 39.0
            v = (y - 16) / 3.0
        elif y <= 25:
            # BODY_FRONT: x 16-55, y 20-25
            u = (x - 16) / 39.0
            v = (y - 20) / 5.0
        else:
            # WAIST: x 0-39, y 26-31
            u = x / 39.0
            v = (y - 26) / 5.0
    else:
        # humanoid_leggings
        if y <= 19:
            u = (x - 4) / 3.0
            v = (y - 16) / 3.0
        elif y <= 26:
            # LEFT_LEG
            u = x / 15.0
            v = (y - 20) / 6.0
        else:
            # RIGHT_LEG
            u = (x - 16) / 23.0
            v = (y - 27) / 4.0

    u = max(0.0, min(1.0, u))
    v = max(0.0, min(1.0, v))
    bx = int(round(u * (block_w - 1)))
    by = int(round(v * (block_h - 1)))
    return bx, by


# ---------------------------------------------------------------------------
# Feature handlers
# ---------------------------------------------------------------------------

def feature_cobble_seams(
    base: tuple[int, int, int],
    x: int,
    y: int,
    block: Image.Image,
    palette: list[tuple[int, int, int]],
    rx: float,
    ry: float,
) -> tuple[int, int, int]:
    """
    Simulate cobblestone's irregular block divisions by darkening pixels that
    land near the inter-stone boundary (detected via luminance jump in source).
    """
    bw, bh = block.size
    bx = int(rx * (bw - 1))
    by = int(ry * (bh - 1))
    # Compare this pixel to its right and below neighbours in the block
    c0 = block.getpixel((bx, by))[:3]
    c1 = block.getpixel((min(bx + 1, bw - 1), by))[:3]
    c2 = block.getpixel((bx, min(by + 1, bh - 1)))[:3]
    lum0 = luminance(*c0)
    lum1 = luminance(*c1)
    lum2 = luminance(*c2)
    contrast = max(abs(lum0 - lum1), abs(lum0 - lum2))
    if contrast > 18:
        # We're on a seam – darken significantly
        dark = quantile_color(palette, 0.05)
        return mix(base, dark, 0.55)
    return base


def feature_blackstone_veins(
    base: tuple[int, int, int],
    x: int,
    y: int,
    block: Image.Image,
    palette: list[tuple[int, int, int]],
    rx: float,
    ry: float,
) -> tuple[int, int, int]:
    """
    Blackstone has subtle purple/blue layer veins. Amplify them by checking
    the B-channel dominance of the sampled block pixel.
    """
    bw, bh = block.size
    bx = int(rx * (bw - 1))
    by = int(ry * (bh - 1))
    r, g, b, _ = block.getpixel((bx, by))
    # If this block pixel is notably more blue than its luminance average
    lum = luminance(r, g, b)
    if b > lum * 1.35 and b > 28:
        # It's a vein pixel – tint slightly toward purple
        purple = quantile_color(palette, 0.75)
        return mix(base, purple, 0.40)
    return base


def feature_diorite_speckle(
    base: tuple[int, int, int],
    x: int,
    y: int,
    block: Image.Image,
    palette: list[tuple[int, int, int]],
    rx: float,
    ry: float,
) -> tuple[int, int, int]:
    """
    Diorite has a distinctive salt-and-pepper speckle of very dark and very
    light pixels. Identify them and reproduce with higher contrast.
    """
    bw, bh = block.size
    bx = int(rx * (bw - 1))
    by = int(ry * (bh - 1))
    r, g, b, _ = block.getpixel((bx, by))
    lum = luminance(r, g, b)
    avg_lum = luminance(*quantile_color(palette, 0.50))
    # Very dark speckle
    if lum < avg_lum * 0.65:
        dark = quantile_color(palette, 0.04)
        return mix(base, dark, 0.70)
    # Very light speckle
    if lum > avg_lum * 1.35:
        light = quantile_color(palette, 0.96)
        return mix(base, light, 0.70)
    return base


def feature_granite_speckle(
    base: tuple[int, int, int],
    x: int,
    y: int,
    block: Image.Image,
    palette: list[tuple[int, int, int]],
    rx: float,
    ry: float,
) -> tuple[int, int, int]:
    """
    Granite has pinkish mineral spots. Detect them via R-channel dominance.
    """
    bw, bh = block.size
    bx = int(rx * (bw - 1))
    by = int(ry * (bh - 1))
    r, g, b, _ = block.getpixel((bx, by))
    lum = luminance(r, g, b)
    if r > lum * 1.15 and r > 120:
        # Pink/salmon speckle – preserve it
        pink = (min(255, r + 12), g, b)
        return mix(base, pink, 0.55)
    return base


def feature_basalt_stripes(
    base: tuple[int, int, int],
    x: int,
    y: int,
    block: Image.Image,
    palette: list[tuple[int, int, int]],
    rx: float,
    ry: float,
) -> tuple[int, int, int]:
    """
    Basalt side texture has vertical dark stripes. Map them to the worn UV
    via the horizontal relative position.
    """
    # Basalt stripes appear roughly every 3-4 pixels in the 16px texture.
    bw, _ = block.size
    bx = int(rx * (bw - 1))
    # Sample a column of the block to detect stripe vs non-stripe
    col_lums = [luminance(*block.getpixel((bx, py))[:3]) for py in range(block.size[1])]
    col_avg = statistics.mean(col_lums)
    global_avg = luminance(*quantile_color(palette, 0.50))
    if col_avg < global_avg * 0.80:
        dark = quantile_color(palette, 0.05)
        return mix(base, dark, 0.40)
    return base


def feature_redstone_circuit(
    base: tuple[int, int, int],
    x: int,
    y: int,
    block: Image.Image,
    palette: list[tuple[int, int, int]],
    rx: float,
    ry: float,
) -> tuple[int, int, int]:
    """
    Redstone block has a strong dark-red background with bright-red circuit
    lines. Amplify contrast to make it legible on armour scale.
    """
    bw, bh = block.size
    bx = int(rx * (bw - 1))
    by = int(ry * (bh - 1))
    r, g, b, _ = block.getpixel((bx, by))
    lum = luminance(r, g, b)
    global_avg = luminance(*quantile_color(palette, 0.50))
    if lum > global_avg * 1.20:
        # Bright circuit line – push toward saturated red
        return mix(base, (220, 18, 8), 0.35)
    elif lum < global_avg * 0.65:
        # Dark background – push toward deep maroon
        return mix(base, (72, 5, 0), 0.50)
    return base


def feature_netherrack_pits(
    base: tuple[int, int, int],
    x: int,
    y: int,
    block: Image.Image,
    palette: list[tuple[int, int, int]],
    rx: float,
    ry: float,
) -> tuple[int, int, int]:
    """
    Netherrack has small dark pores/pits. Identify them via local contrast.
    """
    bw, bh = block.size
    bx = int(rx * (bw - 1))
    by = int(ry * (bh - 1))
    r, g, b, _ = block.getpixel((bx, by))
    lum = luminance(r, g, b)
    avg_lum = luminance(*quantile_color(palette, 0.50))
    if lum < avg_lum * 0.60:
        dark = quantile_color(palette, 0.02)
        return mix(base, dark, 0.65)
    return base


def feature_lapis_gold_highlight(
    base: tuple[int, int, int],
    x: int,
    y: int,
    block: Image.Image,
    palette: list[tuple[int, int, int]],
    rx: float,
    ry: float,
) -> tuple[int, int, int]:
    """
    Lapis lazuli block has distinctive gold/bright specks.
    Detect very bright pixels in the block and tint them gold.
    """
    bw, bh = block.size
    bx = int(rx * (bw - 1))
    by = int(ry * (bh - 1))
    r, g, b, _ = block.getpixel((bx, by))
    lum = luminance(r, g, b)
    avg_lum = luminance(*quantile_color(palette, 0.50))
    if lum > avg_lum * 1.55 and lum > 80:
        # Gold/bright speck
        return mix(base, (180, 148, 30), 0.55)
    return base


FEATURE_HANDLERS = {
    "cobble_seams":       feature_cobble_seams,
    "blackstone_veins":   feature_blackstone_veins,
    "diorite_speckle":    feature_diorite_speckle,
    "granite_speckle":    feature_granite_speckle,
    "basalt_stripes":     feature_basalt_stripes,
    "redstone_circuit":   feature_redstone_circuit,
    "netherrack_pits":    feature_netherrack_pits,
    "lapis_gold_highlight": feature_lapis_gold_highlight,
}

# ---------------------------------------------------------------------------
# Core regeneration
# ---------------------------------------------------------------------------

def regenerate_layer(
    path: Path,
    block: Image.Image,
    palette: list[tuple[int, int, int]],
    cfg: dict[str, Any],
    layer_dir: str,
) -> None:
    mask = Image.open(path).convert("RGBA")
    w, h = mask.size
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    dr, dg, db = cfg.get("correction", (0, 0, 0))
    edge_q = cfg.get("edge_q", 0.05)
    dark_q = cfg.get("dark_q", 0.10)
    light_q = cfg.get("light_q", 0.90)
    feature_name = cfg.get("feature")

    edge_colour = quantile_color(palette, edge_q)
    dark_colour  = quantile_color(palette, dark_q)
    light_colour = quantile_color(palette, light_q)

    # Collect opaque pixel positions to derive UV context
    opaque_ys: list[int] = sorted({y for y in range(h)
                                    for x in range(w)
                                    if mask.getpixel((x, y))[3] > 0})
    y_mid = (min(opaque_ys) + max(opaque_ys)) / 2.0 if opaque_ys else h / 2.0

    block_w, block_h = block.size

    for y in range(h):
        for x in range(w):
            _, _, _, a = mask.getpixel((x, y))
            if a == 0:
                continue

            # 1. Map to block texture coordinate
            bx, by = block_uv_for_pixel(x, y, block_w, block_h, layer_dir)
            sampled = block.getpixel((bx, by))[:3]

            # 2. Apply colour correction
            corrected = (
                clamp(sampled[0] + dr),
                clamp(sampled[1] + dg),
                clamp(sampled[2] + db),
            )

            # 3. Relative position for shading
            rx, ry = bx / max(1, block_w - 1), by / max(1, block_h - 1)

            # 4. Feature handler (texture character)
            if feature_name and feature_name in FEATURE_HANDLERS:
                corrected = FEATURE_HANDLERS[feature_name](
                    corrected, x, y, block, palette, rx, ry
                )

            # 5. Shading: edge → darkest; upper pixels slightly lighter
            if is_edge(mask, x, y):
                final = mix(corrected, edge_colour, 0.52)
            else:
                # Simple top-of-region lightening, bottom darkening
                rel_y = (y - min(opaque_ys)) / max(1, max(opaque_ys) - min(opaque_ys))
                if rel_y < 0.25:
                    final = mix(corrected, light_colour, 0.18)
                elif rel_y > 0.75:
                    final = mix(corrected, dark_colour, 0.18)
                else:
                    final = corrected

            out.putpixel((x, y), (*final, a))

    out.save(path)


# ---------------------------------------------------------------------------
# Check mode helpers
# ---------------------------------------------------------------------------

def would_differ(path: Path, block: Image.Image,
                 palette: list[tuple[int, int, int]],
                 cfg: dict[str, Any], layer_dir: str) -> bool:
    """Return True if regenerating would change the file."""
    if not path.exists():
        return True
    import tempfile, shutil
    tmp = Path(tempfile.mktemp(suffix=".png"))
    shutil.copy(path, tmp)
    regenerate_layer(tmp, block, palette, cfg, layer_dir)
    orig = path.read_bytes()
    new  = tmp.read_bytes()
    tmp.unlink(missing_ok=True)
    return orig != new


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true",
                    help="Write regenerated textures; without this flag runs in check mode.")
    args = ap.parse_args()

    if not MC_CLIENT_JAR.exists():
        raise SystemExit(f"Minecraft client jar not found: {MC_CLIENT_JAR}")

    written = 0
    diffs: list[str] = []

    for family, cfg in FAMILY_CONFIG.items():
        block = load_block_texture(cfg["block_texture"])
        palette = build_palette(block)

        for layer_dir in LAYER_DIRS:
            if layer_dir == "humanoid_baby":
                filename = f"{family}.png"
            elif layer_dir == "humanoid_leggings":
                filename = f"{family}_leggings.png"
            else:
                filename = f"{family}.png"

            path = RES / f"assets/{MOD}/textures/entity/equipment/{layer_dir}/{filename}"
            if not path.exists():
                # humanoid_baby uses same filename as humanoid; skip if missing
                continue

            if args.write:
                regenerate_layer(path, block, palette, cfg, layer_dir)
                written += 1
            else:
                if would_differ(path, block, palette, cfg, layer_dir):
                    diffs.append(str(path.relative_to(ROOT)))

    if args.write:
        print(f"rock worn textures regenerated — files={written}")
    elif diffs:
        print(f"rock worn textures out of date — {len(diffs)} file(s):")
        for d in diffs[:30]:
            print(f"  {d}")
        if len(diffs) > 30:
            print(f"  ... and {len(diffs) - 30} more")
        raise SystemExit(1)
    else:
        print(f"rock worn textures in sync — families={len(FAMILY_CONFIG)}")


if __name__ == "__main__":
    main()
