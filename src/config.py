"""Configuration constants for the Toronto address tile layer build.

Single source of truth. No logic here.
"""

import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_DIR, "data")
BUILD_DIR = os.path.join(PROJECT_DIR, "build")
SITE_DIR = os.path.join(BUILD_DIR, "site")
ASSETS_DIR = os.path.join(PROJECT_DIR, "assets")
LOGS_DIR = os.path.join(PROJECT_DIR, "logs")

MBTILES_PATH = os.path.join(BUILD_DIR, "address-points.mbtiles")
SLIM_PATH = os.path.join(DATA_DIR, "address-points-slim.geojsonl")
COUNT_PATH = os.path.join(DATA_DIR, "address-points.count")
LAST_DOWNLOAD_PATH = os.path.join(DATA_DIR, ".last-download.json")

VECTOR_TILE_DIR = os.path.join(SITE_DIR, "tiles", "vector")
RASTER_TILE_DIR = os.path.join(SITE_DIR, "tiles", "raster")

# Data source: City of Toronto Address Points, published already in WGS84.
DATASET_URL = (
    "https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/"
    "abedd8bc-e3dd-4d45-8e69-79165a76e4fa/resource/"
    "b1c2ab72-dfe7-4b29-8550-6d1cfaa61733/download/address-points-4326.geojson"
)
DATASET_PAGE = (
    "https://open.toronto.ca/dataset/"
    "address-points-municipal-toronto-one-address-repository/"
)
LICENSE_URL = "https://open.toronto.ca/open-data-licence/"
# Plain-ASCII attribution embedded in tile metadata (safe through the WSL shell).
ATTRIBUTION = "(c) City of Toronto, Open Government Licence - Toronto"

# GitHub Pages target. Update both if the repo/account differs.
GITHUB_REPO = "skfd/toronto-addresses-layer"
PAGES_URL = "https://skfd.github.io/toronto-addresses-layer"

# WSL distro that has tippecanoe installed (see wsl-setup.md).
WSL_DISTRO = "Ubuntu"

# Vector tiles. Maxzoom 16 keeps the editor overzoom gap to 3 levels (z16 -> z19).
VECTOR_MINZOOM = 12
VECTOR_MAXZOOM = 16
VECTOR_LAYER_NAME = "addresses"

# Raster tiles. Editors overzoom z18 -> z19.
RASTER_ZOOMS = [16, 17, 18]
RASTER_LABEL_ZOOMS = {17, 18}

# Slim GeoJSON property map: source property key -> short output key.
MVT_PROPERTIES = {
    "ADDRESS_FULL": "addr",
    "ADDRESS_NUMBER": "housenumber",
    "LINEAR_NAME_FULL": "street",
    "LO_NUM_SUF": "suffix",
    "ADDRESS_CLASS": "class",
}
