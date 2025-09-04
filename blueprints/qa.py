from flask import Blueprint, render_template, request, redirect, url_for, g,flash
from .forms import QuestionForm, AnswerForm
from models import QuestionModel, AnswerModel,UserModel
from sqlalchemy import or_
from exts import db
from .decorators import login_required

bp = Blueprint('qa', __name__, url_prefix='/')


@bp.route('/')
def index():
    questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
    return render_template('index.html', questions=questions)


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
            question = QuestionModel(title=title, content=content, author=g.user)
            db.session.add(question)
            db.session.commit()
            return redirect('/')
        else:
            for field,errors in form.errors.items():
                flash(errors[0])
                break
            return redirect(url_for('qa.qa_public'))


@bp.route('/qa/detail/<qa_id>')
def qa_detail(qa_id):
    question = QuestionModel.query.get(qa_id)
    if question:
        return render_template('detail.html', question=question)
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
        return redirect(url_for('qa.qa_detail', qa_id=question_id))
    else:
        flash(form.content.errors[0])
        return redirect(url_for('qa.qa_detail', qa_id=request.form.get('question_id')))


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
