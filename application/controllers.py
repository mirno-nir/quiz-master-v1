from flask import render_template, request, redirect, session, url_for
from flask import current_app as app
from datetime import datetime

from .models import *

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('pwd')
        user = User.query.filter_by(email = email).first()
        if user:
            if user.password == password:
                if user.type == 'admin':
                    return redirect('/admin_dashboard')
                return redirect(f'/user_dashboard/{user.user_id}')
        return render_template('user_not_found.html')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('pwd')
        full_name = request.form.get('fname')
        qualification = request.form.get('qualification')
        dob = request.form.get('dob')
        user = User.query.filter_by(email = email).first()
        if user:
            render_template('already_exist.html')
        else:
            user_record = User(email = email, password = password, full_name = full_name, qualification = qualification, dob = dob)
            db.session.add(user_record)
            db.session.commit()
            db.session.close()
            return redirect('/login')
    return render_template('register.html')

@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dash():
    subject = Subject.query.all()
    chapter = Chapter.query.all()
    return render_template('admin_dashboard.html', subject = subject, chapter = chapter)

@app.route('/add_subject', methods = ['GET', 'POST'])
def add_subject():
    try:
        if request.method == 'POST':
            subject_name = request.form.get('subject_name').strip()
            subject_description = request.form.get('subject_desc').strip()
            subject_record = Subject(subject_name = subject_name, subject_description = subject_description)
            db.session.add(subject_record)
            db.session.commit()
            return redirect('/admin_dashboard')
        return render_template('add_subject.html')
    except Exception as e:
        db.session.rollback()
        db.session.close()
        return 'This Subject already exist or something went wrong!'
    
@app.route('/subject/<int:subject_id>/edit', methods=['GET','POST'])
def edit_subject(subject_id):
    try:
        subject_to_edit = Subject.query.filter_by(subject_id = subject_id).first()
        if request.method == 'GET':
            return render_template('update_subject.html', subject = subject_to_edit)
        if request.method == 'POST':
            subject_to_edit.subject_name = request.form.get('subject_name')
            subject_to_edit.subject_description = request.form.get('subject_desc')
            db.session.commit()
            return redirect('/admin_dashboard')
    except Exception as e:
        db.session.rollback()
        db.session.close()
        return 'This Subject already exist or something went wrong!'


@app.route('/subject/<int:subject_id>/delete', methods=['GET'])
def delete_subject(subject_id):
    subject = Subject.query.filter_by(subject_id = subject_id).first()
    db.session.delete(subject)
    db.session.commit()
    db.session.close()
    return redirect('/admin_dashboard')

@app.route('/add_chapter/<int:subject_id>', methods=['GET', 'POST'])
def add_chapter(subject_id):
    try:
        if request.method == 'GET':
            subject = Subject.query.filter_by(subject_id = subject_id).first()
            subject_name = subject.subject_name
            return render_template('add_chapter.html', subject_id = subject_id, subject_name = subject_name)
        if request.method == 'POST':
            chapter_name = request.form.get('chapter_name').strip()
            chapter_description = request.form.get('chapter_desc').strip()
            chaper_record = Chapter(subject_id = subject_id, chapter_name = chapter_name, chapter_description = chapter_description)
            db.session.add(chaper_record)
            db.session.commit()
            return redirect('/admin_dashboard')
    except Exception as e:
        db.session.rollback()
        db.session.close()
        return 'This Chapter already exist or something went wrong!'
    
@app.route('/chapter/<int:subject_id>/<int:chapter_id>/edit', methods=['GET', 'POST'])
def edit_chapter(subject_id,chapter_id):
    try:
        chapter = Chapter.query.filter_by(chapter_id = chapter_id).first()
        subject = Subject.query.filter_by(subject_id = subject_id).first()
        if request.method == 'GET':
            return render_template('update_chapter.html', chapter = chapter, subject = subject)
        if request.method == 'POST':
            chapter.chapter_name = request.form.get('chapter_name')
            chapter.chapter_description = request.form.get('chapter_desc')
            db.session.commit()
            return redirect('/admin_dashboard')
    except Exception as e:
        db.session.rollback()
        db.session.close()
        return 'This chapter name already exist or something went wrong!'
    
@app.route('/chapter/<int:subject_id>/<int:chapter_id>/delete', methods=['GET'])
def delete_chapter(subject_id, chapter_id):
    chapter = Chapter.query.filter_by(chapter_id = chapter_id).first()
    db.session.delete(chapter)
    db.session.commit()
    db.session.close()
    return redirect('/admin_dashboard')

@app.route('/quiz_mgmt', methods=['GET', 'POST'])
def quiz_management():
    quizzes = Quiz.query.all()
    if request.method == 'GET':
        return render_template('quiz_mgmt.html', quizzes = quizzes)

@app.route('/add_quiz', methods=['GET', 'POST'])
def add_quiz():
    try:
        if request.method == 'GET':
            return render_template('/add_quiz.html')
        if request.method == 'POST':
            chapter_id = request.form.get('chapter_id')
            chapter_exist = Chapter.query.filter_by(chapter_id = chapter_id).first()
            if chapter_exist:
                quiz_date = request.form.get('quiz_date')
                quiz_time_duration = request.form.get('quiz_time_duration')
                quiz_remarks = request.form.get('quiz_remarks')
                quiz_record = Quiz(chapter_id = chapter_id, quiz_date = quiz_date, quiz_time_duration = quiz_time_duration, quiz_remarks = quiz_remarks)
                db.session.add(quiz_record)
                db.session.commit()
                db.session.close()
                return redirect('/quiz_mgmt')
            return 'The chapter does not exist, add chapter first'
    except Exception as e:
        return 'Something went wrong!'
    
