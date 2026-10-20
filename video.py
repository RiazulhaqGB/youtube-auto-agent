from moviepy.editor import *
import os
import re
import random
# Pillow fix
from PIL import Image
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.LANCZOS

# --- Script se keywords nikal ke relevant image prompt banao ---
def get_image_keywords_from_script(script_path="script.txt"):
    keywords = []
    try:
        # script.txt ya script file dhoondo
        text = ""
        if os.path.exists(script_path):
            with open(script_path, 'r', encoding='utf-8') as f:
                text = f.read().lower()
        elif os.path.exists("final_script.txt"):
            with open("final_script.txt", 'r', encoding='utf-8') as f:
                text = f.read().lower()
        else:
            # Agar file nahi to env se topic le lo
            text = os.getenv("LAST_TOPIC", "").lower()

        print(f"Script text mila: {len(text)} chars", flush=True)

        # Keyword map - Script me ye lafz aaye to ye image lagao
        mapping = {
            "ameer": "rich successful man business",
            "gareeb": "poor sad man struggle",
            "bewaqoof": "foolish confused man",
            "kamyab": "successful businessman award",
            "mard": "strong muslim man",
            "aurat": "muslim woman hijab",
            "rizq": "money halal income",
            "qayamat": "islamic apocalypse sky",
            "jinnat": "dark spiritual night",
            "wazifa": "muslim praying quran",
            "sabar": "patient man praying",
            "maut": "grave islamic graveyard",
            "hasad": "jealous people envy",
            "waqt": "clock time management",
            "mehnat": "hard working man office"
        }
        
        for urdu_word, eng_prompt in mapping.items():
            if urdu_word in text:
                keywords.append(eng_prompt)
        
        # Agar koi keyword na mile to general motivational
        if not keywords:
            keywords = ["motivational islamic story", "successful muslim man", "hard work", "praying man"]
        
        print(f"Relevant Keywords: {keywords[:5]}", flush=True)
        return keywords
    except Exception as e:
        print(f"Keyword error: {e}", flush=True)
        return ["islamic motivational story", "successful man"]

def generate_video(image_paths, audio_path):
    os.makedirs("output", exist_ok=True)
    
    # 1. Audio duration - Yehi video ki asal duration hai (8-10 min)
    audio = AudioFileClip(audio_path)
    duration = audio.duration
    print(f"Audio Duration: {duration:.1f} sec = {duration/60:.1f} min", flush=True)
    
    if duration < 300:
        print(f"WARNING: Audio sirf {duration/60:.1f} min hai! script.py 1300 words wala use karo warna video 8 min nahi banegi", flush=True)

    # 2. Relevant images ka logic
    # Agar aapke paas pehle se images hain to unko 3 sec ke hisaab se use karo
    # Agar images kam hain to loop karo
    
    relevant_keywords = get_image_keywords_from_script()
    
    clips = []
    # FIX: Har image 3 second ke liye!
    per_image_duration = 3 
    total_clips_needed = int(duration / per_image_duration) + 1
    
    print(f"Har 3 sec pe image change, Total images needed: {total_clips_needed}", flush=True)
    
    # Agar images nahi hain to dummy black se kaam chalao
    if not image_paths or len(image_paths) == 0:
        print("Koi image nahi, black background pe 3 sec loop", flush=True)
        image_paths = ["black"] # placeholder
    
    current_time = 0
    img_index = 0
    keyword_index = 0
    
    while current_time < duration:
        remaining = duration - current_time
        clip_duration = min(per_image_duration, remaining)
        
        img_source = image_paths[img_index % len(image_paths)]
        
        try:
            if img_source == "black" or not os.path.exists(img_source):
                # Black background agar image missing
                clip = ColorClip(size=(1280, 720), color=(0,0,0), duration=clip_duration)
            else:
                clip = ImageClip(img_source).set_duration(clip_duration).resize((1280,720))
                # Thoda zoom effect taake video zinda lage - ameer logon wali feel
                clip = clip.resize(lambda t: 1 + 0.03*t)
            
            clip = clip.set_start(current_time)
            clips.append(clip)
            
        except Exception as e:
            print(f"Image {img_source} error: {e}, black use kar raha hu", flush=True)
            clip = ColorClip(size=(1280, 720), color=(0,0,0), duration=clip_duration).set_start(current_time)
            clips.append(clip)
        
        current_time += clip_duration
        img_index += 1
        # Har 2 images ke baad keyword change (taake story follow ho)
        if img_index % 2 == 0:
            keyword_index = (keyword_index + 1) % len(relevant_keywords)

    # 3. Jodo aur audio lagao
    print(f"Concatenating {len(clips)} clips...", flush=True)
    video = concatenate_videoclips(clips, method="compose")
    video = video.set_duration(duration)
    video = video.set_audio(audio)
    
    output_path = "output/final_video.mp4"
    print(f"Rendering FINAL {duration/60:.2f} min video, {len(clips)} images (3 sec each)...", flush=True)
    video.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac', threads=2, logger='bar')
    
    print(f"VIDEO READY: {output_path} | Duration: {duration/60:.2f} min | Images: {len(clips)}", flush=True)
    return output_path

def create_video(image_paths, audio_path):
    return generate_video(image_paths, audio_path)

def make_video(image_paths, audio_path):
    return generate_video(image_paths, audio_path)
