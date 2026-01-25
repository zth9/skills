#!/usr/bin/env python3
"""
Wrapper script for easyVoice text-to-speech service.
Automatically manages local Node.js service (no Docker required).
"""

import argparse
import json
import os
import re
import signal
import subprocess
import sys
import time
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path


SCRIPT_DIR = Path(__file__).parent.resolve()
EASYVOICE_DIR = SCRIPT_DIR / "easyvoice"
PID_FILE = SCRIPT_DIR / ".easyvoice.pid"
DEFAULT_HOST = "http://localhost:3000"
DEFAULT_VOICE = "zh-CN-YunyangNeural"
GITHUB_REPO = "https://github.com/cosin2077/easyVoice.git"

# Sentence ending punctuation for merging subtitles
SENTENCE_ENDINGS = {"。", "！", "？", ".", "!", "?", "；", ";", "…"}
# Clause punctuation (merge but allow line break here if too long)
CLAUSE_PUNCTUATION = {"，", ",", "：", ":", "、"}
# All punctuation to strip from subtitle line endings
STRIP_PUNCTUATION = "。！？.!?；;…，,：:、—-"


def check_prerequisites() -> list[str]:
    """Check if required tools are installed."""
    missing = []
    # ffmpeg uses -version instead of --version
    version_flags = {"ffmpeg": "-version"}
    for cmd in ["node", "pnpm", "ffmpeg"]:
        flag = version_flags.get(cmd, "--version")
        try:
            subprocess.run([cmd, flag], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            missing.append(cmd)
    return missing


def check_service(host: str) -> bool:
    """Check if easyVoice service is running."""
    try:
        urllib.request.urlopen(host, timeout=5)
        return True
    except urllib.error.URLError:
        return False
    except Exception:
        return True  # Service might be up but endpoint returns error


def clone_repository() -> bool:
    """Clone easyVoice repository if not exists."""
    if EASYVOICE_DIR.exists():
        print(f"easyVoice already cloned at {EASYVOICE_DIR}")
        return True

    print(f"Cloning easyVoice to {EASYVOICE_DIR}...")
    try:
        subprocess.run(
            ["git", "clone", "--depth", "1", GITHUB_REPO, str(EASYVOICE_DIR)],
            check=True,
        )
        print("Clone completed.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to clone repository: {e}")
        return False


def install_dependencies() -> bool:
    """Install npm dependencies."""
    lock_file = EASYVOICE_DIR / "node_modules" / ".install_complete"
    if lock_file.exists():
        return True

    print("Installing dependencies...")
    try:
        subprocess.run(
            ["pnpm", "install", "-r"],
            cwd=EASYVOICE_DIR,
            check=True,
        )
        lock_file.parent.mkdir(parents=True, exist_ok=True)
        lock_file.touch()
        print("Dependencies installed.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to install dependencies: {e}")
        return False


def build_project() -> bool:
    """Build the project."""
    dist_dir = EASYVOICE_DIR / "packages" / "backend" / "dist"
    if dist_dir.exists():
        return True

    print("Building project...")
    try:
        subprocess.run(
            ["pnpm", "build"],
            cwd=EASYVOICE_DIR,
            check=True,
        )
        print("Build completed.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to build project: {e}")
        return False


def start_service(port: int = 3000) -> bool:
    """Start easyVoice service in the background."""
    if check_service(f"http://localhost:{port}"):
        print(f"Service already running on port {port}")
        return True

    # Setup
    if not clone_repository():
        return False
    if not install_dependencies():
        return False
    if not build_project():
        return False

    print(f"Starting easyVoice service on port {port}...")

    # Start the service in background
    env = os.environ.copy()
    env["PORT"] = str(port)
    env["MODE"] = "production"

    log_file = SCRIPT_DIR / "easyvoice.log"
    with open(log_file, "w") as log:
        process = subprocess.Popen(
            ["pnpm", "start"],
            cwd=EASYVOICE_DIR,
            stdout=log,
            stderr=log,
            env=env,
            start_new_session=True,
        )

    # Save PID
    with open(PID_FILE, "w") as f:
        f.write(str(process.pid))

    # Wait for service to be ready
    print("Waiting for service to start...")
    for i in range(60):
        if check_service(f"http://localhost:{port}"):
            print(f"Service started successfully (PID: {process.pid})")
            return True
        time.sleep(1)
        if i % 10 == 9:
            print(f"  Still waiting... ({i + 1}s)")

    print("Service failed to start. Check easyvoice.log for details.")
    return False


def stop_service() -> bool:
    """Stop the running easyVoice service."""
    if not PID_FILE.exists():
        print("No service PID file found.")
        return True

    try:
        with open(PID_FILE) as f:
            pid = int(f.read().strip())

        # Kill the process group
        os.killpg(os.getpgid(pid), signal.SIGTERM)
        print(f"Service stopped (PID: {pid})")
        PID_FILE.unlink()
        return True
    except ProcessLookupError:
        print("Service was not running.")
        PID_FILE.unlink()
        return True
    except Exception as e:
        print(f"Failed to stop service: {e}")
        return False


def get_status() -> dict:
    """Get service status."""
    status = {
        "installed": EASYVOICE_DIR.exists(),
        "running": check_service(DEFAULT_HOST),
        "pid": None,
    }
    if PID_FILE.exists():
        try:
            with open(PID_FILE) as f:
                status["pid"] = int(f.read().strip())
        except Exception:
            pass
    return status


def parse_srt_time(time_str: str) -> int:
    """Parse SRT timestamp to milliseconds."""
    # Format: HH:MM:SS,mmm
    match = re.match(r"(\d{2}):(\d{2}):(\d{2}),(\d{3})", time_str)
    if not match:
        return 0
    h, m, s, ms = map(int, match.groups())
    return h * 3600000 + m * 60000 + s * 1000 + ms


def format_srt_time(ms: int) -> str:
    """Format milliseconds to SRT timestamp."""
    h = ms // 3600000
    ms %= 3600000
    m = ms // 60000
    ms %= 60000
    s = ms // 1000
    ms %= 1000
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def merge_subtitle_by_sentence(srt_path: Path, max_chars: int = 18) -> None:
    """Merge token-level subtitles into sentence-level subtitles."""
    if not srt_path.exists():
        return

    with open(srt_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Parse SRT entries
    entries = []
    pattern = r"(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.+?)(?=\n\n|\n*$)"
    for match in re.finditer(pattern, content, re.DOTALL):
        idx, start, end, text = match.groups()
        entries.append({
            "start": parse_srt_time(start),
            "end": parse_srt_time(end),
            "text": text.strip()
        })

    if not entries:
        return

    # Merge entries by sentence/clause with max length limit
    merged = []
    current = None

    for entry in entries:
        text = entry["text"]

        if current is None:
            current = {
                "start": entry["start"],
                "end": entry["end"],
                "text": text
            }
        else:
            combined_text = current["text"] + text
            last_char = current["text"][-1] if current["text"] else ""

            # Start new subtitle if:
            # 1. Previous text ends with sentence-ending punctuation
            # 2. Combined text exceeds max_chars and previous ends with any punctuation
            # 3. Combined text is way too long (force break)
            should_break = (
                last_char in SENTENCE_ENDINGS or
                (len(combined_text) > max_chars and last_char in CLAUSE_PUNCTUATION) or
                (len(combined_text) > max_chars + 10)  # Force break if too long
            )

            if should_break:
                merged.append(current)
                current = {
                    "start": entry["start"],
                    "end": entry["end"],
                    "text": text
                }
            else:
                # Merge with current
                current["end"] = entry["end"]
                current["text"] = combined_text

    # Don't forget the last entry
    if current:
        merged.append(current)

    # Write merged SRT
    with open(srt_path, "w", encoding="utf-8") as f:
        for i, entry in enumerate(merged, 1):
            # Strip trailing punctuation from subtitle text
            text = entry['text'].rstrip(STRIP_PUNCTUATION)
            f.write(f"{i}\n")
            f.write(f"{format_srt_time(entry['start'])} --> {format_srt_time(entry['end'])}\n")
            f.write(f"{text}\n\n")


def generate_stream_tts(text: str, voice: str, output: str, host: str) -> bool:
    """Generate speech from long text using streaming API."""
    url = f"{host}/api/v1/tts/createStream"
    data = json.dumps({"text": text, "voice": voice}).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
    )

    # Record timestamp before request for subtitle filename matching
    request_timestamp = int(time.time() * 1000)

    try:
        with urllib.request.urlopen(req, timeout=600) as response:
            content = response.read()

            # Check response type from header
            tts_type = response.headers.get("x-generate-tts-type", "")

            if tts_type == "application/json":
                # JSON response with file paths (cached result)
                response_data = json.loads(content.decode("utf-8"))
                if response_data.get("success") and response_data.get("data", {}).get("audio"):
                    audio_path = response_data["data"]["audio"]
                    srt_path = response_data["data"].get("srt")

                    # Download audio
                    encoded_audio_path = urllib.parse.quote(audio_path, safe="/")
                    audio_url = f"{host}{encoded_audio_path}"
                    with urllib.request.urlopen(audio_url, timeout=300) as audio_response:
                        with open(output, "wb") as f:
                            f.write(audio_response.read())
                    print(f"Audio saved to: {output}")

                    # Download subtitle
                    if srt_path:
                        output_path = Path(output)
                        srt_output = output_path.with_suffix(".srt")
                        encoded_srt_path = urllib.parse.quote(f"/{srt_path}", safe="/")
                        srt_url = f"{host}{encoded_srt_path}"
                        for retry in range(10):
                            try:
                                with urllib.request.urlopen(srt_url, timeout=60) as srt_response:
                                    with open(srt_output, "wb") as f:
                                        f.write(srt_response.read())
                                merge_subtitle_by_sentence(srt_output)
                                print(f"Subtitle saved to: {srt_output}")
                                break
                            except urllib.error.HTTPError as e:
                                if e.code == 404 and retry < 9:
                                    time.sleep(0.5)
                                    continue
                                print(f"Warning: Failed to download subtitle: {e}")
                                break
                            except Exception as e:
                                print(f"Warning: Failed to download subtitle: {e}")
                                break
                    return True
                else:
                    print(f"API Error: {response_data}")
                    return False
            else:
                # Binary audio stream
                with open(output, "wb") as f:
                    f.write(content)
                print(f"Audio saved to: {output}")

                # Try to download subtitle (async generated)
                output_path = Path(output)
                srt_output = output_path.with_suffix(".srt")
                # Create json_data format for subtitle download
                json_data = [{"text": text, "voice": voice}]
                download_subtitle_with_retry(host, json_data, srt_output, request_timestamp)
                return True

    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}")
        return False
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}")
        return False


