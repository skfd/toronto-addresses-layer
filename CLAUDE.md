# CLAUDE.md (project)

Thin consumer of the **address-layerist** engine (`../address-layerist`). This
repo is config, not code.

- Build pipeline + all logic: `../address-layerist/addresslayerist/`. Don't add
  pipeline code here; fix or extend the engine instead.
- Data source / field map / site settings: [`layer.toml`](layer.toml).
- Onboarding a different city is a skill: `../address-layerist/skills/onboard-city/`.

Common commands (run from this repo root):

```
pip install -r requirements.txt   # installs the engine, pinned to a release tag
addressvault pull toronto         # acquire data (engine does not fetch)
python run.py build      # slim + vector + raster + site
python run.py update     # build + publish
```

For engine development, install editable against the sibling checkout instead:
`pip install -e ../address-layerist`.

`publish` force-pushes `build/site/` to an orphan `gh-pages` branch and needs a
git repo with an `origin` remote (do it only when asked).

Toronto is large (~525k addresses, ~590 MB source GeoJSON); a full build is
heavy on disk, CPU, and the WSL tippecanoe step.
