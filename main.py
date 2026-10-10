print("Agent Started...")

from gtts import gTTS
from PIL import Image, ImageDraw
import textwrap, random, os
from moviepy.editor import ColorClip, AudioFileClip, concatenate_videoclips

# 1. TOPIC
topics = ["SHOCKING TRUTH ABOUT SLEEP", "3 AM DANGER EXPOSED", "YOUR MORNING HABIT IS KILLING YOU"]
title = random.choice(topics)
print(f"TITLE: {title}")

# 2. SCRIPT 18 MIN - 2500 WORDS
script = (f"This video is about {title}. Scientists have discovered something shocking. " * 250)
print(f"Words: {len(script.split())}")

# 3. VOICE - gTTS (100% Working)
print("Voice bana raha hun...")
tts = gTTS(text=script, lang='en', slow=False)
tts.save("voice.mp3")
print("Voice Done")

audio = AudioFileClip("voice.mp3")
duration = audio.duration
print(f"DURATION: {duration/60:.1f} min")

# 4. VIDEO
print("Video bana raha hun...")
c1 = ColorClip((1920,1080), color=(10,10,40), duration=duration/2)
c2 = ColorClip((1920,1080), color=(40,10,10), duration=duration/2)
video = concatenate_videoclips([c1,c2])
video = video.set_audio(audio)
video.write_videofile("final_video.mp4", fps=24, codec='libx264', audio_codec='aac')
print("Video Done: final_video.mp4")

# 5. THUMBNAIL - VIDEO KE HISAB SE TEXT KE SAATH
print("Thumbnail bana raha hun...")
img = Image.new('RGB', (1280,720), (5,5,25))
draw = ImageDraw.Draw(img)
draw.rectangle([(5,5),(1275,715)], outline="yellow", width=10)
lines = textwrap.wrap(title, width=18)
y=150
for line in lines:
    draw.text((60, y), line, fill="yellow", stroke_width=2, stroke_fill="black")
    y+=90
draw.text((60, y+30), "WATCH NOW!", fill="white")
img.save("thumbnail.jpg")
print("Thumbnail Done: thumbnail.jpg WITH TITLE")
print("=== SUCCESS ===")
