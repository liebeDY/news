import requests
from bs4 import BeautifulSoup
from slacker import Slacker
import time
import random

with open("C:/Users/clari/Desktop/python/smartstore/news_headline/token1.txt", "r") as f:
    token = f.read()
    
slack = Slacker(token)

with open("headers.txt", "r", encoding="utf-8") as f:
    header = f.read()

headers = {
    "User-Agent" : f"{header}"
}

now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

with open("newsUrl.txt", "r", encoding="utf-8") as f:
    url = f.read()

with open("politicsPageList.txt", "r", encoding="utf-8") as f:
    pageText_list = f.readline()
    page_list  = pageText_list.split(',')

with open("politicsCategorieList.txt", "r", encoding="utf-8") as f:
    text_list = f.readline()
    categorie_list  = text_list.split(',')

idx = 1
for page, categorie in zip(page_list, categorie_list)  :

    index = 1
    params = {
        'sid1' : '100',
        'sid2' : f'{page}'
    }

    response = requests.get(url, headers=headers, params=params )
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')

    titles = soup.select('#main_content > div.list_body.newsflash_body > ul > li > dl > dt > a')
    msg_list = []
    for title in titles :
        my_categorie = categorie +" " + str(index) + " 번째 기사 입니다"
        if title.text.strip() == "" :
            continue
        elif title.text.strip() == "동영상기사" :
            continue
        else :
            my_title = "[ " + title.text.strip() + " ]"
            my_link = title.get('href')
            msg_list.append(my_categorie)
            msg_list.append(my_title)
            msg_list.append(my_link)
            msg_list.append(" ")
            index += 1
    dateMsg = f"현재 시간 {now}"
    chanerName = f"#정치_0{idx}_{categorie}"
    msg = " \n ".join(msg_list)
    print(chanerName)
    print(msg)
    slack.chat.post_message(chanerName, msg)
    slack.chat.post_message(chanerName, dateMsg)
    slack.chat.post_message(chanerName, '----------완료되었습니다----------')
    time.sleep(random.randrange(2, 6, 1))
    idx = idx + 1
print("\n완료되었습니다.")