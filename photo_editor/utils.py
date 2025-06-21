"""Utility functions for the photo editor."""

from pathlib import Path
from typing import Iterable

from PIL import Image

SUPPORTED_FORMATS = {"JPEG", "PNG", "TIFF", "BMP", "GIF", "DNG"}


def load_images_from_folder(folder: Path) -> Iterable[Image.Image]:
    """Yield images from a folder."""
    for ext in SUPPORTED_FORMATS:
        for path in folder.glob(f"*.{ext.lower()}"):
            try:
                yield Image.open(path)
            except Exception:
                continue
