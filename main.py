import os
import random
import sys

import script
import voice
import video
import youtube
import title as title_gen
import thumbnail
import images

print("=== AUTO YOUTUBE AGENT START ===", flush=True)

topics = ["Zindagi Ka Asal Raaz", "Kamyabi Ka Wazifa", "Ghareebi Se Nikalne Ka Tariqa"]
topic = random.choice(topics)
print(f"Topic: {topic}", flush=True)

def to_text(data):
    # tuple / list ko string me badlo
    if isinstance(data, (tuple, list)):
        return " ".join([str(x) for x in data])
    return str(data)

try:
    print("Step 1: Generating Script...", flush=True)
    if hasattr(script, 'generate_script'):
        try:
            raw_script = script.generate_script(topic)
        except TypeError:
            raw_script = script.generate_script()
    else:
        raw_script = topic
    
    final_script = to_text(raw_script)
    print(f"Script length: {len(final_script)} chars", flush=True)
    
    with open("final_script.txt", "w", encoding="utf-8") as f:
        f.write(final_script)

    print("Step 2: Generating Title...", flush=True)
    title_text, desc, hashtags, tags = title_gen.generate_title_and_hashtags(topic)

    print("Step 3: Generating Voice...", flush=True)
    if hasattr(voice, 'generate_voice'):
        try:
            voice.generate_voice(final_script)
        except TypeError:
            voice.generate_voice()

    print("Step 4: Generating Images...", flush=True)
    if hasattr(images, 'generate_images'):
        try:
            images.generate_images(final_script)
        except TypeError:
            images.generate_images()

    print("Step 5: Generating Video...", flush=True)
    if hasattr(video, 'create_video'):
        video.create_video()
    elif hasattr(video, 'generate_video'):
        video.generate_video()

    print("Step 6: Thumbnail...", flush=True)
    if hasattr(thumbnail, 'create_thumbnail'):
        try:
            thumbnail.create_thumbnail(title_text)
        except:
            try:
                thumbnail.create_thumbnail()
            except:
                pass

    print("Step 7: Uploading...", flush=True)
    youtube.upload_video(title_text, desc, tags)

    print("=== ALL DONE ===", flush=True)

except Exception as e:
    print(f"CRITICAL ERROR: {e}", flush=True)
    import traceback
    traceback.print_exc()
    sys.exit(1)
