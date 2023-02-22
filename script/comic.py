import os
import re
import json
import time
import random
import requests
from PIL import Image
from io import BytesIO

"""
function extract(url){
    s = url.split("=");
    return s[s.length-1];
}
var urls=[];
var a = $("h5.title a.apo");
for (let i=0; i<a.length; i++){urls.push(extract(a[i].href))}

"""

NUM_THREADS = 2
RETRY = 3

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36"
}

def exists(cid, lists):
    for d in lists['data']:
        if d['gid'] == cid:
            return True
    return False

def fetch(comic_id, num=None):
    params = {
        "route": "comic/readOnline",
        "comic_id": comic_id
    }
    r = requests.get(f"https://caitlin.top/index.php", params=params, headers=HEADERS)
    html = r.text

    title = re.search(r'<span class="d">(.+)<span>', html).group(1)
    title = title.replace(" ", "")

    root_url = re.search(r'HTTP_IMAGE = "(//.+)";', html).group(1)

    images = re.search(r'Image_List = (\[.+\]);', html).group(1)
    images = json.loads(images)
    images = [f"https:{root_url}{image['sort']}.{image['extension'] if image['extension'] in ['webp', 'jpg'] else 'jpg'}" for image in images]
    # images = [f"https:{root_url}{image['sort']}.jpg" for image in images]
    if isinstance(num, int):
        images = images[:num]
    return title, images

# cid = '658471'
# num = 36
cids = [
    "778076",
    "776928",
    "776932",
    "776936",
    "776645",
    "776444",
    "776462",
    "765596",
    "765597",
    "765598",
    "759226",
    "759228",
    "752388",
    "746944",
    "748321",
    "750133",
    "699494",
    "688746",
    "688756",
    "675710",
    "667985",
    "663706",
    "658471",
    "636714",
    "636723",
    "636517",
    "636440",
    "636215",
    "636125",
    "636075",
    "635902",
    "635673",
    "632502",
    "622067",
    "613130",
    "613201",
    "612919",
    "612956",
    "593516",
    "589994",
    "589996",
    "589999",
    "590001",
    "585844",
    "585847",
    "585407",
    "585409",
    "583866",
    "583869",
    "583847",
    "552298",
    "551878"
]

with open(f"../photo/data/comic.json", 'r', encoding="utf-8") as f:
    lists = json.load(f)
    lists["data"].clear()


for cid in cids:
    if exists(cid, lists):
        continue

    title, urls = fetch(cid)
    
    r = requests.get(urls[0], headers=HEADERS)
    im = Image.open(BytesIO(r.content))
    data = {
        "title": title,
        "gid": cid,
        "root": '',
        "data": [
            [url, im.width, im.height, url, im.width, im.height] for url in urls
        ]
    }
    with open(f"../photo/data/comic/{cid}.json", 'w', encoding="utf-8") as f:
        json.dump(data, f)

    lists['data'].append(
        {"title": title, "gid": cid, "pages": len(urls), "cover": urls[0]}
    )
    print(title)
    time.sleep(random.random())

lists['amount'] = len(lists['data'])
with open(f"../photo/data/comic.json", 'w', encoding="utf-8") as f:
    json.dump(lists, f)