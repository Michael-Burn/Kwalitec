#!/usr/bin/env python3
"""BI-000 — Official Kwalitec Brand Pack builder.

Rebuilds the approved logo as clean geometric SVG paths (no bitmap tracing).
Generates SVG masters, PNG exports, icons, social, and print assets.
"""

from __future__ import annotations

import math
import os
import struct
import subprocess
import zlib
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path("/Users/kwalitec/Desktop/kwalitec")
OUT = ROOT / "app/static/assets/branding"
BUILD = ROOT / "instance/brand_build"
SRC = Path("/Users/kwalitec/Downloads/Approved Kwalitec Logo.png")

# ---------------------------------------------------------------------------
# Colour system (permanent brand tokens)
# ---------------------------------------------------------------------------
COLORS = {
    "primary_blue": "#3B4FB8",
    "primary_dark": "#0D1B2A",
    "deep_navy": "#0A1628",
    "midnight": "#020D24",
    "gold": "#E8B02B",
    "gold_hover": "#F0C040",
    "white": "#FFFFFF",
    "text_secondary": "#8B93A7",
    "divider": "#1E2A3D",
}

# Soft CMYK approximations for print docs (device-independent guidance)
CMYK = {
    "primary_blue": (67, 57, 0, 28),
    "primary_dark": (69, 36, 0, 84),
    "deep_navy": (75, 45, 0, 84),
    "midnight": (95, 65, 0, 86),
    "gold": (0, 24, 81, 9),
    "gold_hover": (0, 20, 73, 6),
    "white": (0, 0, 0, 0),
    "text_secondary": (17, 12, 0, 35),
    "divider": (53, 34, 0, 76),
}


def hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def hex_to_hsl(h: str) -> tuple[int, int, int]:
    r, g, b = [c / 255 for c in hex_to_rgb(h)]
    mx, mn = max(r, g, b), min(r, g, b)
    l = (mx + mn) / 2
    if mx == mn:
        return 0, 0, round(l * 100)
    d = mx - mn
    s = d / (2 - mx - mn) if l > 0.5 else d / (mx + mn)
    if mx == r:
        hue = (g - b) / d + (6 if g < b else 0)
    elif mx == g:
        hue = (b - r) / d + 2
    else:
        hue = (r - g) / d + 4
    return round(hue * 60), round(s * 100), round(l * 100)


# ---------------------------------------------------------------------------
# Master symbol geometry (hand-built, normalised 0–100 space)
# viewBox covers ascending gold tip that extends slightly past x=100.
# ---------------------------------------------------------------------------
# Gold dot unit (1U) — diameter ≈ 14.3 → use 14 as brand spacing unit in this space
GOLD_DOT_CX, GOLD_DOT_CY, GOLD_DOT_R = 46.4, 22.4, 7.15

# White book page (left cover / L-foot)
PATH_WHITE = (
    "M 0.8 38.5 "
    "C 0.8 36.2 2.4 34.6 4.6 34.6 "
    "L 8.2 34.6 "
    "C 9.0 34.6 9.6 35.3 9.6 36.2 "
    "L 9.6 81.5 "
    "C 9.6 82.2 9.9 83.0 10.6 83.6 "
    "C 18.5 90.0 28.5 95.5 38.5 99.0 "
    "C 39.6 99.4 40.2 98.4 39.4 97.5 "
    "C 32.0 89.5 22.5 84.0 12.5 81.8 "
    "L 9.6 81.2 "
    "L 0.8 81.2 "
    "C 0.3 81.2 0.0 80.7 0.0 80.1 "
    "L 0.0 39.3 "
    "C 0.0 38.8 0.3 38.5 0.8 38.5 Z"
)

# Blue left page / upper lobe (completes open-book top-left)
PATH_BLUE_LEFT = (
    "M 10.5 25.5 "
    "C 9.2 25.5 8.5 26.8 9.0 28.0 "
    "C 11.5 34.0 20.0 38.5 29.5 41.5 "
    "C 34.5 43.2 38.5 43.8 40.5 43.5 "
    "C 41.5 43.3 41.8 42.0 41.0 41.2 "
    "C 35.0 35.5 26.5 30.5 18.5 27.5 "
    "C 15.5 26.4 12.5 25.5 10.5 25.5 Z"
)

