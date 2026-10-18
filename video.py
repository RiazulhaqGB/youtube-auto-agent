import requests, random, os, time
from PIL import Image
from moviepy.editor import ImageClip, concatenate_videoclips

def get_topic_images(topic, num_images=5):
    """Topic ke hisab se 5 images download karega"""
    images = []
    
    # Topic se 5 alag prompts banao - taake har clip alag lage
    prompts = [
        f"{topic}, cricket stadium, dramatic, 4k",
        f"{topic}, close up action, cinematic lighting",
        f"Pakistan vs England cricket match, crowd cheering",
        f"{topic}, serious face, press conference",
        f"cricket ball hitting stumps, slow motion, 4k"
    ]

    os.makedirs("clips", exist_ok=True)

    for i in range(num_images):
        try:
            prompt = prompts[i % len(prompts)]
            # Seed random taake har bar new image aaye
            url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(prompt)}?width=1280&height=720&seed={random.randint(1,9999999)}&nologo=true"
            r = requests.get(url, timeout=30)
            if r.status_code == 200 and len(r.content) > 15000:
                path = f"clips/clip_{i}.jpg"
                open(path, "wb").write(r.content)
                images.append(path)
                print(f"Image {i+1} ready: {prompt}")
            time.sleep(2) # Thora gap taake block na ho
        except Exception as e:
            print(f"Image {i} fail: {e}")
            continue
    
    return images

def create_video_with_clips(image_paths, audio_path="voice.mp3", output_path="final_video.mp4"):
    """Har image ko 6 second ka clip banayega, zoom effect ke sath"""
    clips = []
    
    for img_path in image_paths:
        try:
            # Har clip 6 second ka
            clip = ImageClip(img_path, duration=6)
            
            # Zoom in effect - thora movement taake video lage, photo na lage
            # 1280x720 se thora zoom karega
            clip = clip.resize(lambda t: 1 + 0.08 * t) # 8% zoom in 6 sec me
            clip = clip.set_position(("center", "center")).resize((1280, 720))
            
            clips.append(clip)
        except Exception as e:
            print(f"Clip error {img_path}: {e}")

    if not clips:
        print("No clips found!")
        return None

    # Sab clips ko jor do - 5 clips x 6 sec = 30 sec video
    final_video = concatenate_videoclips(clips, method="compose")
    
    # Agar voice hai to usko laga do
    if os.path.exists(audio_path):
        from moviepy.editor import AudioFileClip
        audio = AudioFileClip(audio_path)
        # Video ko audio ke length tak cut karo
        final_video = final_video.set_duration(audio.duration)
        final_video = final_video.set_audio(audio)

    final_video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")
    print(f"FINAL VIDEO READY: {output_path}")
    return output_path

def generate_topic_video(topic, audio_file="voice.mp3"):
    images = get_topic_images(topic, num_images=5)
    if images:
        return create_video_with_clips(images, audio_file)
    return None

if __name__ == "__main__":
    generate_topic_video("Harry Brook Pakistan Team ke liye Khatra")
