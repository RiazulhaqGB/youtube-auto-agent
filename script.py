import os, re, random
from googleapiclient.discovery import build

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
YT_API_KEY = os.getenv("YT_API_KEY")

def get_trending_from_youtube():
    youtube = build("youtube", "v3", developerKey=YT_API_KEY)
    # Mix topics: PK Trending + Global + Search
    queries = ["trending today Pakistan", "viral news today", "mystery facts", "technology 2026", "world top story"]
    search_q = random.choice(queries)
    req = youtube.search().list(part="snippet", q=search_q, regionCode="PK", maxResults=15, order="viewCount", type="video")
    res = req.execute()
    viral = [item["snippet"]["title"] for item in res["items"]]
    # Most Popular bhi mix karo
    pop = youtube.videos().list(part="snippet,statistics", chart="mostPopular", regionCode="PK", maxResults=10).execute()
    for it in pop["items"]:
        viral.append(it["snippet"]["title"])
    topic = random.choice(viral)
    print(f"Selected Viral Topic: {topic} (from {search_q})", flush=True)
    return topic

def clean_script_for_voice(text):
    text = re.sub(r'[*#_`"“”\[\]\(\)\{\}]', '', text)
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def generate_script(channel_name="World Trending Hub"):
    topic = get_trending_from_youtube()
    from google import genai
    from google.genai import types
    client = genai.Client(api_key=GEMINI_API_KEY)
    prompt = f"""
    You are viral scriptwriter for YouTube channel '{channel_name}'.
    Topic: "{topic}"
    Write 100% ORIGINAL script in PURE URDU SCRIPT (اردو رسم الخط).
    RULES:
    1. Sirf Urdu script, No English words like book, like, share etc.
    2. Topic TRENDING hai, is liye Islamic fix story nahi. Topic ke mutabiq likho - agar technology hai to technology, mystery hai to mystery, news hai to news.
    3. Length: 1300-1500 words
    4. Structure: Strong Hook (5 sec), 5-6 interesting points with facts/story/example, Strong Ending with question.
    5. No * # symbols.
    """
    response = client.models.generate_content(model='gemini-flash-lite-latest', contents=prompt, config=types.GenerateContentConfig(temperature=0.95, max_output_tokens=8000))
    script = clean_script_for_voice(response.text.strip())
    if len(script.split()) < 800:
        r2 = client.models.generate_content(model='gemini-flash-lite-latest', contents=f"Is Urdu script ko 1300 words tak expand karo:\n\n{script}")
        script = clean_script_for_voice(r2.text.strip())
    print(f"SCRIPT READY: {len(script.split())} words", flush=True)
    return topic, script