# Blue K stem (vertical bar at spine)
PATH_BLUE_STEM = (
    "M40.0 37.0 "
    "C40.0 35.8 40.9 35.0 42.0 35.0 "
    "H43.5 "
    "C44.6 35.0 45.5 35.8 45.5 37.0 "
    "V97.2 "
    "C45.5 98.4 44.6 99.2 43.5 99.2 "
    "H42.0 "
    "C40.9 99.2 40.0 98.4 40.0 97.2 Z"
)

# Blue K upper arm
PATH_BLUE_UPPER = (
    "M44.5 37.5 "
    "C54.0 35.0 68.0 31.5 80.0 31.8 "
    "C84.5 32.0 88.5 33.2 88.8 35.5 "
    "C89.0 37.2 87.0 38.5 85.0 39.2 "
    "C72.0 44.0 60.0 52.0 51.5 60.5 "
    "C50.0 62.0 47.5 61.5 46.5 59.5 "
    "C45.0 56.0 44.5 50.0 44.5 44.0 "
    "C44.5 41.5 44.5 39.0 44.5 37.5 Z"
)

# Blue K lower arm
PATH_BLUE_LOWER = (
    "M46.0 64.0 "
    "C50.0 64.0 54.0 67.5 58.5 73.0 "
    "C66.0 82.0 75.0 91.5 83.5 98.0 "
    "C84.8 99.0 84.2 100.5 82.6 100.2 "
    "C74.0 98.5 66.5 91.5 59.5 83.5 "
    "C53.5 76.5 48.5 70.5 45.5 68.0 "
    "C44.0 66.8 44.5 64.0 46.0 64.0 Z"
)

# Gold ascending stroke — tapered ribbon (smooth cubic construction)
PATH_GOLD_STROKE = (
    "M43.2 53.8 "
    "C47.0 46.5 52.5 37.5 59.0 29.5 "
    "C66.5 20.5 76.0 11.5 87.5 5.0 "
    "C94.5 1.2 100.5 -0.2 103.8 0.6 "
    "C105.0 0.9 105.2 2.5 104.2 3.2 "
    "C98.5 7.2 93.0 12.5 88.0 18.5 "
    "C80.5 27.5 74.0 37.0 69.0 45.5 "
    "C65.0 52.0 61.5 57.5 58.5 61.5 "
    "C57.5 62.8 55.8 62.5 55.2 61.0 "
    "C52.0 55.5 48.0 54.5 43.2 53.8 Z"
)


def symbol_group(
    *,
    white: str,
    blue: str,
    gold: str,
    include_white: bool = True,
) -> str:
    """Return SVG group for the symbol in 0–105 normalised space."""
    parts = ['<g id="symbol">']
    if include_white:
        parts.append(f'  <path id="book" fill="{white}" d="{PATH_WHITE}"/>')
    parts.append(f'  <path id="book-left" fill="{blue}" d="{PATH_BLUE_LEFT}"/>')
    parts.append(f'  <path id="k-stem" fill="{blue}" d="{PATH_BLUE_STEM}"/>')
    parts.append(f'  <path id="k-upper" fill="{blue}" d="{PATH_BLUE_UPPER}"/>')
    parts.append(f'  <path id="k-lower" fill="{blue}" d="{PATH_BLUE_LOWER}"/>')
    parts.append(f'  <path id="ascent" fill="{gold}" d="{PATH_GOLD_STROKE}"/>')
    parts.append(
        f'  <circle id="gold-dot" cx="{GOLD_DOT_CX}" cy="{GOLD_DOT_CY}" '
        f'r="{GOLD_DOT_R}" fill="{gold}"/>'
    )
    parts.append("</g>")
    return "\n".join(parts)


