import os, asyncio, random, requests, textwrap
import edge_tts
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import *

PEXELS_KEY = os.getenv("PEXELS_API_KEY") # GitHub Secret me add karna

async def make_ai_voice(text, file="voice.mp3"):
    # Real AI Voice - Christopher - US Male
    communicate = edge_tts.Communicate(text, "en-US-ChristopherNeural")
    await communicate.save(file)
    return file

def get_topic():
    return random.choice([
        "The Shocking Truth About Deep Sleep and Your Brain",
        "Why 3 AM is The Most Dangerous Hour - Science Explained",
        "This Habit is Destroying Your Future Without You Knowing"
    ])

def get_script(topic):
    # 18 min = 2600 words
    base = f"""Today we talk about {topic}. This is very important for your life.
    Scientists discovered that your brain works in mysterious ways. If you understand this, your life will change completely.
    Let me explain in detail with real examples and scientific facts.
    """
    return base * 120 # Lamba kar diya 18 min ke liye

def download_pexels_clips(query, count=5):
    clips = []
    if not PEXELS_KEY:
        # Agar key nahi to color clips (Safe)
        for i in range(5):
            clips.append(ColorClip((1920,1080), color=(random.randint(0,40),random.randint(0,40),random.randint(20,60)), duration=220).set_fps(24))
        return clips
    # Real Pexels API
    headers = {"Authorization": PEXELS_KEY}
    r = requests.get(f"https://api.pexels.com/videos/search?query={query}&per_page={count}", headers=headers)
    # Download logic yahan ayega (abhi color se kaam chalao)
    return clips

def make_thumbnail(topic, out="thumbnail.jpg"):
    img = Image.new('RGB', (1280,720), (5,5,20))
    draw = ImageDraw.Draw(img)
    try: font = ImageFont.truetype("arial.ttf", 80)
    except: font = ImageFont.load_default()
    lines = textwrap.wrap(topic.upper(), width=18)
    y=100
    for l in lines:
        draw.text((60,y), l, fill="yellow", font=font, stroke_width=4, stroke_fill="red")
        y+=110
    img.save(out)
    return out

async def main():
    print("AGENT START")
    topic = get_topic()
    script = get_script(topic)
    print(f"Topic: {topic}")
    
    # VOICE
    await make_ai_voice(script, "voice.mp3")
    audio = AudioFileClip("voice.mp3")
    print(f"Voice Duration: {audio.duration/60:.1f} min")
    
    # VIDEO CLIPS
    bg_clips = download_pexels_clips(topic)
    # Duration ko voice ke equal karo
    final_bg = concatenate_videoclips([c.set_duration(audio.duration/len(bg_clips)) for c in bg_clips])
    
    # PHOTO PLACEMENT + TEXT
    txt = TextClip(topic, fontsize=60, color='white', stroke_color='black', stroke_width=2, method='caption', size=(1400,400))
    txt = txt.set_position('center').set_duration(audio.duration)
    
    final = CompositeVideoClip([final_bg, txt]).set_audio(audio)
    final.write_videofile("final_video.mp4", fps=24, codec='libx264')
    
    # THUMBNAIL
    make_thumbnail(topic)
    print("VIDEO + THUMBNAIL READY - 18-20 MIN")

if __name__ == "__main__":
    asyncio.run(main())
