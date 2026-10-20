import os
import random
import sys
import glob

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
    if isinstance(data, (tuple, list)):
        return " ".join([str(x) for x in data])
    return str(data)

try:
    print("Step 1: Generating Script...", flush=True)
    try:
        raw_script = script.generate_script(topic)
    except TypeError:
        raw_script = script.generate_script()
    final_script = to_text(raw_script)
    print(f"Script OK: {len(final_script)} chars", flush=True)
    
    with open("final_script.txt", "w", encoding="utf-8") as f:
        f.write(final_script)

    print("Step 2: Title...", flush=True)
    title_text, desc, hashtags, tags = title_gen.generate_title_and_hashtags(topic)

    print("Step 3: Voice...", flush=True)
    audio_path = None
    if hasattr(voice, 'generate_voice'):
        try:
            audio_path = voice.generate_voice(final_script)
        except TypeError:
            audio_path = voice.generate_voice()
    
    # Audio path dhundo agar function ne return nahi kiya
    if not audio_path:
        for p in ["voice.mp3", "output/voice.mp3", "audio.mp3", "final.mp3"]:
            if os.path.exists(p):
                audio_path = p
                break
    print(f"Audio path: {audio_path}", flush=True)

    print("Step 4: Images...", flush=True)
    image_paths = None
    if hasattr(images, 'generate_images'):
        try:
            image_paths = images.generate_images(final_script)
        except TypeError:
            image_paths = images.generate_images()
    
    if not image_paths:
        # Folder se images dhoondo
        image_paths = glob.glob("images/*.jpg") + glob.glob("images/*.png") + glob.glob("output/*.jpg")
    
    print(f"Images found: {len(image_paths) if image_paths else 0}", flush=True)

    print("Step 5: Video... (Final step)", flush=True)
    # Ab sahi tarike se call karo
    if hasattr(video, 'create_video'):
        try:
            video.create_video(image_paths, audio_path)
        except TypeError:
            # Agar usko 3 args chahiye to
            try:
                video.create_video(image_paths, audio_path, final_script)
            except:
                video.create_video()
    elif hasattr(video, 'generate_video'):
        video.generate_video(image_paths, audio_path)

    print("Step 6: Thumbnail...", flush=True)
    if hasattr(thumbnail, 'create_thumbnail'):
        try:
            thumbnail.create_thumbnail(title_text)
        except:
            pass

    print("Step 7: Uploading...", flush=True)
    youtube.upload_video(title_text, desc, tags)

    print("=== ALL DONE - SUCCESS ===", flush=True)

except Exception as e:
    print(f"CRITICAL ERROR: {e}", flush=True)
    import traceback
    traceback.print_exc()
    sys.exit(1)
