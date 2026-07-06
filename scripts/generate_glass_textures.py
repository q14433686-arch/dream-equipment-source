#!/usr/bin/env python3
"""Generate translucent glass equipment textures.

Two passes:
  1. Item textures (inventory / handheld) — PNG with real intermediate alpha,
     rendered via MC's item_translucent pipeline (no mixin required).
  2. Worn equipment layers (humanoid / humanoid_leggings / humanoid_baby) —
     CUTOUT-compatible hollowed-frame approach:
       • Outer border pixels → opaque glass frame colours (alpha 255)
       • Inner pixels        → fully transparent (alpha 0)
       • Sparse highlight dots preserved (alpha 255, bright colour)
     This matches vanilla block/glass visual language exactly.

Run:
    python3 scripts/generate_glass_textures.py            # check mode
    python3 scripts/generate_glass_textures.py --write    # write mode
"""
from __future__ import annotations

import argparse
import io
import zipfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
RES  = ROOT / "src/main/resources"
MOD  = "dream_equipment"
MC_CLIENT_JAR = Path.home() / ".gradle/caches/fabric-loom/26.1.2/minecraft-client.jar"

# ---------------------------------------------------------------------------
# Glass colour palette — derived from vanilla block/glass (RGBA 255)
# and adapted to match existing glass armour tone (#81afb7 family)
# ---------------------------------------------------------------------------

# Worn layer colours (all alpha=255, CUTOUT compatible)
WORN_EDGE_MAIN   = (123, 168, 183, 255)   # main border  — near #7ba8b7
WORN_EDGE_DARK   = (80,  150, 170, 255)   # shadow edge  — near #5096aa
WORN_EDGE_BRIGHT = (230, 255, 255, 255)   # highlight dot — near #e6ffff
WORN_TRANSPARENT = (0,   0,   0,   0)     # fully hollow interior

# Item texture colours (real alpha, rendered translucent by MC)
# Main body: #a8d4e8 with alpha 105  (matches stained-glass interior feel)
ITEM_FILL_ALPHA  = 105    # interior semi-transparent fill
ITEM_EDGE_ALPHA  = 255    # opaque border
ITEM_HL_ALPHA    = 200    # highlight line, slightly opaque

ITEM_FILL   = (168, 212, 232)   # #a8d4e8  — light glass blue
ITEM_EDGE   = (80,  148, 168)   # #5094a8  — deep glass teal (opaque border)
ITEM_HL     = (220, 245, 252)   # #dcf5fc  — bright highlight
ITEM_SHADOW = (55,  110, 130)   # #376e82  — dark shadow edge
ITEM_ACCENT = (100, 170, 190)   # #64aabe  — mid-tone

# ---------------------------------------------------------------------------
# Worn layer generation
# ---------------------------------------------------------------------------

def is_edge(arr, x: int, y: int) -> bool:
    """True if opaque pixel (x,y) has at least one transparent neighbour."""
    h, w = arr.shape[:2]
    if arr[y, x, 3] == 0:
        return False
    for nx, ny in ((x-1, y), (x+1, y), (x, y-1), (x, y+1)):
        if nx < 0 or ny < 0 or nx >= w or ny >= h or arr[ny, nx, 3] == 0:
            return True
    return False


def is_2nd_ring(arr, x: int, y: int) -> bool:
    """True if pixel is one step inside the outer border (for thin frame)."""
    h, w = arr.shape[:2]
    if arr[y, x, 3] == 0:
        return False
    for nx, ny in ((x-1, y), (x+1, y), (x, y-1), (x, y+1)):
        if 0 <= nx < w and 0 <= ny < h and arr[ny, nx, 3] > 0:
            if is_edge(arr, nx, ny):
                return True
    return False


