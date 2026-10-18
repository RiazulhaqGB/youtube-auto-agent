import os
import random
import requests
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# Pakistan me viral hone wale topics ka backup list
VIRAL_URDU_TOPICS = [
    "Islami Waqiat Jo Aapko Rula Dengay",
    "Qayamat Ki Nishaniyan Jo Puri Ho Chuki Hain",
    "Jinnat Ka Sach - Kya Wo Hamare Beech Rehte Hain?",
    "Rizq Me Barkat Ka Wazifa",
    "Zehni Dabao Ko Khatam Karne Ka Tariqa",
    "Kamyab Logon Ki 5 Adatain",
    "Hasad Se Bachne Ka Tarika",
    "Mout Ke Baad Kya Hota Hai?"
]

def get_trending_from_youtube():
    try:
        print("Trending check kar raha hu YouTube PK se...", flush=True)
        # token.json se YouTube service banao
        if not os.path.exists("token.json"):
            return None
            
        creds = Credentials.from_authorized_user_file("token.json", ["https://www.googleapis.com/auth/youtube.upload"])
        youtube = build("youtube", "v3", credentials=creds)
        
        request = youtube.videos().list(
            part="snippet",
            chart="mostPopular",
            regionCode="PK",
            maxResults=10
        )
        response = request.execute()
        
        trending_titles = [item["snippet"]["title"] for item in response["items"]]
        print(f"Trending Mila: {trending_titles[:3]}", flush=True)
        
        # Trending title se inspiration leke apna topic banao
        base = random.choice(trending_titles)
        return f"{base} - Haqeeqat Kya Hai?"
        
    except Exception as e:
        print(f"Trending API fail: {e}, backup topic use kar raha hu", flush=True)
        return None

def generate_script():
    # 1. Pehle YouTube Trend check karo
    trending_topic = get_trending_from_youtube()
    
    # 2. Agar trend na mile to viral list se uthao
    if not trending_topic:
        topic = random.choice(VIRAL_URDU_TOPICS)
    else:
        topic = trending_topic

    # 3. Ab Urdu Script Banao (Viral Style)
    script = f"""
Assalam-o-Alaikum! Kya aap jante hain {topic} ke bare me haqeeqat kya hai?

Aaj ki is video me hum baat karenge ek aise sach ke bare me jo aksar log nazar andaaz kar dete hain.

Pehli baat: Zindagi me jo kuch bhi hota hai, uske peeche Allah ki hikmat hoti hai.
Dusri baat: Insaan jaldbazi me faisle karke apni zindagi kharab kar leta hai.
Teesri baat: Agar aap sabar aur shukar se kaam lenge to aapki zindagi badal jayegi.

{topic} ye sirf ek lafz nahi, ye ek sabaq hai ham sab ke liye.

Is video ko akhir tak dekhen, kyunki akhir me main aapko ek aisa wazifa bataunga jo aapki mushkilat aasan kar dega.

Video pasand aaye to Like aur Subscribe zaroor karen.
"""
    return topic, script.strip()
