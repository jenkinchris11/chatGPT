"""Command line interface for the photo editor."""

import argparse
from pathlib import Path

from PIL import Image

from .catalog import Catalog
from .editor import Editor, brighten, denoise, apply_hsl
from .presets import Preset, PresetLibrary
from .ai import AIEngine


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Minimal Photo Editor")
    p.add_argument("catalog", type=Path, help="Path to image folder")
    p.add_argument("--output", type=Path, default=Path("output"), help="Output folder")
    p.add_argument("--preset", type=str, help="Apply preset by name")
    p.add_argument("--brightness", type=float, default=1.0, help="Brightness factor")
    p.add_argument("--denoise", action="store_true", help="Apply simple denoise")
    p.add_argument("--hsl", nargs=3, type=float, metavar=("H", "S", "L"), help="HSL adjustments")
    p.add_argument("--assistant", type=str, help="Use AI assistant by name")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    args.output.mkdir(exist_ok=True)

    catalog = Catalog(path=args.catalog)
    catalog.load()

    presets = PresetLibrary(folder=args.catalog / "presets")
    presets.load()

    engine = AIEngine()
    assistant = engine.get(args.assistant or "default")

    for idx, image in enumerate(catalog):
        editor = Editor(image=image)
        if args.preset and args.preset in presets.presets:
            preset = presets.presets[args.preset]
            if "brightness" in preset.settings:
                editor.apply(brighten, preset.settings["brightness"])
        if args.brightness != 1.0:
            editor.apply(brighten, args.brightness)
        if args.denoise:
            editor.apply(denoise)
        if args.hsl:
            h, s, l = args.hsl
            editor.apply(apply_hsl, h, s, l)
        out_path = args.output / f"image_{idx}.jpg"
        editor.save(out_path)
        tags = assistant.suggest_hashtags("sample photo")
        print(f"Saved {out_path} with hashtags: {' '.join(tags)}")


if __name__ == "__main__":
    main()
