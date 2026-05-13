# ============================================
# T.E.J.A AI INDUSTRIES
# video_builder.py — V1
# Builds final video from images + voiceover
# Using MoviePy (free, open source)
# ============================================

import os
import sys
from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    concatenate_videoclips,
    CompositeAudioClip
)
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import (
    VIDEO_FPS,
    IMAGE_DURATION_SECONDS,
    IMAGE_WIDTH,
    IMAGE_HEIGHT,
    OUTPUT_FOLDER,
    MUSIC_FOLDER
)


def create_placeholder_image(scene_text, index, width=1280, height=720):
    """
    Creates a simple colored placeholder image with scene text.
    Used when actual AI image generation is not available.
    """
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Alternate background colors for visual variety
    colors = [
        (15, 25, 50),   # Dark navy
        (25, 15, 50),   # Dark purple
        (15, 40, 30),   # Dark green
        (50, 20, 15),   # Dark red
        (30, 30, 15),   # Dark yellow
        (15, 35, 50),   # Dark cyan
        (45, 15, 35),   # Dark pink
        (20, 20, 40),   # Dark blue
    ]

    bg_color = colors[index % len(colors)]
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Draw a simple border
    border_color = (100, 150, 255)
    draw.rectangle([10, 10, width-10, height-10], outline=border_color, width=3)

    # Add TEJA branding at top
    draw.text((width//2, 50), "T.E.J.A AI INDUSTRIES",
              fill=(100, 150, 255), anchor="mm")

    # Add scene number
    draw.text((width//2, height//2 - 40), f"Scene {index + 1}",
              fill=(200, 200, 200), anchor="mm")

    # Add scene description (wrap long text)
    words = scene_text.split()
    lines = []
    current_line = []
    for word in words:
        current_line.append(word)
        if len(" ".join(current_line)) > 50:
            lines.append(" ".join(current_line[:-1]))
            current_line = [word]
    if current_line:
        lines.append(" ".join(current_line))

    y_start = height//2
    for line in lines[:4]:  # Max 4 lines
        draw.text((width//2, y_start), line,
                  fill=(220, 220, 220), anchor="mm")
        y_start += 35

    img_path = os.path.join(OUTPUT_FOLDER, f"scene_{index+1:02d}.png")
    img.save(img_path)
    return img_path


def build_video(image_paths, audio_path, output_filename="teja_video.mp4", title=""):
    """
    Combines images and audio into a final MP4 video.

    image_paths: list of image file paths (in order)
    audio_path: path to the voiceover MP3 file
    output_filename: name of the output video file
    title: video title (for logging)
    Returns: dict with success status and output path
    """

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)

    try:
        # Load the audio file
        print("  Loading audio...")
        audio = AudioFileClip(audio_path)
        total_duration = audio.duration
        print(f"  Audio duration: {total_duration:.1f} seconds")

        # Calculate how long each image should show
        # Divide total audio duration evenly across all images
        num_images = len(image_paths)
        duration_per_image = total_duration / num_images
        print(f"  {num_images} images — {duration_per_image:.1f} sec each")

        # Create video clips from each image
        print("  Building image clips...")
        clips = []
        for i, img_path in enumerate(image_paths):
            if not os.path.exists(img_path):
                print(f"  Warning: Image not found: {img_path} — skipping")
                continue

            clip = ImageClip(img_path).set_duration(duration_per_image)
            clip = clip.resize((IMAGE_WIDTH, IMAGE_HEIGHT))
            clips.append(clip)
            print(f"  Clip {i+1}/{num_images} ready ✓")

        if not clips:
            return {"success": False, "error": "No valid image clips found."}

        # Join all image clips together
        print("  Joining clips...")
        final_video = concatenate_videoclips(clips, method="compose")

        # Add the voiceover audio
        final_video = final_video.set_audio(audio)

        # Write the final video file
        print("  Rendering final video... (this may take a minute)")
        final_video.write_videofile(
            output_path,
            fps=VIDEO_FPS,
            codec="libx264",
            audio_codec="aac",
            verbose=False,
            logger=None
        )

        # Check output file exists
        if os.path.exists(output_path):
            size_mb = os.path.getsize(output_path) / (1024 * 1024)
            print(f"  Video created: {output_path} ({size_mb:.1f} MB)")
            return {"success": True, "path": output_path, "duration": total_duration}
        else:
            return {"success": False, "error": "Video file was not created."}

    except Exception as e:
        return {"success": False, "error": f"Video build failed: {str(e)}"}


# Quick test
if __name__ == "__main__":
    print("Testing video builder...")

    # Create 3 test placeholder images
    test_scenes = [
        "A young engineer staring at his phone screen late at night",
        "Lines of code flowing like a river of light",
        "A rocket launching into a sky full of stars"
    ]

    print("Creating placeholder images...")
    image_paths = []
    for i, scene in enumerate(test_scenes):
        path = create_placeholder_image(scene, i)
        image_paths.append(path)
        print(f"  Image {i+1} created: {path}")

    print("\nNote: To test full video build, run main.py")
    print("Video builder loaded successfully ✓")
