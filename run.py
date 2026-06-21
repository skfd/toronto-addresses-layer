"""Thin entry point: the pipeline lives in the address-layerist engine.

    python run.py build     # fetch + slim + vector + raster + site
    python run.py update    # build + publish
See `python run.py --help` or `addresslayerist onboard` for more.
"""

from addresslayerist.cli import main

if __name__ == "__main__":
    main()
