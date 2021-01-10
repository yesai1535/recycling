import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
client = MongoClient('localhost', 5000)
db = client.dbsparta
# DB에 저장할 뉴의 출처 url을 가져옵니다.


def get_articles_naver():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get('https://search.naver.com/search.naver?sm=tab_hty.top&where=news&query=%EB%B6%84%EB%A6%AC%EC%88%98%EA%B1%B0&oquery=filezilla&tqi=U%2FezJwp0YiRssc1P6zdssssstOs-022241', headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    uls = soup.select('# main_pack > section > div > div.group_news > ul')
    urls = []

    for ul in uls:
        a = ul.select_one('div.news_area > a')
        if a is not None:
            base_url = 'https://search.naver.com/search.naver?sm=tab_hty.top&where=news&query=%EB%B6%84%EB%A6%AC%EC%88%98%EA%B1%B0&oquery=filezilla&tqi=U%2FezJwp0YiRssc1P6zdssssstOs-022241'
            url = base_url + a['href']
            urls.append(url)
    return urls


# 출처 url로부터 뉴스의 사진, 제목, 기사 정보를 가져오고 news 콜렉션에 저장합니다.
def insert_articles(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    title = soup.select_one('#sp_nws1 > div.news_wrap.api_ani_send > div > a').text
    image = soup.select_one('#sp_nws1 > div.news_wrap.api_ani_send > a > img')['src']
    desc = soup.select_one('#sp_nws1 > div.news_wrap.api_ani_send > div > div.news_dsc > div > a').text
    doc = {
        'title': title,
        'image': image,
        'description': desc,
        'url': url,
    }
    db.articles.insert_one(doc)
    print('완료!', title)

# 기존 news 콜렉션을 삭제하고, 출처 url들을 가져온 후, 크롤링하여 DB에 저장합니다.
def insert_all():
    db.articles.drop()  # news 콜렉션을 모두 지워줍니다.
    urls = get_articles_naver()
    for url in urls:
        insert_articles(url)
### 실행하기
insert_all()