import os
import sys

# Folder ka chakkar khatam
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Agar files youtube-auto-agent folder ke andar hain to usko bhi path me daalo
for root, dirs, files in os.walk(BASE_DIR):
    if "video.py" in files:
        sys.path.insert(0, root)
        print(f"Found video.py in: {root}", flush=True)

sys.path.insert(0, BASE_DIR)
print("--- LOG START ---", flush=True)
print(f"Files in BASE: {os.listdir(BASE_DIR)}", flush=True)

from script import generate_script
from voice import generate_voice
from images import generate_images
# Ab ye error nahi dega
from video import generate_video
from youtube import upload_video
from thumbnail import generate_thumbnail
import traceback

try:
    print("1. Script bana raha hu...", flush=True)
    topic, script = generate_script()
    print(f"TOPIC: {topic}", flush=True)

    print("2. Voice bana raha hu...", flush=True)
    audio_path = generate_voice(script)
    
    print("3. Images download kar raha hu...", flush=True)
    image_paths = generate_images(topic)

    print("4. Video bana raha hu...", flush=True)
    video_path = generate_video(image_paths, audio_path)

    print("5. Thumbnail bana raha hu...", flush=True)
    thumb_path = generate_thumbnail(topic)

    print("6. YouTube pe upload kar raha hu...", flush=True)
    video_id = upload_video(video_path, thumb_path, topic, script)
    print(f"UPLOAD DONE! Video ID: {video_id}", flush=True)

except Exception as e:
    print(f"ERROR AAYA: {e}", flush=True)
    traceback.print_exc()
    sys.exit(1)

print("ALL DONE!", flush=True)
