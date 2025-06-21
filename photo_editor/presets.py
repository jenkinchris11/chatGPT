"""Preset management."""

from dataclasses import dataclass, field
from pathlib import Path
import json
from typing import Dict


@dataclass
class Preset:
    name: str
    settings: Dict[str, float]

    def save(self, path: Path) -> None:
        path.write_text(json.dumps(self.settings))

    @classmethod
    def load(cls, path: Path) -> "Preset":
        return cls(name=path.stem, settings=json.loads(path.read_text()))


@dataclass
class PresetLibrary:
    folder: Path
    presets: Dict[str, Preset] = field(default_factory=dict)

    def load(self) -> None:
        self.presets.clear()
        for preset_file in self.folder.glob("*.json"):
            preset = Preset.load(preset_file)
            self.presets[preset.name] = preset

    def add(self, preset: Preset) -> None:
        self.presets[preset.name] = preset
        preset.save(self.folder / f"{preset.name}.json")
