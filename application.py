from flask import Flask, g, render_template, request, redirect, url_for, session, abort
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

    messages = db.relationship('Message',
                               backref=db.backref('writer', lazy='joined'),
                               lazy='dynamic')


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    writer_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.Text, nullable=False)

    def __init__(self, writer_user_id, content):
        self.writer_user_id = writer_user_id
        self.content = content

    def __repr__(self):
        return '<Message %r>' % self.id


def get_countdown():
    return datetime(2017, 11, 16) - datetime.now()


@app.before_request
def before_request():
    ''' 매 요청 전에 실행 '''
    g.countdown = get_countdown()

    if 'user_id' in session:
        g.user = User.query.filter_by(id=session['user_id']).one()
    else:
        g.user = None


@app.teardown_request
def teardown_request(exception):
    ''' 매 요청 마지막에 실행 '''
    pass


@app.route('/')
def index():
    user = None
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.filter_by(id=user_id).one()

    comments = Message.query.all()
    return render_template('index.html', comments=comments)


@app.route('/users/<int:user_id>')
def user_profile(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return abort(404)

    return render_template('profile.html', user=user)


@app.route('/new_comment')
def new_comment():
    return render_template('write.html')


@app.route('/new_comment', methods=['POST'])
def post_comment():
    if not g.user:
        return abort(401)

    message = Message(writer_user_id=g.user.id,
                      content=request.form['content'])
    db.session.add(message)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/signup')
def signup_form():
    return render_template('signup.html')


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

    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
