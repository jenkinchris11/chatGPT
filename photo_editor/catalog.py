"""Catalog management."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Iterable

from PIL import Image

from . import utils


@dataclass
class Catalog:
    path: Path
    images: List[Image.Image] = field(default_factory=list)

    def load(self) -> None:
        """Load images from the catalog path."""
        self.images = list(utils.load_images_from_folder(self.path))

    def __iter__(self) -> Iterable[Image.Image]:
        yield from self.images

