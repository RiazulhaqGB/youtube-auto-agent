import os
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def get_authenticated_service():
    # GitHub Secrets se credentials lo
    client_id = os.getenv("YOUTUBE_CLIENT_ID")
    client_secret = os.getenv("YOUTUBE_CLIENT_SECRET")
    refresh_token = os.getenv("YOUTUBE_REFRESH_TOKEN")
    
    if not all([client_id, client_secret, refresh_token]):
        raise Exception("YOUTUBE secrets missing! Settings -> Secrets me check karo")
    
    # token.json ko GitHub pe live banao
    creds_data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "type": "authorized_user"
    }
    
    # Temp token.json banao
    with open("token.json", "w") as f:
        json.dump(creds_data, f)
    
    print("token.json created from secrets", flush=True)
    
    creds = Credentials.from_authorized_user_file("token.json", ["https://www.googleapis.com/auth/youtube.upload"])
    return build("youtube", "v3", credentials=creds)

def upload_video(video_path, title, description, tags=[]):
    youtube = get_authenticated_service()
    
    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "22"
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False
        }
    }
    
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype="video/*")
    print(f"Uploading: {title}", flush=True)
    response = youtube.videos().insert(part="snippet,status", body=request_body, media_body=media).execute()
    print(f"Uploaded! Video ID: {response['id']}", flush=True)
    return response