def svg_wrap(content: str, view_box: str, width: str | None = None, height: str | None = None, label: str = "Kwalitec") -> str:
    w = f' width="{width}"' if width else ""
    h = f' height="{height}"' if height else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view_box}"{w}{h} '
        f'role="img" aria-label="{label}" fill="none">\n'
        f"  <!-- Kwalitec official brand mark — BI-000 hand-built vector (no raster) -->\n"
        f"{content}\n"
        f"</svg>\n"
    )


def build_icon_svg(white: str, blue: str, gold: str, include_white: bool = True) -> str:
    # Padding around symbol for optical balance / safe rendering at 16px
    body = symbol_group(white=white, blue=blue, gold=gold, include_white=include_white)
    # Shift slightly for optical centering within square
    content = f'  <g transform="translate(4, 4) scale(1.12)">{body}\n  </g>'
    return svg_wrap(content, "0 0 128 128")


def build_wordmark_svg(text_fill: str, gold: str) -> str:
    """Wordmark uses live text (Inter) + gold i-dot overlay — not outlined."""
    # Layout: viewBox sized for "Kwalitec" at font-size 48, weight 600
    # Gold i-dot positioned over the i tittle area
    content = f"""  <text
    id="wordmark"
    x="0" y="52"
    fill="{text_fill}"
    font-family="Inter, Manrope, Sora, system-ui, sans-serif"
    font-size="48"
    font-weight="600"
    letter-spacing="-0.02em"
  >Kwalitec</text>
  <!-- Gold tittle replaces default i-dot (hide via covering) -->
  <rect x="149" y="12" width="14" height="14" fill="{text_fill if text_fill != COLORS['gold'] else COLORS['midnight']}" opacity="0"/>
  <circle id="i-dot" cx="156.5" cy="18" r="5.2" fill="{gold}"/>"""
    # Note: browser text metrics vary; for master lockups we position the i-dot
    # using a measured Inter SemiBold layout. The rect is a no-op placeholder.
    return svg_wrap(content, "0 0 250 64", label="Kwalitec")


def build_primary_svg(
    *,
    white: str,
    blue: str,
    gold: str,
    text_fill: str,
    include_white_book: bool = True,
) -> str:
    """Full lockup: symbol + wordmark."""
    symbol = symbol_group(white=white, blue=blue, gold=gold, include_white=include_white_book)
    # Symbol ~108 wide in norm space; scale to sit beside wordmark
    # Wordmark baseline aligns with symbol bottom; x-height ~ half symbol
    content = f"""  <g id="lockup">
    <g transform="translate(0, 8) scale(1.05)">
{symbol}
    </g>
    <g transform="translate(128, 0)">
      <text
        x="0" y="78"
        fill="{text_fill}"
        font-family="Inter, Manrope, Sora, system-ui, sans-serif"
        font-size="42"
        font-weight="600"
        letter-spacing="-0.015em"
      >Kwalitec</text>
      <circle cx="137.2" cy="48.5" r="4.6" fill="{gold}"/>
    </g>
  </g>"""
    return svg_wrap(content, "0 0 360 128", label="Kwalitec")


def build_monochrome_icon(fill: str) -> str:
    body = symbol_group(white=fill, blue=fill, gold=fill, include_white=True)
    content = f'  <g transform="translate(4, 4) scale(1.12)">{body}\n  </g>'
    return svg_wrap(content, "0 0 128 128")


def build_monochrome_lockup(fill: str) -> str:
    symbol = symbol_group(white=fill, blue=fill, gold=fill)
    content = f"""  <g id="lockup">
    <g transform="translate(0, 8) scale(1.05)">
{symbol}
    </g>
    <g transform="translate(128, 0)">
      <text
        x="0" y="78"
        fill="{fill}"
        font-family="Inter, Manrope, Sora, system-ui, sans-serif"
        font-size="42"
        font-weight="600"
        letter-spacing="-0.015em"
      >Kwalitec</text>
      <circle cx="137.2" cy="48.5" r="4.6" fill="{fill}"/>
    </g>
  </g>"""
    return svg_wrap(content, "0 0 360 128")


