import os
import random
import sys
import glob
import re
import asyncio

import script
import voice
import video
import youtube
import title as title_gen
import thumbnail
import images

print("=== AUTO YOUTUBE AGENT START - VIRAL MODE ===", flush=True)

def to_text(data):
    if isinstance(data, (tuple, list)):
        return " ".join([str(x) for x in data])
    return str(data)

def clean_script_for_voice(text):
    """Script ko voice ke liye 100% saaf karega - voice.py ko touch nahi karega"""
    print("Cleaning script for voice...", flush=True)
    # English ke fazool lafz hatao jo TTS fail karte hain
    text = re.sub(r'\b(book|word|chapter|point|topic|hook|script|video)\b', '', text, flags=re.IGNORECASE)
    # Kharab symbols hatao
    text = re.sub(r'[*#_`"“”\[\]\(\)\{\}<>|]', '', text)
    text = re.sub(r'https?://\S+', '', text)
    # Emojis hatao
    emoji_pattern = re.compile("[" u"\U0001F600-\U0001F64F" u"\U0001F300-\U0001F5FF" u"\U0001F680-\U0001F6FF" u"\U0001F1E0-\U0001F1FF" "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    return text.strip()

try:
    print("Step 1: Generating Script from TRENDING...", flush=True)
    result = script.generate_script()
    
    if isinstance(result, tuple) and len(result) == 2:
        topic, final_script = result
    else:
        final_script = to_text(result)
        topic = "Qayamat Ki Nishaniyan"

    print(f"FINAL TOPIC: {topic}", flush=True)
    print(f"Script RAW: {len(final_script)} chars", flush=True)
    
    # --- YAHAN ASAL FIX HAI ---
    final_script = clean_script_for_voice(final_script)
    print(f"Script CLEANED: {len(final_script)} chars", flush=True)
    
    if len(final_script) < 100:
        raise Exception(f"Script cleaning ke baad khali ho gaya! Original: {len(final_script)}")

    with open("final_script.txt", "w", encoding="utf-8") as f:
        f.write(final_script)

    print("Step 2: Viral Title via Gemini...", flush=True)
    # FIX: Sahi tarike se call karna hai (path, topic)
    try:
        title_text, desc, hashtags, tags = title_gen.generate_title_and_hashtags("final_script.txt", topic)
    except TypeError:
        # Agar purana title.py ho to backup
        title_text, desc, hashtags, tags = title_gen.generate_title_and_hashtags(topic)
    print(f"Title: {title_text}", flush=True)

    print("Step 3: Voice...", flush=True)
    audio_path = None
    if hasattr(voice, 'generate_voice'):
        try:
            # voice.py async hai ya sync, dono handle
            if asyncio.iscoroutinefunction(voice.generate_voice):
                audio_path = asyncio.run(voice.generate_voice(final_script))
            else:
                audio_path = voice.generate_voice(final_script)
        except TypeError:
            # Agar voice.py bina argument ke hai to file se padhega
            if asyncio.iscoroutinefunction(voice.generate_voice):
                audio_path = asyncio.run(voice.generate_voice())
            else:
                audio_path = voice.generate_voice()
    
    if not audio_path:
        for p in ["voice.mp3", "output/voice.mp3", "audio.mp3", "final.mp3", "output/final_voice.mp3"]:
            if os.path.exists(p):
                audio_path = p
                break
    
    if not audio_path or not os.path.exists(audio_path):
        raise Exception(f"Audio file nahi bani! Path check: {audio_path}")
        
    print(f"Audio path: {audio_path}", flush=True)

    print("Step 4: Images...", flush=True)
    image_paths = None
    if hasattr(images, 'generate_images'):
        try:
            image_paths = images.generate_images(final_script)
        except TypeError:
            image_paths = images.generate_images()
    
    if not image_paths:
        image_paths = glob.glob("images/*.jpg") + glob.glob("images/*.png") + glob.glob("output/*.jpg") + glob.glob("*.jpg")
    
    print(f"Images found: {len(image_paths) if image_paths else 0}", flush=True)

    print("Step 5: Video...", flush=True)
    if hasattr(video, 'create_video'):
        video.create_video(image_paths, audio_path)
    elif hasattr(video, 'generate_video'):
        video.generate_video(image_paths, audio_path)

    print("Step 6: Thumbnail...", flush=True)
    if hasattr(thumbnail, 'create_thumbnail'):
        try:
            thumbnail.create_thumbnail(title_text)
        except Exception as e:
            print(f"Thumbnail skip: {e}")

    print("Step 7: Uploading to YouTube...", flush=True)
    youtube.upload_video(title_text, desc, tags)

    print("=== ALL DONE - VIRAL SUCCESS ===", flush=True)

except Exception as e:
    print(f"CRITICAL ERROR: {e}", flush=True)
    import traceback
    traceback.print_exc()
    sys.exit(1)
