# ============================================
# T.E.J.A AI INDUSTRIES
# story_generator.py — V1
# Generates story script using Gemini API
# ============================================

import requests
import sys
import os

# Add parent folder to path so we can import settings
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import GEMINI_URL

def generate_story(topic, channel="storytelling"):
    """
    Takes a topic and generates a full narrated story script.
    channel: "storytelling" or "ai_journey"
    Returns: dict with title, script, scenes list
    """

    if channel == "ai_journey":
        style_instruction = """
        Write in an engaging anime-style narrative. 
        The main character is a young self-taught AI developer from India
        building his dream with zero money but unlimited determination.
        Tone: inspiring, relatable, slightly dramatic like an anime protagonist.
        """
    else:
        style_instruction = """
        Write in a captivating storytelling style suitable for US audience.
        Tone: engaging, vivid, emotional, cinematic.
        """

    prompt = f"""
    You are a professional YouTube video scriptwriter.
    {style_instruction}

    Create a complete video script for this topic: {topic}

    Return ONLY a JSON object in this exact format, nothing else:
    {{
        "title": "Video title here",
        "hook": "First 5 seconds attention grabbing line",
        "script": "Full narration script here. Should take 2-3 minutes to read aloud.",
        "scenes": [
            "Scene 1 description",
            "Scene 2 description",
            "Scene 3 description",
            "Scene 4 description",
            "Scene 5 description",
            "Scene 6 description",
            "Scene 7 description",
            "Scene 8 description"
        ],
        "call_to_action": "Subscribe and follow line at the end"
    }}

    Rules:
    - Script must be natural spoken English
    - Between 300 to 450 words total (fits 2-3 min video)
    - Exactly 8 scenes
    - Each scene description should be one clear sentence
    - US audience friendly language
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
        raw_text = result["candidates"][0]["content"]["parts"][0]["text"]

        # Clean up response - remove markdown code blocks if present
        raw_text = raw_text.strip()
        if raw_text.startswith("```"):
            raw_text = raw_text.split("```")[1]
            if raw_text.startswith("json"):
                raw_text = raw_text[4:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]

        import json
        story_data = json.loads(raw_text.strip())
        return {"success": True, "data": story_data}

    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timed out. Check your internet connection."}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"Network error: {str(e)}"}
    except (KeyError, IndexError):
        return {"success": False, "error": "Unexpected response from Gemini API."}
    except Exception as e:
        return {"success": False, "error": f"Story generation failed: {str(e)}"}


# Quick test — run this file directly to test
if __name__ == "__main__":
    print("Testing story generator...")
    result = generate_story("A boy who never gave up on his dreams", channel="ai_journey")
    if result["success"]:
        print("SUCCESS!")
        print("Title:", result["data"]["title"])
        print("Hook:", result["data"]["hook"])
        print("Scenes:", len(result["data"]["scenes"]), "scenes generated")
    else:
        print("FAILED:", result["error"])