def generate_worn_layer(src_path: Path, dst_path: Path) -> None:
    """
    Replace interior pixels with transparent, keep a 1–2 px glass border.
    Add sparse highlight dots at corners / panel centres.
    """
    src = Image.open(src_path).convert("RGBA")
    import numpy as np
    arr  = np.array(src)
    out  = Image.new("RGBA", src.size, (0, 0, 0, 0))
    w, h = src.size

    # Pre-compute opaque mask
    opaque = arr[:, :, 3] > 0

    # Identify highlight positions in original (bright pixels)
    orig_bright = set()
    for y in range(h):
        for x in range(w):
            if opaque[y, x]:
                r, g, b = arr[y, x, :3]
                # original highlight colour was #e6ffff → very bright cyan-white
                lum = 0.2126*r + 0.7152*g + 0.0722*b
                if lum > 200:
                    orig_bright.add((x, y))

    # Paint new layer
    for y in range(h):
        for x in range(w):
            if not opaque[y, x]:
                continue  # keep transparent

            edge = is_edge(arr, x, y)
            ring = is_2nd_ring(arr, x, y) if not edge else False

            if edge:
                # Outer 1-px border — use dark or main depending on original
                r0 = int(arr[y, x, 0])
                lum = 0.2126*r0 + 0.7152*int(arr[y, x, 1]) + 0.0722*int(arr[y, x, 2])
                if lum < 100:
                    colour = WORN_EDGE_DARK
                else:
                    colour = WORN_EDGE_MAIN
                out.putpixel((x, y), colour)

            elif (x, y) in orig_bright and ring:
                # Preserve high-value detail one pixel inside the border
                out.putpixel((x, y), WORN_EDGE_BRIGHT)

            elif ring:
                # 2nd ring: very faint continuation of frame, mostly transparent
                # but keep a subtle line on top/left faces (light direction)
                # We keep it transparent to maximise visibility of body beneath.
                out.putpixel((x, y), WORN_TRANSPARENT)

            else:
                # Interior — fully transparent (player body shows through)
                out.putpixel((x, y), WORN_TRANSPARENT)

    dst_path.parent.mkdir(parents=True, exist_ok=True)
    out.save(dst_path)


# ---------------------------------------------------------------------------
# Item texture generation
# ---------------------------------------------------------------------------

def luminance(r: int, g: int, b: int) -> float:
    return 0.2126*r + 0.7152*g + 0.0722*b


def generate_item_texture(src_path: Path, dst_path: Path) -> None:
    """
    Replace all opaque pixels with glass-translucent colours:
      - Border pixels (edge adjacent to transparent) → opaque glass border
      - Highlight pixels (originally very bright)    → bright, alpha=200
      - Dark outline pixels (originally near-black)  → deep shadow, alpha=255
      - Interior fill                                 → semi-transparent fill
    """
    src = Image.open(src_path).convert("RGBA")
    import numpy as np
    arr  = np.array(src)
    out  = Image.new("RGBA", src.size, (0, 0, 0, 0))
    w, h = src.size

    opaque = arr[:, :, 3] > 0

    for y in range(h):
        for x in range(w):
            if not opaque[y, x]:
                continue

            r0, g0, b0 = int(arr[y, x, 0]), int(arr[y, x, 1]), int(arr[y, x, 2])
            lum = luminance(r0, g0, b0)
            edge = is_edge(arr, x, y)

            if lum < 50:
                # Near-black outline pixel (original dark outline)
                out.putpixel((x, y), (*ITEM_EDGE, ITEM_EDGE_ALPHA))

            elif edge and lum < 140:
                # Dark border pixel — glass frame, opaque
                out.putpixel((x, y), (*ITEM_EDGE, ITEM_EDGE_ALPHA))

            elif edge and lum >= 140:
                # Bright border pixel — lighter glass edge
                out.putpixel((x, y), (*ITEM_HL, ITEM_HL_ALPHA))

            elif lum > 200:
                # Interior highlight / glint
                out.putpixel((x, y), (*ITEM_HL, ITEM_HL_ALPHA))

            elif lum < 80:
                # Interior shadow
                out.putpixel((x, y), (*ITEM_SHADOW, ITEM_EDGE_ALPHA))

            elif lum < 130:
                # Interior mid-dark
                out.putpixel((x, y), (*ITEM_ACCENT, ITEM_FILL_ALPHA))

            else:
                # Interior standard fill — semi-transparent
                out.putpixel((x, y), (*ITEM_FILL, ITEM_FILL_ALPHA))

    dst_path.parent.mkdir(parents=True, exist_ok=True)
    out.save(dst_path)


