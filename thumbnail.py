from PIL import Image, ImageDraw, ImageFont
import os, glob, random, re, requests

W, H = 1280, 720
BORDER = 24
FONT_URL = "https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoNastaliqUrdu/NotoNastaliqUrdu-Bold.ttf"
FONT_PATH = "NotoNastaliqUrdu-Bold.ttf"

def ensure_font():
    if os.path.exists(FONT_PATH):
        return FONT_PATH
    # Try other names
    for p in ["Jameel Noori Nastaleeq.ttf", "NotoNastaliqUrdu-Bold.ttf"]:
        if os.path.exists(p):
            return p
    print(f"Downloading Urdu font...", flush=True)
    try:
        r = requests.get(FONT_URL, timeout=30)
        if r.status_code == 200:
            open(FONT_PATH, "wb").write(r.content)
            print(f"Font downloaded: {FONT_PATH}", flush=True)
            return FONT_PATH
    except Exception as e:
        print(f"Font download fail: {e}", flush=True)
    return None

def wrap_text(text, limit=20):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        if len(cur + " " + w) <= limit:
            cur = (cur + " " + w).strip()
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines[:3]

def safe_urdu(text):
    # Agar reshaper hai to use karo warna simple
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)
    except:
        return text

def generate_thumbnail(title_text, image_paths=None):
    print(f"[THUMBNAIL] Title: {title_text}", flush=True)
    font_file = ensure_font()
    
    # Background
    bg_files = glob.glob("images/*.jpg") + glob.glob("output/*.jpg")
    if bg_files:
        try:
            bg = Image.open(random.choice(bg_files)).convert("RGB").resize((W, H))
        except:
            bg = Image.new("RGB", (W, H), (25,25,25))
    else:
        bg = Image.new("RGB", (W, H), (25,25,25))

    dark = Image.new("RGB", (W, H), (0,0,0))
    bg = Image.blend(bg, dark, 0.5)
    
    # Font load - YEHI FIX HAI
    if font_file and os.path.exists(font_file):
        try:
            big_font = ImageFont.truetype(font_file, 110)
        except Exception as e:
            print(f"Font load error {e}, using DejaVu", flush=True)
            big_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 90)
    else:
        # Fallback - English me likh dega taake fail na ho
        print("No Urdu font, using English fallback font", flush=True)
        big_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 80)
        # Urdu ko Roman me convert kar do taake error na aaye
        title_text = re.sub(r'[^\x00-\x7F]+', ' ', title_text) # non-ascii hatao
        if not title_text.strip():
            title_text = "Qayamat Ki Nishani"

    draw = ImageDraw.Draw(bg)
    lines = wrap_text(title_text, 22)
    fixed = [safe_urdu(l) for l in lines]

    y = 180
    for line in fixed:
        try:
            bbox = draw.textbbox((0,0), line, font=big_font, stroke_width=12)
            tw = bbox[2] - bbox[0]
        except:
            tw = 600
        x = (W - tw)//2
        # Peela + kala stroke
        try:
            draw.text((x, y), line, font=big_font, fill="#FFEB00", stroke_width=14, stroke_fill="black")
        except UnicodeEncodeError:
            # Last resort - English
            draw.text((x, y), "Qayamat Ki Nishani", font=big_font, fill="#FFEB00", stroke_width=10, stroke_fill="black")
        y += 150

    final_img = Image.new("RGB", (W+BORDER*2, H+BORDER*2), "red")
    final_img.paste(bg, (BORDER, BORDER))
    
    os.makedirs("output", exist_ok=True)
    for p in ["output/thumbnail.jpg", "thumbnail.jpg"]:
        final_img.save(p, quality=95)
    
    print(f"[THUMBNAIL] Done", flush=True)
    return "output/thumbnail.jpg"

# Compatibility - is liye tumhara error aa raha tha
def create_thumbnail(t): return generate_thumbnail(t)
def make_thumbnail(t): return generate_thumbnail(t)
def create(t): return generate_thumbnail(t)
