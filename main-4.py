# ============================================
# T.E.J.A AI INDUSTRIES
# main.py — V1 Master Controller
# Runs the full video generation pipeline
# ============================================

import os
import sys
import json
from datetime import datetime

# Import all engine modules
from engine.story_generator import generate_story
from engine.image_prompt_generator import generate_image_prompts
from engine.voice_generator import generate_voiceover
from engine.video_builder import build_video, create_placeholder_image
from engine.cloud_uploader import upload_to_cloud
from config.settings import OUTPUT_FOLDER


def teja_header():
    print("\n" + "="*50)
    print("   T.E.J.A AI INDUSTRIES")
    print("   Technology for Evolution Journey of Ascension")
    print("   Video Engine V1")
    print("="*50 + "\n")


def run_pipeline(topic, channel="storytelling", style="cinematic"):
    """
    Full pipeline: topic → finished video uploaded to cloud.

    topic: your video idea in plain text
    channel: "storytelling" or "ai_journey"
    style: "cinematic", "anime", "realistic"
    """

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"\n[ TEJA ENGINE ] Starting pipeline at {timestamp}")
    print(f"Topic   : {topic}")
    print(f"Channel : {channel}")
    print(f"Style   : {style}\n")

    # ── STEP 1: Generate story and script ──────────────────
    print("[ STEP 1/5 ] Generating story and script...")
    story_result = generate_story(topic, channel=channel)

    if not story_result["success"]:
        print("FAILED at Step 1:", story_result["error"])
        return False

    story = story_result["data"]
    print(f"  Title: {story['title']}")
    print(f"  Scenes: {len(story['scenes'])} scenes")
    print("  Step 1 complete ✓\n")

    # ── STEP 2: Generate image prompts ─────────────────────
    print("[ STEP 2/5 ] Generating image prompts...")
    prompts_result = generate_image_prompts(story["scenes"], style=style)

    if not prompts_result["success"]:
        print("FAILED at Step 2:", prompts_result["error"])
        return False

    print("  Step 2 complete ✓\n")

    # ── STEP 3: Generate voiceover audio ───────────────────
    print("[ STEP 3/5 ] Generating voiceover...")
    full_script = f"{story['hook']} {story['script']} {story['call_to_action']}"
    audio_filename = f"voice_{timestamp}.mp3"

    voice_result = generate_voiceover(full_script, audio_filename)

    if not voice_result["success"]:
        print("FAILED at Step 3:", voice_result["error"])
        return False

    print("  Step 3 complete ✓\n")

    # ── STEP 4: Create images and build video ──────────────
    print("[ STEP 4/5 ] Building video...")

    # Create placeholder images for each scene
    # (Replace this section later with real AI image generation)
    image_paths = []
    for i, scene in enumerate(story["scenes"]):
        img_path = create_placeholder_image(scene, i)
        image_paths.append(img_path)

    video_filename = f"teja_{channel}_{timestamp}.mp4"
    video_result = build_video(
        image_paths,
        voice_result["path"],
        video_filename,
        title=story["title"]
    )

    if not video_result["success"]:
        print("FAILED at Step 4:", video_result["error"])
        return False

    duration = round(video_result["duration"], 1)
    print(f"  Video duration: {duration} seconds")
    print("  Step 4 complete ✓\n")

    # ── STEP 5: Upload to Google Cloud ─────────────────────
    print("[ STEP 5/5 ] Uploading to Google Cloud Storage...")
    upload_result = upload_to_cloud(video_result["path"], video_filename)

    if not upload_result["success"]:
        # Upload failed but video was still created locally
        print(f"  Upload warning: {upload_result['error']}")
        print(f"  Video saved locally at: {video_result['path']}")
    else:
        print(f"  Cloud URL: {upload_result['url']}")
        print("  Step 5 complete ✓\n")

    # ── SUMMARY ───────────────────────────────────────────
    print("\n" + "="*50)
    print("  PIPELINE COMPLETE!")
    print(f"  Title    : {story['title']}")
    print(f"  Duration : {duration} seconds")
    print(f"  File     : {video_filename}")
    if upload_result["success"]:
        print(f"  URL      : {upload_result['url']}")
    print("="*50 + "\n")

    # Save a log of this video
    log_entry = {
        "timestamp": timestamp,
        "topic": topic,
        "title": story["title"],
        "channel": channel,
        "duration": duration,
        "filename": video_filename,
        "url": upload_result.get("url", "local only")
    }

    log_path = os.path.join(OUTPUT_FOLDER, "video_log.json")
    logs = []
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            try:
                logs = json.load(f)
            except:
                logs = []
    logs.append(log_entry)
    with open(log_path, "w") as f:
        json.dump(logs, f, indent=2)

    return True


def main():
    teja_header()

    print("Choose channel:")
    print("1. Storytelling (Mythology / Motivation)")
    print("2. AI Journey (Anime style — your story)")

    choice = input("\nEnter 1 or 2: ").strip()

    if choice == "1":
        channel = "storytelling"
        style = "cinematic"
    elif choice == "2":
        channel = "ai_journey"
        style = "anime"
    else:
        print("Invalid choice. Defaulting to storytelling.")
        channel = "storytelling"
        style = "cinematic"

    topic = input("\nEnter your video topic or idea:\n> ").strip()

    if not topic:
        print("No topic entered. Exiting.")
        return

    success = run_pipeline(topic, channel=channel, style=style)

    if success:
        print("Your video is ready! Go post it. 🚀")
    else:
        print("Pipeline failed. Check the errors above and try again.")


if __name__ == "__main__":
    main()
