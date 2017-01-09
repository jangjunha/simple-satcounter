from flask import Flask, g, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    writer = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __init__(self, writer, content):
        self.writer = writer
        self.content = content

    def __repr__(self):
        return '<Message %r>' % self.id


def get_countdown():
    return datetime(2017, 11, 16) - datetime.now()


@app.route('/')
def index():
    countdown = get_countdown()

    comments = Message.query.order_by('-id').all()
    return render_template('index.html', countdown=countdown, comments=comments)


@app.route('/new_comment')
def new_comment():
    countdown = get_countdown()
    return render_template('write.html', countdown=countdown)


@app.route('/new_comment', methods=['POST'])
def post_comment():
    message = Message(writer=request.form['writer'],
                      content=request.form['content'])
    db.session.add(message)
    db.session.commit()

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
