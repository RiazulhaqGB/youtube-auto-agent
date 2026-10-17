import os, random, requests, time
from moviepy.editor import *
from gtts import gTTS
from PIL import Image, ImageDraw
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

print("START - URDU VOICE + REAL CLIPS")

TOPIC = random.choice(["Top 5 Billionaire Habits", "AI Se Paisa Kaise Kamaye 2026", "Ameer Logon Ki Soch"])

# 8 MIN KA URDU SCRIPT - 2 BAR REPEAT SE 8 MIN PAKKA
urdu_script = f"""
Assalam o Alaikum dosto, World Trending Hub me khush amdeed.
Aaj ki video {TOPIC} par hai. Ye video aapki zindagi badal sakti hai.

Chapter 1: Dosto {TOPIC} aaj kal bohat viral hai. Har banda ameer banna chahta hai. Lekin ameer banne ka raaz kya hai?

Chapter 2: Pehli aadat, subah 5 baje uthna. Duniya ke 90 percent billionaire subah 5 baje uthte hain. Early to bed early to rise.

Chapter 3: Dusri aadat, roz kitab parhna. Elon Musk, Bill Gates roz ek ghanta kitab parhte hain. Kitab se dimag tez hota hai.

Chapter 4: Teesri aadat, paisa invest karna. Gareeb log paisa save karte hain, ameer log invest karte hain. AI aur YouTube me invest karo.

Chapter 5: Chauthi aadat, risk lena. Bina risk ke koi bara kaam nahi hota. Steve Jobs ne risk liya aur Apple banaya.

Chapter 6: Panchwi aadat, consistency. Roz kaam karo, chahay dil kare ya na kare. Yehi kamyabi ki kunji hai.

Chapter 7: Ek larke ki kahani, usne YouTube automation shuru kiya, 3 mahine kuch nahi mila, lekin himmat nahi haari, aaj 5 lakh kama raha hai.

Chapter 8: Aap kya karein? Subah jaldi utho, roz 30 minute kitab parho, income ka 10 percent invest karo, aur ek naya skill seekho.

Chapter 9: Dosto agar aapne ye 5 aadatein apna li to 6 mahine me aap khud me farq dekhenge. Kamyabi raat o raat nahi milti.

Chapter 10: Video pasand aayi to subscribe karo, bell dabao, comment me likho kaunsi aadat aaj se shuru kar rahe ho. Allah Hafiz.
"""
# Double kar diya taake 8 min ho
full_script = urdu_script * 2

# 1. URDU VOICE
print("URDU VOICE BANA RAHA HUN...")
tts = gTTS(text=full_script, lang='ur', slow=False, tld='com.pk') # com.pk se sahi urdu
tts.save("voice.mp3")
audio = AudioFileClip("voice.mp3")
TOTAL = audio.duration
print(f"VOICE DURATION: {TOTAL/60:.1f} MIN - URDU ME")

# 2. REAL AI PHOTO CLIPS - HAR 6 SEC PE NAYI PHOTO
print("AI PHOTOS BANA RAHA HUN - REAL CLIPS...")
clips = []
# 8 min = 80 clips, lekin time bachane ke liye har 8 sec pe clip
num_clips = int(TOTAL // 8) + 1

prompts = [
    f"billionaire lifestyle, {TOPIC}, luxury, money, success",
    f"young man reading book, success mindset, library",
    f"investing in AI, stock market, futuristic business",
    f"risk taking businessman, motivation, mountain top",
    f"consistency, hard work, gym, discipline, 8k",
    f"youtube automation, money from laptop, pakistani boy",
    f"morning routine 5am, sunrise, billionaire waking up",
    f"success, luxury car, dubai, money rain"
]

for i in range(num_clips):
    start = i*8
    dur = min(8, TOTAL - start)
    if dur <= 0: break
    
    try:
        # FREE AI PHOTO - Pollinations
        p_prompt = random.choice(prompts)
        img_url = f"https://image.pollinations.ai/prompt/{p_prompt}?width=1280&height=720&nologo=true&seed={random.randint(1,99999)}"
        r = requests.get(img_url, timeout=20)
        open(f"clip_{i}.jpg", "wb").write(r.content)
        print(f"Photo {i+1}/{num_clips} OK")
        clip = ImageClip(f"clip_{i}.jpg", duration=dur)
    except:
        # Backup agar net slow ho
        color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        img = Image.new('RGB', (1280,720), color)
        ImageDraw.Draw(img).text((50,300), f"{TOPIC} Part {i+1}", fill="white")
        img.save(f"clip_{i}.jpg")
        clip = ImageClip(f"clip_{i}.jpg", duration=dur)

    # Zoom Effect - Video jaisa lagega
    clip = clip.resize(lambda t: 1 + 0.04*t).set_position('center').set_start(start)
    clips.append(clip)

final = CompositeVideoClip(clips, size=(1280,720)).set_duration(TOTAL).set_audio(audio)
final.write_videofile("final_video.mp4", fps=24, codec='libx264')
print("VIDEO WITH PHOTOS READY!")

# 3. AI THUMBNAIL
try:
    thumb_prompt = f"viral youtube thumbnail {TOPIC}, shocked face, money, MrBeast style, bright"
    thumb_url = f"https://image.pollinations.ai/prompt/{thumb_prompt}?width=1280&height=720&nologo=true"
    open("thumbnail.jpg", "wb").write(requests.get(thumb_url, timeout=30).content)
    img = Image.open("thumbnail.jpg")
    draw = ImageDraw.Draw(img)
    draw.rectangle([0,0,1279,719], outline=(255,255,0), width=15)
    draw.rectangle([0,0,1280,150], fill=(200,0,0))
    draw.text((20,30), TOPIC.upper(), fill="white")
    img.save("thumbnail.jpg")
except:
    pass

# 4. AUTO UPLOAD (TUMHARE 4 SECRETS)
try:
    CLIENT_ID = os.getenv("YT_CLIENT_ID")
    CLIENT_SECRET = os.getenv("YT_CLIENT_SECRET")
    REFRESH_TOKEN = os.getenv("YT_REFRESH_TOKEN")
    creds = Credentials(None, refresh_token=REFRESH_TOKEN, token_uri='https://oauth2.googleapis.com/token', client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    youtube = build('youtube', 'v3', credentials=creds)
    req = youtube.videos().insert(
        part="snippet,status",
        body={"snippet":{"title":f"{TOPIC} | Urdu Motivation","description":f"{TOPIC} full urdu video","categoryId":"27"},"status":{"privacyStatus":"public"}},
        media_body=MediaFileUpload("final_video.mp4")
    )
    res = req.execute()
    vid = res['id']
    youtube.thumbnails().set(videoId=vid, media_body=MediaFileUpload("thumbnail.jpg")).execute()
    print(f"UPLOADED: https://youtube.com/watch?v={vid}")
except Exception as e:
    print(f"Upload error: {e}")
