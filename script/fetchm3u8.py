import os
import re
import json
import requests

with open("../video/data/playlist.json", "r", encoding="utf-8") as f:
    videos = json.load(f)

data = []
for item in videos:
    url = item["src"]
    r = requests.get(url)
    html = r.text
    video_duration = re.search(r'var video_duration = "(\d+)";', html).group(1)
    video_id = re.search(r'var video_id = "(\d+)";', html).group(1)
    poster = re.search(r'poster="(.+\.jpg)"', html).group(1)
    m3u8 = re.search(r'source src="(.+)"', html).group(1)
    player_logo_link = re.search(r'player_logo_link = "(http.+)";', html).group(1)
    title = player_logo_link.split("/")[-1]

    d = {
        "vid": video_id,
        "title": title,
        "duration": int(video_duration),
        "poster": poster,
        "m3u8": m3u8
    }
    data.append(d)
with open("../video/data/list.json", "w", encoding="utf-8") as f:
    json.dump(data, f)
print(data)


