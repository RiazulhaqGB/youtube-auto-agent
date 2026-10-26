import os, re, sys, glob, asyncio, time, random, requests, urllib.parse
import script, video, youtube, title as title_gen, thumbnail, images
from edge_tts import Communicate
from datetime import datetime
import pytz

print("=== WORLD TRENDING HUB AUTO AGENT START ===", flush=True)

CHANNEL_NAME = "World Trending Hub"
VOICE = "ur-PK-AsadNeural" # آپ والی گہری آواز
KARACHI_TZ = pytz.timezone("Asia/Karachi")

def is_retryable_error(e):
    msg = str(e).lower()
    return "503" in msg or "unavailable" in msg or "high demand" in msg or "500" in msg

def check_upload_time():
    if os.getenv("FORCE_RUN") == "true":
        print("FORCE RUN: Time check skip kar raha hu...", flush=True)
        return True
    now = datetime.now(KARACHI_TZ)
    if 8 <= now.hour <= 20:
        return True
    print(f"Abhi Karachi time {now.hour} baj rahe hain, 8AM-8PM ka wait kar raha hu...", flush=True)
    return False

# === NAYA FUNCTION: TOPIC SE IMAGE AUTO DOWNLOAD ===
def download_topic_image(query, save_path="output/topic.jpg"):
    os.makedirs("output", exist_ok=True)
    try:
        clean_query = re.sub(r'[^\w\s]', '', query) # صرف الفاظ رکھو
        clean_query = " ".join(clean_query.split()[:4]) # صرف پہلے 4 لفظ
        if not clean_query:
            clean_query = "sufi story"
        encoded = urllib.parse.quote(clean_query)
        url = f"https://source.unsplash.com/1280x720/?{encoded}"
        print(f"Downloading thumbnail image for: {clean_query}", flush=True)
        r = requests.get(url, timeout=20)
        if r.status_code == 200 and len(r.content) > 10000:
            with open(save_path, "wb") as f:
                f.write(r.content)
            print(f"Topic image saved: {save_path}", flush=True)
            return save_path
    except Exception as e:
        print(f"Topic image download failed: {e}", flush=True)
    return None

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
            # === YAHAN VOICE SLOW KI HAI ===
            # rate -15% = aap wali dusri wali sufi wali awaz jaisa
            # pitch -2Hz = awaz ko bhari karna
            text_with_pause = text.replace("۔", "۔ ... ").replace(".", ". ... ")
            comm = Communicate(text_with_pause, VOICE, rate="-15%", pitch="-2Hz", volume="+10%")
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
    print(f"Voice ko {len(chunks)} tukron me baanta", flush=True)
    temp_files = []
    for i, ch in enumerate(chunks):
        out = f"output/c_{i}.mp3"
        ok = await make_audio_safe(ch, out)
        if ok: temp_files.append(out)
    
    if not temp_files:
        raise Exception("NoAudioReceived - Edge TTS blocked")
    list_file = "output/list.txt"
    final = "output/voice.mp3"
    with open(list_file, "w", encoding="utf-8") as f:
        for tf in temp_files:
            f.write(f"file '{os.path.abspath(tf)}'\n")
    os.system(f'ffmpeg -y -f concat -safe 0 -i {list_file} -c copy {final}')
    return final

if not check_upload_time():
    print("Upload time nahi hai, exit. Cron dubara chalega.", flush=True)
    sys.exit(0)

topic = None
final_script = None
for attempt in range(5):
    try:
        print(f"Generating script... Attempt {attempt+1}/5", flush=True)
        topic, final_script = script.generate_script(channel_name=CHANNEL_NAME)
        break
    except Exception as e:
        print(f"Script Error: {e}", flush=True)
        if is_retryable_error(e) and attempt < 4:
            wait = (2 ** attempt) + random.random()
            print(f"503 Error - Gemini busy, waiting {wait:.1f}s and retrying...", flush=True)
            time.sleep(wait)
            continue
        else:
            import traceback; traceback.print_exc()
            if attempt == 4:
                sys.exit(1)
            continue

try:
    final_script = clean_text(final_script)
    with open("final_script.txt", "w", encoding="utf-8") as f: f.write(final_script)
    print(f"Script OK: {len(final_script.split())} words | Topic: {topic}", flush=True)

    for attempt in range(3):
        try:
            title_text, desc, hashtags, tags = title_gen.generate_title_and_hashtags("final_script.txt", topic, channel_name=CHANNEL_NAME)
            break
        except Exception as e:
            if is_retryable_error(e) and attempt < 2:
                print(f"Title 503, retrying {attempt+1}...", flush=True)
                time.sleep(3)
                continue
            raise e

    audio_path = asyncio.run(generate_final_voice(final_script))
    print(f"FINAL AUDIO: {os.path.getsize(audio_path)} bytes", flush=True)

    image_paths = images.generate_images(topic, num_images=6)
    
    # === THUMBNAIL AUTO IMAGE LOGIC ===
    topic_thumb_img = download_topic_image(topic, "output/topic.jpg")
    if topic_thumb_img and os.path.exists(topic_thumb_img):
        thumb_path = thumbnail.generate_thumbnail(title_text, [topic_thumb_img])
    else:
        thumb_path = thumbnail.generate_thumbnail(title_text, image_paths)

    result = youtube.upload_video(title_text, desc, tags, thumb_path)
    
    with open("last_upload.txt","w") as f:
        f.write(f"{result['id']},{int(time.time())},{topic}")
    print("=== DONE ===", flush=True)

except Exception as e:
    print(f"CRITICAL ERROR: {e}", flush=True)
    import traceback; traceback.print_exc(); sys.exit(1)
