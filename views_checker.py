import os, time
from youtube import get_views
if os.path.exists("last_upload.txt"):
    vid, ts, topic = open("last_upload.txt").read().split(",",2)
    if time.time() - int(ts) > 86400: # 24 hours
        v=get_views(vid)
        print(f"Video {vid} views {v}")
        if v < 100:
            open("low_views.txt","w").write(topic)
            print("Low views, next topic will be changed")
