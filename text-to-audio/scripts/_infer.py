#!/usr/bin/env python3
"""
ChatTTS inference script. Runs inside the venv with torch/ChatTTS available.
"""

import argparse
import random
import sys
from pathlib import Path

import ChatTTS
import torch
import numpy as np
from scipy.io import wavfile

SKILL_DIR = Path(__file__).parent.parent.resolve()


def main():
    parser = argparse.ArgumentParser(description="ChatTTS inference")
    parser.add_argument("--text", required=True, help="Text to synthesize")
    parser.add_argument("--output", required=True, help="Output file path")
    parser.add_argument("--seed", type=int, default=None, help="Speaker seed")
    parser.add_argument("--temperature", type=float, default=0.3)
    parser.add_argument("--top-p", type=float, default=0.7)
    parser.add_argument("--top-k", type=int, default=20)
    parser.add_argument("--prompt", default="[oral_2][laugh_0][break_6]")
    parser.add_argument("--format", choices=["wav", "mp3"], default="wav")
    args = parser.parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Initialize ChatTTS with models stored in skill directory
    print("Loading ChatTTS model...")
    chat = ChatTTS.Chat()
    chat.load(compile=False, custom_path=str(SKILL_DIR))

    # Sample speaker
    seed = args.seed if args.seed is not None else random.randint(0, 2**32 - 1)
    print(f"Using speaker seed: {seed}")
    torch.manual_seed(seed)
    rand_spk = chat.sample_random_speaker()

    # Build inference params
    params_infer = ChatTTS.Chat.InferCodeParams(
        spk_emb=rand_spk,
        temperature=args.temperature,
        top_P=args.top_p,
        top_K=args.top_k,
    )

    params_refine = ChatTTS.Chat.RefineTextParams(
        prompt=args.prompt,
    )

    # Run inference
    print("Generating speech...")
    wavs = chat.infer(
        [args.text],
        params_infer_code=params_infer,
        skip_refine_text=True,
    )

    if not wavs or len(wavs) == 0:
        print("Error: No audio generated")
        sys.exit(1)

    # Save WAV
    wav_path = output_path if args.format == "wav" else output_path.with_suffix(".wav")
    audio_data = (wavs[0] * 32767).astype(np.int16)
    wavfile.write(str(wav_path), 24000, audio_data)
    print(f"WAV saved to: {wav_path}")

    # Convert to MP3 if requested
    if args.format == "mp3":
        try:
            from pydub import AudioSegment
            audio = AudioSegment.from_wav(str(wav_path))
            mp3_path = output_path.with_suffix(".mp3")
            audio.export(str(mp3_path), format="mp3")
            wav_path.unlink()
            print(f"MP3 saved to: {mp3_path}")
        except ImportError:
            print("Warning: pydub not available, keeping WAV format")
        except Exception as e:
            print(f"Warning: MP3 conversion failed ({e}), keeping WAV format")

    print("Done.")


if __name__ == "__main__":
    main()
