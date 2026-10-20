import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

YT_REFRESH_TOKEN = os.getenv("YT_REFRESH_TOKEN")
YT_CLIENT_ID = os.getenv("YT_CLIENT_ID")
YT_CLIENT_SECRET = os.getenv("YT_CLIENT_SECRET")

def get_youtube_service():
    print("Auth without scope issue...", flush=True)
    creds = Credentials(
        token=None,
        refresh_token=YT_REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=YT_CLIENT_ID,
        client_secret=YT_CLIENT_SECRET
    )
    return build("youtube", "v3", credentials=creds)

def upload_video(title, description, tags):
    video_path = "final_video.mp4"
    if not os.path.exists(video_path):
        video_path = "output/final_video.mp4"

    print(f"File: {video_path}", flush=True)
    youtube = get_youtube_service()

    body = {
        "snippet": {
            "title": title[:95],
            "description": description,
            "tags": tags.split(",") if isinstance(tags, str) else tags,
            "categoryId": "27"
        },
        "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False}
    }

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
    resp = youtube.videos().insert(part="snippet,status", body=body, media_body=media).execute()
    print(f"UPLOADED: https://youtube.com/watch?v={resp['id']}", flush=True)
    return resp
