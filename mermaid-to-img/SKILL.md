---
name: mermaid-to-img
description: Convert Mermaid diagrams to high-quality images with multiple themes, formats (PNG/JPG/SVG/PDF), custom fonts, and background options.
version: 1.0.0
entry_point: scripts/mermaid_to_img.py
dependencies: ["node", "npx", "@mermaid-js/mermaid-cli"]
---

# Mermaid to Image

A lightweight CLI tool that converts Mermaid diagrams to high-quality images with Material Design theme support.

## Quick Start

### Basic Usage

```bash
# Direct input
python3 scripts/mermaid_to_img.py "graph TD; A-->B"

# From file
python3 scripts/mermaid_to_img.py -f diagram.mmd

# Specify output path
python3 scripts/mermaid_to_img.py -o output.png "graph TD; A-->B"
```

### Using Different Themes

```bash
# Dark theme
python3 scripts/mermaid_to_img.py --theme dark -o dark.png "graph TD; A-->B"

# Forest theme
python3 scripts/mermaid_to_img.py --theme forest -o forest.png "graph TD; A-->B"

# List all themes
python3 scripts/mermaid_to_img.py --list-themes
```

### Output Different Formats

```bash
# SVG vector (transparent background)
python3 scripts/mermaid_to_img.py -o diagram.svg "graph TD; A-->B"

# JPG (auto white background)
python3 scripts/mermaid_to_img.py -o diagram.jpg "graph TD; A-->B"

# PNG with transparent background
python3 scripts/mermaid_to_img.py --transparent -o diagram.png "graph TD; A-->B"

# PNG with custom background color
python3 scripts/mermaid_to_img.py -b "#f0f0f0" -o diagram.png "graph TD; A-->B"
```

### Custom Font and Size

```bash
# Custom font
python3 scripts/mermaid_to_img.py --font "Arial" -o diagram.png "graph TD; A-->B"

# Specify output size
python3 scripts/mermaid_to_img.py -w 800 -H 600 -o diagram.png "graph TD; A-->B"
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| `<mermaid_code>` | Mermaid code (positional argument) |
| `-f, --file` | Read Mermaid code from file |
| `-o, --output` | Output file path (default: `mermaid_output.png`) |
| `-t, --theme` | Theme selection (default: `material`) |
| `--format` | Output format: `png`, `jpg`, `svg`, `pdf` |
| `--scale` | Scale factor for high-resolution (default: 3) |
| `-b, --background` | Background color (e.g., `#ffffff`, `white`, `transparent`) |
| `--transparent` | Transparent background (PNG/SVG only) |
| `--font` | Custom font (e.g., `"Arial"`, `"Microsoft YaHei"`) |
| `-w, --width` | Output width (pixels) |
| `-H, --height` | Output height (pixels) |
| `--list-themes` | List all available themes |

## Themes

| Theme | Description |
|-------|-------------|
| `material` | **Default** - Google Material Design style with white cards and shadows |
| `default` | Mermaid default theme |
| `dark` | Dark theme |
| `forest` | Green forest theme |
| `neutral` | Neutral gray theme |

## Output Formats

| Format | Description |
|--------|-------------|
| `png` | PNG image (default transparent, 3x high-resolution) |
| `jpg/jpeg` | JPG image (auto white background) |
| `svg` | SVG vector (transparent, infinite scaling) |
| `pdf` | PDF document |

## Supported Diagram Types

- Flowchart (flowchart/graph)
- Sequence Diagram (sequenceDiagram)
- Class Diagram (classDiagram)
- State Diagram (stateDiagram)
- Entity Relationship Diagram (erDiagram)
- Gantt Chart (gantt)
- Pie Chart (pie)
- Mind Map (mindmap)
- Timeline (timeline)
- And more...

## Material Theme Features

- Google Material Design style
- White cards with shadow effects
- Roboto font (with Noto Sans SC for CJK support)
- Professional grayscale color scheme
- 3x resolution for high-quality output

## License

MIT
