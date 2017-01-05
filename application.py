from flask import Flask, g, render_template, request, redirect, url_for
from datetime import datetime
import sqlite3


app = Flask(__name__)


def get_countdown():
    return datetime(2017, 11, 16) - datetime.now()


def get_db():
    db = getattr(g, '_database', None)

    if db is None:
        db = g._database = sqlite3.connect("satcounter.db")
    return db


@app.teardown_appcontext
def close_connection(expn):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    countdown = get_countdown()

    db = get_db()
    comments = db.execute("SELECT * FROM comments LIMIT 10").fetchall()
    return render_template('index.html', countdown=countdown, comments=comments)


@app.route('/new_comment')
def new_comment():
    countdown = get_countdown()
    return render_template('write.html', countdown=countdown)


@app.route('/new_comment', methods=['POST'])
def post_comment():
    db = get_db()
    db.execute(
        "INSERT INTO comments (writer, content) VALUES (?, ?)",
        (request.form['writer'], request.form['content'])
    )
    db.commit()

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
