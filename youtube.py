from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
import os

def upload_video(file_path, title, description, thumbnail_path=None):
    # Secrets se token lega
    creds = Credentials.from_authorized_user_file("token.json", ["https://www.googleapis.com/auth/youtube.upload"])
    youtube = build("youtube", "v3", credentials=creds)

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {"title": title, "description": description, "categoryId": "22"},
            "status": {"privacyStatus": "public"}
        },
        media_body=MediaFileUpload(file_path, resumable=True)
    )
    response = request.execute()
    video_id = response["id"]
    print(f"Uploaded Video ID: {video_id}")

    # Thumbnail upload
    if thumbnail_path and os.path.exists(thumbnail_path):
        youtube.thumbnails().set(videoId=video_id, media_body=MediaFileUpload(thumbnail_path)).execute()
        print("Thumbnail Uploaded!")
    
    return video_id
