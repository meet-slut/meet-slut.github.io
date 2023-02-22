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
# cids = [
#     "778076",
#     "776928",
#     "776932",
#     "776936",
#     "776645",
#     "776444",
#     "776462",
#     "765596",
#     "765597",
#     "765598",
#     "759226",
#     "759228",
#     "752388",
#     "746944",
#     "748321",
#     "750133",
#     "699494",
#     "688746",
#     "688756",
#     "675710",
#     "667985",
#     "663706",
#     "658471",
#     "636714",
#     "636723",
#     "636517",
#     "636440",
#     "636215",
#     "636125",
#     "636075",
#     "635902",
#     "635673",
#     "632502",
#     "622067",
#     "613130",
#     "613201",
#     "612919",
#     "612956",
#     "593516",
#     "589994",
#     "589996",
#     "589999",
#     "590001",
#     "585844",
#     "585847",
#     "585407",
#     "585409",
#     "583866",
#     "583869",
#     "583847",
#     "552298",
#     "551878"
# ]

cids = [
"274622", # [浪漫書店 (ML)] 人妻管理人～団地にいる人妻は全員俺が管理する [中国翻訳]
"25303", # [ツンデレお肉 (ぽんち)] ボテ腹でヤりまくり!!!堕落ビッチ性活 [中国翻訳]
"32357", # [甚助屋 (甚助)] 牝課長 女下座 [中国翻訳] [DL版]
"31916", # [甚助屋 (甚助)] 続・牝課長女下座 犠牲妻 [中国翻訳] [DL版]
"52517", # [BLACK FORCE] 愛する叔母が不良に催眠を掛けられ僕の目の前で性的玩具にされていく日々 [中国翻訳]
"646986", # [BLACK FORCE] 大好きな幼馴染の凌辱寝取られビデオレター [中国翻訳]
"55902", # [さーくるスパイス] 地味だけどエロい身体したお母さんを風俗堕ち寸前で救った母子相姦 [中国翻訳]
"300641", # [フリーハンド魂 (フリーハンド)] オカズは今日も、妻のボテ腹濃厚セックス。[中国翻訳]
"480181", # [瑠璃りんご] SEXだけは上手いチャラ男にどはまりしちゃった奥さんの寝取られ性活 [中国翻訳]
"618546", # [三乳亭 (三乳亭しん太)] 失踪した妻からの寝取られビデオレター [中国翻訳]
"619293", # [三乳亭しん太] 人妻限定セックスコンパニオン [中国翻訳] [DL版]
"706455", # [三乳亭しん太] 寝取って欲しいと貸し出した妻が本当に寝取られた [中国翻訳]
"742994", # [三乳亭しん太] 妻が調教師の玩具になりました。 (コミック エグゼ 09) [中国翻訳] [DL版]
"391377", # [堀江耽閨] 熟女ゲーム [中国翻訳]
"383063", # [堀江耽閨] 熟女ゲーム 2 [中国翻訳]
"383061", # [堀江耽閨] 熟女ゲーム 3 [中国翻訳]
"383024", # [堀江耽閨] 熟女ゲーム 4 [中国翻訳]
"382823", # [堀江耽閨] 熟女ゲーム 5 [中国翻訳]
"480181", # [瑠璃りんご] SEXだけは上手いチャラ男にどはまりしちゃった奥さんの寝取られ性活 [中国翻訳]
"522993", # [瑠璃りんご] ハメまくりの停止世界～時間を止めればカースト頂点のエリート牝でも毎日勝手に種付けし放題～ [中国翻訳]
"616923", # [割り箸効果] 潔癖堅物な妻のセックスはメス豚時代の下品仕様 [中国翻訳]
"749326", # [ドーシア (テラスMC)] 奴隷家族 [中国翻訳]
"529290", # [規制当局 (リヒャルト・バフマン)] 放課後代理妻 義父は娘を孕ませたい [中国翻訳] [DL版]
"694591", # [規制当局 (リヒャルト・バフマン)] 放課後代理妻2 僕の彼女は父親に種付けされている [中国翻訳] [DL版]
"701477", # [規制当局 (リヒャルト・バフマン)] 放課後代理妻3 卒業式は妊婦で… [中国翻訳] [DL版]
]
with open(f"../photo/data/comic.json", 'r', encoding="utf-8") as f:
    lists = json.load(f)
    # lists["data"].clear()


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