def generate_simple_tts(text: str, voice: str, output: str, host: str) -> bool:
    """Generate speech from simple text."""
    # Use streaming API for long text (>200 chars)
    if len(text) > 200:
        return generate_stream_tts(text, voice, output, host)

    url = f"{host}/api/v1/tts/generate"
    data = json.dumps({"text": text, "voice": voice}).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
    )

    try:
        with urllib.request.urlopen(req, timeout=300) as response:
            response_data = json.loads(response.read().decode("utf-8"))

        # API returns JSON with audio file path
        if response_data.get("success") and response_data.get("data", {}).get("audio"):
            audio_path = response_data["data"]["audio"]
            srt_path = response_data["data"].get("srt")

            # URL encode the path to handle non-ASCII characters
            encoded_audio_path = urllib.parse.quote(audio_path, safe="/")
            audio_url = f"{host}{encoded_audio_path}"

            # Download the actual audio file
            with urllib.request.urlopen(audio_url, timeout=300) as audio_response:
                with open(output, "wb") as f:
                    f.write(audio_response.read())
            print(f"Audio saved to: {output}")

            # Download subtitle file if available
            if srt_path:
                output_path = Path(output)
                srt_output = output_path.with_suffix(".srt")
                encoded_srt_path = urllib.parse.quote(f"/{srt_path}", safe="/")
                srt_url = f"{host}{encoded_srt_path}"

                # Subtitle is generated asynchronously, retry a few times
                for retry in range(10):
                    try:
                        with urllib.request.urlopen(srt_url, timeout=60) as srt_response:
                            with open(srt_output, "wb") as f:
                                f.write(srt_response.read())
                        merge_subtitle_by_sentence(srt_output)
                        print(f"Subtitle saved to: {srt_output}")
                        break
                    except urllib.error.HTTPError as e:
                        if e.code == 404 and retry < 9:
                            time.sleep(0.5)  # Wait for async subtitle generation
                            continue
                        print(f"Warning: Failed to download subtitle: {e}")
                        break
                    except Exception as e:
                        print(f"Warning: Failed to download subtitle: {e}")
                        break

            return True
        else:
            print(f"API Error: {response_data}")
            return False
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}")
        return False
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}")
        return False


