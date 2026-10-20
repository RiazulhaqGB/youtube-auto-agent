from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import textwrap
import random

def generate_thumbnail(topic, output_path="thumbnail.jpg"):
    # Pillow fix
    if not hasattr(Image, 'ANTIALIAS'):
        Image.ANTIALIAS = Image.LANCZOS

    # Background - Topic ke hisaab se auto
    if "cricket" in topic.lower() or "pak vs" in topic.lower() or "babar" in topic.lower():
        bg_prompt = f"cricket stadium dramatic lights {topic}"
    else:
        bg_prompt = f"wise old man white beard suit mountain cinematic {topic}"

    safe_prompt = requests.utils.quote(bg_prompt)
    url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1280&height=720&nologo=true&seed={random.randint(1,99999)}&model=flux"

    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        img = Image.open(BytesIO(r.content)).convert("RGB")
    except Exception as e:
        print(f"BG fail {e}")
        img = Image.new("RGB", (1280,720), (18,18,18))
    
    draw = ImageDraw.Draw(img, "RGBA")
    draw.rectangle([0, 0, 850, 720], fill=(0,0,0,160)) # dark left

    try:
        font_big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
    except:
        font_big = ImageFont.load_default()
        font_small = font_big

    # ====== YAHAN FIX KIYA ======
    # Jo bhi TOPIC video ka hai, wahi thumbnail pe aayega!
    # Koi fixed urdu_map nahi!
    display_text = topic  # <--- Bas yehi line! Video ka title hi thumbnail ka title
    
    wrapped_text = textwrap.fill(display_text, width=18)

    # Decoration
    draw.text((50, 50), "━━━ ✦ ━━━", fill=(212,175,55), font=font_small)
    
    # Text - Aapka wala Yellow + Red + Black shadow
    x, y = 50, 150
    draw.text((x+4, y+4), wrapped_text, fill="black", font=font_big) # shadow
    draw.text((x, y), wrapped_text, fill="yellow", stroke_width=8, stroke_fill="red", font=font_big)
    
    draw.text((50, y+280), "━━━ ✦ ━━━", fill=(212,175,55), font=font_small)
    
    # Duration badge
    draw.rectangle([1130, 630, 1245, 675], fill=(0,0,0))
    draw.text((1145, 635), "6:39", fill=(255,255,255), font=font_small)

    img.save(output_path, quality=95)
    print(f"Thumbnail OK - Video ke mutabiq: {display_text}")
    return output_path
