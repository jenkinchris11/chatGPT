"""Sharing utilities for social media platforms."""

from pathlib import Path
from typing import Dict, Tuple, List

# Predefined platform sizes (width, height)
SOCIAL_PRESETS: Dict[str, Tuple[int, int]] = {
    "instagram": (1080, 1080),
    "twitter": (1200, 675),
    "facebook": (1200, 630),
}

CUSTOM_PRESETS: Dict[str, Tuple[int, int]] = {}


def add_platform(name: str, width: int, height: int) -> None:
    """Add a custom social media platform."""
    CUSTOM_PRESETS[name] = (width, height)


def share(path: Path, platforms: List[str]) -> None:
    """Pretend to share an image to the given platforms."""
    for platform in platforms:
        size = CUSTOM_PRESETS.get(platform) or SOCIAL_PRESETS.get(platform)
        if not size:
            print(f"Unknown platform {platform}")
            continue
        print(f"Shared {path} to {platform} with size {size[0]}x{size[1]}")
