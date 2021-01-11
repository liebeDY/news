import requests
from bs4 import BeautifulSoup
from slacker import Slacker
import time
import random

with open("C:/Users/clari/Desktop/python/smartstore/news_headline/token1.txt", "r") as f:
    token = f.read()

print(token)

slack = Slacker(token)

headers = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
}

now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

# 정치 100 경제 101 사회 102 생활/문화 103 세계 104 IT/과학 105

url = "https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&"

# https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=101&sid2=259

page_list = ['264', '265', '268', '266', '267', '269']
categorie_list = ['청와대', '국회정당', '북한', '행정', '국방외교', '정치일반']
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
    slack.chat.post_message(chanerName, msg)
    slack.chat.post_message(chanerName, dateMsg)
    slack.chat.post_message(chanerName, '----------완료되었습니다----------')
    time.sleep(random.randrange(2, 6, 1))
    idx = idx + 1
print("\n완료되었습니다.")