# ---------------------------------------------------------------------------
# Refine blue K path — rebuild from geometric primitives for cleaner anchors
# ---------------------------------------------------------------------------
def rebuild_clean_paths() -> None:
    """Replace draft paths with tighter geometric constructions."""
    global PATH_WHITE, PATH_BLUE_LEFT, PATH_BLUE_STEM, PATH_BLUE_UPPER
    global PATH_BLUE_LOWER, PATH_GOLD_STROKE

    PATH_WHITE = (
        "M1.2 37.8 "
        "C1.2 35.8 2.8 34.4 4.8 34.4 "
        "H8.5 "
        "C9.4 34.4 10.0 35.1 10.0 36.0 "
        "V80.8 "
        "C10.0 81.6 10.4 82.4 11.2 83.0 "
        "C20.5 90.2 30.2 95.8 38.8 99.0 "
        "C39.8 99.4 40.4 98.5 39.6 97.6 "
        "C31.5 89.8 21.2 84.2 11.8 81.6 "
        "H1.2 "
        "C0.5 81.6 0.0 81.1 0.0 80.4 "
        "V39.0 "
        "C0.0 38.3 0.5 37.8 1.2 37.8 Z"
    )
    PATH_BLUE_LEFT = (
        "M11.0 25.2 "
        "C9.5 25.2 8.6 26.8 9.2 28.2 "
        "C12.5 35.0 22.0 40.0 32.5 42.8 "
        "C36.5 44.0 39.8 44.2 41.0 43.6 "
        "C42.0 43.1 42.0 41.8 41.0 41.0 "
        "C34.5 35.8 25.5 30.8 17.5 27.6 "
        "C15.0 26.6 13.0 25.2 11.0 25.2 Z"
    )
    PATH_BLUE_STEM = (
        "M40.0 37.0 "
        "C40.0 35.8 40.9 35.0 42.0 35.0 "
        "H43.5 "
        "C44.6 35.0 45.5 35.8 45.5 37.0 "
        "V97.2 "
        "C45.5 98.4 44.6 99.2 43.5 99.2 "
        "H42.0 "
        "C40.9 99.2 40.0 98.4 40.0 97.2 Z"
    )
    PATH_BLUE_UPPER = (
        "M44.5 37.5 "
        "C54.0 35.0 68.0 31.5 80.0 31.8 "
        "C84.5 32.0 88.5 33.2 88.8 35.5 "
        "C89.0 37.2 87.0 38.5 85.0 39.2 "
        "C72.0 44.0 60.0 52.0 51.5 60.5 "
        "C50.0 62.0 47.5 61.5 46.5 59.5 "
        "C45.0 56.0 44.5 50.0 44.5 44.0 "
        "C44.5 41.5 44.5 39.0 44.5 37.5 Z"
    )
    PATH_BLUE_LOWER = (
        "M46.0 64.0 "
        "C50.0 64.0 54.0 67.5 58.5 73.0 "
        "C66.0 82.0 75.0 91.5 83.5 98.0 "
        "C84.8 99.0 84.2 100.5 82.6 100.2 "
        "C74.0 98.5 66.5 91.5 59.5 83.5 "
        "C53.5 76.5 48.5 70.5 45.5 68.0 "
        "C44.0 66.8 44.5 64.0 46.0 64.0 Z"
    )
    PATH_GOLD_STROKE = (
        "M43.2 53.8 "
        "C47.0 46.5 52.5 37.5 59.0 29.5 "
        "C66.5 20.5 76.0 11.5 87.5 5.0 "
        "C94.5 1.2 100.5 -0.2 103.8 0.6 "
        "C105.0 0.9 105.2 2.5 104.2 3.2 "
        "C98.5 7.2 93.0 12.5 88.0 18.5 "
        "C80.5 27.5 74.0 37.0 69.0 45.5 "
        "C65.0 52.0 61.5 57.5 58.5 61.5 "
        "C57.5 62.8 55.8 62.5 55.2 61.0 "
        "C52.0 55.5 48.0 54.5 43.2 53.8 Z"
    )


