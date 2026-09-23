#!/usr/bin/env python3
"""
Generate English TTS audio (.ogg) for all 75 bingo balls (B1-B15, I16-I30,
N31-N45, G46-G60, O61-O75).
"""

import os
import sys
from gtts import gTTS
from pydub import AudioSegment

# Standard bingo letter -> number range mapping
RANGES = {
    "B": range(1, 16),
    "I": range(16, 31),
    "N": range(31, 46),
    "G": range(46, 61),
    "O": range(61, 76),
}


def generate_bingo_audio(output_dir="bingo_audio"):
    os.makedirs(output_dir, exist_ok=True)

    balls = [f"{letter}{num}" for letter, nums in RANGES.items() for num in nums]

    print(f"Generating {len(balls)} bingo ball audio files into '{output_dir}/'...")

    for ball in balls:
        letter, number = ball[0], ball[1:]
        text = f"{letter} {number}"  # e.g. "B 1" reads more naturally than "B1"
        ogg_path = os.path.join(output_dir, f"{ball}.ogg")

        if os.path.exists(ogg_path):
            print(f"  {ball}.ogg already exists, skipping")
            continue

        # 1. Generate speech with gTTS (outputs mp3)
        tmp_mp3 = os.path.join(output_dir, f"_tmp_{ball}.mp3")
        tts = gTTS(text=text, lang="en")
        tts.save(tmp_mp3)

        # 2. Convert mp3 -> ogg (Vorbis) using pydub/ffmpeg
        audio = AudioSegment.from_mp3(tmp_mp3)
        audio.export(ogg_path, format="ogg")

        os.remove(tmp_mp3)
        print(f"  Created {ball}.ogg")

    # Generate "Bingo!" voiceline
    bingo_text = "Bingo!"
    bingo_ogg_path = os.path.join(output_dir, "bingo.ogg")
    if not os.path.exists(bingo_ogg_path):
        tmp_bingo_mp3 = os.path.join(output_dir, "_tmp_bingo.mp3")
        tts = gTTS(text=bingo_text, lang="en")
        tts.save(tmp_bingo_mp3)

        audio = AudioSegment.from_mp3(tmp_bingo_mp3)
        audio.export(bingo_ogg_path, format="ogg")

        os.remove(tmp_bingo_mp3)
        print(f"  Created bingo.ogg")

    print("Done!")


if __name__ == "__main__":
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "bingo_audio"
    generate_bingo_audio(out_dir)
