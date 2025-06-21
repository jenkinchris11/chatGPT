"""Photo Editor - a minimal photo editing library.

This package provides a skeleton implementation for managing image catalogs,
applying basic edits, storing presets and interacting with simple AI helpers.
"""

# Re-export frequently used classes at the package level for convenience
from .catalog import Catalog, MultiCatalog
from . import gui

# Export commonly used classes and modules at the package level
__all__ = [
    "Catalog",
    "MultiCatalog",
    "catalog",
    "editor",
    "presets",
    "ai",
    "gui",
]
