"""Render address points into labelled raster (PNG) map tiles using Pillow.

Pure Python -- no native dependencies, runs the same on Windows and Linux.
"""

import json
import os
from collections import defaultdict

from PIL import Image, ImageDraw, ImageFont

from src import config
from src.tilemath import TILE_SIZE, lonlat_to_pixel

DOT_COLOR = (224, 33, 138, 255)        # magenta -- visible over aerial imagery
DOT_RADIUS = 2
LABEL_COLOR = (0, 0, 0, 255)
HALO_COLOR = (255, 255, 255, 235)
FONT_PATH = os.path.join(config.ASSETS_DIR, "font", "DejaVuSans.ttf")
FONT_SIZE = 11
STROKE_WIDTH = 1                       # white halo width, in pixels
LABEL_GAP = 2                          # gap between the dot and the label


def build_raster(slim_path=None):
    """Render PNG tiles for every zoom in config.RASTER_ZOOMS.

    Returns a dict {zoom: tile_count}.
    """
    slim_path = slim_path or config.SLIM_PATH
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    return {z: _render_zoom(slim_path, z, font) for z in config.RASTER_ZOOMS}


def _render_zoom(slim_path, zoom, font):
    """Bucket every point into its tile for one zoom, then render each tile."""
    label = zoom in config.RASTER_LABEL_ZOOMS
    print(f"Raster z{zoom}: bucketing points ...")
    tiles = defaultdict(list)  # (tx, ty) -> [(ox, oy, housenumber), ...]
    with open(slim_path, encoding="utf-8") as f:
        for line in f:
            feat = json.loads(line)
            lon, lat = feat["geometry"]["coordinates"]
            housenumber = feat["properties"].get("housenumber", "")
            gx, gy = lonlat_to_pixel(lon, lat, zoom)
            _bucket_point(tiles, gx, gy, housenumber, font, label)

    out_dir = os.path.join(config.RASTER_TILE_DIR, str(zoom))
    print(f"Raster z{zoom}: rendering {len(tiles):,} tiles (labels={label}) ...")

    made_dirs = set()
    for (tx, ty), points in tiles.items():
        img = _render_tile(points, font, label)
        tdir = os.path.join(out_dir, str(tx))
        if tdir not in made_dirs:
            os.makedirs(tdir, exist_ok=True)
            made_dirs.add(tdir)
        img.save(os.path.join(tdir, f"{ty}.png"), optimize=True)
    return len(tiles)


def _bucket_point(tiles, gx, gy, housenumber, font, label):
    """Add a point to every tile its dot + label footprint overlaps.

    A point near a tile edge is added to the neighbouring tile too, with an
    out-of-range offset, so labels and dots straddling a seam render whole in
    both tiles instead of being clipped at the boundary.
    """
    half_h = max(DOT_RADIUS, FONT_SIZE / 2) + STROKE_WIDTH
    left = gx - DOT_RADIUS - STROKE_WIDTH
    right = gx + DOT_RADIUS + STROKE_WIDTH
    if label and housenumber:
        right = (gx + DOT_RADIUS + LABEL_GAP
                 + font.getlength(housenumber) + STROKE_WIDTH)

    tx0, tx1 = int(left // TILE_SIZE), int(right // TILE_SIZE)
    ty0, ty1 = int((gy - half_h) // TILE_SIZE), int((gy + half_h) // TILE_SIZE)
    for tx in range(tx0, tx1 + 1):
        for ty in range(ty0, ty1 + 1):
            tiles[(tx, ty)].append(
                (gx - tx * TILE_SIZE, gy - ty * TILE_SIZE, housenumber)
            )


def _render_tile(points, font, label):
    img = Image.new("RGBA", (TILE_SIZE, TILE_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    for ox, oy, _ in points:
        draw.ellipse(
            [ox - DOT_RADIUS, oy - DOT_RADIUS, ox + DOT_RADIUS, oy + DOT_RADIUS],
            fill=DOT_COLOR,
        )
    if label:
        for ox, oy, housenumber in points:
            if housenumber:
                _draw_label(draw, ox + DOT_RADIUS + LABEL_GAP, oy, housenumber,
                            font)
    return img


def _draw_label(draw, x, y, text, font):
    """Draw text vertically centred on y, with a clean white halo."""
    draw.text(
        (x, y), text, font=font, fill=LABEL_COLOR,
        stroke_width=STROKE_WIDTH, stroke_fill=HALO_COLOR, anchor="lm",
    )
