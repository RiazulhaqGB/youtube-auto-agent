from moviepy.editor import *
import os

def generate_video(image_paths, audio_path):
    os.makedirs("output", exist_ok=True)
    print(f"Video bana raha hu, images: {len(image_paths)}", flush=True)
    
    audio = AudioFileClip(audio_path)
    duration = audio.duration
    per_image = duration / len(image_paths) if image_paths else 1
    
    clips = []
    for img in image_paths:
        clip = ImageClip(img).set_duration(per_image).set_fps(24).resize((1280,720))
        clips.append(clip)
    
    video = concatenate_videoclips(clips, method="compose")
    video = video.set_audio(audio)
    
    output_path = "output/final_video.mp4"
    video.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')
    print(f"Video ready: {output_path}", flush=True)
    return output_path

# Backup naam ke liye bhi same function - taake import error na aaye
def create_video(image_paths, audio_path):
    return generate_video(image_paths, audio_path)

def make_video(image_paths, audio_path):
    return generate_video(image_paths, audio_path)
