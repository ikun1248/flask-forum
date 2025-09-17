import wtforms
from flask import g
from wtforms.validators import Email,Length,EqualTo,InputRequired,Regexp
from models import UserModel,EmailCaptchaModel
from flask_wtf.file import FileAllowed, FileRequired, FileField,FileSize

from exts import db

class EmailForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message='邮箱格式错误')])

    def validate_email(self,field):
        email=field.data
        user=UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError('该邮箱已被注册')


class RegisterForm(wtforms.Form):
    email=wtforms.StringField(validators=[Email(message='邮箱格式错误')])
    captcha=wtforms.StringField(validators=[])
    username = wtforms.StringField(validators=[
        Length(min=4, max=12, message='用户名长度为4-12位'),
        Regexp(
            regex=r'^[A-Za-z0-9]+$',
            message='用户名只能包含英文和数字'
        )
    ])
    password=wtforms.StringField(validators=[Length(min=6,max=20,message='密码长度为6-20位')])
    password_confirm=wtforms.StringField(validators=[EqualTo('password',message='两个密码不一致')])

    def validate_email(self,field):
        email=field.data
        user=UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError('该邮箱已被注册')

    def validate_username(self,field):
        username=field.data
        user=UserModel.query.filter_by(username=username).first()
        if user:
            raise wtforms.ValidationError('该用户名已被使用')

    def validate_captcha(self,field):
        captcha=field.data
        email=self.email.data
        captcha_model=EmailCaptchaModel.query.filter_by(email=email,captcha=captcha).first()
        if not captcha_model:
            raise wtforms.ValidationError('验证码错误')

class QuestionForm(wtforms.Form):
    title=wtforms.StringField(validators=[Length(min=3,max=100,message='标题格式错误,输入范围在3-100')])
    content=wtforms.StringField(validators=[Length(min=3,message='内容字数在3个字以上')])

class AnswerForm(wtforms.Form):
    content=wtforms.StringField(validators=[Length(min=1,message='内容不能为空')])
    question_id=wtforms.IntegerField(validators=[InputRequired(message='必须要传入问题id')])

class AvatarUploadForm(wtforms.Form):
    avatar=wtforms.FileField(validators=[
        FileRequired(message='请选择头像'),
        FileAllowed(['jpg','png','jpeg','gif'],message='仅能上传图片'),
        FileSize(max_size=1024*1024*2,message="头像大小不能超过2MB")
    ])

class NicknameForm(wtforms.Form):
    nickname=wtforms.StringField(validators=[InputRequired(message='名称不能为空')])
    def validate_nickname(self,field):
        nickname=field.data
        user=UserModel.query.filter_by(nickname=nickname).first()
        if user and user!=g.user:
            raise wtforms.ValidationError('该昵称已被使用')

class PasswordResetForm(wtforms.Form):
    old_password=wtforms.StringField(validators=[Length(min=6,max=20,message='密码格式错误')])
    new_password=wtforms.StringField(validators=[Length(min=6,max=20,message='密码格式错误')])
    confirm_password=wtforms.StringField(validators=[EqualTo('new_password',message='两个密码不一致')])

class EmailResetFrom(wtforms.Form):
    captcha=wtforms.StringField(validators=[])
    new_email=wtforms.StringField(validators=[Email(message='邮箱格式错误')])
    def validate_captcha(self,field):
        captcha=field.data
        email=self.new_email.data
        captcha_model=EmailCaptchaModel.query.filter_by(email=email,captcha=captcha).first()
        if not captcha_model:
            raise wtforms.ValidationError('验证码错误')
        else:
            db.session.delete(captcha_model)
            db.session.commit()




