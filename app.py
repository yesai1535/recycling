from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)


app = Flask(__name__)

client = MongoClient('localhost', 5000)  # mongoDB는 5000 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만들거나 사용합니다.

# DB에 저장할 영화인들의 출처 url을 가져옵니다.
# HTML을 주는 부분
@app.route('/index')
def home():
    return render_template('index.html')

@app.route('/news')
def get_articles_naver():
    return render_template('news.html')

@app.route('/process')
def post_processes():
    return render_template('process.html')


# API 역할을 하는 부분
@app.route('/index', methods=['POST'])
def get_articles_naver():
    # 1. 클라이언트로부터 데이터를 받기
    url = request.form['url']
    title = request.form['title']
    desc = request.form['description']
    image = request.form['image']

    # 2. meta tag를 스크래핑하기
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    og_title = soup.select_one('meta[property="og:title"]')
    og_image = soup.select_one('meta[property="og:image"]')
    og_desc = soup.select_one('meta[property="og:description"]')

    title = og_title['content']
    desc = og_desc['content']
    image = og_image['content']

    doc = {
        'title': title,
        'image': image,
        'desc': desc,
        'url': url

    }

    article = {'url': url, 'title': title, 'desc': desc, 'image': image}

    # 3. mongoDB에 데이터를 넣기
    db.articles.insert_one(article)

    return jsonify({'result': 'success'})



@app.route('/news', methods=['GET'])
def read_articles():
    # 1. mongoDB에서 _id 값을 제외한 모든 데이터 조회해오기(Read)
    articles = list(db.articles.find({}, {'_id': 0}))

    # 2. articles라는 키 값으로 articles 정보 보내주기
    return jsonify({'result': 'success', 'articles': articles})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

