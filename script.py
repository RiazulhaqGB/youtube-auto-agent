import os
import re
from googleapiclient.discovery import build

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
YT_API_KEY = os.getenv("YT_API_KEY")

def get_trending_from_youtube():
    if not YT_API_KEY:
        raise Exception("YT_API_KEY missing!")
    youtube = build("youtube", "v3", developerKey=YT_API_KEY)
    request = youtube.videos().list(part="snippet,statistics", chart="mostPopular", regionCode="PK", maxResults=20)
    response = request.execute()
    viral_list = []
    for item in response["items"]:
        title = item["snippet"]["title"]
        views = int(item.get("statistics", {}).get("viewCount", 0))
        viral_list.append({"title": title, "views": views})
    viral_list.sort(key=lambda x: x["views"], reverse=True)
    top_title = viral_list[0]["title"]
    print(f"Selected Viral Topic: {top_title}", flush=True)
    return top_title

def clean_script_for_voice(text):
    """ Ye function script ko voice ke liye saaf karega """
    print("Cleaning script for voice...", flush=True)
    # 1. English ke fazool lafz hatao
    bad_words = ["book", "word", "chapter", "point", "topic", "hook", "script", "video", "like", "share", "subscribe", "channel"]
    for w in bad_words:
        text = re.sub(rf'\b{w}\b', '', text, flags=re.IGNORECASE)
    
    # 2. Aise symbols hatao jo TTS ko fail karte hain: * # _ ``` [ ] ( ) 
    text = re.sub(r'[*#_`"“”\[\]\(\)\{\}]', '', text)
    text = re.sub(r'https?://\S+', '', text) # links hatao
    
    # 3. Emojis hatao
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F" u"\U0001F300-\U0001F5FF" u"\U0001F680-\U0001F6FF" u"\U0001F1E0-\U0001F1FF" "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)
    
    # 4. Double spaces khatam
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    
    # 5. Agar text me Roman Urdu bach gaya to usko bhi saaf karo, sirf Urdu rehne do
    text = text.strip()
    if len(text) < 100:
        raise Exception("Script cleaning ke baad khali ho gaya!")
    
    return text

def generate_script():
    if not GEMINI_API_KEY:
        raise Exception("GEMINI_API_KEY missing!")
    if not YT_API_KEY:
        raise Exception("YT_API_KEY missing!")
    topic = get_trending_from_youtube()

    from google import genai
    from google.genai import types
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    prompt = f"""
    You are viral YouTube scriptwriter for 'World of Wisdom'.
    Topic: "{topic}"
    Write 100% ORIGINAL script in PURE URDU SCRIPT (اردو رسم الخط).
    RULES:
    1. Sirf Urdu script: یہ زندگی ایک امتحان ہے
    2. NO English words at all: book, word, like, share etc mana hai
    3. NO symbols like * # [ ] 
    4. Length: 1300-1500 words
    5. Structure: Hook, 6 points with hadith/story, Ending with Dua
    """
    
    response = client.models.generate_content(
        model='gemini-flash-lite-latest',
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.9, max_output_tokens=8000)
    )
    
    script = response.text.strip()
    
    # YAHAN FIX LAGAYA HAI - VOICE.PY KO TOUCH KIYE BAGAIR
    script = clean_script_for_voice(script)

    if len(script.split()) < 800:
        print("Expanding...", flush=True)
        response2 = client.models.generate_content(
            model='gemini-flash-lite-latest',
            contents=f"Is Urdu script ko 1300 words tak expand karo, English lafz ke bagair:\n\n{script}"
        )
        script = clean_script_for_voice(response2.text.strip())

    print(f"SCRIPT READY & CLEANED: {len(script.split())} words", flush=True)
    return topic, script