# ---------------------------------------------------------------------------
# File manifest
# ---------------------------------------------------------------------------

WORN_LAYERS = [
    # (src relative path, dst relative path)  — same file, in-place rewrite
    ("humanoid",          "glass.png",          "glass.png"),
    ("humanoid_leggings", "glass_leggings.png",  "glass_leggings.png"),
    ("humanoid_baby",     "glass.png",           "glass.png"),
]

ITEM_TEXTURES = [
    "glass_helmet",
    "glass_chestplate",
    "glass_leggings",
    "glass_boots",
    "glass_sword",
    "glass_axe",
    "glass_spear",
    "glass_spear_in_hand",
]


def collect_tasks() -> list[tuple[str, Path, Path]]:
    tasks = []

    # Worn layers
    for layer_dir, src_file, dst_file in WORN_LAYERS:
        base = RES / f"assets/{MOD}/textures/entity/equipment/{layer_dir}"
        src  = base / src_file
        dst  = base / dst_file   # same path — in-place
        if src.exists():
            tasks.append(("worn", src, dst))

    # Item textures
    for name in ITEM_TEXTURES:
        src = RES / f"assets/{MOD}/textures/item/{name}.png"
        if src.exists():
            tasks.append(("item", src, src))   # in-place

    return tasks


# ---------------------------------------------------------------------------
# Check mode helpers
# Generation is a destructive one-way transform, so check mode tests
# structural properties of the output rather than re-rendering from disk.
# ---------------------------------------------------------------------------

def _check_worn_ok(path: Path) -> bool:
    """Worn glass layer: no semi-transparent pixels (CUTOUT); interior hollowed."""
    import numpy as np
    from PIL import Image as _PILImage
    if not path.exists():
        return False
    arr = np.array(_PILImage.open(path).convert("RGBA"))
    semi   = int(((arr[:,:,3] > 0) & (arr[:,:,3] < 255)).sum())
    opaque = int((arr[:,:,3] == 255).sum())
    return semi == 0 and opaque < 500   # original worn was 632; after hollowing ~349


def _check_item_ok(path: Path) -> bool:
    """Item glass texture: must contain semi-transparent pixels."""
    import numpy as np
    from PIL import Image as _PILImage
    if not path.exists():
        return False
    arr = np.array(_PILImage.open(path).convert("RGBA"))
    semi = int(((arr[:,:,3] > 0) & (arr[:,:,3] < 255)).sum())
    return semi > 0


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    tasks  = collect_tasks()
    written = 0
    diffs:  list[str] = []

    for kind, src, dst in tasks:
        if args.write:
            if kind == "worn":
                generate_worn_layer(src, dst)
            else:
                generate_item_texture(src, dst)
            written += 1
        else:
            if kind == "worn":
                ok = _check_worn_ok(dst)
            else:
                ok = _check_item_ok(dst)
            if not ok:
                diffs.append(str(dst.relative_to(ROOT)))

    if args.write:
        print(f"glass textures regenerated — files={written}")
    elif diffs:
        print(f"glass textures out of date — {len(diffs)} file(s):")
        for d in diffs[:20]:
            print(f"  {d}")
        raise SystemExit(1)
    else:
        print(f"glass textures in sync — files={len(tasks)}")


if __name__ == "__main__":
    main()
