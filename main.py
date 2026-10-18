import os, random, requests, asyncio, textwrap, sys
from PIL import Image, ImageDraw, ImageFont
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

print("FINAL REAL AI AGENT - FULL READY")

CLIENT_ID = os.getenv("YT_CLIENT_ID")
CLIENT_SECRET = os.getenv("YT_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("YT_REFRESH_TOKEN")
creds = Credentials(None, refresh_token=REFRESH_TOKEN, token_uri='https://oauth2.googleapis.com/token', client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
youtube = build('youtube', 'v3', credentials=creds)

# STEP 1: WORLD TRENDING
world_topics = []
for region in ["US", "GB", "IN", "PK", "DE"]:
    try:
        res = youtube.videos().list(part="snippet", chart="mostPopular", regionCode=region, maxResults=8).execute()
        for item in res.get('items', []):
            t = item['snippet']['title']
            if len(t) > 15 and "music" not in t.lower():
                world_topics.append(t)
    except: pass

TOPIC = random.choice(world_topics) if world_topics else "World Breaking News Today"
TOPIC = TOPIC.replace("|","-").replace("#","")[:90]
print(f"TOPIC: {TOPIC}")

# STEP 2: REAL AI ONLY - NO FALLBACK TEMPLATE
def real_ai_writer(topic):
    print("Calling REAL AI...")
    for attempt in range(3):
        try:
            prompt = f"Write a detailed 800-word viral YouTube news script in Urdu Roman about: {topic}. Make it 100% unique, engaging, 12 paragraphs, no repeat, include background, reasons why viral, future impact, call to action. Start with Assalam o Alaikum dosto. Language: Urdu Roman + some English."
            url = f"https://text.pollinations.ai/{requests.utils.quote(prompt)}?model=openai&seed={random.randint(1,9999999)}"
            r = requests.get(url, timeout=60)
            if r.status_code == 200 and len(r.text) > 400:
                print(f"REAL AI SCRIPT RECEIVED on attempt {attempt+1}!")
                return r.text[:5000]
        except Exception as e:
            print(f"AI try {attempt+1} fail {e}")
            continue
    print("AI FAILED 3 TIMES - STOPPING")
    raise Exception("Real AI failed - Please retry workflow")

full_text = real_ai_writer(TOPIC)
print(f"SCRIPT LENGTH: {len(full_text)}")

# STEP 3: TITLE DESC
title_final = f"{TOPIC} | World Trending Today"
desc_final = f"{title_final}\n\n{full_text[:500]}\n\n#Trending #Viral #BreakingNews"

# STEP 4: VOICE - EDGE-TTS WITH GTTS FALLBACK (NO MORE 403 ERROR)
async def make_voice_edge(text):
    import edge_tts
    communicate = edge_tts.Communicate(text, "ur-PK-AsadNeural", rate="-15%", pitch="-5Hz")
    await communicate.save("voice.mp3")

async def make_voice():
    try:
        print("Trying Edge-TTS Asad voice...")
        await asyncio.wait_for(make_voice_edge(full_text), timeout=40)
        print("Edge-TTS VOICE DONE")
    except Exception as e:
        print(f"Edge-TTS failed 403, switching to gTTS: {e}")
        from gtts import gTTS
        # gTTS fallback - kabhi fail nahi hota
        tts = gTTS(text=full_text, lang='ur', slow=False)
        tts.save("voice.mp3")
        print("gTTS VOICE DONE - BACKUP")

asyncio.run(make_voice())

asyncio.run(make_voice())

from moviepy.editor import AudioFileClip, ImageClip, CompositeVideoClip
audio = AudioFileClip("voice.mp3")
TOTAL = audio.duration

# STEP 5: VIDEO CLIPS - FIXED NO BACKEND ERROR
clips = []
num_clips = int(TOTAL // 4) + 1
for i in range(num_clips):
    start = i*4
    dur = min(4, TOTAL-start)
    if dur <= 0: break
    img_path = f"c_{i}.jpg"
    # Try download, agar fail to solid color image
    try:
        url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(TOPIC + ' news cinematic')}?width=1280&height=720&seed={random.randint(1,9999999)}&nologo=true"
        r = requests.get(url, timeout=25)
        if r.status_code==200 and len(r.content) > 8000:
            open(img_path,"wb").write(r.content)
            # Verify image is valid
            Image.open(img_path).verify()
        else:
            raise Exception("Small file")
    except:
        # Fallback - valid jpg bana dega, kabhi error nahi ayega
        img = Image.new('RGB',(1280,720),(random.randint(10,50), random.randint(10,50), random.randint(10,50)))
        d = ImageDraw.Draw(img)
        try:
            f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 50)
        except:
            f = ImageFont.load_default()
        d.text((100,300), TOPIC[:40], fill=(255,255,255), font=f)
        img.save(img_path, "JPEG")
        print(f"Fallback image created {img_path}")
    
    clips.append(ImageClip(img_path, duration=dur).set_start(start))

final = CompositeVideoClip(clips, size=(1280,720)).set_duration(TOTAL).set_audio(audio)
final.write_videofile("final_video.mp4", fps=24, codec='libx264', audio_codec='aac', logger=None)
print("VIDEO RENDERED")

# STEP 6: THUMBNAIL WITH TEXT
try:
    url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(TOPIC + ' dramatic breaking news')}?width=1280&height=720&seed={random.randint(1,9999999)}&nologo=true"
    r = requests.get(url, timeout=25)
    open("thumbnail.jpg","wb").write(r.content)
    img = Image.open("thumbnail.jpg").convert("RGB")
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 62)
        small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 38)
    except:
        font = ImageFont.load_default(); small = font
    draw.rectangle([0,500,1280,720], fill=(0,0,0))
    draw.rectangle([0,0,1279,719], outline=(255,255,0), width=10)
    draw.text((30,505), "WORLD TRENDING!", fill=(255,255,0), font=small)
    draw.text((30,550), textwrap.fill(TOPIC[:45], width=20), fill=(255,255,255), font=font, stroke_width=3, stroke_fill=(0,0,0))
    img.save("thumbnail.jpg")
    print("THUMBNAIL DONE")
except Exception as e:
    print(f"Thumb fail {e}")
    Image.new('RGB',(1280,720),(255,0,0)).save("thumbnail.jpg")

# STEP 7: UPLOAD
req = youtube.videos().insert(part="snippet,status", body={"snippet":{"title":title_final[:95],"description":desc_final,"tags":TOPIC.split()[:8],"categoryId":"25"},"status":{"privacyStatus":"public"}}, media_body=MediaFileUpload("final_video.mp4", resumable=True))
res = req.execute()
vid = res['id']
youtube.thumbnails().set(videoId=vid, media_body=MediaFileUpload("thumbnail.jpg")).execute()
print(f"DONE https://youtube.com/watch?v={vid}")
