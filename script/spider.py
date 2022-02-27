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
        "root": f"https://img.xchina.xyz/photos/{gid}/",
        "data": []
    }
    for i in range(1, 1+pages):
        d = {
            "thumbnail": f"{i:04d}_300x0.jpg",
            "enlarged": f"{i:04d}.jpg",
            "eWidth": 0,
            "eHeight": 0,
            "tWidth": 0,
            "tHeight": 0,
        }
        try:
            response = requests.get(f"https://img.xchina.xyz/photos/{gid}/{d['thumbnail']}", headers=headers, timeout=15)
            d["tWidth"], d["tHeight"] = Image.open(BytesIO(response.content)).size

            response = requests.get(f"https://img.xchina.xyz/photos/{gid}/{d['enlarged']}", headers=headers, timeout=15)
            d["eWidth"], d["eHeight"] = Image.open(BytesIO(response.content)).size

            data["data"].append(d)
            print(d["enlarged"], " done")
        except:
            print(d['enlarged'], "fail..................")

        
        
        time.sleep(random.random())
    with open(f"data/{gid}.json", 'w') as f:
        json.dump(data, f)

tojson("61eb0967af7e1", 480, "国模苏菲亚宾馆人体私拍套图")
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
