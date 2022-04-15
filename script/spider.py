from io import BytesIO
import requests
from PIL import Image

# img_url = "https://profile.csdnimg.cn/F/6/F/3_cyj5201314"
# response = requests.get(img_url)
# f = BytesIO(response.content)
# img = Image.open(f)
# print(img.size)

import time
import random
import json


def tojson(gid, pages, title):
    headers = {
        "referer": f"https://xchina.xyz/photo/id-{gid}.html",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
    }
    data = {
        "title": title,
        "gid": gid,
        "root": "https://img.xchina.club/photos",
        "data": []
    }
    failed = []
    for i in range(1, 1+pages):
        thumbnail = f"{i:04d}_300x0.jpg"
        enlarged = f"{i:04d}.jpg"

        try:
            response = requests.get(f"{data['root']}/{gid}/{thumbnail}", headers=headers, timeout=15)
            tWidth, tHeight = Image.open(BytesIO(response.content)).size
            response = requests.get(f"https://img.xchina.club/photos/{gid}/{enlarged}", headers=headers, timeout=15)
            eWidth, eHeight = Image.open(BytesIO(response.content)).size
            data["data"].append([thumbnail, tWidth, tHeight, enlarged, eWidth, eHeight])

            print(enlarged, " done")
        except:
            print(enlarged, "fail..................")
            failed.append(i)
        time.sleep(random.random()/3)

    print(failed)
    with open(f"{gid}.json", 'w') as f:
        json.dump(data, f)
    print({"title": title, "gid": gid, "pages": pages})

tojson("624c53c714eb2", 913, "国模菲菲大尺度人体私拍套图")

"""
61ff6f9b010ec    国模苏雅大尺度人体私拍套图
614744206f460    国模紫嫣宾馆大尺度人体私拍套图
6148afc303653    国模王小妞宾馆大尺度人体私拍套图
61dab8c2c0b3e    国模李子瑶宾馆大尺度人体私拍套图
61a718ed0ccb7    国模龙馨宾馆大尺度人体私拍套图
61dac848d53d0    国模李梓熙野外大尺度私拍套图

61c6c28caa317    国模子欣宾馆大尺度人体私拍套图
61eb0967af7e1    国模苏菲亚宾馆人体私拍套图
"""
