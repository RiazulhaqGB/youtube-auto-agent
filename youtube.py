import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

YT_REFRESH_TOKEN = os.getenv("YT_REFRESH_TOKEN")
YT_CLIENT_ID = os.getenv("YT_CLIENT_ID")
YT_CLIENT_SECRET = os.getenv("YT_CLIENT_SECRET")

def get_youtube_service():
    token_data = {
        "client_id": YT_CLIENT_ID,
        "client_secret": YT_CLIENT_SECRET,
        "refresh_token": YT_REFRESH_TOKEN,
        "type": "authorized_user"
    }
    creds = Credentials.from_authorized_user_info(token_data, ["https://www.googleapis.com/auth/youtube"])
    return build("youtube", "v3", credentials=creds)

def upload_video(title, description, tags):
    print(f"Uploading: {title}", flush=True)
    
    # VIDEO FILE FIX - hamesha final_video.mp4 hi upload hogi
    video_path = "final_video.mp4"
    if not os.path.exists(video_path):
        # backup search
        if os.path.exists("output/final_video.mp4"):
            video_path = "output/final_video.mp4"
        else:
            print(f"ERROR: Video file not found! {video_path}", flush=True)
            return

    print(f"Found video: {video_path}", flush=True)
    
    youtube = get_youtube_service()
    
    # Clean title - YouTube pe | wala issue nahi
    clean_title = title[:95] if len(title) > 95 else title
    
    body = {
        "snippet": {
            "title": clean_title,
            "description": description,
            "tags": tags.split(",") if isinstance(tags, str) else tags,
            "categoryId": "27"
        },
        "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False}
    }

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype="video/*")
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = request.execute()
    print(f"UPLOAD SUCCESS: https://youtube.com/watch?v={response['id']}", flush=True)
    return response
