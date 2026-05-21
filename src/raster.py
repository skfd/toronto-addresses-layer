"""Render address points into labelled raster (PNG) map tiles using Pillow.

Pure Python -- no native dependencies, runs the same on Windows and Linux.
"""

import json
import os
from collections import defaultdict

from PIL import Image, ImageDraw, ImageFont

from src import config
from src.tilemath import TILE_SIZE, pixel_in_tile

DOT_COLOR = (224, 33, 138, 255)        # magenta -- visible over aerial imagery
DOT_RADIUS = 2
LABEL_COLOR = (0, 0, 0, 255)
HALO_COLOR = (255, 255, 255, 235)
FONT_PATH = os.path.join(config.ASSETS_DIR, "font", "DejaVuSans-Bold.ttf")
FONT_SIZE = 10


def build_raster(slim_path=None):
    """Render PNG tiles for every zoom in config.RASTER_ZOOMS.

    Returns a dict {zoom: tile_count}.
    """
    slim_path = slim_path or config.SLIM_PATH
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    return {z: _render_zoom(slim_path, z, font) for z in config.RASTER_ZOOMS}


def _render_zoom(slim_path, zoom, font):
    """Bucket every point into its tile for one zoom, then render each tile."""
    print(f"Raster z{zoom}: bucketing points ...")
    tiles = defaultdict(list)  # (tx, ty) -> [(ox, oy, housenumber), ...]
    with open(slim_path, encoding="utf-8") as f:
        for line in f:
            feat = json.loads(line)
            lon, lat = feat["geometry"]["coordinates"]
            tx, ty, ox, oy = pixel_in_tile(lon, lat, zoom)
            tiles[(tx, ty)].append(
                (ox, oy, feat["properties"].get("housenumber", ""))
            )

    label = zoom in config.RASTER_LABEL_ZOOMS
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
                _draw_label(draw, ox + DOT_RADIUS + 1, oy, housenumber, font)
    return img


def _draw_label(draw, x, y, text, font):
    """Draw text with a 1-px white halo, vertically centered on y."""
    y -= FONT_SIZE // 2
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx or dy:
                draw.text((x + dx, y + dy), text, font=font, fill=HALO_COLOR)
    draw.text((x, y), text, font=font, fill=LABEL_COLOR)
