import requests, random, textwrap
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

def generate_thumbnail(topic="Harry Brook Pakistan Team ke liye Khatra"):
    W, H = 1280, 720
    
    # 1. Base - Pro News Gradient (Dark Blue to Navy)
    base = Image.new('RGB', (W, H), (8, 25, 90))
    draw = ImageDraw.Draw(base)
    for y in range(H):
        # Gradient effect
        blue = int(90 + y * 0.15)
        red = int(8 + y * 0.05)
        draw.line([(0, y), (W, y)], fill=(red, 15, min(blue, 180)))

    # 2. Background Image - Topic ke hisab se
    try:
        # Topic se image prompt banao
        prompt = f"{topic}, news, cinematic, 4k, dramatic lighting"
        url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(prompt)}?width=1280&height=720&seed={random.randint(1,999999)}&nologo=true"
        r = requests.get(url, timeout=25)
        if r.status_code == 200 and len(r.content) > 10000:
            open("bg_temp.jpg", "wb").write(r.content)
            bg = Image.open("bg_temp.jpg").convert("RGB").resize((W, H))
            # Blur + Darken taake text saaf nazar aaye
            bg = bg.filter(ImageFilter.GaussianBlur(3))
            bg = ImageEnhance.Brightness(bg).enhance(0.6)
            base = Image.blend(base, bg, 0.7)
            print(f"Background downloaded for: {topic}")
    except Exception as e:
        print(f"BG failed, using gradient only: {e}")

    draw = ImageDraw.Draw(base, "RGBA")

    # 3. Fonts - Urdu + English ke liye
    try:
        # GitHub me ye font available hai
        font_ur_big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 95)
        font_ur_mid = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 65)
        font_en = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 50)
    except:
        font_ur_big = ImageFont.load_default()
        font_ur_mid = ImageFont.load_default()
        font_en = ImageFont.load_default()

    # 4. Topic ko 2 hisso me divide - Auto Text Logic
    # Agar topic me "Harry Brook" hai to Urdu me convert
    if "harry" in topic.lower() or "brook" in topic.lower():
        line1 = "ہیری بروک"
        line2 = "پاکستان ٹیم کے لیے بڑا خطرہ!"
        line3 = "ENGLAND vs PAKISTAN"
    elif "india" in topic.lower():
        line1 = "بھارت کو بڑا جھٹکا"
        line2 = topic[:35]
        line3 = "BREAKING NEWS"
    else:
        # General logic - topic ko wrap karo
        wrapped = textwrap.wrap(topic, width=22)
        line1 = wrapped[0] if len(wrapped) > 0 else topic[:20]
        line2 = wrapped[1] if len(wrapped) > 1 else ""
        line3 = "BREAKING NEWS TODAY"

    # 5. Text Draw with Stroke (Black outline + Color fill)
    def text_with_stroke(pos, text, font, fill_color, stroke_color=(0,0,0), stroke_width=6):
        x, y = pos
        # Stroke
        for dx in range(-stroke_width, stroke_width+1):
            for dy in range(-stroke_width, stroke_width+1):
                if dx*dx + dy*dy <= stroke_width*stroke_width:
                    draw.text((x+dx, y+dy), text, font=font, fill=stroke_color)
        # Main fill
        draw.text((x, y), text, font=font, fill=fill_color)

    # Line 1 - Yellow (Sab se important)
    text_with_stroke((70, 110), line1, font_ur_big, (255, 235, 0))
    # Line 2 - White
    text_with_stroke((70, 260), line2, font_ur_mid, (255, 255, 255))
    # Line 3 - Green Tag
    # Green box behind line3
    draw.rectangle([(70, 430), (750, 500)], fill=(0, 200, 80, 230))
    draw.text((90, 440), line3, font=font_en, fill=(255,255,255))

    # 6. Save - High Quality
    base = base.convert("RGB")
    base.save("thumbnail.jpg", "JPEG", quality=98, optimize=True)
    print(f"THUMBNAIL READY: {line1} | {line2}")
    return "thumbnail.jpg"

# --- TEST ---
if __name__ == "__main__":
    # Yahan topic change karke test kar sakte ho
    TOPIC = "Harry Brook Pakistan Team ke liye Khatra"
    generate_thumbnail(TOPIC)
