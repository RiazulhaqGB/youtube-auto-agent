import sys
print("--- LOG START ---", flush=True)

from script import generate_script
from voice import generate_voice
from images import generate_images
from video import generate_video
from youtube import upload_video
from thumbnail import generate_thumbnail
import os
import traceback

try:
    print("1. Script bana raha hu...", flush=True)
    topic, script = generate_script()
    print(f"TOPIC: {topic}", flush=True)

    print("2. Voice bana raha hu...", flush=True)
    audio_path = generate_voice(script)
    print(f"Audio: {audio_path}", flush=True)

    print("3. Images download kar raha hu...", flush=True)
    image_paths = generate_images(topic)
    print(f"Images: {len(image_paths)} mil gayi", flush=True)

    print("4. Video bana raha hu...", flush=True)
    video_path = generate_video(image_paths, audio_path)
    print(f"Video: {video_path}", flush=True)

    print("5. Thumbnail bana raha hu...", flush=True)
    thumb_path = generate_thumbnail(topic)
    print(f"Thumb: {thumb_path}", flush=True)

    print("6. YouTube pe upload kar raha hu...", flush=True)
    video_id = upload_video(video_path, thumb_path, topic, script)
    print(f"UPLOAD DONE! Video ID: {video_id}", flush=True)

except Exception as e:
    print(f"ERROR AAYA: {e}", flush=True)
    traceback.print_exc()
    sys.exit(1)  # <-- Is se green tick nahi, red cross ayega fail hone par

print("ALL DONE!", flush=True)
