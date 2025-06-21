"""Basic editing operations."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from PIL import Image, ImageEnhance, ImageFilter


def brighten(image: Image.Image, factor: float = 1.2) -> Image.Image:
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)


def apply_hsl(image: Image.Image, h: float = 0.0, s: float = 1.0, l: float = 1.0) -> Image.Image:
    """Apply simple HSL adjustment."""
    # Convert to HSL and adjust
    img = image.convert("RGB")
    r, g, b = img.split()
    # Placeholder: just adjust brightness for lightness
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(l)
    return img


def denoise(image: Image.Image) -> Image.Image:
    return image.filter(ImageFilter.MedianFilter(size=3))


def save(image: Image.Image, path: Path) -> None:
    image.save(path)


@dataclass
class History:
    edits: List[str] = field(default_factory=list)


@dataclass
class Editor:
    image: Image.Image
    history: History = field(default_factory=History)

    def apply(self, func, *args, **kwargs):
        self.image = func(self.image, *args, **kwargs)
        self.history.edits.append(func.__name__)

    def save(self, path: Path) -> None:
        save(self.image, path)

