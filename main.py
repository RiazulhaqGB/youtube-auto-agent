import os
import random
import sys

# Aapki files import
import script
import voice
import video
import youtube
import title as title_gen
import thumbnail
import images

print("=== AUTO YOUTUBE AGENT START ===", flush=True)

# 1. Topic Select
topics = [
    "Zindagi Ka Asal Raaz",
    "Kamyabi Ka Wazifa",
    "Ghareebi Se Nikalne Ka Tariqa",
    "Dil Ko Sukoon Kaise Mile"
]
topic = random.choice(topics)
print(f"Topic: {topic}", flush=True)

try:
    # 2. Script Generate
    print("Step 1: Generating Script...", flush=True)
    final_script = script.generate_script(topic) if hasattr(script, 'generate_script') else topic
    
    # Save for title.py to read
    with open("final_script.txt", "w", encoding="utf-8") as f:
        f.write(str(final_script))

    # 3. Title / Hashtags Generate (Aapka wala code)
    print("Step 2: Generating Title...", flush=True)
    title_text, desc, hashtags, tags = title_gen.generate_title_and_hashtags(topic)

    # 4. Voice Generate
    print("Step 3: Generating Voice...", flush=True)
    if hasattr(voice, 'generate_voice'):
        voice.generate_voice(final_script)
    else:
        print("voice.py me function nahi mila", flush=True)

    # 5. Images Generate
    print("Step 4: Generating Images...", flush=True)
    if hasattr(images, 'generate_images'):
        images.generate_images(final_script)

    # 6. Video Generate
    print("Step 5: Generating Video... (Is me 5-7 min lagega)", flush=True)
    if hasattr(video, 'create_video'):
        video.create_video()
    elif hasattr(video, 'generate_video'):
        video.generate_video()

    # 7. Thumbnail
    print("Step 6: Generating Thumbnail...", flush=True)
    if hasattr(thumbnail, 'create_thumbnail'):
        thumbnail.create_thumbnail(title_text)

    # 8. Upload to YouTube
    print("Step 7: Uploading to YouTube...", flush=True)
    youtube.upload_video(title_text, desc, tags)

    print("=== ALL DONE, VIDEO UPLOADED ===", flush=True)

except Exception as e:
    print(f"CRITICAL ERROR: {e}", flush=True)
    import traceback
    traceback.print_exc()
    sys.exit(1)
