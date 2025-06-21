# Photo Editor

This repository contains a simplified photo editing framework demonstrating how
a larger application could be structured. The focus is on showing the various
modules and their interactions rather than providing a complete replacement for
professional tools like Photoshop or Lightroom.

## Features

- Load a folder of images as a catalog
- Apply basic edits such as brightness, denoise and HSL adjustments
- Save and load presets
- Simple AI assistant that can suggest hashtags

## Usage

```
python -m photo_editor.cli <catalog_path> --brightness 1.2 --denoise
```

Presets are stored in a `presets` folder inside the catalog directory as JSON
files. Each preset can hold arbitrary settings, for example:

```
{"brightness": 1.1}
```

The project is intentionally lightweight and provides placeholders for more
advanced functionality (masking, generative AI, culling, etc.) that could be
implemented in the future.
