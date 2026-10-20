from gtts import gTTS
import os

def generate_voice(text, output_path="voice.mp3"):
    try:
        if os.path.exists(output_path):
            os.remove(output_path)
    except:
        pass

    # Text saaf karo
    text = text.strip()
    if len(text) < 5:
        text = "Assalam o Alaikum dosto, aaj ki kahani sunte hain."

    print(f"Generating voice: {text[:80]}...", flush=True)

    # Purana wala gTTS - Hindi/Urdu mix
    tts = gTTS(text=text, lang='ur', slow=False)
    tts.save(output_path)

    if os.path.exists(output_path):
        print(f"Voice OK, size: {os.path.getsize(output_path)}", flush=True)
        return output_path
    else:
        raise Exception("Voice file not created!")

if __name__ == "__main__":
    generate_voice("Ye purani wali awaaz ka test hai")
