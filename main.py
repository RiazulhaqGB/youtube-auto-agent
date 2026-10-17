import os, random, requests
from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip
from gtts import gTTS
from PIL import Image, ImageDraw
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

print("FIXED AGENT START - NO ERROR")

TOPIC = random.choice(["Top 5 Billionaire Habits", "AI Se Paisa Kamaye 2026"])

# Urdu script - short for test, baad me bada kar dena
urdu_script = f"Assalam o Alaikum dosto, {TOPIC} par video hai. " * 60  # 3 min ke liye, test pass hote hi *2 kar dena

# FIX 1: tld hataya - ab error nahi
print("Voice bana raha hun...")
tts = gTTS(text=urdu_script, lang='ur', slow=False)
tts.save("voice.mp3")
audio = AudioFileClip("voice.mp3")
TOTAL = audio.duration
print(f"DURATION: {TOTAL:.1f} sec")

# FIX 2: resize lambda hataya - simple clip
print("Photos bana raha hun...")
clips = []
num_clips = int(TOTAL // 8) + 1
for i in range(num_clips):
    start = i*8
    dur = min(8, TOTAL - start)
    if dur <= 0: break
    try:
        # AI Photo
        prompt = f"billionaire money success {i}"
        url = f"https://image.pollinations.ai/prompt/{prompt}?width=1280&height=720&nologo=true&seed={random.randint(1,9999)}"
        r = requests.get(url, timeout=25)
        open(f"c_{i}.jpg", "wb").write(r.content)
        clip = ImageClip(f"c_{i}.jpg", duration=dur)
        print(f"Photo {i+1} OK")
    except Exception as e:
        print(f"Photo {i+1} backup: {e}")
        img = Image.new('RGB', (1280,720), (random.randint(0,255), random.randint(0,255), 100))
        img.save(f"c_{i}.jpg")
        clip = ImageClip(f"c_{i}.jpg", duration=dur)
    
    # Simple set_start - no resize lambda
    clips.append(clip.set_start(start))

final = CompositeVideoClip(clips, size=(1280,720)).set_duration(TOTAL).set_audio(audio)
final.write_videofile("final_video.mp4", fps=24, codec='libx264', audio_codec='aac')
print("VIDEO DONE")

# Thumbnail
try:
    t_url = f"https://image.pollinations.ai/prompt/viral thumbnail {TOPIC}?width=1280&height=720"
    open("thumbnail.jpg", "wb").write(requests.get(t_url, timeout=20).content)
except:
    Image.new('RGB', (1280,720), (255,0,0)).save("thumbnail.jpg")

# Auto Upload
try:
    print("Uploading...")
    CLIENT_ID = os.getenv("YT_CLIENT_ID")
    CLIENT_SECRET = os.getenv("YT_CLIENT_SECRET")
    REFRESH_TOKEN = os.getenv("YT_REFRESH_TOKEN")
    
    if not CLIENT_ID or not CLIENT_SECRET or not REFRESH_TOKEN:
        print("SECRETS MISSING! Check GitHub Secrets")
        exit(0)

    creds = Credentials(None, refresh_token=REFRESH_TOKEN, token_uri='https://oauth2.googleapis.com/token', client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    youtube = build('youtube', 'v3', credentials=creds)
    
    req = youtube.videos().insert(
        part="snippet,status",
        body={"snippet":{"title":f"{TOPIC} Urdu","description":TOPIC,"categoryId":"27"},"status":{"privacyStatus":"public"}},
        media_body=MediaFileUpload("final_video.mp4", resumable=True)
    )
    res = req.execute()
    vid = res['id']
    print(f"UPLOADED: https://youtube.com/watch?v={vid}")
    youtube.thumbnails().set(videoId=vid, media_body=MediaFileUpload("thumbnail.jpg")).execute()
    print("DONE!")
except Exception as e:
    print(f"Upload Error (video bana hai, sirf upload fail): {e}")
