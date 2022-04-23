import requests
from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString
import os, time, random
SAVE_PATH = "./"
ROOT = "https://99zipai.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36",
}



def article(url):
    r = requests.get(ROOT+url, headers=HEADERS)
    if r.status_code != 200:
        print(r.text)
    assert r.status_code == 200
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, "html.parser")
    title = soup.find("div", attrs={"class": "item_title"}).h1.text.strip()
    div = soup.find("div", attrs={"class": "content_left"})
    content = [title]
    for idx, ele in enumerate(div.contents):
        if isinstance(ele, Tag):
            if ele.name == "img":
                if isinstance(content[-1], str):
                    content.append([ele.get("src")])
                else:
                    content[-1].append(ele.get("src"))
        elif isinstance(ele, NavigableString):
            t = ele.strip()
            if t != "":
                t = t.replace("\n", "")
                content.append(t)
        else:
            print("Unknown :", type(ele), ele)
    print(content)
    
def worklist(uid):
    url = f"{ROOT}/my/{uid}/"
    r = requests.get(url, headers=HEADERS)
    assert r.status_code == 200, r.text
    r.encoding = r.apparent_encoding
    # print(r.text)
    soup = BeautifulSoup(r.text, "html.parser")
    h2 = soup.find(name="h2", attrs={"itemprop": "name"})
    print(h2.text)
    ul = soup.find(name="ul", attrs={"class": "ul_author_list cl"})
    for idx, li in enumerate(ul.findAll("li")):
        a = li.a
        print(a.text, ROOT+"/"+a.get("href"))


# worklist("93")
# article("/selfies/202105/121680.html")
article("/selfies/202105/121680.html")
