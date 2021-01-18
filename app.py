from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)


app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 5000 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만들거나 사용합니다.

# DB에 저장할 영화인들의 출처 url을 가져옵니다.
# HTML을 주는 부분
@app.route('/')
def get_home_page():
    return render_template('index.html')

@app.route('/news')
def get_news_page():
    return render_template('news.html')

@app.route('/process')
def get_process_page():
    return render_template('process.html')


@app.route('/news/kor', methods=['GET'])
def get_korean_news():
    # 1. mongoDB에서 _id 값을 제외한 모든 데이터 조회해오기(Read)
    articles = list(db.articles.find({'isKor': True}, {'_id': 0}))

    # 2. articles라는 키 값으로 articles 정보 보내주기
    return jsonify({'result': 'success', 'articles': articles})

@app.route('/news/eng', methods=['GET'])
def get_english_news():
    # 1. mongoDB에서 _id 값을 제외한 모든 데이터 조회해오기(Read)
    articles = list(db.articles.find({'isKor': False}, {'_id': 0}))

    # 2. articles라는 키 값으로 articles 정보 보내주기
    return jsonify({'result': 'success', 'articles': articles})

if __name__ == '__main__':
    app.run('0.0.0.0', port=27017, debug=True)

