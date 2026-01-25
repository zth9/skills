---
name: text-to-audio
description: Convert text to speech audio using easyVoice with multi-character dubbing support. Use when user wants to generate audio/speech from text, create audiobooks, or needs text-to-speech with different character voices.
# EXTENDED METADATA (MANDATORY)
github_url: https://github.com/cosin2077/easyVoice
github_hash: 75761d426907d2b9d47d5fbccab743f3ac875c57
version: 0.1.0
created_at: 2026-01-25
entry_point: scripts/wrapper.py
dependencies: ["node", "pnpm", "ffmpeg"]
---

# Text to Audio

Convert text to high-quality speech audio using [easyVoice](https://github.com/cosin2077/easyVoice).

> **Note**: This skill depends on the [easyVoice](https://github.com/cosin2077/easyVoice) project. The wrapper script will automatically clone it to `scripts/easyvoice/` on first run. The cloned directory is excluded from version control via `.gitignore`.

## Features

- Text-to-speech conversion with streaming support
- Multi-character dubbing with different voices
- AI-powered voice recommendation
- Automatic subtitle generation
- Supports 100k+ characters (novel-length content)
- Adjustable speech rate, pitch, and volume

## Usage

The agent should use this skill when:
- User wants to convert text to speech/audio
- User wants to create audiobook from text
- User needs multi-character voice dubbing
- User wants to generate audio with subtitles

## Prerequisites

```bash
# Install Node.js (if not installed)
brew install node

# Install pnpm
npm install -g pnpm

# Install ffmpeg (required for audio processing)
brew install ffmpeg
```

## Quick Start

### 1. Simple Text-to-Speech

```bash
python scripts/wrapper.py --text "Hello, this is a test." --output output.mp3
```

The wrapper will automatically:
1. Clone easyVoice repository (first time only)
2. Install dependencies
3. Start the service
4. Generate audio

### 2. Multi-Character Dubbing

```bash
python scripts/wrapper.py --json-file characters.json --output output.mp3
```

### 3. Manual Service Management

```bash
# Start service manually
python scripts/wrapper.py --start-service

# Stop service
python scripts/wrapper.py --stop-service

# Check service status
python scripts/wrapper.py --status
```

## API Endpoints

### Simple TTS
- **POST** `/api/v1/tts/generate`
- Body: `{ "text": "your text", "voice": "zh-CN-YunxiNeural" }`

### Multi-Character TTS
- **POST** `/api/v1/tts/generateJson`
- Body: JSON array with character definitions

## Voice Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `voice` | `zh-CN-YunyangNeural` | Voice name from [voice list](https://github.com/cosin2077/easyVoice/blob/main/packages/backend/src/llm/prompt/voiceList.json) |
| `rate` | `+0%` | Speech rate adjustment |
| `pitch` | `+0Hz` | Pitch adjustment |
| `volume` | `+0%` | Volume adjustment |

## Example: Multi-Character JSON

```json
[
  {
    "desc": "Narrator",
    "text": "Once upon a time...",
    "voice": "zh-CN-YunxiNeural",
    "rate": "0%",
    "volume": "0%"
  },
  {
    "desc": "Character A",
    "text": "Hello there!",
    "voice": "zh-CN-YunjianNeural",
    "volume": "40%"
  }
]
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `3000` | Service port |
| `OPENAI_BASE_URL` | `https://api.openai.com/v1` | OpenAI compatible API |
| `OPENAI_API_KEY` | - | API key for AI voice recommendation |
| `EDGE_API_LIMIT` | `3` | Edge-TTS concurrency limit |

## Output

Audio files are saved to the specified `--output` path. Subtitle files (SRT format) are automatically generated alongside the audio file with the same name but `.srt` extension.

Example:
```bash
python scripts/wrapper.py --text "Hello world" --output /tmp/hello.mp3
# Generates:
#   /tmp/hello.mp3  (audio file)
#   /tmp/hello.srt  (subtitle file)
```
