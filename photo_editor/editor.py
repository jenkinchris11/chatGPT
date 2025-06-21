"""Basic editing operations."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from PIL import Image, ImageEnhance, ImageFilter, ImageDraw
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


def overlay_image(image: Image.Image, overlay: Image.Image, opacity: float = 0.5) -> Image.Image:
    """Overlay another image with given opacity."""
    base = image.convert("RGBA")
    over = overlay.resize(image.size).convert("RGBA")
    blended = Image.blend(base, over, opacity)
    return blended.convert(image.mode)


def mask_brighten(
    image: Image.Image, box: tuple[int, int, int, int], factor: float
) -> Image.Image:
    """Brighten a rectangular region."""
    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rectangle(box, fill=255)
    enhancer = ImageEnhance.Brightness(image)
    bright = enhancer.enhance(factor)
    return Image.composite(bright, image, mask)

def save(image: Image.Image, path: Path) -> None:
    image.save(path)


@dataclass
class History:
    edits: List[str] = field(default_factory=list)


@dataclass
class Editor:
    image: Image.Image
    history: History = field(default_factory=History)
    metadata: dict = field(default_factory=dict)
    edited: bool = False


    def apply(self, func, *args, **kwargs):
        self.image = func(self.image, *args, **kwargs)
        self.history.edits.append(func.__name__)
        self.edited = True

    def undo(self) -> None:
        if not self.history.edits:
            return
        # For simplicity reload original - real implementation would step back
        self.edited = False

    def add_metadata(self, key: str, value: str) -> None:
        self.metadata[key] = value


    def save(self, path: Path) -> None:
        save(self.image, path)

