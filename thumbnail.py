import os, requests, random
from PIL import Image, ImageDraw, ImageFont
# Ye 2 library lazmi hain warna Urdu dibbe banega
import arabic_reshaper
from bidi.algorithm import get_display

# Urdu font ka link - ye auto download hoga
FONT_URL = "https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoNastaliqUrdu/NotoNastaliqUrdu-Regular.ttf"
FONT_PATH = "NotoNastaliqUrdu.ttf"

def get_urdu_font(size=80):
    if not os.path.exists(FONT_PATH):
        try:
            print("Downloading Urdu font...", flush=True)
            r = requests.get(FONT_URL, timeout=30)
            open(FONT_PATH, "wb").write(r.content)
            print("Font downloaded OK", flush=True)
        except Exception as e:
            print(f"Font download failed: {e}", flush=True)
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except:
        return ImageFont.load_default()

def fix_urdu(text):
    # Yehi asal fix hai - dibbo ka hal
    try:
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)
    except:
        return text

def generate_thumbnail(title_text, image_paths=None):
    os.makedirs("output", exist_ok=True)
    output_path = "output/thumbnail.jpg"
    
    # 1. Background
    bg = None
    if image_paths and len(image_paths) > 0 and os.path.exists(image_paths[0]):
        try:
            bg = Image.open(image_paths[0]).convert("RGB").resize((1280, 720))
        except:
            pass
    
    if bg is None:
        bg = Image.new("RGB", (1280, 720), (20, 10, 30))
    
    # 2. Dark overlay taake text chamke
    overlay = Image.new("RGBA", (1280, 720), (0, 0, 0, 140))
    bg = Image.alpha_composite(bg.convert("RGBA"), overlay).convert("RGB")
    
    draw = ImageDraw.Draw(bg)
    
    # 3. Title saaf karo - 2 lines me todo
    text = title_text.strip()[:80]
    if len(text) > 25:
        mid = len(text)//2
        space_idx = text.rfind(' ', 0, mid+10)
        if space_idx != -1:
            line1 = text[:space_idx]
            line2 = text[space_idx+1:]
        else:
            line1 = text[:mid]
            line2 = text[mid:]
    else:
        line1 = text
        line2 = ""

    # Yahan fix lagaya hai
    line1 = fix_urdu(line1)
    line2 = fix_urdu(line2)

    font_big = get_urdu_font(85)
    font_small = get_urdu_font(75)

    # 4. Text draw - White + Black stroke
    def draw_centered_line(text_line, y, font):
        if not text_line.strip():
            return
        bbox = draw.textbbox((0,0), text_line, font=font, stroke_width=8)
        w = bbox[2] - bbox[0]
        x = (1280 - w) // 2
        # PIL ka naya stroke behtar hai aapke loop se
        draw.text((x, y), text_line, font=font, fill="white", stroke_width=8, stroke_fill="black")

    if line2:
        draw_centered_line(line1, 220, font_big)
        draw_centered_line(line2, 350, font_small)
    else:
        draw_centered_line(line1, 290, font_big)

    # 5. Brand text
    try:
        small_font = get_urdu_font(35)
        draw.text((30, 670), "World Trending Hub", font=small_font, fill=(255,255,255))
    except:
        pass

    bg.save(output_path, quality=95)
    print(f"Thumbnail Done: {output_path}", flush=True)
    return output_path
