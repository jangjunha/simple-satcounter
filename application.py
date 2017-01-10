from flask import Flask, g, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'development-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


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

    user = None
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.filter_by(id=user_id).one()

    comments = Message.query.order_by('-id').all()
    return render_template('index.html',
                           countdown=countdown,
                           comments=comments,
                           user=user)


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


@app.route('/signup')
def signup_form():
    countdown = get_countdown()
    return render_template('signup.html', countdown=countdown)


@app.route('/signup', methods=['POST'])
def signup():
    user = User()
    user.username = request.form['username']
    user.password = generate_password_hash(request.form['password'])
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user is None:
            error = '아이디 또는 비밀번호가 잘못되었습니다.'
        elif not check_password_hash(user.password, request.form['password']):
            error = '아이디 또는 비밀번호가 잘못되었습니다.'
        else:
            session['user_id'] = user.id
            return redirect(url_for('index'))

    countdown = get_countdown()
    return render_template('login.html', countdown=countdown, error=error)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
