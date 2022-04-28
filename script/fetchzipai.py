import requests
from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString
import os, time, random
import json
SAVE_PATH = "./"
ROOT = "https://99zipai.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36",
}



def article(url, confirm=False):
    aid = url.split("/")[-1].split(".")[0]
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
                src = ele.get("src")
                if "d/file/selfies" not in src:
                    continue
                if src.startswith("/"):
                    src = ROOT + src

                if isinstance(content[-1], str):
                    content.append([src])
                else:
                    content[-1].append(src)
        elif isinstance(ele, NavigableString):
            t = ele.strip()
            if t != "":
                t = t.replace("\n", "")
                content.append(t)
        else:
            print("Unknown :", type(ele), ele)
    if confirm:
        print(content)
        if input("Download [y/n]? ").lower()[0] != "y":
            return 
    with open(f"photo/data/zipai/{aid}.json", "w") as f:
        json.dump({"data": content}, f)
    print([str(aid), title])
    
def worklist(uid):
    # url = f"{ROOT}/my/{uid}/"
    url = f"https://99zipai.com/e/space/ulist.php?page=0&mid=1&line=80&tempid=10&orderby=&myorder=0&userid={uid}"
    r = requests.get(url, headers=HEADERS)
    assert r.status_code == 200, r.text
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, "html.parser")
    total = soup.find("a", attrs={"class": "sh_1"}).span.text.strip()

    user = soup.find(name="h2", attrs={"itemprop": "name"}).text.strip()
    print(total, user)
    ul = soup.find(name="ul", attrs={"class": "ul_author_list cl"})
    for idx, li in enumerate(ul.findAll("li")):
        a = li.a
        yield a.text, a.get("href")

def main(author):
    data = []
    for title, href in worklist(author):
        if input(f"Download {title}({ROOT+href})[y/n]?: ")[0].lower() == "y":
            article(href)
            data.append([href.split("/")[-1].split(".")[0], title])
    print(data[::-1])
        

# worklist("7744")
# article("/selfies/202105/121680.html")
# article("/selfies/202105/121680.html")

# for uid in range(1000, 1100):
#     for title, href in worklist(str(uid)):
#         print(title, ROOT+href)
#     if input(f"Continue [y/n]?: ")[0].lower() == "y":
#         pass
#     else:
#         break


# article("/selfies/201807/68971.html")
# main("12765")


while True:
    inp = input("$ ").strip()
    if inp.lower() == "exit":
        print("Exit system!")
        break
    elif inp.lower() == "pwd":
        print(f"pwd: {os.getcwd()}")
    elif inp.lower() == "":
        pass
    elif inp.split()[0].strip().lower() in ["article", "author"]:
        cmd, *args = inp.split()
        if cmd.strip() == "article":
            article(args[0], True)
        # print(cmd, args)
    else:
        print(f"Command {inp} is not defined!")


"""
https://99zipai.com/selfies/202111/127295.html
https://99zipai.com/selfies/202204/133807.html
https://99zipai.com/my/13871/
https://99zipai.com/my/13300/
https://99zipai.com/my/14097/
https://99zipai.com/my/4045/
# https://99zipai.com/selfies/202202/130208.html
https://99zipai.com/my/9926/
https://99zipai.com/my/13411/



"""