rebuild_clean_paths()


# ---------------------------------------------------------------------------
# Write SVG masters
# ---------------------------------------------------------------------------
def write_svgs() -> dict[str, Path]:
    svg_dir = OUT / "svg"
    C = COLORS
    files = {
        "logo-primary.svg": build_primary_svg(
            white=C["white"], blue=C["primary_blue"], gold=C["gold"], text_fill=C["white"]
        ),
        "logo-primary-dark.svg": build_primary_svg(
            white=C["white"], blue=C["primary_blue"], gold=C["gold"], text_fill=C["white"]
        ),
        "logo-primary-light.svg": build_primary_svg(
            white=C["primary_dark"],
            blue=C["primary_blue"],
            gold=C["gold"],
            text_fill=C["primary_dark"],
        ),
        "logo-icon.svg": build_icon_svg(C["white"], C["primary_blue"], C["gold"]),
        "logo-icon-dark.svg": build_icon_svg(C["white"], C["primary_blue"], C["gold"]),
        "logo-icon-light.svg": build_icon_svg(
            C["primary_dark"], C["primary_blue"], C["gold"]
        ),
        "logo-monochrome-black.svg": build_monochrome_lockup(C["primary_dark"]),
        "logo-monochrome-white.svg": build_monochrome_lockup(C["white"]),
        "logo-wordmark.svg": build_wordmark_svg(C["primary_dark"], C["gold"]),
        # Icon-only monochrome helpers for print/embroidery
        "logo-icon-mono-black.svg": build_monochrome_icon(C["primary_dark"]),
        "logo-icon-mono-white.svg": build_monochrome_icon(C["white"]),
    }
    paths = {}
    for name, content in files.items():
        p = svg_dir / name
        p.write_text(content, encoding="utf-8")
        paths[name] = p
        print(f"  wrote {p.relative_to(ROOT)}")
    return paths


# ---------------------------------------------------------------------------
# Raster helpers (qlmanage + Pillow)
# ---------------------------------------------------------------------------
def rasterize_svg(svg_path: Path, size: int, dest: Path, background: tuple | None = None) -> None:
    """Render SVG via macOS Quick Look, then resize/crop to exact size."""
    tmp_dir = BUILD / "ql"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    # Render oversized for quality
    render_size = max(size * 2, 512)
    subprocess.run(
        ["qlmanage", "-t", "-s", str(render_size), "-o", str(tmp_dir), str(svg_path)],
        check=True,
        capture_output=True,
    )
    ql_out = tmp_dir / f"{svg_path.name}.png"
    if not ql_out.exists():
        raise FileNotFoundError(f"qlmanage failed for {svg_path}")
    im = Image.open(ql_out).convert("RGBA")
    # Trim transparent/near-empty margins then fit into size×size or width box
    bbox = im.getbbox()
    if bbox:
        im = im.crop(bbox)
    # Target canvas
    if dest.name.startswith("logo-primary") or "wordmark" in dest.name or "lockup" in dest.name:
        # Horizontal lockup — height = size, width proportional
        h = size
        w = max(1, round(im.width * h / im.height))
        im = im.resize((w, h), Image.Resampling.LANCZOS)
    else:
        # Square icon — fit inside size with padding
        canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        # leave ~6% padding
        pad = max(1, int(size * 0.06))
        fit = size - 2 * pad
        scale = min(fit / im.width, fit / im.height)
        nw, nh = max(1, round(im.width * scale)), max(1, round(im.height * scale))
        im = im.resize((nw, nh), Image.Resampling.LANCZOS)
        ox, oy = (size - nw) // 2, (size - nh) // 2
        canvas.paste(im, (ox, oy), im)
        im = canvas

    if background is not None:
        bg = Image.new("RGBA", im.size, background)
        bg.alpha_composite(im)
        im = bg

    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest, "PNG", optimize=True)
    ql_out.unlink(missing_ok=True)


