import json
import os

file = "photo/data/6218fef298aa1"

with open(f"{file}.json", 'r', encoding="utf-8") as f:
    data = json.load(f)
images = data["data"]
title = data["title"]
gid = data["hash"]
pages = len(images)

data = {
    "title": title,
    "gid": gid,
    "root": "https://img.xchina.fun/photos",
    "data": []
}
print(images)
for i in range(pages):
    ele = images[i]
    data["data"].append([ele["thumbnail"], ele["tWidth"], ele["tHeight"], ele["enlarged"], ele["eWidth"], ele["eHeight"]])

print({
    "title": title,
    "gid": gid,
    "pages": pages
})
with open(f"{file}.json", 'w', encoding="utf-8") as f:
    json.dump(data, f)
