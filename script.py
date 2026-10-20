import os
import random
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# SAHI NAAM - GitHub secrets ke mutabiq
YT_REFRESH_TOKEN = os.getenv("YT_REFRESH_TOKEN")
YT_CLIENT_ID = os.getenv("YT_CLIENT_ID")
YT_CLIENT_SECRET = os.getenv("YT_CLIENT_SECRET")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def get_authenticated_youtube():
    token_data = {
        "client_id": YT_CLIENT_ID,
        "client_secret": YT_CLIENT_SECRET,
        "refresh_token": YT_REFRESH_TOKEN,
        "type": "authorized_user"
    }
    creds = Credentials.from_authorized_user_info(token_data, ["https://www.googleapis.com/auth/youtube"])
    return build("youtube", "v3", credentials=creds)

def get_trending_from_youtube():
    try:
        print("Trending check PK se...", flush=True)
        youtube = get_authenticated_youtube()
        request = youtube.videos().list(part="snippet,statistics", chart="mostPopular", regionCode="PK", maxResults=20)
        response = request.execute()
        viral_list = []
        for item in response["items"]:
            title = item["snippet"]["title"]
            views = int(item.get("statistics", {}).get("viewCount", 0))
            if views > 50000:
                viral_list.append({"title": title, "views": views})
        if viral_list:
            viral_list.sort(key=lambda x: x["views"], reverse=True)
            top = viral_list[0]
            print(f"Viral Found: {top['title']}", flush=True)
            return top["title"]
        titles = [item["snippet"]["title"] for item in response["items"]]
        return random.choice(titles) if titles else None
    except Exception as e:
        print(f"Trending fail: {e}", flush=True)
        return None

def generate_script():
    topic = get_trending_from_youtube()
    if not topic:
        topic = "Qayamat Ki Nishaniyan Jo Puri Ho Chuki Hain"

    print(f"FINAL TOPIC: {topic}", flush=True)

    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        Topic: {topic}
        Write VERY LONG 1300-1500 words script in Roman Urdu for YouTube World of Wisdom style.
        Hook 100 words, 6 points each 200 words story, ending 150 words.
        Topic: {topic}
        """
        response = model.generate_content(prompt)
        script = response.text.strip()
        if len(script.split()) < 900:
            r2 = model.generate_content(f"Is ko 1300 words tak lamba karo: {script}")
            script = r2.text.strip()
        print(f"Script ready: {len(script.split())} words", flush=True)
        return topic, script
    except Exception as e:
        print(f"Script error {e}", flush=True)
        long_script = f"Assalam-o-Alaikum! Aaj ki video hai {topic} pe. " * 150
        return topic, long_script