def make_ico(png_sizes: dict[int, Path], dest: Path) -> None:
    """Build a multi-resolution favicon.ico from PNG frames."""
    images = []
    for s in sorted(png_sizes):
        images.append(Image.open(png_sizes[s]).convert("RGBA"))
    # Pillow ICO writer
    images[0].save(
        dest,
        format="ICO",
        sizes=[(im.width, im.height) for im in images],
        append_images=images[1:],
    )


def make_maskable(src: Path, dest: Path, size: int = 512) -> None:
    """Maskable icon with safe zone (~80% content)."""
    im = Image.open(src).convert("RGBA")
    canvas = Image.new("RGBA", (size, size), hex_to_rgb(COLORS["midnight"]) + (255,))
    safe = int(size * 0.8)
    scale = min(safe / im.width, safe / im.height)
    nw, nh = max(1, round(im.width * scale)), max(1, round(im.height * scale))
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas.paste(im, ((size - nw) // 2, (size - nh) // 2), im)
    canvas.save(dest, "PNG", optimize=True)


def make_social(icon_svg: Path, kind: str, dest: Path) -> None:
    """Social profile / OG images from master vector."""
    specs = {
        "og": (1200, 630, COLORS["midnight"]),
        "twitter": (1200, 600, COLORS["midnight"]),
        "linkedin": (400, 400, COLORS["midnight"]),
        "github": (500, 500, COLORS["midnight"]),
    }
    w, h, bg = specs[kind]
    # Rasterize icon large
    tmp = BUILD / f"social_{kind}_icon.png"
    rasterize_svg(icon_svg, 512, tmp)
    icon = Image.open(tmp).convert("RGBA")
    canvas = Image.new("RGBA", (w, h), hex_to_rgb(bg) + (255,))
    # Icon size relative to canvas
    target = int(min(w, h) * (0.42 if kind in ("og", "twitter") else 0.72))
    scale = target / max(icon.width, icon.height)
    nw, nh = max(1, round(icon.width * scale)), max(1, round(icon.height * scale))
    icon = icon.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas.paste(icon, ((w - nw) // 2, (h - nh) // 2), icon)
    canvas.convert("RGB").save(dest, "PNG", optimize=True)
    tmp.unlink(missing_ok=True)


def make_print_assets(svg_paths: dict[str, Path]) -> None:
    """Print-ready transparent PNGs + SVG copies with CMYK guidance comments."""
    print_dir = OUT / "print"
    # Large transparent masters
    for name, key in [
        ("logo-primary-print.png", "logo-primary-dark.svg"),
        ("logo-icon-print.png", "logo-icon-dark.svg"),
        ("logo-icon-mono-print.png", "logo-icon-mono-black.svg"),
        ("logo-wordmark-print.png", "logo-wordmark.svg"),
    ]:
        rasterize_svg(svg_paths[key], 2048, print_dir / name)

    # CMYK-annotated SVG companions (RGB fills retained for compatibility;
    # CMYK values documented for professional print conversion)
    cmyk_note = "\n".join(
        f"  - {k}: C={v[0]} M={v[1]} Y={v[2]} K={v[3]}" for k, v in CMYK.items()
    )
    for src_name in [
        "logo-primary-dark.svg",
        "logo-icon-dark.svg",
        "logo-icon-mono-black.svg",
        "logo-monochrome-black.svg",
        "logo-wordmark.svg",
    ]:
        src = svg_paths[src_name]
        text = src.read_text(encoding="utf-8")
        annotated = text.replace(
            "<!-- Kwalitec official brand mark — BI-000 hand-built vector (no raster) -->",
            "<!-- Kwalitec official brand mark — BI-000 hand-built vector (no raster) -->\n"
            "<!-- PRINT / CMYK conversion targets (approximate):\n"
            + cmyk_note
            + "\n     Convert to CMYK in a print RIP / Adobe / Affinity before plate output."
            " Transparent background. Suitable for cards, apparel, embroidery, banners. -->",
        )
        (print_dir / src_name.replace(".svg", "-print.svg")).write_text(
            annotated, encoding="utf-8"
        )


def validate_svgs(svg_dir: Path) -> list[str]:
    issues = []
    for p in sorted(svg_dir.glob("*.svg")):
        text = p.read_text(encoding="utf-8")
        if "<image" in text or "data:image" in text or "xlink:href" in text:
            issues.append(f"{p.name}: contains embedded raster")
        if "trace" in text.lower() and "hand-built" not in text:
            issues.append(f"{p.name}: suspicious trace comment")
        if not text.strip().startswith("<svg"):
            issues.append(f"{p.name}: does not start with <svg")
    return issues


def write_color_spec() -> Path:
    lines = [
        "# Kwalitec Colour Specification",
        "",
        "Permanent brand colour tokens (BI-000).",
        "",
        "| Token | HEX | RGB | HSL | CSS Variable | CMYK (approx) |",
        "|---|---|---|---|---|---|",
    ]
    css_names = {
        "primary_blue": "--brand-primary-blue",
        "primary_dark": "--brand-primary-dark",
        "deep_navy": "--brand-deep-navy",
        "midnight": "--brand-midnight",
        "gold": "--brand-gold",
        "gold_hover": "--brand-gold-hover",
        "white": "--brand-white",
        "text_secondary": "--brand-text-secondary",
        "divider": "--brand-divider",
    }
    for key, hexv in COLORS.items():
        r, g, b = hex_to_rgb(hexv)
        h, s, l = hex_to_hsl(hexv)
        c, m, y, k = CMYK[key]
        lines.append(
            f"| {key.replace('_', ' ').title()} | `{hexv}` | `{r}, {g}, {b}` | "
            f"`{h}°, {s}%, {l}%` | `{css_names[key]}` | `{c}/{m}/{y}/{k}` |"
        )
    lines.extend(
        [
            "",
            "## CSS custom properties",
            "",
            "```css",
            ":root {",
        ]
    )
    for key, hexv in COLORS.items():
        lines.append(f"  {css_names[key]}: {hexv};")
    lines.extend(["}", "```", ""])
    path = OUT / "COLOUR_SPECIFICATION.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def main() -> None:
    print("=== BI-000 Brand Pack Builder ===")
    OUT.mkdir(parents=True, exist_ok=True)
    for sub in ("svg", "png", "icons", "social", "print"):
        (OUT / sub).mkdir(parents=True, exist_ok=True)

    print("\n[1] Writing SVG masters…")
    svg_paths = write_svgs()

    print("\n[2] Validating SVGs…")
    issues = validate_svgs(OUT / "svg")
    if issues:
        print("VALIDATION ISSUES:")
        for i in issues:
            print(" ", i)
    else:
        print("  OK — no embedded rasters")

    print("\n[3] PNG exports…")
    png_dir = OUT / "png"
    sizes = [64, 128, 256, 512, 1024]
    # Primary lockup (dark variant renders white wordmark — export on transparent)
    for size in sizes:
        rasterize_svg(svg_paths["logo-primary-dark.svg"], size, png_dir / f"logo-primary-{size}.png")
        rasterize_svg(svg_paths["logo-icon-dark.svg"], size, png_dir / f"logo-icon-{size}.png")
        rasterize_svg(svg_paths["logo-wordmark.svg"], size, png_dir / f"logo-wordmark-{size}.png")
        print(f"  {size}px primary/icon/wordmark")

    # Canonical unsuffixed aliases at 512
    for alias, src in [
        ("logo-primary.png", "logo-primary-512.png"),
        ("logo-icon.png", "logo-icon-512.png"),
        ("logo-wordmark.png", "logo-wordmark-512.png"),
    ]:
        (png_dir / alias).write_bytes((png_dir / src).read_bytes())

    print("\n[4] Application icons…")
    icons = OUT / "icons"
    # Favicon SVG = icon dark (works on light chrome tabs with care; also provide light)
    favicon_svg = icons / "favicon.svg"
    favicon_svg.write_text(svg_paths["logo-icon-light.svg"].read_text(encoding="utf-8"), encoding="utf-8")

    fav_pngs = {}
    for s in (16, 32, 48):
        dest = icons / f"favicon-{s}.png"
        rasterize_svg(svg_paths["logo-icon-light.svg"], s, dest)
        fav_pngs[s] = dest
    make_ico(fav_pngs, icons / "favicon.ico")

    rasterize_svg(svg_paths["logo-icon-dark.svg"], 180, icons / "apple-touch-icon.png",
                  background=hex_to_rgb(COLORS["midnight"]) + (255,))
    # Re-export apple on midnight square properly
    tmp = BUILD / "apple_tmp.png"
    rasterize_svg(svg_paths["logo-icon-dark.svg"], 180, tmp)
    apple = Image.new("RGBA", (180, 180), hex_to_rgb(COLORS["midnight"]) + (255,))
    ic = Image.open(tmp).convert("RGBA")
    # fit with padding
    pad = 18
    fit = 180 - 2 * pad
    scale = min(fit / ic.width, fit / ic.height)
    nw, nh = max(1, round(ic.width * scale)), max(1, round(ic.height * scale))
    ic = ic.resize((nw, nh), Image.Resampling.LANCZOS)
    apple.paste(ic, ((180 - nw) // 2, (180 - nh) // 2), ic)
    apple.save(icons / "apple-touch-icon.png", "PNG", optimize=True)

    for s, name in [(192, "android-192.png"), (512, "android-512.png")]:
        canvas = Image.new("RGBA", (s, s), hex_to_rgb(COLORS["midnight"]) + (255,))
        tmp = BUILD / f"and_{s}.png"
        rasterize_svg(svg_paths["logo-icon-dark.svg"], s, tmp)
        ic = Image.open(tmp).convert("RGBA")
        pad = int(s * 0.12)
        fit = s - 2 * pad
        scale = min(fit / ic.width, fit / ic.height)
        nw, nh = max(1, round(ic.width * scale)), max(1, round(ic.height * scale))
        ic = ic.resize((nw, nh), Image.Resampling.LANCZOS)
        canvas.paste(ic, ((s - nw) // 2, (s - nh) // 2), ic)
        canvas.save(icons / name, "PNG", optimize=True)

    make_maskable(icons / "android-512.png", icons / "maskable-icon.png", 512)

    # mstile 150
    mstile = Image.new("RGBA", (150, 150), hex_to_rgb(COLORS["primary_dark"]) + (255,))
    tmp = BUILD / "mstile_tmp.png"
    rasterize_svg(svg_paths["logo-icon-dark.svg"], 150, tmp)
    ic = Image.open(tmp).convert("RGBA")
    pad = 18
    fit = 150 - 2 * pad
    scale = min(fit / ic.width, fit / ic.height)
    nw, nh = max(1, round(ic.width * scale)), max(1, round(ic.height * scale))
    ic = ic.resize((nw, nh), Image.Resampling.LANCZOS)
    mstile.paste(ic, ((150 - nw) // 2, (150 - nh) // 2), ic)
    mstile.save(icons / "mstile-150.png", "PNG", optimize=True)
    print("  favicons, apple, android, maskable, mstile")

    print("\n[5] Social assets…")
    social = OUT / "social"
    make_social(svg_paths["logo-icon-dark.svg"], "og", social / "og-logo.png")
    make_social(svg_paths["logo-icon-dark.svg"], "twitter", social / "twitter-x-logo.png")
    make_social(svg_paths["logo-icon-dark.svg"], "linkedin", social / "linkedin-square.png")
    make_social(svg_paths["logo-icon-dark.svg"], "github", social / "github-profile.png")
    print("  og, twitter, linkedin, github")

    print("\n[6] Print assets…")
    make_print_assets(svg_paths)
    print("  transparent PNG + CMYK-annotated SVG")

    print("\n[7] Colour specification…")
    write_color_spec()

    print("\nDone.")


if __name__ == "__main__":
    main()