def generate_multi_character_tts(json_data: list, output: str, host: str) -> bool:
    """Generate speech from multi-character JSON."""
    url = f"{host}/api/v1/tts/generateJson"
    data = json.dumps({"data": json_data}).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
    )

    # Record timestamp before request for subtitle filename matching
    request_timestamp = int(time.time() * 1000)

    try:
        with urllib.request.urlopen(req, timeout=600) as response:
            content = response.read()

            # Check if response is JSON (error) or binary audio
            try:
                response_data = json.loads(content.decode("utf-8"))
                # If we get here, it's JSON - likely an error or file path response
                if response_data.get("success") and response_data.get("data", {}).get("audio"):
                    audio_path = response_data["data"]["audio"]
                    srt_path = response_data["data"].get("srt")
                    encoded_path = urllib.parse.quote(audio_path, safe="/")
                    audio_url = f"{host}{encoded_path}"
                    with urllib.request.urlopen(audio_url, timeout=600) as audio_response:
                        with open(output, "wb") as f:
                            f.write(audio_response.read())
                    print(f"Audio saved to: {output}")

                    # Download subtitle if available
                    if srt_path:
                        output_path = Path(output)
                        srt_output = output_path.with_suffix(".srt")
                        encoded_srt_path = urllib.parse.quote(f"/{srt_path}", safe="/")
                        srt_url = f"{host}{encoded_srt_path}"
                        try:
                            with urllib.request.urlopen(srt_url, timeout=60) as srt_response:
                                with open(srt_output, "wb") as f:
                                    f.write(srt_response.read())
                            merge_subtitle_by_sentence(srt_output)
                            print(f"Subtitle saved to: {srt_output}")
                        except Exception as e:
                            print(f"Warning: Failed to download subtitle: {e}")
                    return True
                else:
                    print(f"API Error: {response_data}")
                    return False
            except (json.JSONDecodeError, UnicodeDecodeError):
                # Binary audio data - write directly
                with open(output, "wb") as f:
                    f.write(content)
                print(f"Audio saved to: {output}")

                # For streaming response, subtitle is generated asynchronously on server
                # Try to fetch it after a short delay
                output_path = Path(output)
                srt_output = output_path.with_suffix(".srt")
                download_subtitle_with_retry(host, json_data, srt_output, request_timestamp)

        return True
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}")
        return False
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}")
        return False


