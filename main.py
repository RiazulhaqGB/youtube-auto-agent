import os
from thumbnail import generate_thumbnail
from voice import generate_voice
from video import get_topic_images, create_video_with_clips
from youtube import upload_video

TOPIC = "Harry Brook Pakistan Team ke liye Khatra"
SCRIPT = f"{TOPIC}. Aaj ke match mein Harry Brook sabse bada khatra hai. Pakistan team ko special planning karni hogi."

THUMBNAIL_FILE = "thumbnail.jpg"
VOICE_FILE = "voice.mp3"
FINAL_VIDEO = "final_video.mp4"

def main():
    print(f"START: {TOPIC}")
    generate_thumbnail(TOPIC, THUMBNAIL_FILE)
    generate_voice(SCRIPT, VOICE_FILE)
    
    images = get_topic_images(TOPIC, 5)
    if images:
        create_video_with_clips(images, VOICE_FILE, FINAL_VIDEO)
        print("Video Ready, Ab Upload...")
        upload_video(FINAL_VIDEO, TOPIC, SCRIPT, THUMBNAIL_FILE)
    print("ALL DONE!")

if __name__ == "__main__":
    main()
