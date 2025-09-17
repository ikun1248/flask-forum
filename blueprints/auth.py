from flask import Blueprint,render_template,request,jsonify,redirect,url_for,session,flash
from models import *
from exts import mail,db
from flask_mail import Message
import random,string
from .forms import *
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.datastructures import MultiDict
from sqlalchemy import or_

bp=Blueprint('auth',__name__,url_prefix='/auth')
@bp.route('/login',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('/login.html')
    else:
        username=request.form['username']
        password=request.form['password']
        user=UserModel.query.filter(or_(
            UserModel.email==username,UserModel.username==username)
        ).first()
        if not user:
            return jsonify({'success':False,'message':'用户名或邮箱不存在'})
        else:
            if check_password_hash(user.password,password):
                session['user_id']=user.id
                return jsonify({'success':True,'message':'登录成功!'})
            else:
                return jsonify({'success':False,'message':'密码错误'})

@bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')

def id_to_base36(num):
    chars = '0123456789abcdefghijklmnopqrstuvwxyz'
    result = ''
    while num > 0:
        num, remainder = divmod(num, 36)
        result = chars[remainder] + result
    return result or '0'

def generate_default_nickname(num):
    chars = '0123456789abcdefghijklmnopqrstuvwxyz'
    suffix = ''
    while num > 0:
        num, remainder = divmod(num, 36)
        suffix = chars[remainder] + suffix
    return f"用户_{suffix}"

@bp.route('/register',methods=['GET','POST'])
def register():
    if request.method=='GET':
        return render_template('register.html')
    else:
        form=RegisterForm(request.form)
        if form.validate():
            email=form.email.data
            username=form.username.data
            password=form.password.data
            captcha=form.captcha.data
            user=UserModel(email=email,username=username,password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            user.nickname=generate_default_nickname(user.id)
            captcha_model = EmailCaptchaModel.query.filter_by(email=email, captcha=captcha).first()
            db.session.delete(captcha_model)
            db.session.commit()
            return jsonify({'success':True,'message':'注册成功！请登录~'})
        else:
            for field, errors in form.errors.items():
                return jsonify({'success':False,'message':errors[0]})

@bp.route('/captcha/email')
def captcha_email():
    email=request.args.get('email')
    form=EmailForm(email=email)
    if form.validate():
        source=string.digits*6
        captcha=random.sample(source,6)
        captcha=''.join(captcha)
        message=Message(subject='王座论坛注册验证码',recipients=[email],body=f'[王座论坛]您的验证码是{captcha}')
        mail.send(message)
        email_captcha=EmailCaptchaModel(email=email,captcha=captcha)
        db.session.add(email_captcha)
        db.session.commit()
        return jsonify({'success':True,'message':'邮箱验证码发送成功'})
    else:
        return jsonify({'success':False,'message':str(form.email.errors[0])})


@bp.route('/mail/test')
def mail_test():
    message=Message(subject='邮箱测试',recipients=['2653335428@qq.com'],body='这是一封测试邮件')
    mail.send(message)
    return '邮件发送成功'




