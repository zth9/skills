---
name: text-to-audio
description: Convert text to natural speech using ChatTTS local AI model. Use when user wants to generate audio/speech from text, create voice content, or needs high-quality Chinese/English text-to-speech synthesis.
# EXTENDED METADATA (MANDATORY)
github_url: https://github.com/2noise/ChatTTS
github_hash: c26573a61ebde14ac456d8ed4b9f96908d3dd8fa
version: 0.2.0
created_at: 2026-01-25
entry_point: scripts/wrapper.py
dependencies: ["python3", "uv"]
---

# Text to Audio

Convert text to natural speech using [ChatTTS](https://github.com/2noise/ChatTTS), a generative speech model designed for conversational scenarios.

## Features

- Local AI model inference (no cloud API required)
- Natural conversational speech style
- Chinese and English support
- Prosody control: laughter, pauses, oral style via prompt tokens
- Reproducible speaker voice via seed
- WAV output (24kHz), optional MP3 conversion (requires ffmpeg)

## Usage

The agent should use this skill when:
- User wants to convert text to speech/audio
- User wants to generate natural-sounding voice content
- User needs Chinese or English TTS with conversational style

## Prerequisites

```bash
# Install uv (Python package manager)
brew install uv

# Optional: Install ffmpeg for MP3 output
brew install ffmpeg
```

## Quick Start

### 1. Install Dependencies (first time)

```bash
python scripts/wrapper.py --install
```

### 2. Simple Text-to-Speech

```bash
python scripts/wrapper.py --text "你好，这是一个测试。" --output output.wav
```

### 3. Specify Speaker Seed

```bash
python scripts/wrapper.py --text "Hello world" --seed 42 --output output.wav
```

### 4. MP3 Output

```bash
python scripts/wrapper.py --text "测试MP3输出" --output output.mp3 --format mp3
```

### 5. Prosody Control

```bash
python scripts/wrapper.py --text "这真是太有趣了" --prompt "[oral_2][laugh_0][break_6]" --output output.wav
```

## CLI Parameters

| Parameter | Short | Default | Description |
|-----------|-------|---------|-------------|
| `--text` | `-t` | - | Text to convert to speech |
| `--output` | `-o` | - | Output file path (.wav or .mp3) |
| `--seed` | `-s` | random | Speaker seed for reproducible voice |
| `--temperature` | - | `0.3` | Temperature for sampling |
| `--top-p` | - | `0.7` | Top-P decoding parameter |
| `--top-k` | - | `20` | Top-K decoding parameter |
| `--prompt` | - | `[oral_2][laugh_0][break_6]` | Prosody prompt tokens |
| `--format` | - | `wav` | Output format: wav or mp3 |
| `--install` | - | - | Install dependencies only |

## Prosody Prompt Tokens

ChatTTS supports special tokens to control speech style:

- `[oral_0]` to `[oral_9]` — Oral/casual speech level
- `[laugh_0]` to `[laugh_9]` — Laughter intensity
- `[break_0]` to `[break_9]` — Pause/break duration

Example: `[oral_2][laugh_0][break_6]` produces natural speech with moderate oral style and longer pauses.

## Output

Audio files are saved to the specified `--output` path. Default format is WAV (24kHz). Use `--format mp3` for MP3 output (requires ffmpeg).
