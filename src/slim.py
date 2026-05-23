"""Convert the full Toronto address GeoJSON into a slim newline-delimited GeoJSON.

The source file is a single ~590 MB GeoJSON FeatureCollection, so it is parsed
as a stream with ijson -- it is never loaded into memory at once. The slim
output (one compact Feature per line) is the shared input to both tile builders.
"""

import json
import os

import ijson

from src import config

# Sanity bounds for the slimmed feature count (the city has ~525k addresses).
MIN_EXPECTED = 400_000
MAX_EXPECTED = 800_000


def slim(src_path):
    """Stream the big GeoJSON into data/address-points-slim.geojsonl.

    Keeps only the MVT_PROPERTIES, converts MultiPoint -> Point. Returns the
    slim file path. Raises if the feature count is implausible.
    """
    print(f"Slimming {src_path} ...")
    os.makedirs(config.DATA_DIR, exist_ok=True)

    count = 0
    skipped = 0
    with open(src_path, "rb") as src, \
            open(config.SLIM_PATH, "w", encoding="utf-8") as out:
        for feature in ijson.items(src, "features.item"):
            point = _first_point(feature.get("geometry") or {})
            if point is None:
                skipped += 1
                continue
            props_in = feature.get("properties") or {}
            props_out = {}
            for src_key, out_key in config.MVT_PROPERTIES.items():
                val = props_in.get(src_key)
                if val is None or val == "":
                    continue
                text = str(val).strip()
                if text and text != "None":
                    props_out[out_key] = text
            # iD's Custom Map Data draws labels from a feature's `name`
            # property -- mirror the housenumber there so dots get a visible
            # number in the editor, matching the raster layer.
            if "housenumber" in props_out:
                props_out["name"] = props_out["housenumber"]
            out.write(json.dumps({
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": list(point)},
                "properties": props_out,
            }) + "\n")
            count += 1
            if count % 100_000 == 0:
                print(f"  {count:,} features ...")

    with open(config.COUNT_PATH, "w", encoding="utf-8") as f:
        f.write(str(count))

    print(f"Done: {config.SLIM_PATH} ({count:,} features, {skipped:,} skipped)")
    if not MIN_EXPECTED <= count <= MAX_EXPECTED:
        raise RuntimeError(
            f"Slim feature count {count:,} is outside the expected range "
            f"{MIN_EXPECTED:,}-{MAX_EXPECTED:,} -- aborting."
        )
    return config.SLIM_PATH


def _first_point(geom):
    """Extract a single (lon, lat) tuple from a Point or MultiPoint geometry."""
    coords = geom.get("coordinates")
    if not coords:
        return None
    gtype = geom.get("type")
    if gtype == "Point":
        pt = coords
    elif gtype == "MultiPoint":
        pt = coords[0]
    else:
        return None
    try:
        lon, lat = float(pt[0]), float(pt[1])
    except (TypeError, ValueError, IndexError):
        return None
    if not (-180.0 <= lon <= 180.0 and -90.0 <= lat <= 90.0):
        return None
    return lon, lat
