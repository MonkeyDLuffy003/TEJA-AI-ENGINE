# ============================================
# T.E.J.A AI INDUSTRIES
# image_prompt_generator.py — V1
# Converts scene descriptions into detailed
# image generation prompts using Gemini API
# ============================================

import requests
import sys
import os
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import GEMINI_URL

def generate_image_prompts(scenes, style="cinematic"):
    """
    Takes a list of scene descriptions and converts each
    into a detailed image generation prompt.

    scenes: list of scene description strings
    style: "cinematic", "anime", "realistic"
    Returns: list of image prompt strings
    """

    if style == "anime":
        style_guide = "anime art style, vibrant colors, dramatic lighting, Studio Ghibli inspired"
    elif style == "cinematic":
        style_guide = "cinematic photography, dramatic lighting, ultra detailed, 4K quality"
    else:
        style_guide = "realistic, photographic, high detail, professional quality"

    image_prompts = []

    for i, scene in enumerate(scenes):
        prompt = f"""
        You are an expert AI image prompt engineer.
        Convert this scene description into a detailed image generation prompt.

        Scene: {scene}
        Style: {style_guide}

        Rules:
        - Return ONLY the image prompt, nothing else
        - Include: subject, setting, lighting, mood, style, quality tags
        - Maximum 50 words
        - No explanations or extra text
        """

        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }

        try:
            response = requests.post(GEMINI_URL, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()
            image_prompt = result["candidates"][0]["content"]["parts"][0]["text"].strip()
            image_prompts.append(image_prompt)
            print(f"  Scene {i+1}/{len(scenes)} prompt generated ✓")

        except requests.exceptions.Timeout:
            # If one scene fails, use a basic fallback prompt
            fallback = f"{scene}, {style_guide}, high quality"
            image_prompts.append(fallback)
            print(f"  Scene {i+1}/{len(scenes)} used fallback prompt")

        except Exception as e:
            fallback = f"{scene}, {style_guide}, high quality"
            image_prompts.append(fallback)
            print(f"  Scene {i+1} error: {str(e)} — used fallback")

    return {"success": True, "prompts": image_prompts}


# Quick test
if __name__ == "__main__":
    test_scenes = [
        "A young boy sitting alone under a tree, looking at a laptop screen",
        "Lines of code appearing on a dark screen, glowing green",
        "A character standing on a mountain top looking at the horizon"
    ]

    print("Testing image prompt generator...")
    result = generate_image_prompts(test_scenes, style="anime")

    if result["success"]:
        print("\nSUCCESS! Generated prompts:")
        for i, p in enumerate(result["prompts"]):
            print(f"\nScene {i+1}: {p}")
    else:
        print("FAILED:", result)
