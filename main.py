import os, re, json, random, textwrap, asyncio, requests
import edge_tts
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, ColorClip
from PIL import Image, ImageDraw, ImageFont

YT_API_KEY = os.getenv("YT_API_KEY")
YT_CLIENT_ID = os.getenv("YT_CLIENT_ID")
YT_CLIENT_SECRET = os.getenv("YT_CLIENT_SECRET")
YT_REFRESH_TOKEN = os.getenv("YT_REFRESH_TOKEN")
PEXELS_KEY = os.getenv("PEXELS_KEY")
TOPICS_FILE = "used_topics.json"

def get_trending_from_youtube():
    try:
        url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&chart=mostPopular&regionCode=PK&maxResults=20&key={YT_API_KEY}"
        r = requests.get(url, timeout=20).json()
        titles = []
        for item in r.get('items', []):
            t = item['snippet']['title']
            t = re.sub(r'[#@|]', ' ', t)
            titles.append(t)
        return titles
    except:
        return []

def get_unique_topic():
    trending = get_trending_from_youtube()
    if not trending:
        trending = ["Shocking Truth Today", "Viral News Pakistan", "Biggest Breaking News"]
    if os.path.exists(TOPICS_FILE):
        with open(TOPICS_FILE, 'r') as f: used = json.load(f)
    else:
        used = []
    available = [t for t in trending if t not in used]
    if not available:
        available = trending
        used = []
    topic = random.choice(available)
    used.append(topic)
    with open(TOPICS_FILE, 'w') as f: json.dump(used[-50:], f)
    print(f"SELECTED TOPIC: {topic}")
    return topic

async def create_voice(text, file="voice.mp3"):
    communicate = edge_tts.Communicate(text, "ur-PK-AsadNeural")
    await communicate.save(file)
    return file

def get_pexels_clips(query, count=6):
    headers = {"Authorization": PEXELS_KEY}
    search_q = " ".join(query.split()[:2])
    url = f"https://api.pexels.com/videos/search?query={search_q}&per_page={count}&size=hd"
    try:
        r = requests.get(url, headers=headers, timeout=30).json()
        clips = []
        for i, v in enumerate(r.get('videos', [])[:count]):
            video_url = v['video_files'][0]['link']
            path = f"clip_{i}.mp4"
            with open(path, 'wb') as f:
                f.write(requests.get(video_url, timeout=30).content)
            clips.append(path)
        return clips
    except:
        return []

def make_thumbnail(text, file="thumbnail.jpg"):
    img = Image.new('RGB', (1280, 720), color=(200, 0, 0))
    draw = ImageDraw.Draw(img)
    try: font = ImageFont.truetype("arial.ttf", 75)
    except: font = ImageFont.load_default()
    lines = textwrap.wrap(text, width=22)
    y=100
    for line in lines[:3]:
        draw.text((40, y), line.upper(), fill="yellow", font=font, stroke_width=8, stroke_fill="black")
        y+=120
    draw.text((40, 600), "TRENDING TODAY!", fill="white", font=font, stroke_width=4, stroke_fill="black")
    img.save(file)
    return file

def get_access_token():
    url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": YT_CLIENT_ID,
        "client_secret": YT_CLIENT_SECRET,
        "refresh_token": YT_REFRESH_TOKEN,
        "grant_type": "refresh_token"
    }
    r = requests.post(url, data=data, timeout=20).json()
    return r.get("access_token")

def upload_to_youtube(video_file, thumbnail_file, topic):
    access_token = get_access_token()
    if not access_token:
        print("FAILED to get access token - Secrets check karo!")
        return
    title = f"{topic} | Viral News Today"
    description = f"""{topic}

Is video me hum baat karenge {topic} ke bare me. Ye khabar aag ki tarah viral ho rahi hai.

#Viral #Trending #Pakistan #News #WHTAuto
Topic: {topic}
"""
    tags = ["viral", "trending", "pakistan news", topic]
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json; charset=UTF-8"}
    body = {
        "snippet": {"title": title[:95], "description": description, "tags": tags, "categoryId": "25"},
        "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False}
    }
    init_url = "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status"
    init_res = requests.post(init_url, headers=headers, json=body)
    upload_url = init_res.headers.get("Location")
    with open(video_file, 'rb') as f:
        upload_res = requests.put(upload_url, headers={"Authorization": f"Bearer {access_token}"}, data=f)
    video_id = upload_res.json().get("id")
    print(f"UPLOADED SUCCESSFULLY! Video ID: {video_id}")
    if video_id and os.path.exists(thumbnail_file):
        thumb_url = f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={video_id}"
        with open(thumbnail_file, 'rb') as f:
            requests.post(thumb_url, headers={"Authorization": f"Bearer {access_token}"}, data=f)
    return video_id

async def main():
    topic = get_unique_topic()
    base_script = f"""Bismillah. Aaj YouTube par sab se zyada trending video {topic} hai.
Dosto ye khabar aag ki tarah viral ho rahi hai. Har koi is bare me baat kar raha hai.
Pehli baat, is video ki haqeeqat kya hai. Dosri baat, iske peeche asal kahani kya hai.
Teesri baat jo sab se zyada shocking hai. Aap video aakhir tak dekhen.
Ye jo {topic} ka waqia hai isne sab ko hairan kar diya hai.
"""
    script = (base_script + "\n\n") * 30
    await create_voice(script)
    clips_path = get_pexels_clips(topic)
    make_thumbnail(topic)
    audio = AudioFileClip("voice.mp3")
    if clips_path:
        video_clips = []
        clip_duration = audio.duration / len(clips_path)
        for c in clips_path:
            try:
                vc = VideoFileClip(c).subclip(0, clip_duration).resize((1280,720))
                video_clips.append(vc)
            except: continue
        final_video = concatenate_videoclips(video_clips, method="compose")
        final_video = final_video.set_audio(audio)
    else:
        final_video = ColorClip((1280,720), color=(0,0,0), duration=audio.duration).set_audio(audio)
    final_video.write_videofile("final_video.mp4", fps=24, codec='libx264', audio_codec='aac')
    upload_to_youtube("final_video.mp4", "thumbnail.jpg", topic)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
