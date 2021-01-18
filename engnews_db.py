import requests
from pymongo import MongoClient
from selenium import webdriver
from bs4 import BeautifulSoup
import time
client = MongoClient('localhost', 27017)
db = client.dbsparta
# 내장 라이브러리이므로 설치할 필요가 없습니다.
# 셀레니움을 실행하는데 필요한 크롬드라이버 파일을 가져옵니다.
chrome_path = '/Users/apple/Desktop/sparta/projects/recycling/chromedriver'
driver = webdriver.Chrome(chrome_path)
# news 페이지 url을 입력합니다.
url = 'https://news.google.com/search?q=recycling&hl=en-US&gl=US&ceid=US%3Aen'
# 크롬을 통해 네이버 주식페이지에 접속합니다.
driver.get(url)
# 정보를 받아오기까지 2초를 잠시 기다립니다.
time.sleep(2)
def get_articles_google():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get('https://news.google.com/search?q=recycling&hl=en-US&gl=US&ceid=US%3Aen', headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    uls = soup.select('#div.93789 > a.VDXfz')
    urls = []
    for ul in uls:
        a = ul.select_one('article > a')
        if a is not None:
            url = a['href']
            urls.append(url)
    return urls
# 출처 url로부터 뉴스의 사진, 제목, 기사 정보를 가져오고 news 콜렉션에 저장합니다.
def insert_engarticles(url):
    headers = {
        'accept-charset': 'UTF-8',
        'Content-Type': 'text/html; charset=utf-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    title = soup.select_one('meta[property="og:title"]')["content"]
    image = soup.select_one('meta[property="og:image"]')["content"]
    desc = soup.select_one('meta[property="og:description"]')["content"]
    doc = {
        'title': title,
        'image': image,
        'description': desc,
        'isKor': False,
        'url': url,
    }
    db.engarticles.insert_one(doc)
    print('완료!', title)
    # 크롬을 종료합니다.

urls = get_articles_google()
for url in urls:
    insert_engarticles(url)
driver.quit()