import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

YT_REFRESH_TOKEN = os.getenv("YT_REFRESH_TOKEN")
YT_CLIENT_ID = os.getenv("YT_CLIENT_ID")
YT_CLIENT_SECRET = os.getenv("YT_CLIENT_SECRET")

def get_youtube_service():
    print("Authenticating YouTube...", flush=True)
    creds = Credentials(
        None,
        refresh_token=YT_REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=YT_CLIENT_ID,
        client_secret=YT_CLIENT_SECRET,
        scopes=[
            "https://www.googleapis.com/auth/youtube.upload",
            "https://www.googleapis.com/auth/youtube"
        ]
    )
    # Force refresh
    from google.auth.transport.requests import Request
    creds.refresh(Request())
    print("Auth OK!", flush=True)
    return build("youtube", "v3", credentials=creds)

def upload_video(title, description, tags):
    print(f"Uploading: {title}", flush=True)
    video_path = "final_video.mp4"
    if not os.path.exists(video_path) and os.path.exists("output/final_video.mp4"):
        video_path = "output/final_video.mp4"
    
    if not os.path.exists(video_path):
        print(f"ERROR: Video not found {video_path}", flush=True)
        return

    youtube = get_youtube_service()
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
