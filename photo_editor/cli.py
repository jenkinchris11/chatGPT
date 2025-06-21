"""Command line interface for the photo editor."""

import argparse
from pathlib import Path

from PIL import Image

from .catalog import Catalog, MultiCatalog
from .editor import (
    Editor,
    brighten,
    denoise,
    apply_hsl,
    overlay_image,
    mask_brighten,
)
from .presets import Preset, PresetLibrary
from .ai import AIEngine
from .social import share, add_platform
from .catalog import Catalog
from .editor import Editor, brighten, denoise, apply_hsl
from .presets import Preset, PresetLibrary
from .ai import AIEngine


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Minimal Photo Editor")
    p.add_argument("catalog", nargs="+", type=Path, help="Path(s) to image folder")
    p.add_argument("catalog", type=Path, help="Path to image folder")
    p.add_argument("--output", type=Path, default=Path("output"), help="Output folder")
    p.add_argument("--preset", type=str, help="Apply preset by name")
    p.add_argument("--brightness", type=float, default=1.0, help="Brightness factor")
    p.add_argument("--denoise", action="store_true", help="Apply simple denoise")
    p.add_argument("--hsl", nargs=3, type=float, metavar=("H", "S", "L"), help="HSL adjustments")
    p.add_argument("--assistant", type=str, help="Use AI assistant by name")
    p.add_argument("--overlay", type=Path, help="Overlay image path")
    p.add_argument(
        "--mask",
        nargs=5,
        type=int,
        metavar=("X", "Y", "W", "H", "F"),
        help="Brighten region X Y W H by factor F",
    )
    p.add_argument("--share", type=str, help="Comma separated platforms")
    p.add_argument("--add-platform", nargs=3, metavar=("NAME", "W", "H"), help="Add custom platform")
    p.add_argument("--metadata", type=str, help="Description for metadata")
    p.add_argument("--filter", choices=["edited", "unedited"], help="Filter images")
    p.add_argument("--auto-suggest", action="store_true", help="Apply assistant suggestions")
    p.add_argument("--ask", action="store_true", help="Show assistant questions")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    args.output.mkdir(exist_ok=True)

    if len(args.catalog) == 1:
        catalog = Catalog(path=args.catalog[0])
    else:
        catalog = MultiCatalog(paths=args.catalog)
    catalog.load()

    preset_folder = args.catalog[0] if len(args.catalog) == 1 else args.catalog[0]
    presets = PresetLibrary(folder=preset_folder / "presets")
    catalog = Catalog(path=args.catalog)
    catalog.load()

    presets = PresetLibrary(folder=args.catalog / "presets")
    presets.load()

    engine = AIEngine()
    assistant = engine.get(args.assistant or "default")

    if args.ask:
        for q in assistant.ask_questions():
            print(f"Question: {q}")

    if args.add_platform:
        name, w, h = args.add_platform
        add_platform(name, int(w), int(h))

    for idx, image in enumerate(catalog):
        editor = Editor(image=image)
        suggestions = assistant.suggest_edit_settings(image)
        if suggestions and not args.auto_suggest:
            print(f"Suggestions for image {idx}: {suggestions}")
        if args.auto_suggest:
            if "brightness" in suggestions and args.brightness == 1.0:
                editor.apply(brighten, suggestions["brightness"])
            if suggestions.get("denoise") and not args.denoise:
                editor.apply(denoise)
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
        if args.overlay:
            overlay = Image.open(args.overlay)
            editor.apply(overlay_image, overlay)
        if args.mask:
            x, y, w, h, f = args.mask
            editor.apply(mask_brighten, (x, y, x + w, y + h), f)
        if args.metadata:
            meta = assistant.create_metadata(args.metadata)
            for k, v in meta.items():
                editor.add_metadata(k, v)
        out_path = args.output / f"image_{idx}.jpg"
        if args.filter == "edited" and not editor.edited:
            continue
        if args.filter == "unedited" and editor.edited:
            continue
        editor.save(out_path)
        tags = assistant.suggest_hashtags(args.metadata or "photo")
        print(f"Saved {out_path} with hashtags: {' '.join(tags)}")
        if args.share:
            share(out_path, [p.strip() for p in args.share.split(',')])
        out_path = args.output / f"image_{idx}.jpg"
        editor.save(out_path)
        tags = assistant.suggest_hashtags("sample photo")
        print(f"Saved {out_path} with hashtags: {' '.join(tags)}")


if __name__ == "__main__":
    main()
