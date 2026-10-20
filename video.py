import os
from moviepy.editor import *

def create_video(image_paths, audio_path):
    print(f"Creating video MAX 12 min...", flush=True)
    if not image_paths:
        image_paths = ["output/title.jpg"]
    
    audio = AudioFileClip(audio_path) if audio_path and os.path.exists(audio_path) else None
    duration = audio.duration if audio else 600
    
    # FORCE CUT TO 12 MINUTES MAX (720 sec)
    if duration > 720:
        print(f"Audio too long {duration}s, cutting to 720s", flush=True)
        duration = 720
        audio = audio.subclip(0, 720)
    
    print(f"Final Duration: {duration}s = {duration/60:.1f} min", flush=True)

    clips = []
    per_image = duration / len(image_paths)
    for img in image_paths:
        if os.path.exists(img):
            try:
                clip = ImageClip(img).set_duration(per_image).resize(height=720).set_fps(24)
                clips.append(clip)
            except: continue

    if not clips:
        print("No images!", flush=True)
        return None

    final = concatenate_videoclips(clips, method="compose")
    if audio:
        final = final.set_audio(audio)
    
    final.write_videofile("final_video.mp4", fps=24, codec='libx264', preset='ultrafast', bitrate="1500k", threads=4, logger='bar')
    print("Video Done 12 min MAX!", flush=True)
    return "final_video.mp4"

def generate_video(image_paths, audio_path):
    return create_video(image_paths, audio_path)
