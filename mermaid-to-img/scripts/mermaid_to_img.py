#!/usr/bin/env python3
"""
Mermaid to Image - Convert Mermaid diagrams to high-quality images.

Supports multiple themes, output formats (PNG/JPG/SVG/PDF), custom fonts, and background options.

License: MIT
"""

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

# Predefined theme configurations
THEMES = {
    "material": {
        "theme": "base",
        "themeVariables": {
            "background": "#ffffff",
            "primaryColor": "#ffffff",
            "primaryTextColor": "rgba(0, 0, 0, 0.87)",
            "primaryBorderColor": "#e0e0e0",
            "lineColor": "#757575",
            "secondaryColor": "#ffffff",
            "tertiaryColor": "#ffffff",
            "fontFamily": '"Roboto", "Noto Sans SC", -apple-system, sans-serif',
            "fontSize": "14px",
        },
        "themeCSS": """
            /* Material Design - Elevation and shadows */
            .node rect, .node circle, .node polygon {
              fill: #ffffff !important;
              stroke: none !important;
              rx: 4px !important;
              ry: 4px !important;
              filter:
                drop-shadow(0 1px 3px rgba(0, 0, 0, 0.12))
                drop-shadow(0 1px 2px rgba(0, 0, 0, 0.24));
            }
            .node .label {
              font-family: "Roboto", "Noto Sans SC", -apple-system, sans-serif;
              font-weight: 500;
              fill: rgba(0, 0, 0, 0.87) !important;
            }
            .edgePath .path {
              stroke: #757575 !important;
              stroke-width: 2px !important;
            }
            .arrowheadPath {
              fill: #757575 !important;
              stroke: #757575 !important;
            }
            .edgeLabel {
              background-color: #ffffff !important;
              color: rgba(0, 0, 0, 0.87) !important;
              font-weight: 500;
            }
            /* Sequence Diagram */
            .actor {
              fill: #ffffff !important;
              stroke: none !important;
              filter:
                drop-shadow(0 1px 3px rgba(0, 0, 0, 0.12))
                drop-shadow(0 1px 2px rgba(0, 0, 0, 0.24)) !important;
            }
            .actor text {
              fill: rgba(0, 0, 0, 0.87) !important;
              font-weight: 500;
            }
            .actor-line {
              stroke: #bdbdbd !important;
              stroke-width: 2px !important;
              stroke-dasharray: 4 4 !important;
            }
            .messageLine0, .messageLine1 {
              stroke: #757575 !important;
              stroke-width: 2px !important;
            }
            .messageText {
              fill: rgba(0, 0, 0, 0.87) !important;
              font-weight: 500;
            }
            .note {
              fill: #ffffff !important;
              stroke: none !important;
              filter:
                drop-shadow(0 2px 4px rgba(0, 0, 0, 0.14))
                drop-shadow(0 4px 5px rgba(0, 0, 0, 0.12)) !important;
            }
            .noteText {
              fill: rgba(0, 0, 0, 0.87) !important;
              font-weight: 500;
            }
            /* Cluster/Subgraph */
            .cluster rect {
              fill: #ffffff !important;
              stroke: #e0e0e0 !important;
              stroke-width: 1px !important;
              rx: 8px !important;
              ry: 8px !important;
              filter:
                drop-shadow(0 1px 3px rgba(0, 0, 0, 0.08))
                drop-shadow(0 1px 2px rgba(0, 0, 0, 0.16));
            }
            .cluster text {
              fill: rgba(0, 0, 0, 0.60) !important;
              font-weight: 500;
              text-transform: uppercase;
              letter-spacing: 1px;
            }
        """
    },
    "default": {
        "theme": "default"
    },
    "dark": {
        "theme": "dark"
    },
    "forest": {
        "theme": "forest"
    },
    "neutral": {
        "theme": "neutral"
    }
}

# Supported output formats
SUPPORTED_FORMATS = ["png", "jpg", "jpeg", "svg", "pdf"]


def get_theme_config(theme_name: str, font_family: str = None) -> dict:
    """Get theme configuration with optional custom font."""
    if theme_name not in THEMES:
        print(f"Warning: Unknown theme '{theme_name}', using 'material'", file=sys.stderr)
        theme_name = "material"

    config = THEMES[theme_name].copy()

    # Update font if custom font is specified
    if font_family and "themeVariables" in config:
        config = json.loads(json.dumps(config))  # Deep copy
        config["themeVariables"]["fontFamily"] = font_family
        # Update CSS font
        if "themeCSS" in config:
            config["themeCSS"] = config["themeCSS"].replace(
                '"Roboto", "Noto Sans SC", -apple-system, sans-serif',
                font_family
            )

    return config


def get_output_format(output_path: str) -> str:
    """Get output format from file extension."""
    ext = Path(output_path).suffix.lower().lstrip(".")
    if ext in SUPPORTED_FORMATS:
        return ext
    return "png"


