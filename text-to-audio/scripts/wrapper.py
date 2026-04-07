#!/usr/bin/env python3
"""
Wrapper script for ChatTTS text-to-speech.
Manages venv environment and delegates inference to _infer.py.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).parent.resolve()
VENV_DIR = SCRIPT_DIR.parent / ".venv"
VENV_PYTHON = VENV_DIR / "bin" / "python"
INFER_SCRIPT = SCRIPT_DIR / "_infer.py"

DEPENDENCIES = [
    "transformers<5.0.0",
    "git+https://github.com/2noise/ChatTTS.git@c26573a61ebde14ac456d8ed4b9f96908d3dd8fa",
    "torchaudio",
    "pydub",
    "requests",
]


def ensure_venv() -> bool:
    """Create venv and install dependencies if not present."""
    marker = VENV_DIR / ".installed"
    if marker.exists():
        return True

    print("Setting up virtual environment...")

    # Create venv with uv
    try:
        subprocess.run(
            ["uv", "venv", str(VENV_DIR), "--python", "3.11"],
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        print("Error: 'uv' is not installed. Install it with: brew install uv")
        return False
    except subprocess.CalledProcessError as e:
        print(f"Failed to create venv: {e.stderr}")
        return False

    # Install dependencies
    print("Installing dependencies (ChatTTS, torchaudio, pydub)...")
    try:
        subprocess.run(
            ["uv", "pip", "install", "--python", str(VENV_PYTHON)] + DEPENDENCIES,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"Failed to install dependencies: {e}")
        return False

    marker.touch()
    print("Dependencies installed successfully.")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Convert text to speech using ChatTTS (local AI model)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Install dependencies
  python wrapper.py --install

  # Simple text-to-speech
  python wrapper.py --text "你好，这是一个测试。" --output output.wav

  # With specific speaker seed
  python wrapper.py --text "Hello world" --seed 42 --output output.wav

  # MP3 output (requires ffmpeg)
  python wrapper.py --text "测试" --output output.mp3 --format mp3

  # Prosody control
  python wrapper.py --text "太有趣了" --prompt "[oral_2][laugh_0][break_6]" --output output.wav
        """,
    )

    parser.add_argument("--text", "-t", help="Text to convert to speech")
    parser.add_argument("--output", "-o", help="Output file path (.wav or .mp3)")
    parser.add_argument("--seed", "-s", type=int, default=None, help="Speaker seed for reproducible voice")
    parser.add_argument("--temperature", type=float, default=0.3, help="Sampling temperature (default: 0.3)")
    parser.add_argument("--top-p", type=float, default=0.7, help="Top-P decoding (default: 0.7)")
    parser.add_argument("--top-k", type=int, default=20, help="Top-K decoding (default: 20)")
    parser.add_argument("--prompt", default="[oral_2][laugh_0][break_6]", help="Prosody prompt tokens")
    parser.add_argument("--format", choices=["wav", "mp3"], default="wav", help="Output format (default: wav)")
    parser.add_argument("--install", action="store_true", help="Install dependencies only")

    args = parser.parse_args()

    # Ensure venv is ready
    if not ensure_venv():
        sys.exit(1)

    if args.install:
        print("Installation complete.")
        sys.exit(0)

    # Validate input
    if not args.text:
        parser.error("--text is required for TTS generation")
    if not args.output:
        parser.error("--output is required for TTS generation")

    # Build inference command
    cmd = [
        str(VENV_PYTHON), str(INFER_SCRIPT),
        "--text", args.text,
        "--output", args.output,
        "--temperature", str(args.temperature),
        "--top-p", str(args.top_p),
        "--top-k", str(args.top_k),
        "--prompt", args.prompt,
        "--format", args.format,
    ]
    if args.seed is not None:
        cmd.extend(["--seed", str(args.seed)])

    # Run inference in venv python
    result = subprocess.run(cmd)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
