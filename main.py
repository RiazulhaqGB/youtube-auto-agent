import sys
print("--- LOG START ---", flush=True)
import os
import requests
from PIL import Image
from moviepy.editor import *

# FIX
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.LANCZOS

def get_topic_images(topic, count=5):
    os.makedirs("clips", exist_ok=True)
    images = []
    for i in range(count):
        url = f"https://image.pollinations.ai/prompt/{topic} cricket?width=1280&height=720&nologo=true&seed={i}"
        try:
            r = requests.get(url, timeout=30)
            path = f"clips/clip_{i}.jpg"
            with open(path, 'wb') as f:
                f.write(r.content)
            images.append(path)
            print(f"Image {i+1} ready: {topic}")
        except Exception as e:
            print(f"Image {i} fail {e}")
    return images

def create_video_with_clips(image_paths, audio_path, output_path):
    try:
        audio = AudioFileClip(audio_path)
        print(f"Voice Ready: {audio_path} Duration {audio.duration}")
        
        clips = []
        duration_per_image = audio.duration / len(image_paths) if image_paths else 5
        
        for img_path in image_paths:
            try:
                clip = ImageClip(img_path, duration=duration_per_image)
                clip = clip.resize(height=720).set_position('center')
                clips.append(clip)
                print(f"Clip ready {img_path}")
            except Exception as e:
                print(f"Clip error {img_path}: {e}")
        
        if not clips:
            print("No clips found!")
            return False
            
        video = CompositeVideoClip(clips, size=(1280,720)).set_audio(audio)
        video.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')
        print(f"Video Ready: {output_path}")
        return True
    except Exception as e:
        print(f"Video creation error: {e}")
        return False