def safe_filename(text: str) -> str:
    """Convert text to safe filename (matching server logic)."""
    import re
    return re.sub(r'[/\\?%*:|"<>\r\n\s#]', '-', text)


def download_subtitle_with_retry(host: str, json_data: list, srt_output: Path, request_timestamp: int, max_retries: int = 30) -> bool:
    """Try to download subtitle file with retries (generated asynchronously on server)."""
    # Generate the same ID pattern as the server does
    voice = json_data[0].get("voice", "zh-CN-YunyangNeural")
    text = "".join(item.get("text", "") for item in json_data)
    text_prefix = safe_filename(text)[:10]

    # Server generates: {voice}-{text[:10]}-{timestamp}.srt
    pattern_prefix = f"{voice}-{text_prefix}-"

    print("Waiting for subtitle generation...")
    for attempt in range(max_retries):
        time.sleep(0.5)

        # Get current timestamp and check a small window of recent timestamps
        current_time = int(time.time() * 1000)
        # Only check timestamps in windows of 100ms increments to reduce requests
        start_ts = request_timestamp + (attempt * 2000)  # Expand search window each retry
        end_ts = min(start_ts + 2000, current_time + 1000)

        for ts in range(start_ts, end_ts, 1):
            srt_filename = f"{pattern_prefix}{ts}.srt"
            encoded_srt_path = urllib.parse.quote(f"/{srt_filename}", safe="/")
            srt_url = f"{host}{encoded_srt_path}"

            try:
                with urllib.request.urlopen(srt_url, timeout=1) as srt_response:
                    with open(srt_output, "wb") as f:
                        f.write(srt_response.read())
                    merge_subtitle_by_sentence(srt_output)
                    print(f"Subtitle saved to: {srt_output}")
                    return True
            except Exception:
                continue

    print("Note: Subtitle not available for multi-character mode (async generation)")
    return False


