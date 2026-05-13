# ============================================
# T.E.J.A AI INDUSTRIES
# Configuration Settings — V1
# ============================================
# INSTRUCTIONS:
# Replace the placeholder values below with your real keys.
# Never share this file publicly or commit real keys to GitHub.
# Use GitHub Secrets for production.
# ============================================

import os

# ---- GEMINI API ----
# Get your key from: https://aistudio.google.com
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "your_gemini_api_key_here")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

# ---- GOOGLE CLOUD STORAGE ----
# Your bucket name from Google Cloud Console
GCS_BUCKET_NAME = os.environ.get("GCS_BUCKET_NAME", "your_bucket_name_here")
GCS_CREDENTIALS_FILE = "gcs_credentials.json"

# ---- VIDEO SETTINGS ----
VIDEO_FPS = 24
IMAGE_DURATION_SECONDS = 8      # How long each image shows in video
MAX_VIDEO_DURATION_SECONDS = 180  # 3 minutes max
IMAGE_WIDTH = 1280
IMAGE_HEIGHT = 720

# ---- VOICE SETTINGS ----
# American English voices for US audience
VOICE_MALE = "en-US-GuyNeural"
VOICE_FEMALE = "en-US-JennyNeural"
DEFAULT_VOICE = VOICE_FEMALE

# ---- OUTPUT PATHS ----
OUTPUT_FOLDER = "outputs"
MUSIC_FOLDER = "assets/music"

# ---- CHANNEL SETTINGS ----
CHANNEL_1_NAME = "TEJA_AI_Journey"    # Anime AI journey channel
CHANNEL_2_NAME = "TEJA_Storytelling"  # Mythology and stories channel
