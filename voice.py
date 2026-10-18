import asyncio
import edge_tts
import os

# BEST MALE VOICES - bilkul human jaisa
VOICE_MALE_URDU = "ur-PK-AsadNeural"
VOICE_MALE_ENGLISH = "en-US-GuyNeural"

async def _make_audio(text, output_file):
    communicate = edge_tts.Communicate(
        text, 
        VOICE_MALE_URDU,
        rate="-5%",  # anchor jaisa slow
        pitch="+2Hz"
    )
    await communicate.save(output_file)
    print(f"Urdu Male Voice Ready: {output_file}", flush=True)

def generate_voice(script_text, output_file="output/voice.mp3"):
    os.makedirs("output", exist_ok=True)
    
    # Main wale code ko output/voice.mp3 chahiye hota hai
    if not output_file.startswith("output/"):
        output_file = "output/voice.mp3"

    try:
        # GitHub Actions me asyncio ka masla aata hai, is liye ye tariqa
        try:
            asyncio.run(_make_audio(script_text, output_file))
        except RuntimeError:
            # Agar loop pehle se chal raha ho to
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(_make_audio(script_text, output_file))

    except Exception as e:
        print(f"Urdu voice fail, English male try kar raha hu: {e}", flush=True)
        async def fallback():
            communicate = edge_tts.Communicate(script_text, VOICE_MALE_ENGLISH, rate="-5%")
            await communicate.save(output_file)
        try:
            asyncio.run(fallback())
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(fallback())
            
    print(f"Final Voice Path: {output_file}", flush=True)
    return output_file

if __name__ == "__main__":
    generate_voice("Breaking news, Harry Brook Pakistan team ke liye bada khatra ban gaye hain. Pakistan ko soch samajh kar khelna hoga.")
