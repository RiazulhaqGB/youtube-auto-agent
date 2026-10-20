import os
import random
import json
import requests
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# Aapke secrets
YT_API_KEY = os.getenv("YT_API_KEY")
TY_TOKEN_RAW = os.getenv("TY_FRESH_TOKAN")

# --- Token ko file me likh do taake error na aaye ---
def setup_token():
    if not TY_TOKEN_RAW:
        print("TY_FRESH_TOKAN secret nahi mila", flush=True)
        return False
    try:
        # Agar secret me pura JSON hai to file bana do
        if not os.path.exists("token.json"):
            # Secret kabhi string me JSON hota hai
            data = TY_TOKEN_RAW.strip()
            # Agar base64 ya direct JSON
            try:
                json_data = json.loads(data)
                with open("token.json", "w") as f:
                    json.dump(json_data, f)
                print("token.json bana diya TY_FRESH_TOKAN se", flush=True)
            except:
                # Agar already file content hai to direct likh do
                with open("token.json", "w") as f:
                    f.write(data)
                print("token.json direct likh diya", flush=True)
        return True
    except Exception as e:
        print(f"Token setup fail: {e}", flush=True)
        return False

def get_trending_from_youtube():
    try:
        print("Trending check kar raha hu YouTube PK se...", flush=True)
        if not setup_token():
            return None
            
        if not os.path.exists("token.json"):
            print("token.json abhi bhi nahi hai", flush=True)
            return None
            
        creds = Credentials.from_authorized_user_file("token.json", ["https://www.googleapis.com/auth/youtube"])
        youtube = build("youtube", "v3", credentials=creds)
        
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
            stats = item.get("statistics", {})
            views = int(stats.get("viewCount", 0))
            if views > 50000:
                viral_list.append({"title": title, "views": views})
        
        if viral_list:
            viral_list.sort(key=lambda x: x["views"], reverse=True)
            top = viral_list[0]
            print(f"PK Trending Viral: {top['title']} - {top['views']} views", flush=True)
            return top["title"]
        
        # Agar trending me views kam hain to random trending title
        titles = [item["snippet"]["title"] for item in response["items"]]
        return random.choice(titles) if titles else None
        
    except Exception as e:
        print(f"Trending API fail: {e}", flush=True)
        return None

def get_viral_from_search_api():
    # Aapke YT_API_KEY se search
    if not YT_API_KEY:
        return None
    try:
        print(f"YouTube Search API se viral dhoond raha hu...", flush=True)
        query = random.choice(["World of Wisdom", "bewaqoof mardon", "kamyab logon ki nishaniyan"])
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {"part": "snippet", "q": query, "type": "video", "order": "viewCount", "maxResults": 10, "key": YT_API_KEY}
        r = requests.get(url, params=params, timeout=15)
        data = r.json()
        if data.get("items"):
            title = data["items"][0]["snippet"]["title"]
            print(f"Search API Viral: {title}", flush=True)
            return title
    except Exception as e:
        print(f"Search API fail: {e}", flush=True)
    return None

def generate_script():
    # 1. Pehle PK Trending (TY_FRESH_TOKAN se)
    topic = get_trending_from_youtube()
    
    # 2. Nahi mila to YT_API_KEY se search viral
    if not topic:
        topic = get_viral_from_search_api()
    
    # 3. Dono fail to Gemini se naya viral banao - LIST NAHI
    if not topic:
        try:
            import google.generativeai as genai
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            model = genai.GenerativeModel('gemini-1.5-flash')
            resp = model.generate_content("Create 1 viral trending YouTube title in Roman Urdu, Pakistan audience, like World of Wisdom, high views, just title")
            topic = resp.text.strip().split("\n")[0]
        except:
            topic = "Qayamat Ki Nishaniyan Jo Puri Ho Chuki Hain - Haqeeqat Kya Hai?"

    print(f"FINAL VIRAL TOPIC: {topic}", flush=True)

    # --- 8-10 MINUTE KA LAMBA SCRIPT ---
    try:
        import google.generativeai as genai
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        Topic: {topic} (Real viral from YouTube PK)
        Write VERY LONG 1300-1500 words script in Roman Urdu for YouTube.
        Hook 100 words, 6 points each 200 words story, ending 150 words.
        Roman Urdu, emotional, viral style.
        Write on: {topic}
        """
        response = model.generate_content(prompt)
        script = response.text.strip()
        # Lamba check
        if len(script.split()) < 900:
            r2 = model.generate_content(f"Is ko 1300 words tak lamba karo: {script}")
            script = r2.text.strip()
        print(f"Script ready: {len(script.split())} words", flush=True)
        return topic, script
    except Exception as e:
        print(f"Script error {e}", flush=True)
        long_script = f"Assalam-o-Alaikum! Aaj ki video hai {topic} pe. " * 300
        return topic, long_script
