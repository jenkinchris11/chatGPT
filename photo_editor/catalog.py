"""Catalog management."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Iterable, Sequence

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


@dataclass
class MultiCatalog:
    """Combine several catalogs into one."""

    paths: Sequence[Path]
    images: List[Image.Image] = field(default_factory=list)

    def load(self) -> None:
        self.images.clear()
        for path in self.paths:
            self.images.extend(utils.load_images_from_folder(path))

    def __iter__(self) -> Iterable[Image.Image]:
        yield from self.images

