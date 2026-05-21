"""Render the GitHub Pages landing page into the build output."""

import os
import shutil
from datetime import date

from src import config


def build_site():
    """Render index.html, copy index.css, write .nojekyll into build/site/."""
    os.makedirs(config.SITE_DIR, exist_ok=True)

    point_count = "525,000+"
    if os.path.isfile(config.COUNT_PATH):
        with open(config.COUNT_PATH, encoding="utf-8") as f:
            point_count = f"{int(f.read().strip()):,}"

    with open(os.path.join(config.ASSETS_DIR, "index.html.tmpl"),
              encoding="utf-8") as f:
        html = f.read()

    replacements = {
        "{{PAGES_URL}}": config.PAGES_URL,
        "{{VECTOR_URL}}": f"{config.PAGES_URL}/tiles/vector/{{z}}/{{x}}/{{y}}.pbf",
        "{{RASTER_URL}}": f"{config.PAGES_URL}/tiles/raster/{{z}}/{{x}}/{{y}}.png",
        "{{RASTER_URL_JOSM}}": (
            f"{config.PAGES_URL}/tiles/raster/{{zoom}}/{{x}}/{{y}}.png"
        ),
        "{{VECTOR_URL_JOSM}}": (
            f"{config.PAGES_URL}/tiles/vector/{{zoom}}/{{x}}/{{y}}.pbf"
        ),
        "{{BUILD_DATE}}": date.today().isoformat(),
        "{{POINT_COUNT}}": point_count,
        "{{GITHUB_REPO}}": config.GITHUB_REPO,
        "{{DATASET_PAGE}}": config.DATASET_PAGE,
        "{{LICENSE_URL}}": config.LICENSE_URL,
    }
    for key, value in replacements.items():
        html = html.replace(key, value)

    with open(os.path.join(config.SITE_DIR, "index.html"), "w",
              encoding="utf-8") as f:
        f.write(html)
    shutil.copy(
        os.path.join(config.ASSETS_DIR, "index.css"),
        os.path.join(config.SITE_DIR, "index.css"),
    )
    # .nojekyll stops GitHub Pages running Jekyll over the tile directories.
    open(os.path.join(config.SITE_DIR, ".nojekyll"), "w").close()
    print(f"Site rendered: {config.SITE_DIR}")
