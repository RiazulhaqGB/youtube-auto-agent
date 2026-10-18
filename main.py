import os

# ===== Hamari 3 alag files =====
from thumbnail import generate_thumbnail
from voice import generate_voice
from video import get_topic_images, create_video_with_clips

# ================= CONFIG =================
# Yahan se topic change kar sakte ho
TOPIC = "Harry Brook Pakistan Team ke liye Khatra"

SCRIPT = f"""{TOPIC}. 
Aaj ke match mein Harry Brook Pakistan team ke liye sabse bada khatra ban gaye hain.
Pakistan ko is khiladi se bachne ke liye khas planning karni hogi.
Dekhte hain Pakistan team is challenge ka kaise samna karti hai."""

THUMBNAIL_FILE = "thumbnail.jpg"
VOICE_FILE = "voice.mp3"
FINAL_VIDEO = "final_video.mp4"

# ================= MAIN FUNCTION =================
def main():
    print(f"===== YOUTUBE AUTO AGENT START =====")
    print(f"Topic: {TOPIC}")

    # STEP 1: THUMBNAIL
    print("\n[1/3] Thumbnail bana raha hun...")
    try:
        generate_thumbnail(TOPIC, output_path=THUMBNAIL_FILE)
        print(f" Thumbnail Ready: {THUMBNAIL_FILE}")
    except Exception as e:
        print(f" Thumbnail Error: {e}")

    # STEP 2: VOICE (Male Human)
    print("\n[2/3] Male Human Voice bana raha hun...")
    try:
        generate_voice(SCRIPT, VOICE_FILE)
        print(f" Voice Ready: {VOICE_FILE}")
    except Exception as e:
        print(f" Voice Error: {e}")

    # STEP 3: VIDEO CLIPS (Har 6 sec baad change)
    print("\n[3/3] Video clips bana raha hun (Topic ke hisab se)...")
    try:
        # Topic ke hisab se 5 images lo
        images = get_topic_images(TOPIC, num_images=5)
        
        if images and len(images) > 0:
            # Har image ko 6 sec ka clip banao + voice lagao
            create_video_with_clips(images, VOICE_FILE, FINAL_VIDEO)
            print(f" FINAL VIDEO READY: {FINAL_VIDEO}")
        else:
            print(" Images download nahi hui, internet check karo")
    except Exception as e:
        print(f" Video Error: {e}")

    print("\n===== ALL DONE JANI! =====")
    print(f"Files: {THUMBNAIL_FILE}, {VOICE_FILE}, {FINAL_VIDEO}")

if __name__ == "__main__":
    main()
