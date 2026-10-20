import os
import json
import re
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def get_authenticated_service():
    client_id = os.getenv("YT_CLIENT_ID")
    client_secret = os.getenv("YT_CLIENT_SECRET")
    refresh_token = os.getenv("YT_REFRESH_TOKEN")
    
    if not all([client_id, client_secret, refresh_token]):
        raise Exception("YT secrets missing!")
    
    creds_data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "type": "authorized_user"
    }
    
    with open("token.json", "w") as f:
        json.dump(creds_data, f)
    
    creds = Credentials.from_authorized_user_file("token.json", ["https://www.googleapis.com/auth/youtube.upload"])
    return build("youtube", "v3", credentials=creds)

def clean_tags(tags_list):
    clean = []
    for tag in tags_list:
        # sirf letters, numbers, space rakho, 30 char se zyada nahi
        t = re.sub(r'[^a-zA-Z0-9 ]', '', str(tag)).strip()
        if t and len(t) >= 2 and len(t) <= 25:
            clean.append(t)
        if len(clean) >= 12:  # max 12 tags
            break
    # agar abhi bhi khali ho to default tags
    if not clean:
        clean = ["history", "facts", "story"]
    return clean

def upload_video(video_path, title, description, tags=[]):
    youtube = get_authenticated_service()
    
    # Tags ko saaf karo - yahi error tha!
    safe_tags = clean_tags(tags)
    print(f"Original tags: {tags} -> Clean tags: {safe_tags}", flush=True)

    request_body = {
        "snippet": {
            "title": title[:90],  # title 100 se kam hona chahiye
            "description": description[:4000],
            "tags": safe_tags,
            "categoryId": "22"
        },
        "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False}
    }
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype="video/*")
    print(f"Uploading: {title}", flush=True)
    response = youtube.videos().insert(part="snippet,status", body=request_body, media_body=media).execute()
    print(f"Uploaded! ID: {response['id']}", flush=True)
    return response
