import os, random, requests, json, asyncio, textwrap, re
import edge_tts
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont

print("TRENDING AGENT Started...")

PEXELS_KEY = os.getenv("PEXELS_KEY")
YT_API_KEY = os.getenv("YT_API_KEY")
TOPICS_FILE = "used_topics.json"

def get_trending_from_youtube():
    print("Fetching YouTube Trending PK...")
    try:
        # YouTube Most Popular PK
        url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&chart=mostPopular&regionCode=PK&maxResults=20&key={YT_API_KEY}"
        r = requests.get(url, timeout=20).json()
        titles = []
        for item in r.get('items', []):
            t = item['snippet']['title']
            # Clean title
            t = re.sub(r'[#@|]', '', t)
            titles.append(t)
        print(f"Found {len(titles)} trending titles")
        return titles
    except Exception as e:
        print(f"Trending API fail: {e}")
        return []

def get_unique_topic():
    trending = get_trending_from_youtube()
    if not trending:
        # Fallback viral topics if API fail
        trending = ["Shocking Truth Today", "Viral News Pakistan", "Biggest Breaking News", "3 AM Horror Story", "Today's Viral Video"]

    # Avoid repeat
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

    with open(TOPICS_FILE, 'w') as f: json.dump(used[-50:], f) # last 50 keep

    print(f"SELECTED TRENDING TOPIC: {topic}")
    return topic

async def create_voice(text, file="voice.mp3"):
    communicate = edge_tts.Communicate(text, "ur-PK-AsadNeural")
    await communicate.save(file)
    return file

def get_pexels_clips(query, count=6):
    headers = {"Authorization": PEXELS_KEY}
    # Search Pexels with first 2 words of trending topic
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
    y=180
    for line in lines[:3]:
        draw.text((40, y), line.upper(), fill="yellow", font=font, stroke_width=6, stroke_fill="black")
        y+=120
    draw.text((40, 600), "TRENDING TODAY!", fill="white", font=font, stroke_width=4, stroke_fill="black")
    img.save(file)
    return file

async def main():
    topic = get_unique_topic()

    # 18 MIN SCRIPT BASED ON TRENDING TOPIC
    base_script = f"""Bismillah. Aaj YouTube par sab se zyada trending video {topic} hai.
    Dosto ye khabar aag ki tarah viral ho rahi hai. Har koi is bare me baat kar raha hai.
    Pehli baat, is video ki haqeeqat kya hai. Dosri baat, iske peeche asal kahani kya hai.
    Teesri baat jo sab se zyada shocking hai. Aap video akhir tak dekhen.
    Ye jo {topic} ka waqia hai isne sab ko hairan kar diya hai.
    """
    script = base_script * 40 # ~18 min

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
    print("TRENDING VIDEO READY!")

if __name__ == "__main__":
    asyncio.run(main())
