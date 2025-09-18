from exts import db
from sqlalchemy import func
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

    questions=db.relationship('QuestionModel',back_populates='author')
    answers=db.relationship('AnswerModel',back_populates='author')
    likes=db.relationship('LikeModel',back_populates='user')
    view_histories=db.relationship('ViewLogModel',back_populates='user')


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
    category=db.Column(db.String(100),nullable=False)
    tags=db.Column(db.String(100))
    create_time=db.Column(db.DateTime,default=datetime.now)

    author_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    author=db.relationship(UserModel,back_populates='questions')

    likes=db.relationship('LikeModel',back_populates='question',cascade='all,delete-orphan')
    view_histories=db.relationship('ViewLogModel',back_populates='question',cascade='all,delete-orphan')
    answers=db.relationship('AnswerModel',back_populates='question',cascade='all,delete-orphan')

    @property
    def tag_list(self):
        return self.tags.split(',') if self.tags else []

    @staticmethod
    def get_all_category_counts():
        result=db.session.query(
            QuestionModel.category,
            func.count(QuestionModel.id)
        ).group_by(QuestionModel.category).all()
        return dict(result)


class AnswerModel(db.Model):
    __tablename__='answer'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    content=db.Column(db.Text,nullable=False)
    create_time=db.Column(db.DateTime,default=datetime.now)

    author_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    question_id=db.Column(db.Integer,db.ForeignKey('question.id'))
    author=db.relationship(UserModel,back_populates='answers')
    question=db.relationship(QuestionModel,back_populates='answers')

class LikeModel(db.Model):
    __tablename__='like'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    user=db.relationship(UserModel,back_populates='likes')
    question_id=db.Column(db.Integer,db.ForeignKey('question.id'))
    question=db.relationship(QuestionModel,back_populates='likes')

    create_time=db.Column(db.DateTime,default=datetime.now)
    is_active=db.Column(db.Boolean,default=True)

    __table_args__=(
        db.UniqueConstraint('user_id','question_id',name='unique_user_question_like'),
    )

class ViewLogModel(db.Model):
    __tablename__='view_log'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    count=db.Column(db.Integer,default=0)
    view_time=db.Column(db.DateTime,default=datetime.now)

    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    user=db.relationship(UserModel,back_populates='view_histories')
    question_id=db.Column(db.Integer,db.ForeignKey('question.id'))
    question=db.relationship(QuestionModel,back_populates='view_histories')

    @staticmethod
    def get_total_counts(question_id):
        total=(
            db.session.query(func.sum(ViewLogModel.count))
            .filter(ViewLogModel.question_id==question_id)
            .scalar()
        )
        return total or 0









