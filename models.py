from exts import db
from datetime import datetime

class UserModel(db.Model):
    __tablename__='user'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    username=db.Column(db.String(20),nullable=False)
    gender=db.Column(db.String(2),default='男')
    nickname=db.Column(db.String(20),nullable=True)
    province=db.Column(db.String(10),nullable=True)
    city=db.Column(db.String(10),nullable=True)
    password=db.Column(db.String(255),nullable=False)
    email=db.Column(db.String(50),nullable=False,unique=True)
    join_time=db.Column(db.DateTime,default=datetime.now)
    avatar=db.Column(db.String(256),default='default.jpg')

class EmailCaptchaModel(db.Model):
    __tablename__='email_captcha'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    email=db.Column(db.String(50),nullable=False)
    captcha=db.Column(db.String(10),nullable=False)

class QuestionModel(db.Model):
    __tablename__='question'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    title=db.Column(db.String(100),nullable=False)
    content=db.Column(db.Text,nullable=False)
    create_time=db.Column(db.DateTime,default=datetime.now)

    author_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    author=db.relationship(UserModel,backref='questions')

class AnswerModel(db.Model):
    __tablename__='answer'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    content=db.Column(db.Text,nullable=False)
    create_time=db.Column(db.DateTime,default=datetime.now)

    author_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    question_id=db.Column(db.Integer,db.ForeignKey('question.id'))
    author=db.relationship(UserModel,backref='answers')
    question=db.relationship(QuestionModel,backref=db.backref('answers',order_by=create_time.desc()))