@app.route('/quiz/<int:chapter_id>/<int:quiz_id>/edit', methods=['GET', 'POST'])
def edit_quiz(chapter_id, quiz_id):
    quiz = Quiz.query.filter_by(quiz_id = quiz_id).first()
    if request.method == 'GET':
        return render_template('update_quiz.html', chapter_id = chapter_id, quiz = quiz)
    if request.method == 'POST':
        quiz.quiz_date = request.form.get('quiz_date')
        quiz.quiz_time_duration = request.form.get('quiz_time_duration')
        quiz.quiz_remarks = request.form.get('quiz_remarks')
        db.session.commit()
        db.session.close()
        return redirect('/quiz_mgmt')

@app.route('/quiz/<int:chapter_id>/<int:quiz_id>/delete', methods=['GET'])
def delete_quiz(chapter_id, quiz_id):
    quiz = Quiz.query.filter_by(quiz_id = quiz_id).first()
    db.session.delete(quiz)
    db.session.commit()
    db.session.close()
    return redirect('/quiz_mgmt')
    
@app.route('/add_question/<int:chapter_id>/<int:quiz_id>', methods=['GET', 'POST'])
def add_question(chapter_id, quiz_id):
    if request.method == 'GET':
        chapter = Chapter.query.filter_by(chapter_id = chapter_id).first()
        chapter_name = chapter.chapter_name
        return render_template('add_question.html', chapter_id = chapter_id, chapter_name = chapter_name, quiz_id = quiz_id)
    if request.method == 'POST':
        question_title = request.form.get('question_title')
        question_statement = request.form.get('question_statement')
        correct_option = request.form.get('correct_option')
        option_1 = request.form.get('op_1')
        option_2 = request.form.get('op_2')
        option_3 = request.form.get('op_3')
        option_4 = request.form.get('op_4')
        option_list = [option_1, option_2, option_3, option_4]
        if correct_option in option_list:
            question_record = Question(quiz_id = quiz_id, chapter_id = chapter_id, question_title = question_title, question_statement = question_statement, correct_option = correct_option, option_1 = option_1, option_2 = option_2, option_3 = option_3, option_4 = option_4)
            db.session.add(question_record)
            db.session.commit()
            db.session.close()
            return redirect(f'/add_question/{chapter_id}/{quiz_id}')
        else:
            return 'Enter a valid correct option from the entered options'
        

@app.route('/question/<int:chapter_id>/<int:quiz_id>/<int:question_id>/edit', methods=['GET', 'POST'])
def update_question(chapter_id, quiz_id, question_id):
    question = Question.query.filter_by(question_id = question_id).first()
    if request.method == 'GET':
        return render_template('update_question.html', question = question, question_id = question_id, chapter_id = chapter_id, quiz_id = quiz_id)
    if request.method == 'POST':
        question.question_title = request.form.get('question_title')
        question.question_statement = request.form.get('question_statement')
        question.correct_option = request.form.get('correct_option')
        question.option_1 = request.form.get('op_1')
        question.option_2 = request.form.get('op_2')
        question.option_3 = request.form.get('op_3')
        question.option_4 = request.form.get('op_4')
        option_list = [question.option_1, question.option_2, question.option_3, question.option_4]
        if question.correct_option in option_list:
            db.session.commit()
            db.session.close()
            return redirect('/quiz_mgmt')
        else:
            return 'Enter a valid correct option from the entered options'

@app.route('/question/<int:chapter_id>/<int:quiz_id>/<int:question_id>/delete', methods=['GET'])
def delete_question(chapter_id, quiz_id, question_id):
    question = Question.query.filter_by(question_id = question_id).first()
    db.session.delete(question)
    db.session.commit()
    db.session.close()
    return redirect('/quiz_mgmt')

'''FOR USERS'''

@app.route('/user_dashboard/<int:user_id>', methods=['GET'])
def user_dashboard(user_id):
    if request.method == 'GET':
        quizzes = Quiz.query.all()
        for quiz in quizzes:
            current_date = datetime.now().date()  #will give current date
            quiz.is_upcomming = datetime.strptime(quiz.quiz_date, '%Y-%m-%d').date() > current_date     # strptime will convert date-string in to valid time.
            quiz.is_active = datetime.strptime(quiz.quiz_date, '%Y-%m-%d').date() <= current_date
        return render_template('user_dashboard.html', quizzes = quizzes, user_id = user_id)
    
@app.route('/user/<int:user_id>/quiz/<int:quiz_id>/view', methods=['GET'])
def view_quiz_by_user(user_id, quiz_id):
    quiz = Quiz.query.filter_by(quiz_id = quiz_id).first()
    chapter_id = quiz.chapter_id
    chapter = Chapter.query.filter_by(chapter_id = chapter_id).first()
    return render_template('view_quiz.html', quiz = quiz, chapter = chapter, user_id = user_id, quiz_id = quiz_id)


@app.route('/user/<int:user_id>/quiz/<int:quiz_id>/start', methods=['GET', 'POST'])
def start_quiz_by_user(user_id, quiz_id):
    quiz = Quiz.query.filter_by(quiz_id = quiz_id).first()
    questions = Question.query.filter_by(quiz_id = quiz_id)
    return render_template('/start_quiz.html', quiz = quiz, questions = questions)