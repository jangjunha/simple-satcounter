from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime


app = Flask(__name__)


comments = [
    {
        'writer': '김희규',
        'content': '많이 남은 것 같지? 많이 남았어'
    },
    {
        'writer': '장준하',
        'content': '♚♚히어로즈 오브 더 스☆톰♚♚가입시$$전원 카드팩☜☜뒷면100%증정※ ♜월드오브 워크래프트♜펫 무료증정￥ 특정조건 §§디아블로3§§★공허의유산★초상화♜오버워치♜겐지스킨￥획득기회@@@ 즉시이동http://kr.battle.net/heroes/ko/'
    }
]


@app.route('/')
def index():
    countdown = datetime(2017, 11, 16) - datetime.now()
    dday = countdown.days

    return render_template('index.html', countdown=dday, comments=comments)


@app.route('/new_comment')
def new_comment():
    return render_template('write.html')


@app.route('/new_comment', methods=['POST'])
def post_comment():
    print("작성자: %s" % request.form['writer'])
    print("내용: %s" % request.form['content'])

    comments.append({
        'writer': request.form['writer'],
        'content': request.form['content']
    })

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
