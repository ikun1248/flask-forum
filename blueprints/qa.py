from flask import Blueprint, render_template, request, redirect, url_for, g,flash,jsonify
from .forms import QuestionForm, AnswerForm
from models import QuestionModel, AnswerModel,UserModel,LikeModel,ViewLogModel
from sqlalchemy import or_
from exts import db
from .decorators import login_required
from datetime import datetime

bp = Blueprint('qa', __name__, url_prefix='/')


@bp.route('/')
def index():
    questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
    questions_count=db.session.query(QuestionModel).count()
    answers_count=db.session.query(AnswerModel).count()
    users_count=db.session.query(UserModel).count()
    category_counts=QuestionModel.get_all_category_counts()
    return render_template(
        'index.html',
        questions=questions,
        questions_count=questions_count,
        answers_count=answers_count,
        users_count=users_count,
        category_counts=category_counts
    )



@bp.route('/qa/public', methods=['GET', 'POST'])
@login_required
def qa_public():
    if request.method == 'GET':
        return render_template('public_question.html')
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            tags=form.tags.data
            tags=','.join(tags)
            category=form.category.data
            question = QuestionModel(title=title, content=content, category=category,tags=tags,author=g.user)
            db.session.add(question)
            db.session.commit()
            return jsonify({'success':True,'message':'帖子发送成功'})
        else:
            for field,errors in form.errors.items():
                return jsonify({'success':False,'message':errors[0]})


@bp.route('/qa/detail/<qa_id>')
@login_required
def qa_detail(qa_id):
    question = QuestionModel.query.get(qa_id)
    is_like=False
    like=LikeModel.query.filter_by(user_id=g.user.id,question_id=qa_id,is_active=True).first()
    like_count = LikeModel.query.filter_by(question_id=qa_id, is_active=True).count()
    if like :
        is_like=True
    if question:
        view_log=ViewLogModel.query.filter_by(user_id=g.user.id,question_id=qa_id).first()
        if not view_log:
            view_log=ViewLogModel(user_id=g.user.id,question_id=qa_id,count=0)
            db.session.add(view_log)
        view_log.count+=1
        view_log.view_time=datetime.now()
        db.session.commit()
        view_count = ViewLogModel.get_total_counts(qa_id)
        return render_template(
            'detail.html',
            question=question,
            is_like=is_like,
            like_count=like_count,
            view_count=view_count
        )
    return redirect('/')


@bp.post('/answer/public')
@login_required
def answer_public():
    form = AnswerForm(request.form)
    if form.validate():
        content = form.content.data
        question_id = form.question_id.data
        answer = AnswerModel(content=content, question_id=question_id, author=g.user)
        db.session.add(answer)
        db.session.commit()
        return jsonify({'success':True,'message':'回复发送成功'})
    else:
        return jsonify({'success':False,'message':form.content.errors[0]})


@bp.route('search')
@login_required
def search():
    q = request.args.get('q')
    questions = QuestionModel.query.filter(
        or_(QuestionModel.title.contains(q),QuestionModel.content.contains(q),UserModel.username.contains(q))
    ).order_by(QuestionModel.create_time.desc()).all()
    if questions:
        return render_template('index.html', questions=questions)
    else:
        flash("未找到相关帖子")
        return redirect('/')

@bp.post('/qa/delete/<qa_id>')
@login_required
def qa_delete(qa_id):
    question=QuestionModel.query.get(qa_id)
    if not question:
        return jsonify({'success':False,'message':'帖子不存在'})
    if question.author_id!=g.user.id:
        return jsonify({'success':False,'message':'没有权限删除此帖子'})

    db.session.delete(question)
    db.session.commit()
    return jsonify({'success':True,'message':'删除成功'})

@bp.route('/qa/edit/<qa_id>',methods=['GET','POST'])
@login_required
def qa_edit(qa_id):
    question = QuestionModel.query.get(qa_id)
    if g.user == question.author:
        if request.method=='GET':
            return render_template('edit_question.html',question=question)
        else:
            form=QuestionForm(request.form)
            if form.validate():
                title=form.title.data
                content=form.content.data
                category=form.category.data
                tags=form.tags.data
                tags=','.join(tags)
                question.title=title
                question.content=content
                question.category=category
                question.tags=tags
                db.session.commit()
                return jsonify({'success':True,'message':'修改成功!'})
            else:
                for field,errors in form.errors.items():
                    return jsonify({'success':False,'message':errors[0]})
                    break
    else:
        return redirect('/');

@bp.post('/qa/like/<qa_id>')
@login_required
def qa_like(qa_id):
    user_id=g.user.id
    try:
        like=LikeModel.query.filter_by(user_id=user_id,question_id=qa_id).first()
        if like:
            if like.is_active:
                like.is_active=False
                db.session.commit()
                return jsonify({'success':True,'message':'取消点赞成功'})
            else:
                like.is_active=True
                db.session.commit()
                return jsonify({'success':True,'message':'点赞成功'})
        else:
            like=LikeModel(user_id=user_id,question_id=qa_id)
            db.session.add(like)
            db.session.commit()
            return jsonify({'success': True, 'message': '点赞成功'})
    except Exception as e:
        return jsonify({'success':False,'message':str(e)})






