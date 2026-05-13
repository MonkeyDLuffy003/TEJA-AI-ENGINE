# ============================================
# T.E.J.A AI INDUSTRIES
# voice_generator.py — V1
# Converts script text to voiceover audio
# Using Edge TTS (completely free)
# ============================================

import asyncio
import edge_tts
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import DEFAULT_VOICE, OUTPUT_FOLDER

def generate_voiceover(script_text, output_filename="voiceover.mp3", voice=DEFAULT_VOICE):
    """
    Converts script text to a voiceover MP3 file.

    script_text: the full narration script string
    output_filename: name of output audio file
    voice: Edge TTS voice name
    Returns: dict with success status and file path
    """

    # Make sure output folder exists
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)

    async def _generate():
        communicate = edge_tts.Communicate(script_text, voice)
        await communicate.save(output_path)

    try:
        asyncio.run(_generate())

        # Check file was actually created and has content
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            size_kb = os.path.getsize(output_path) / 1024
            print(f"  Voiceover created: {output_path} ({size_kb:.1f} KB)")
            return {"success": True, "path": output_path}
        else:
            return {"success": False, "error": "Audio file was not created properly."}

    except Exception as e:
        return {"success": False, "error": f"Voice generation failed: {str(e)}"}


def list_available_voices():
    """Lists all available US English voices."""
    us_voices = [
        "en-US-JennyNeural      (Female - warm, friendly)",
        "en-US-GuyNeural        (Male - clear, professional)",
        "en-US-AriaNeural       (Female - natural, expressive)",
        "en-US-DavisNeural      (Male - casual, conversational)",
        "en-US-AmberNeural      (Female - calm, soothing)",
    ]
    print("\nAvailable US English Voices:")
    for v in us_voices:
        print(" -", v)


# Quick test
if __name__ == "__main__":
    test_script = """
    In a world where technology is evolving faster than ever,
    one young engineer decided to build his own AI — from scratch,
    with nothing but a phone, determination, and a dream.
    This is the story of T.E.J.A AI Industries.
    And it starts today.
    """

    print("Testing voice generator...")
    list_available_voices()

    result = generate_voiceover(test_script, "test_voice.mp3")

    if result["success"]:
        print("SUCCESS! Audio saved at:", result["path"])
    else:
        print("FAILED:", result["error"])
