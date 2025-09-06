from flask import Blueprint,request,render_template,url_for,flash,redirect,g,jsonify
from .decorators import login_required
from werkzeug.utils import secure_filename
from .forms import AvatarUploadForm,NicknameForm,PasswordResetForm,EmailResetFrom
from exts import db
from models import UserModel,QuestionModel
from werkzeug.security import generate_password_hash,check_password_hash
import os

bp=Blueprint('profile',__name__,url_prefix='/profile')

@bp.route('/')
@login_required
def index():
    user=g.user
    my_posts=QuestionModel.query.filter_by(author_id=user.id).order_by(QuestionModel.create_time.desc()).all()
    return render_template('profile.html',my_posts=my_posts)

@bp.route('/avatar_upload',methods=['POST'])
@login_required
def avatar_upload():
    form=AvatarUploadForm(avatar=request.files['avatar'])
    if form.validate():
        file=form.avatar.data
        filename=str(g.user.id)+'_'+secure_filename(file.filename)
        file_path='./static/images/avatar/'
        try:
            if g.user.avatar != 'default.jpg':
                os.remove(file_path+g.user.avatar)
        except:
            pass
        file.save(file_path + filename)
        g.user.avatar=filename
        db.session.commit()
        flash('头像上传成功')
    else:
        flash(form.avatar.errors[0])
    return redirect(url_for('profile.index',username=g.user.username))

@bp.route('nickname_upload',methods=['POST'])
@login_required
def nickname_upload():
    form=NicknameForm(request.form)
    if form.validate():
        nickname=form.nickname.data
        g.user.nickname=nickname
        db.session.commit()
    else:
        flash(form.nickname.errors[0])
    return redirect(url_for('profile.index'))

@bp.route('gender_upload',methods=['POST'])
@login_required
def gender_upload():
    gender=request.form['gender']
    if g.user.gender !=gender:
        g.user.gender=gender
        db.session.commit()
    return redirect(url_for('profile.index'))

@bp.route('address_upload',methods=['POST'])
@login_required
def address_upload():
    province=request.form['province']
    city=request.form['city']
    g.user.province=province
    g.user.city=city
    db.session.commit()
    return redirect(url_for('profile.index'))

@bp.route('password_reset',methods=['POST'])
@login_required
def password_reset():
    form=PasswordResetForm(request.form)
    if form.validate():
        old_password=form.old_password.data
        new_password=form.new_password.data
        if check_password_hash(g.user.password,old_password):
            g.user.password=generate_password_hash(new_password)
            db.session.commit()
            print('密码修改成功')
        else:
            print('旧密码错误')
    else:
        for field,errors in form.errors.items():
            print(errors[0])
            break
    return redirect(url_for('profile.index'))

@bp.route('email_reset',methods=['POST'])
@login_required
def email_reset():
    form=EmailResetFrom(request.form)
    if form.validate():
        new_email=form.new_email.data
        g.user.email=new_email
        db.session.commit()
        flash("邮箱修改成功!")
    else:
        for field,errors in form.errors.items():
            flash(errors[0])
            break
    return redirect(url_for('profile.index'))











