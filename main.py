# 12 STEPS FINAL - EDGE-TTS HUMAN VOICE - NO KEY
import os, random, textwrap, requests, time, asyncio
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import *
import edge_tts

# STEP 1: VIRAL TOPIC
VIRAL_TOPICS = ["Elon Musk Billionaire Mindset 2026","AI Will Make You Rich","7 Habits Of Millionaires","Why Poor Stay Poor"]
topic = random.choice(VIRAL_TOPICS)
title = f"{topic} | Powerful Motivation"
description = f"{topic}\n#motivation #success #money #2026\n100% AI Generated - No Copyright"
print(f"[1-4] Topic: {topic}")

# STEP 5: HUMAN VOICE - EDGE-TTS
script_template = f"Welcome to {topic}. Success is mindset. Rich people think different. Let's learn about {topic}. Step one clarity. Step two action. Step three discipline. Step four patience. Step five belief. {topic} will change your life. "
full_script = script_template * 60 # ~18 min

async def make_voice():
    communicate = edge_tts.Communicate(full_script, "en-US-GuyNeural")
    await communicate.save("voice.mp3")

print("[5] Human voice bana raha hun...")
asyncio.run(make_voice())
audio = AudioFileClip("voice.mp3")
print(f"Duration: {audio.duration/60:.1f} min")

# STEP 6: AI IMAGES - NO KEY
os.makedirs("ai_clips", exist_ok=True)
prompts = [f"{topic}, cinematic 8k", "success money luxury motivational", f"{topic} futuristic city", "millionaire lifestyle cinematic"]
image_files = []
for i,p in enumerate(prompts):
    url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(p)}?width=1280&height=720&seed={random.randint(1,99999)}&nologo=true"
    try:
        r = requests.get(url, timeout=90)
        if r.status_code==200:
            path=f"ai_clips/img_{i}.jpg"
            open(path,'wb').write(r.content)
            image_files.append(path)
            print(f"Image {i+1} OK")
        time.sleep(2)
    except: pass

if not image_files:
    img = Image.new('RGB',(1280,720),color=(0,0,0))
    ImageDraw.Draw(img).text((100,300),topic,fill=(255,255,255))
    img.save("ai_clips/f.jpg")
    image_files=["ai_clips/f.jpg"]

# STEP 7,8,11: EDIT + 18 MIN
print("[7,8,11] Editing...")
dur = audio.duration/len(image_files)
clips = [ImageClip(p,duration=dur).set_duration(dur).resize(height=720).set_position('center').resize(lambda t: 1+0.04*t) for p in image_files]
video = CompositeVideoClip(clips,size=(1280,720)).set_audio(audio).set_duration(audio.duration)
video.write_videofile("final_video.mp4",fps=24,codec='libx264',audio_codec='aac')

# STEP 12: THUMBNAIL
thumb=Image.new('RGB',(1280,720),color=(20,20,20))
draw=ImageDraw.Draw(thumb)
draw.text((50,100),textwrap.fill(topic,width=18),fill=(255,255,0))
draw.text((50,550),"WATCH NOW",fill="white")
thumb.save("thumbnail.jpg")

# STEP 9: UPLOAD (agar secrets hain to)
print("[9] Ready to upload - final_video.mp4 + thumbnail.jpg")
print("=== 12/12 DONE ===")
# STEP 9: REAL UPLOAD
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
try:
   creds = Credentials(None, 
        refresh_token=os.environ.get("YT_REFRESH_TOKEN"), 
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ.get("YT_CLIENT_ID"),
        client_secret=os.environ.get("YT_CLIENT_SECRET"),
        scopes=["https://www.googleapis.com/auth/youtube.upload"])
    youtube = build("youtube","v3",credentials=creds)
    media = MediaFileUpload("final_video.mp4", mimetype="video/mp4", resumable=True)
    req = youtube.videos().insert(part="snippet,status", body={"snippet":{"title":title[:95],"description":description,"tags":["motivation"]}, "status":{"privacyStatus":"public"}}, media_body=media)
    res = req.execute()
    print(f"VIDEO UPLOADED: https://youtu.be/{res['id']}")
    youtube.thumbnails().set(videoId=res['id'], media_body=MediaFileUpload("thumbnail.jpg")).execute()
    print("THUMBNAIL DONE")
except Exception as e:
    print(f"Upload fail: {e} - Video local me hai")
