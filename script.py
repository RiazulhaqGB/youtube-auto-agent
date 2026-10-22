import os
from googleapiclient.discovery import build

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
YT_API_KEY = os.getenv("YT_API_KEY")

def get_trending_from_youtube():
    if not YT_API_KEY:
        raise Exception("YT_API_KEY missing in GitHub Secrets!")
    print("Viral check via YouTube API Key (PK Trending)...", flush=True)
    youtube = build("youtube", "v3", developerKey=YT_API_KEY)
    request = youtube.videos().list(
        part="snippet,statistics",
        chart="mostPopular",
        regionCode="PK",
        maxResults=20
    )
    response = request.execute()
    viral_list = []
    for item in response["items"]:
        title = item["snippet"]["title"]
        views = int(item.get("statistics", {}).get("viewCount", 0))
        viral_list.append({"title": title, "views": views})
    viral_list.sort(key=lambda x: x["views"], reverse=True)
    print("Top 5 viral PK:", flush=True)
    for v in viral_list[:5]:
        print(f" - {v['title']} [{v['views']} views]", flush=True)
    top_title = viral_list[0]["title"]
    print(f"Selected Viral Topic: {top_title}", flush=True)
    return top_title

def generate_script():
    if not GEMINI_API_KEY:
        raise Exception("GEMINI_API_KEY missing!")
    if not YT_API_KEY:
        raise Exception("YT_API_KEY missing!")
    topic = get_trending_from_youtube()
    print(f"FINAL TOPIC FOR GEMINI: {topic}", flush=True)
    import google.generativeai as genai
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash')
    prompt = f"""
    You are viral YouTube scriptwriter for channel 'World of Wisdom'.
    Analyze this viral trending topic from Pakistan: "{topic}"
    Write a 100% ORIGINAL, VIRAL script in Roman Urdu.
    REQUIREMENTS:
    - Language: Simple Roman Urdu
    - Length: 1300-1500 words (12-15 min video)
    - Style: Emotional, Islamic, Moral, Curious hook like trending videos
    - Structure: Hook 100 words, 6 Points each 200 words with story/hadith, Ending 150 words with Dua + CTA
    - Do NOT repeat sentences.
    Topic: {topic}
    """
    print("Generating script from Gemini...", flush=True)
    response = model.generate_content(prompt)
    if not response.text:
        raise Exception(f"Gemini returned empty! Full response: {response}")
    script = response.text.strip()
    if len(script.split()) < 1000:
        print(f"Script short {len(script.split())} words, expanding via Gemini...", flush=True)
        expand_prompt = f"Is script ko 1300 words tak expand karo, repetition ke bagair:\n\n{script}"
        response2 = model.generate_content(expand_prompt)
        script = response2.text.strip()
    if len(script.split()) < 800:
        raise Exception(f"Gemini failed to generate long script, got only {len(script.split())} words")
    print(f"SCRIPT READY: {len(script.split())} words via Gemini", flush=True)
    return topic, script
