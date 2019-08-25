import urllib.request
import re
import pymongo


MONGO_DB = 'qiushibaike'
MONGO_URI = 'localhost'
collection = 'joke'


def save_to_mongo(item):
    client = pymongo.MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    db[collection].insert(item)


def joke_crawler(url, count):
    headers = {
        "User-Agent": "Mozilla/5.0(Windows NT6.1; WOW64)AppleWebKit/537.36(KHTML,likeGecko)Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36"
    }
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)
    HTML = response.read().decode("utf-8")
    pat = r'<div class="author clearfix">(.*?)<span class="stats-vote"><i class="number">'
    re_joke = re.compile(pat, re.S)
    divList = re_joke.findall(HTML)
    dic = {}
    for div in divList:
        count += 1
        # 用户名
        re_u = re.compile(r'<h2>(.*?)</h2>', re.S)
        username = re_u.findall(div)
        username = username[0]
        # 段子
        re_d = re.compile(r'<div class="content">\n<span>(.*?)</span>', re.S)
        duanzi = re_d.findall(div)
        duanzi = duanzi[0]
        item = {}
        item['username'] = username.strip()
        item['content'] = duanzi.strip().replace('<br>', '').replace('<br/>', '')
        dic[str(count)+username] = duanzi
        save_to_mongo(item)
    return dic


count = 0
for i in range(1, 11):
    url = "https://www.qiushibaike.com/text/page/"+str(i)+"/"
    info = joke_crawler(url, count)
    for k, v in info.items():
        with open(r"F:\PycharmProject\Files\joke.txt", "a", encoding="utf-8")as f1:
            f1.write(k + "说：" + v)
