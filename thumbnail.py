from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import textwrap

def generate_thumbnail(topic, output_path="thumbnail.jpg"):
    # FIX for new Pillow
    if not hasattr(Image, 'ANTIALIAS'):
        Image.ANTIALIAS = Image.LANCZOS

    # Pollinations se cricket background - ye hamesha chalega
    url = f"https://image.pollinations.ai/prompt/cricket stadium dramatic {requests.utils.quote(topic)}?width=1280&height=720&nologo=true"
    try:
        r = requests.get(url, timeout=20)
        img = Image.open(BytesIO(r.content)).convert("RGB")
        print(f"Background image loaded from Pollinations")
    except Exception as e:
        print(f"Background fail {e}, using black")
        img = Image.new("RGB", (1280,720), (20,20,20))
    
    draw = ImageDraw.Draw(img)
    
    # Font
    try:
        font = ImageFont.truetype("arial.ttf", 80)
    except:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
        except:
            font = ImageFont.load_default()

    # Text ko wrap karo taake screen se bahar na jaye
    wrapped_text = textwrap.fill(topic, width=18)
    
    # Laal border, peela text + thoda shadow
    x, y = 50, 200
    draw.text((x, y), wrapped_text, fill="yellow", stroke_width=10, stroke_fill="red", font=font)
    
    img.save(output_path)
    print(f"Thumbnail saved: {output_path}")
    return output_path
