import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def get_youtube_service():
    creds=Credentials(token=None, refresh_token=os.getenv("YT_REFRESH_TOKEN"), token_uri="https://oauth2.googleapis.com/token", client_id=os.getenv("YT_CLIENT_ID"), client_secret=os.getenv("YT_CLIENT_SECRET"))
    return build("youtube", "v3", credentials=creds)

def upload_video(title, description, tags, thumb_path=None):
    youtube=get_youtube_service()
    video_path="final_video.mp4" if os.path.exists("final_video.mp4") else "output/final_video.mp4"
    body={"snippet":{"title":title[:95],"description":description,"tags":tags.split(",") if isinstance(tags,str) else tags,"categoryId": "24"},"status":{"privacyStatus":"public","selfDeclaredMadeForKids":False}}
    media=MediaFileUpload(video_path,chunksize=-1,resumable=True)
    resp=youtube.videos().insert(part="snippet,status", body=body, media_body=media).execute()
    vid=resp['id']
    if thumb_path and os.path.exists(thumb_path):
        youtube.thumbnails().set(videoId=vid, media_body=MediaFileUpload(thumb_path)).execute()
    print(f"UPLOADED: https://youtube.com/watch?v={vid}",flush=True)
    return resp

def get_views(video_id):
    youtube=get_youtube_service()
    r=youtube.videos().list(part="statistics", id=video_id).execute()
    if r["items"]: return int(r["items"][0]["statistics"].get("viewCount",0))
    return 0
