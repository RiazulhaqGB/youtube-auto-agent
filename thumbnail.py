import os, requests
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

FONT_PATH = "NotoNastaliqUrdu.ttf"

# Ye 3 link 100% working hain
FONT_URLS = [
    "https://raw.githubusercontent.com/google/fonts/main/ofl/notonastaliqurdu/NotoNastaliqUrdu%5Bwght%5D.ttf",
    "https://raw.githubusercontent.com/google/fonts/main/ofl/notonastaliqurdu/NotoNastaliqUrdu-Regular.ttf",
    "https://github.com/google/fonts/raw/main/ofl/notonaskharabic/NotoNaskhArabic-Regular.ttf"
]

def get_urdu_font(size=80):
    # 1. Check agar file nahi hai to download karo
    if not os.path.exists(FONT_PATH) or os.path.getsize(FONT_PATH) < 50000:
        print(f"Font missing, downloading...", flush=True)
        for url in FONT_URLS:
            try:
                print(f"Trying: {url}", flush=True)
                r = requests.get(url, timeout=45, allow_redirects=True)
                print(f"Status: {r.status_code}, Size: {len(r.content)}", flush=True)
                if r.status_code == 200 and len(r.content) > 40000:
                    with open(FONT_PATH, "wb") as f:
                        f.write(r.content)
                    print(f"FONT SAVED: {FONT_PATH} -> {len(r.content)} bytes", flush=True)
                    break
            except Exception as e:
                print(f"Download error {url}: {e}", flush=True)

    # 2. Load karo
    if os.path.exists(FONT_PATH):
        try:
            return ImageFont.truetype(FONT_PATH, size)
        except Exception as e:
            print(f"Truetype error: {e}", flush=True)

    # 3. Agar sab fail ho jaye to crash na karo, default do
    print("WARNING: Using default font - Urdu will be boxes!", flush=True)
    return ImageFont.load_default()

def fix_urdu(text):
    try:
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)
    except:
        return text

def generate_thumbnail(title_text, image_paths=None):
    os.makedirs("output", exist_ok=True)
    output_path = "output/thumbnail.jpg"
    
    bg = None
    if image_paths and len(image_paths) > 0 and os.path.exists(image_paths[0]):
        try:
            bg = Image.open(image_paths[0]).convert("RGB").resize((1280, 720))
        except:
            pass
    if bg is None:
        bg = Image.new("RGB", (1280, 720), (20, 10, 30))
    
    overlay = Image.new("RGBA", (1280, 720), (0, 0, 0, 140))
    bg = Image.alpha_composite(bg.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(bg)
    
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

    line1 = fix_urdu(line1)
    line2 = fix_urdu(line2)

    font_big = get_urdu_font(85)
    font_small = get_urdu_font(75)

    def draw_centered_line(text_line, y, font):
        if not text_line.strip():
            return
        bbox = draw.textbbox((0,0), text_line, font=font, stroke_width=8)
        w = bbox[2] - bbox[0]
        x = (1280 - w) // 2
        draw.text((x, y), text_line, font=font, fill="white", stroke_width=8, stroke_fill="black")

    if line2:
        draw_centered_line(line1, 220, font_big)
        draw_centered_line(line2, 350, font_small)
    else:
        draw_centered_line(line1, 290, font_big)

    try:
        small_font = get_urdu_font(35)
        draw.text((30, 670), "World Trending Hub", font=small_font, fill=(255,255,255))
    except:
        pass

    bg.save(output_path, quality=95)
    print(f"Thumbnail Done: {output_path}", flush=True)
    return output_path
