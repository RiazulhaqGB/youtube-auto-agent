import asyncio
import edge_tts

# BEST MALE VOICES - bilkul human jaisa
# Urdu ke liye: ur-PK-AsadNeural (MALE)
# English ke liye: en-US-GuyNeural (MALE)

VOICE_MALE_URDU = "ur-PK-AsadNeural"
VOICE_MALE_ENGLISH = "en-US-GuyNeural" # Agar Urdu fail ho to backup

async def _make_audio(text, output_file="voice.mp3"):
    # Speed thori slow rakhi hai taake anchor jaisa lage
    communicate = edge_tts.Communicate(
        text, 
        VOICE_MALE_URDU,
        rate="-5%",  # thora slow, human touch
        pitch="+2Hz"
    )
    await communicate.save(output_file)
    print(f"Voice Ready: {output_file}")

def generate_voice(text="Harry Brook ne Pakistan ke khilaf century bana di hai", output_file="voice.mp3"):
    try:
        # Urdu text ke liye best
        asyncio.run(_make_audio(text, output_file))
    except Exception as e:
        print(f"Urdu voice fail, trying English male: {e}")
        # Fallback
        async def fallback():
            communicate = edge_tts.Communicate(text, VOICE_MALE_ENGLISH, rate="-5%")
            await communicate.save(output_file)
        asyncio.run(fallback())
    return output_file

if __name__ == "__main__":
    # Test
    generate_voice("Breaking news, Harry Brook Pakistan team ke liye bada khatra ban gaye hain. Pakistan ko soch samajh kar khelna hoga.")
