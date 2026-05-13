# ============================================
# T.E.J.A AI INDUSTRIES
# cloud_uploader.py — V1
# Uploads finished video to Google Cloud Storage
# ============================================

import os
import sys
from google.cloud import storage

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import GCS_BUCKET_NAME, GCS_CREDENTIALS_FILE


def upload_to_cloud(local_file_path, destination_filename=None):
    """
    Uploads a local file to Google Cloud Storage bucket.

    local_file_path: path to the file on your device
    destination_filename: name to save as in cloud (optional)
    Returns: dict with success status and public URL
    """

    if not os.path.exists(local_file_path):
        return {"success": False, "error": f"File not found: {local_file_path}"}

    # Use original filename if no destination given
    if destination_filename is None:
        destination_filename = os.path.basename(local_file_path)

    try:
        # Connect to Google Cloud Storage
        if os.path.exists(GCS_CREDENTIALS_FILE):
            client = storage.Client.from_service_account_json(GCS_CREDENTIALS_FILE)
        else:
            # Uses environment variable GOOGLE_APPLICATION_CREDENTIALS
            client = storage.Client()

        bucket = client.bucket(GCS_BUCKET_NAME)
        blob = bucket.blob(destination_filename)

        print(f"  Uploading {os.path.basename(local_file_path)} to cloud...")
        blob.upload_from_filename(local_file_path)

        # Make the file publicly accessible
        blob.make_public()
        public_url = blob.public_url

        file_size_mb = os.path.getsize(local_file_path) / (1024 * 1024)
        print(f"  Uploaded successfully! ({file_size_mb:.1f} MB)")
        print(f"  Public URL: {public_url}")

        return {"success": True, "url": public_url, "filename": destination_filename}

    except Exception as e:
        return {"success": False, "error": f"Upload failed: {str(e)}"}


def list_cloud_videos():
    """Lists all video files stored in your cloud bucket."""
    try:
        if os.path.exists(GCS_CREDENTIALS_FILE):
            client = storage.Client.from_service_account_json(GCS_CREDENTIALS_FILE)
        else:
            client = storage.Client()

        bucket = client.bucket(GCS_BUCKET_NAME)
        blobs = bucket.list_blobs()

        videos = []
        for blob in blobs:
            if blob.name.endswith(".mp4"):
                videos.append({
                    "name": blob.name,
                    "size_mb": round(blob.size / (1024 * 1024), 1),
                    "url": blob.public_url
                })

        return {"success": True, "videos": videos, "count": len(videos)}

    except Exception as e:
        return {"success": False, "error": str(e)}


# Quick test
if __name__ == "__main__":
    print("Testing cloud uploader...")
    print("Listing existing videos in bucket...")
    result = list_cloud_videos()
    if result["success"]:
        print(f"Found {result['count']} videos in cloud storage")
        for v in result["videos"]:
            print(f"  - {v['name']} ({v['size_mb']} MB)")
    else:
        print("Could not connect:", result["error"])
        print("Make sure GCS credentials are set up correctly.")
