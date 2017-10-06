from flask import Flask, render_template, request, url_for, redirect, session
import config
from models import User, Question, Comment
from exts import db
from decorators import login_required
from sqlalchemy import or_

# initialize a Flask object with argument __name__
app = Flask(__name__)
# import configuration file to set config properties
app.config.from_object(config)
# SQLAlchemy from flask-sqlalchemy moudule has a instanse db
# db initialized with no argument ,so need init_app(app)
db.init_app(app)


@app.route('/')
def index():
    questions = Question.query.order_by('-create_time').all()
    return render_template("index.html", questions=questions)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter(User.username == username, User.password == password).first()
        if user:
            session['user_id'] = user.id
            session.permanent = True
            return redirect(url_for("index"))
        else:
            return render_template('error.html', message='用户名或密码不正确,请检查!')


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # 数据校验
        user1 = User.query.filter(User.telephone == telephone).first()
        user2 = User.query.filter(User.username == username).first()
        if user1:
            return render_template('error.html', message='该手机号已被注册,请更换手机号!')
        elif user2:
            return render_template('error.html', message='该用户名已被注册,请更换用户名!')
        elif password1 != password2:
            return render_template('error.html', message='密码与确认密码不一致!')
        else:
            user = User(telephone=telephone, username=username, password=password1)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("login"))


@app.context_processor
def context_processor():
    user_id = session.get("user_id")
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user': user}
    else:
        return {}


@app.route("/logout/")
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route("/question/", methods=['GET', 'POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template("question.html")
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        user_id = session.get("user_id")
        user = User.query.filter(User.id == user_id).first()
        question = Question(title=title, content=content)
        question.author = user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for("index"))


@app.route('/search/', methods=['GET'])
def search():
    keywords = request.args.get('keywords')
    # condition = '%{}%'.format(keywords)
    # questions = Question.query.filter(Question.title.like(condition)).order_by('-create_time').all()
    questions = Question.query.filter(
        or_(Question.content.contains(keywords), Question.title.contains(keywords))).order_by('-create_time').all()
    return render_template("index.html", questions=questions)


@app.route("/detail/<question_id>")
def detail(question_id):
    question = Question.query.filter(Question.id == question_id).first()
    # comments = Comment.query.filter(Comment.question_id == question_id).order_by('-comment_time').all()
    total_comment = len(question.comments)
    return render_template("detail.html", question=question,
                           comments=question.comments, total_comment=total_comment)


@app.route("/add_comment", methods=['POST'])
@login_required
def comment():
    comment = request.form.get('comment')
    question_id = request.form.get('question_id')
    user_id = session.get("user_id")
    comment_obj = Comment(comment_content=comment, question_id=question_id, user_id=user_id)
    db.session.add(comment_obj)
    db.session.commit()
    return redirect(url_for("detail", question_id=question_id))


if __name__ == '__main__':
    app.run()
