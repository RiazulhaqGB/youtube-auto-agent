import os, random, requests, asyncio
from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip
from PIL import Image, ImageDraw, ImageFont
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

print("FINAL MASTER CODE START")

# TOPIC
TOPIC = random.choice([
    "Top 5 Billionaire Habits That Make You Rich",
    "AI Se Paisa Kaise Kamaye 2026 Me",
    "Ameer Logon Ki Soch - Rich Mindset Secrets"
])

# 1. SCRIPT - NO REPEAT - 10 ALAG CHAPTERS
chapters = [
    f"Assalam o Alaikum dosto, World Trending Hub me khush amdeed. Aaj ki video {TOPIC} par hai jo aapki zindagi badal degi.",
    f"Dosto {TOPIC} aaj kal bohat trending me hai. Har koi ameer banna chahta hai lekin raaz kisi ko nahi pata.",
    "Pehli aadat subah 5 baje uthna. Duniya ke 90 percent billionaire subah 5 baje uthte hain. Is se din lamba aur productive hota hai.",
    "Dusri aadat roz kitab parhna. Warren Buffett roz 500 pages parhte hain. Kitab se dimag tez hota hai aur naye ideas aate hain.",
    "Teesri aadat paisa invest karna. Gareeb log paisa save karte hain, ameer log paisa invest karte hain. AI aur YouTube is waqt best investment hai.",
    "Chauthi aadat risk lena. Bina risk ke koi bara kaam nahi hota. Steve Jobs ne college chora aur Apple jaisi company banayi.",
    "Panchwi aadat consistency yani mustaqil mizaji. Roz kaam karo chahay dil kare ya na kare. Roz 1 percent behtar bano.",
    "Ek larke ki kahani suno jo YouTube automation me 3 mahine tak fail hota raha lekin usne himmat nahi haari, aaj wo mahine ka 5 lakh kama raha hai.",
    "To dosto aapko kya karna hai? Kal se subah jaldi utho, roz 30 minute kitab parho, apni income ka 10 percent invest karna shuru karo.",
    "Dosto ye 5 aadatein agar aapne apna li to 6 mahine me aapki zindagi me zameen asman ka farq aayega. Video pasand aaye to like aur subscribe zaroor karna."
]

# 7 Minute ke liye 2 bar repeat = 20 chapters
full_text = " ".join(chapters * 2)
print(f"TOPIC: {TOPIC} - Text Length: {len(full_text)}")

# 2. HASHTAGS - TOPIC KE HISAB SE AUTO
def get_hashtags(topic):
    t = topic.lower()
    if "billionaire" in t or "rich" in t or "ameer" in t:
        return ["#billionaire", "#richmindset", "#successhabits", "#motivationurdu", "#billionairemindset", "#viral"]
    elif "AI" in topic or "paisa" in t:
        return ["#ai", "#makemoneyonline", "#ai2026", "#onlineearning", "#youtubeautomation", "#trending"]
    else:
        return ["#success", "#motivation", "#mindset", "#lifelessons", "#trending", "#viral"]

hashtags_list = get_hashtags(TOPIC)
hashtags_str = " ".join(hashtags_list)
description_final = f"{TOPIC}\n\nAaj ki video me {TOPIC} ke bare me detail me baat karenge jo aapki life badal degi.\n\nVideo ko end tak dekhen!\n\n{hashtags_str}\n#youtubeauto"
tags_clean = [h.replace("#","") for h in hashtags_list]
print(f"HASHTAGS: {hashtags_str}")

# 3. VOICE - HUMAN + FALLBACK (GitHub 403 Fix)
async def make_voice():
    try:
        print("Trying Human Voice ur-PK-AsadNeural...")
        import edge_tts
        voice = "ur-PK-AsadNeural"
        communicate = edge_tts.Communicate(full_text, voice)
        await communicate.save("voice.mp3")
        print("Human Voice OK!")
    except Exception as e:
        print(f"Edge-TTS Blocked 403 ({e}), Switching to gTTS Backup...")
        from gtts import gTTS
        # gTTS me 4000 char limit
        tts = gTTS(text=full_text[:3900], lang='ur', tld='com')
        tts.save("voice.mp3")
        print("Backup gTTS Voice OK!")

asyncio.run(make_voice())

audio = AudioFileClip("voice.mp3")
TOTAL = audio.duration
print(f"VOICE READY - Duration: {TOTAL/60:.2f} min")

# 4. VIDEO CLIPS - REAL PHOTOS - NO COLOR
print("Downloading Real Photos...")
clips = []
num_clips = int(TOTAL // 6) + 1

for i in range(num_clips):
    start = i*6
    dur = min(6, TOTAL - start)
    if dur <= 0:
        break
    img_path = f"c_{i}.jpg"
    try:
        # Picsum - Real photo, kabhi block nahi hota
        url = f"https://picsum.photos/seed/{random.randint(1,999999)}/1280/720"
        r = requests.get(url, timeout=20)
        open(img_path, "wb").write(r.content)
        print(f"Clip {i+1}/{num_clips} - Real Photo OK")
    except Exception as e:
        print(f"Photo fail {e}, making backup")
        Image.new('RGB', (1280,720), (40, 40, 90)).save(img_path)
    
    clip = ImageClip(img_path, duration=dur).set_start(start)
    clips.append(clip)

final = CompositeVideoClip(clips, size=(1280,720)).set_duration(TOTAL).set_audio(audio)
final.write_videofile("final_video.mp4", fps=24, codec='libx264', audio_codec='aac')
print("VIDEO DONE - REAL PHOTOS, NO COLOR")

# 5. THUMBNAIL - CLEAN - NO TEXT
print("Making Clean Thumbnail - NO TEXT")
try:
    r = requests.get(f"https://picsum.photos/seed/{random.randint(1,999999)}/1280/720", timeout=20)
    open("thumbnail.jpg", "wb").write(r.content)
    img = Image.open("thumbnail.jpg")
    # Sirf Yellow Border - Text Bilkul Nahi
    draw = ImageDraw.Draw(img)
    draw.rectangle([0,0,1279,719], outline=(255,255,0), width=12)
    img.save("thumbnail.jpg")
    print("THUMBNAIL CLEAN - NO TEXT - VIRAL STYLE")
except Exception as e:
    print(f"Thumb error {e}")
    Image.new('RGB', (1280,720), (30,30,30)).save("thumbnail.jpg")

# 6. UPLOAD WITH HASHTAGS
try:
    print("Uploading to YouTube...")
    CLIENT_ID = os.getenv("YT_CLIENT_ID")
    CLIENT_SECRET = os.getenv("YT_CLIENT_SECRET")
    REFRESH_TOKEN = os.getenv("YT_REFRESH_TOKEN")
    
    creds = Credentials(None, refresh_token=REFRESH_TOKEN, token_uri='https://oauth2.googleapis.com/token', client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    youtube = build('youtube', 'v3', credentials=creds)
    
    req = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": TOPIC,
                "description": description_final,
                "tags": tags_clean,
                "categoryId": "27"
            },
            "status": {"privacyStatus": "public"}
        },
        media_body=MediaFileUpload("final_video.mp4", resumable=True)
    )
    res = req.execute()
    vid = res['id']
    print(f"UPLOADED SUCCESS: https://youtube.com/watch?v={vid}")
    youtube.thumbnails().set(videoId=vid, media_body=MediaFileUpload("thumbnail.jpg")).execute()
    print("THUMBNAIL UPLOADED - ALL DONE")
except Exception as e:
    print(f"Upload Error: {e}")
