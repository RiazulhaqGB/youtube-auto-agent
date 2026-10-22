import os, re, sys, glob, asyncio, shutil, time
import script
import video, youtube, title as title_gen, thumbnail, images
from edge_tts import Communicate

print("=== AUTO AGENT START - FIXED MODE ===", flush=True)

VOICE = "ur-PK-AsadNeural" # Tumhari voice yahi hai, change nahi ki

def clean_text(text):
    text = re.sub(r'[*#_`"“”\[\]\(\)\{\}<>|@]', '', text)
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def split_chunks(text, max_len=700):
    sentences = re.split(r'(?<=[۔؟!.!\n])\s+', text)
    chunks, cur = [], ""
    for s in sentences:
        if len(cur) + len(s) < max_len:
            cur += " " + s
        else:
            if cur: chunks.append(cur.strip())
            cur = s
    if cur: chunks.append(cur.strip())
    return [c for c in chunks if len(c) > 10]

async def make_audio_safe(text, out_path):
    for attempt in range(3):
        try:
            comm = Communicate(text, VOICE)
            await comm.save(out_path)
            if os.path.exists(out_path) and os.path.getsize(out_path) > 2000:
                return True
        except Exception as e:
            print(f"TTS Retry {attempt+1} failed: {e}", flush=True)
            await asyncio.sleep(2)
    return False

async def generate_final_voice(full_text):
    os.makedirs("output", exist_ok=True)
    chunks = split_chunks(full_text, 700)
    print(f"Voice ko {len(chunks)} tukron me baanta: {len(full_text)} chars", flush=True)
    temp_files = []
    for i, ch in enumerate(chunks):
        out = f"output/c_{i}.mp3"
        ok = await make_audio_safe(ch, out)
        if ok:
            temp_files.append(out)
            print(f"Chunk {i+1}/{len(chunks)} OK", flush=True)
        else:
            print(f"Chunk {i+1} SKIP - NoAudio", flush=True)
    
    if not temp_files:
        raise Exception("NoAudioReceived - Sab chunks fail, Edge TTS blocked")

    list_file = "output/list.txt"
    final = "output/voice.mp3"
    with open(list_file, "w", encoding="utf-8") as f:
        for tf in temp_files:
            f.write(f"file '{os.path.abspath(tf)}'\n")
    os.system(f'ffmpeg -y -f concat -safe 0 -i {list_file} -c copy {final}')
    return final

# --- MAIN FLOW ---
try:
    result = script.generate_script()
    if isinstance(result, tuple): topic, final_script = result
    else: final_script = str(result); topic = "Qayamat Ki Nishaniyan"

    final_script = clean_text(final_script)
    with open("final_script.txt", "w", encoding="utf-8") as f: f.write(final_script)
    print(f"Script OK: {len(final_script.split())} words", flush=True)

    title_text, desc, hashtags, tags = title_gen.generate_title_and_hashtags("final_script.txt", topic)

    # VOICE FIX - voice.py ko call nahi kar rahe, direct robust function
    audio_path = asyncio.run(generate_final_voice(final_script))
    print(f"FINAL AUDIO: {audio_path} {os.path.getsize(audio_path)} bytes", flush=True)

    image_paths = images.generate_images(final_script) if hasattr(images, 'generate_images') else glob.glob("images/*.jpg")
    video.create_video(image_paths, audio_path)
    thumbnail.create_thumbnail(title_text)
    youtube.upload_video(title_text, desc, tags)
    print("=== DONE ===", flush=True)

except Exception as e:
    print(f"CRITICAL ERROR: {e}", flush=True)
    import traceback; traceback.print_exc(); sys.exit(1)
