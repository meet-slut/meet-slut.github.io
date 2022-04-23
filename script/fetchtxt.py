import re
import requests
from lxml import etree

def fetchBook(bid):
    url = f"https://aaread.space/book/{bid}"
    r = requests.get(url, headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"})
    html = etree.HTML(r.text)

    info = html.xpath("//div[@class='book-information cf']/div[@class='book-info']")[0]
    title = info.xpath("h1/em/text()")[0]
    author = info.xpath("h1/a/text()")[0].strip()[:-2]
    labels = info.xpath("p/span/i/text()")
    total = (info.xpath("p[@class='total']/span/text()")[0].strip(), info.xpath("p[@class='total']/em/text()")[0].strip())
    intro = info.xpath("p[@class='intro']/text()")[0].strip()

    ul = html.xpath("//div[@class='volume']/ul[@class='cf']")[0]
    chapters = []
    for i, j, k in zip(ul.xpath("li/a/@title"), ul.xpath("li/a/@href"), ul.xpath("li/a/text()")):
        matchobj = re.search("发布时间：(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) 章节字数：(\d+)", i)
        date, words = matchobj.groups()
        chapterid = j.split("/")[-1]
        subtitle = k.strip()
        chapters.append([chapterid, subtitle, date, words])
    
    data = {
        "bookid": bid,
        "title": title,
        "author": author,
        "labels": labels,
        "total": total,
        "intro": intro,
        "chapters": chapters
    }
    # data = {k: eval(k) for k in ["title", "author", "labels", "total", "intro", "chapters"]}
    print(data)

    return data
    

def fetchChapter(bid, cid):
    url = "https://aaread.space/ajax/chapter/chapterContent.php"
    params = {
        "bookId": bid,
        "chapterId": cid,
        "authorId": 0
    }
    r = requests.get(url, params=params, headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"})

    text = r.json()["data"]["chapterInfo"]["content"]
    c = re.search("<style> \.(.*) {display:none;}</style>", text).group(1)
    text = re.sub("<style> .* {display:none;}</style>", "", text)
    pattern = "<[^p]+ class='"+c+"'>.*?</[^p]+>"
    text = re.sub(pattern, "", text)
    
    html = etree.HTML(text)

    paragraphs = []
    for p in html.xpath("//p/text()"):
        p = p.strip()
        if p:
            paragraphs.append(p)
    print(paragraphs)


if __name__ == "__main__":
    # fetchBook("2059")
    fetchChapter("2059", '136422')