def render_mermaid(
    mermaid_code: str,
    output_path: str,
    theme: str = "material",
    scale: int = 3,
    background_color: str = None,
    transparent: bool = False,
    font_family: str = None,
    width: int = None,
    height: int = None,
) -> bool:
    """Render Mermaid code to image."""

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Write mermaid code
        input_file = tmpdir / "input.mmd"
        input_file.write_text(mermaid_code, encoding="utf-8")

        # Get theme config
        config = get_theme_config(theme, font_family)

        # Write config file
        config_file = tmpdir / "config.json"
        config_file.write_text(json.dumps(config, indent=2), encoding="utf-8")

        # Determine output format
        output_format = get_output_format(output_path)

        # Determine background color
        if transparent:
            bg_color = "transparent"
        elif background_color:
            bg_color = background_color
        else:
            # PNG and SVG default to transparent, JPG defaults to white
            if output_format in ["jpg", "jpeg"]:
                bg_color = "#ffffff"
            else:
                bg_color = "transparent"

        # Build command
        cmd = [
            "npx", "--yes", "@mermaid-js/mermaid-cli",
            "-i", str(input_file),
            "-o", output_path,
            "-c", str(config_file),
            "-s", str(scale),
            "-b", bg_color,
        ]

        # Add size parameters
        if width:
            cmd.extend(["-w", str(width)])
        if height:
            cmd.extend(["-H", str(height)])

        print(f"Generating {output_format.upper()} diagram...")
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"Error: {result.stderr}", file=sys.stderr)
            return False

        print(f"✓ Diagram saved to: {output_path}")
        return True


def main():
    parser = argparse.ArgumentParser(
        description="Mermaid to Image - Convert Mermaid diagrams to high-quality images",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "graph TD; A-->B"
  %(prog)s -f diagram.mmd -o output.png
  %(prog)s --theme dark -o dark.svg "sequenceDiagram; A->>B: Hello"
  %(prog)s --format jpg --background "#f0f0f0" "flowchart LR; A-->B"
  %(prog)s --transparent -o diagram.png "graph TD; A-->B"

Themes: material (default), default, dark, forest, neutral
Formats: png, jpg/jpeg, svg, pdf
        """
    )

    parser.add_argument(
        "code",
        nargs="?",
        help="Mermaid code"
    )
    parser.add_argument(
        "-f", "--file",
        help="Read Mermaid code from file"
    )
    parser.add_argument(
        "-o", "--output",
        default="mermaid_output.png",
        help="Output file path (default: mermaid_output.png)"
    )
    parser.add_argument(
        "-t", "--theme",
        choices=list(THEMES.keys()),
        default="material",
        help="Theme (default: material)"
    )
    parser.add_argument(
        "--format",
        choices=SUPPORTED_FORMATS,
        help="Output format (can also be detected from output file extension)"
    )
    parser.add_argument(
        "--scale",
        type=int,
        default=3,
        help="Scale factor for high-resolution output (default: 3)"
    )
    parser.add_argument(
        "-b", "--background",
        help="Background color (e.g., #ffffff, white, transparent)"
    )
    parser.add_argument(
        "--transparent",
        action="store_true",
        help="Transparent background (works with PNG/SVG)"
    )
    parser.add_argument(
        "--font",
        help='Custom font (e.g., "Arial", "Microsoft YaHei")'
    )
    parser.add_argument(
        "-w", "--width",
        type=int,
        help="Output width (pixels)"
    )
    parser.add_argument(
        "-H", "--height",
        type=int,
        help="Output height (pixels)"
    )
    parser.add_argument(
        "--list-themes",
        action="store_true",
        help="List all available themes"
    )

    args = parser.parse_args()

    # List themes
    if args.list_themes:
        print("Available themes:")
        for name in THEMES:
            print(f"  - {name}")
        sys.exit(0)

    # Get mermaid code
    if args.file:
        try:
            mermaid_code = Path(args.file).read_text(encoding="utf-8")
        except FileNotFoundError:
            print(f"Error: File not found - {args.file}", file=sys.stderr)
            sys.exit(1)
    elif args.code:
        mermaid_code = args.code
    else:
        # Read from stdin
        if not sys.stdin.isatty():
            mermaid_code = sys.stdin.read()
        else:
            parser.print_help()
            sys.exit(1)

    # Process output path and format
    output_path = args.output
    if args.format:
        # Ensure output path uses correct extension
        output_ext = Path(output_path).suffix.lower().lstrip(".")
        if output_ext != args.format:
            output_path = str(Path(output_path).with_suffix(f".{args.format}"))

    # Render diagram
    success = render_mermaid(
        mermaid_code=mermaid_code,
        output_path=output_path,
        theme=args.theme,
        scale=args.scale,
        background_color=args.background,
        transparent=args.transparent,
        font_family=args.font,
        width=args.width,
        height=args.height,
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
