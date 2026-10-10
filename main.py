import os, random, asyncio, textwrap
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ColorClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip
import edge_tts

async def make_voice(text):
    print("AI Voice bana raha hun...")
    comm = edge_tts.Communicate(text, "en-US-ChristopherNeural")
    await comm.save("voice.mp3")
    print("Voice Ready")
    return "voice.mp3"

def make_thumbnail(title):
    print(f"Thumbnail bana raha hun: {title}")
    img = Image.new('RGB', (1280, 720), color=(15, 15, 35))
    draw = ImageDraw.Draw(img)
    # Text - Title ke hisab se
    short = title.upper()[:30]
    try:
        # Bada font
        font = ImageFont.load_default()
        # PIL default pe bada likhne ke liye
        draw.rectangle([(0,0),(1280,720)], fill=(10,10,30))
        draw.rectangle([(10,10),(1270,710)], outline="yellow", width=8)
        lines = textwrap.wrap(short, width=15)
        y = 200
        for line in lines:
            draw.text((80, y), line, fill="yellow", font=font, stroke_width=2, stroke_fill="red")
            y+=120
        draw.text((80, y+50), "WATCH NOW!", fill="white")
    except Exception as e:
        print(f"Thumb error {e}")
    img.save("thumbnail.jpg")
    print("Thumbnail Ready: thumbnail.jpg")
    return "thumbnail.jpg"

def main_logic():
    topics = [
        "The Shocking Truth About Deep Sleep",
        "Why 3 AM Is Dangerous For Your Brain",
        "This Morning Habit Destroys Your Future"
    ]
    title = random.choice(topics)
    print(f"TOPIC LOCKED: {title}")
    
    # 18 min ke liye 2500 words
    script = f"Today we discuss {title}. " * 400
    print(f"Script Length: {len(script.split())} words")

    # Voice
    asyncio.run(make_voice(script))
    audio = AudioFileClip("voice.mp3")
    duration = audio.duration
    print(f"FINAL DURATION: {duration/60:.2f} Minutes - LOCKED!")

    # Video - No TextClip, sirf color background (Pexels key ke bina bhi chalega)
    print("Video Clips bana raha hun...")
    clip1 = ColorClip((1920,1080), color=(20,20,40), duration=duration/2)
    clip2 = ColorClip((1920,1080), color=(40,20,20), duration=duration/2)
    video = concatenate_videoclips([clip1, clip2])
    video = video.set_audio(audio)
    
    print("Final Video Render...")
    video.write_videofile("final_video.mp4", fps=24, codec='libx264', audio_codec='aac')
    
    # Thumbnail - Title ke hisab se text ke saath
    make_thumbnail(title)
    
    print("=== ALL DONE ===")
    print(f"TITLE: {title}")
    print(f"VIDEO: final_video.mp4 - {duration/60:.1f} min")
    print("THUMBNAIL: thumbnail.jpg - WITH TITLE TEXT")

if __name__ == "__main__":
    main_logic()
