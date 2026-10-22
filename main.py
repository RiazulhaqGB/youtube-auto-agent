import os
import re
import sys
import glob
import asyncio
import shutil

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
    print("Cleaning script for voice...", flush=True)
    text = re.sub(r'[*#_`"“”\[\]\(\)\{\}<>|]', '', text)
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'\b(book|word|chapter|topic|point|hook|script|video)\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    return text.strip()

def split_for_voice(text, max_len=850):
    sentences = re.split(r'(?<=[۔؟!.])\s+', text)
    chunks = []
    cur = ""
    for s in sentences:
        if len(cur) + len(s) < max_len:
            cur += " " + s
        else:
            if cur.strip():
                chunks.append(cur.strip())
            cur = s
    if cur.strip():
        chunks.append(cur.strip())
    return [c for c in chunks if len(c) > 20]

try:
    print("Step 1: Generating Script...", flush=True)
    result = script.generate_script()
    if isinstance(result, tuple) and len(result) == 2:
        topic, final_script = result
    else:
        final_script = to_text(result)
        topic = "Qayamat Ki Nishaniyan"

    final_script = clean_script_for_voice(final_script)
    print(f"FINAL TOPIC: {topic}", flush=True)
    print(f"Script CLEANED: {len(final_script)} chars, {len(final_script.split())} words", flush=True)
    
    if len(final_script) < 100:
        raise Exception("Script empty after cleaning!")

    with open("final_script.txt", "w", encoding="utf-8") as f:
        f.write(final_script)

    print("Step 2: Viral Title...", flush=True)
    try:
        title_text, desc, hashtags, tags = title_gen.generate_title_and_hashtags("final_script.txt", topic)
    except TypeError:
        title_text, desc, hashtags, tags = title_gen.generate_title_and_hashtags(topic)
    print(f"Title: {title_text}", flush=True)

    print("Step 3: Voice - Chunking Mode (voice.py untouched)...", flush=True)
    os.makedirs("output", exist_ok=True)
    chunks = split_for_voice(final_script, 850)
    print(f"Split into {len(chunks)} small chunks", flush=True)
    
    temp_audios = []
    for i, ch in enumerate(chunks):
        print(f"Generating voice chunk {i+1}/{len(chunks)} - {len(ch)} chars", flush=True)
        try:
            if asyncio.iscoroutinefunction(voice.generate_voice):
                audio_path = asyncio.run(voice.generate_voice(ch))
            else:
                audio_path = voice.generate_voice(ch)
        except TypeError:
            # agar voice.py argument nahi leta to hum final_script.txt overwrite karke call karenge
            with open("final_script.txt", "w", encoding="utf-8") as f:
                f.write(ch)
            if asyncio.iscoroutinefunction(voice.generate_voice):
                audio_path = asyncio.run(voice.generate_voice())
            else:
                audio_path = voice.generate_voice()
        
        # voice.py ne jahan bhi file banayi usko pakro
        if not audio_path or not os.path.exists(audio_path):
            for p in ["voice.mp3", "output/voice.mp3", "audio.mp3", "final.mp3", "output/final_voice.mp3"]:
                if os.path.exists(p):
                    audio_path = p
                    break
        
        if not audio_path or not os.path.exists(audio_path):
            raise Exception(f"Chunk {i} audio not created!")

        chunk_out = f"output/chunk_{i}.mp3"
        shutil.copy(audio_path, chunk_out)
        temp_audios.append(chunk_out)
        print(f"Chunk {i+1} saved: {chunk_out}", flush=True)

    # Merge all chunks
    list_file = "output/concat_list.txt"
    final_audio = "output/voice.mp3"
    with open(list_file, "w", encoding="utf-8") as lf:
        for tf in temp_audios:
            lf.write(f"file '{os.path.abspath(tf)}'\n")
    
    os.system(f'ffmpeg -y -f concat -safe 0 -i {list_file} -c copy {final_audio}')
    
    if not os.path.exists(final_audio):
        raise Exception("Final voice merge failed!")
    
    print(f"FINAL AUDIO READY: {final_audio} - {os.path.getsize(final_audio)} bytes", flush=True)
    audio_path = final_audio

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