def main():
    parser = argparse.ArgumentParser(
        description="Convert text to speech using easyVoice (local Node.js)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Simple text-to-speech (auto-starts service)
  python wrapper.py --text "Hello world" --output hello.mp3

  # With specific voice
  python wrapper.py --text "Hello" --voice zh-CN-XiaoyiNeural --output hello.mp3

  # Multi-character from JSON file
  python wrapper.py --json-file characters.json --output story.mp3

  # Service management
  python wrapper.py --start-service
  python wrapper.py --stop-service
  python wrapper.py --status
        """,
    )

    parser.add_argument("--text", "-t", help="Text to convert to speech")
    parser.add_argument("--json-file", "-j", help="JSON file with multi-character data")
    parser.add_argument("--json", help="JSON string with multi-character data")
    parser.add_argument("--output", "-o", help="Output audio file path")
    parser.add_argument("--voice", "-v", default=DEFAULT_VOICE, help=f"Voice name (default: {DEFAULT_VOICE})")
    parser.add_argument("--host", default=DEFAULT_HOST, help=f"easyVoice service URL (default: {DEFAULT_HOST})")
    parser.add_argument("--port", type=int, default=3000, help="Port for the service (default: 3000)")

    # Service management
    parser.add_argument("--start-service", action="store_true", help="Start the easyVoice service")
    parser.add_argument("--stop-service", action="store_true", help="Stop the easyVoice service")
    parser.add_argument("--status", action="store_true", help="Show service status")

    args = parser.parse_args()

    # Handle service management commands
    if args.status:
        status = get_status()
        print(f"Installed: {status['installed']}")
        print(f"Running: {status['running']}")
        if status["pid"]:
            print(f"PID: {status['pid']}")
        sys.exit(0)

    if args.stop_service:
        success = stop_service()
        sys.exit(0 if success else 1)

    if args.start_service:
        # Check prerequisites first
        missing = check_prerequisites()
        if missing:
            print(f"Missing prerequisites: {', '.join(missing)}")
            print("Install them with:")
            if "node" in missing:
                print("  brew install node")
            if "pnpm" in missing:
                print("  npm install -g pnpm")
            if "ffmpeg" in missing:
                print("  brew install ffmpeg")
            sys.exit(1)
        success = start_service(args.port)
        sys.exit(0 if success else 1)

    # Validate input for TTS generation
    if not args.text and not args.json_file and not args.json:
        parser.error("One of --text, --json-file, --json, or a service command is required")

    if not args.output:
        parser.error("--output is required for TTS generation")

    # Check prerequisites
    missing = check_prerequisites()
    if missing:
        print(f"Missing prerequisites: {', '.join(missing)}")
        print("Install them with:")
        if "node" in missing:
            print("  brew install node")
        if "pnpm" in missing:
            print("  npm install -g pnpm")
        if "ffmpeg" in missing:
            print("  brew install ffmpeg")
        sys.exit(1)

    # Auto-start service if not running
    if not check_service(args.host):
        print("Service not running, starting automatically...")
        if not start_service(args.port):
            sys.exit(1)

    # Generate audio
    if args.text:
        success = generate_simple_tts(args.text, args.voice, args.output, args.host)
    elif args.json_file:
        with open(args.json_file, "r", encoding="utf-8") as f:
            json_data = json.load(f)
        success = generate_multi_character_tts(json_data, args.output, args.host)
    else:
        json_data = json.loads(args.json)
        success = generate_multi_character_tts(json_data, args.output, args.host)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
