from flask import render_template, request, redirect, session, url_for
from flask import current_app as app
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
import calendar

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
            chapters = Chapter.query.all()
            return render_template('/add_quiz.html', chapters = chapters)
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

@app.route('/user_dashboard/<int:user_id>', methods=['GET', 'POST'])
def user_dashboard(user_id):
    user = User.query.filter_by(user_id = user_id).first()
    user_full_name = user.full_name
    quizzes = Quiz.query.all()
    for quiz in quizzes:
        current_date = datetime.now().date()  #will give current date
        quiz.is_upcomming = datetime.strptime(quiz.quiz_date, '%Y-%m-%d').date() > current_date     # strptime will convert date-string in to valid time.
        quiz.is_active = datetime.strptime(quiz.quiz_date, '%Y-%m-%d').date() <= current_date
    return render_template('user_dashboard.html', quizzes = quizzes, user_id = user_id, user_full_name = user_full_name)
    
@app.route('/user/<int:user_id>/quiz/<int:quiz_id>/view', methods=['GET'])
def view_quiz_by_user(user_id, quiz_id):
    quiz = Quiz.query.filter_by(quiz_id = quiz_id).first()
    chapter_id = quiz.chapter_id
    chapter = Chapter.query.filter_by(chapter_id = chapter_id).first()
    return render_template('view_quiz.html', quiz = quiz, chapter = chapter, user_id = user_id, quiz_id = quiz_id)

# quiz start ############################
# @app.route('/user/<int:user_id>/quiz/<int:quiz_id>/start', methods=['GET'])
# def start_quiz(user_id, quiz_id):
#     first_question = Question.query.filter_by(quiz_id = quiz_id).order_by(Question.question_id.asc()).first()
#     if first_question:
#         session['current_question_id'] = first_question.question_id
#         session['question_attempt_record'] = {}
#         return redirect(url_for('show_quiz_question', user_id = user_id, quiz_id = quiz_id))
#     return 'Thre are no questions for this quiz at the moment!'

# @app.route('/user/<int:user_id>/quiz/<int:quiz_id>/question', methods=['GET'])
# def show_quiz_question(user_id, quiz_id):
#     question_id = session.get('current_question_id', None)
#     if question_id is None:
#         return redirect(url_for('start_quiz', user_id = user_id, quiz_id = quiz_id))
#     question = Question.query.get_or_404(question_id)
#     return render_template('start_quiz.html', question = question, quiz_id = quiz_id, user_id = user_id)

# @app.route('/user/<int:user_id>/quiz/<int:quiz_id>/question', methods=['POST'])
# def next_quiz_question(user_id, quiz_id):
#     current_question_id = session.get('current_question_id', None)
#     attempted_question = Question.query.filter_by(question_id = current_question_id).first()
#     if current_question_id is None:
#         return redirect(url_for('start_quiz', user_id = user_id, quiz_id = quiz_id))
#     selected_answer = request.form.get('option')
#     if attempted_question.correct_option == selected_answer:
#         question_result = True
#         print('yes')
#     else:
#         question_result = False
#         print('no')
#     session['question_attempt_record'][str(current_question_id)] = {}
#     session['question_attempt_record'][str(current_question_id)]['selected_answer'] = selected_answer
#     session['question_attempt_record'][str(current_question_id)]['question_result'] = question_result
#     next_question = Question.query.filter_by(quiz_id = quiz_id).filter(Question.question_id > current_question_id).first()
#     if next_question:
#         session['current_question_id'] = next_question.question_id
#         return redirect(url_for('show_quiz_question', user_id = user_id, quiz_id = quiz_id))
#     return redirect(url_for('quiz_finished', user_id = user_id, quiz_id = quiz_id))

# @app.route('/user/<int:user_id>/quiz/<int:quiz_id>/quiz_finished')
# def quiz_finished(user_id, quiz_id):
#     time_stamp = datetime.now()
#     score = 0
#     print(session['question_attempt_record'])
#     for question in session['question_attempt_record']:
#         score += int(session['question_attempt_record'][question]['question_result'])
#         user_attempt_record = User_attempt(user_id = user_id, quiz_id = quiz_id, question_id = question, chosen_option = session['question_attempt_record'][question]['selected_answer'], option_result = session['question_attempt_record'][question]['question_result'], time_stamp = time_stamp)
#         db.session.add(user_attempt_record)
#         db.session.commit()
#         db.session.close()
#         print(question)
#     scores_record = Scores(user_id = user_id, quiz_id = quiz_id, time_stamp = time_stamp, quiz_time_duration = score, total_score = score)
#     db.session.add(scores_record)
#     db.session.commit()
#     db.session.close()
#     return redirect(url_for('user_dashboard', user_id = user_id))


@app.route('/user/<int:user_id>/quiz/<int:quiz_id>/start', methods=['GET'])
def start_quiz(user_id, quiz_id):
    first_question = Question.query.filter_by(quiz_id = quiz_id).order_by(Question.question_id.asc()).first()
    if first_question:
        session['current_question_id'] = first_question.question_id
        session['answers'] = {}
        return redirect(url_for('show_quiz_question', user_id = user_id, quiz_id = quiz_id))
    return 'There are no questions in this quiz at the moment.'

@app.route('/user/<int:user_id>/quiz/<int:quiz_id>/question', methods=['GET', 'POST'])
def show_quiz_question(user_id, quiz_id):
    question_id = session.get('current_question_id', None)
    if question_id is None:
        return redirect(url_for('start_quiz', user_id = user_id, quiz_id = quiz_id))
    
    question = Question.query.get_or_404(question_id)
    return render_template('start_quiz.html', question = question, user_id = user_id, quiz_id = quiz_id)

@app.route('/user/<int:user_id>/quiz/<int:quiz_id>/next', methods=['POST'])
def next_quiz_question(user_id, quiz_id):
    current_question_id = session.get('current_question_id', None)
    attempted_question = Question.query.filter_by(question_id = current_question_id).first()
    if current_question_id is None:
        return redirect(url_for('start_quiz'), user_id = user_id, quiz_id = quiz_id)
    
    answer_selected = request.form.get('option')
    if answer_selected:
        session['answer_selected'] = answer_selected
        if attempted_question.correct_option == answer_selected:
            option_result = True
        else:
            option_result = False
        
        session['answers'][str(current_question_id)] = [answer_selected, option_result]

    next_question = Question.query.filter_by(quiz_id = quiz_id).filter(Question.question_id > current_question_id).first()
    if next_question:
        session['current_question_id'] = next_question.question_id
        return redirect(url_for('show_quiz_question', user_id = user_id, quiz_id = quiz_id))
    
    return redirect(url_for('quiz_finished', user_id = user_id, quiz_id = quiz_id))

@app.route('/user/<int:user_id>/quiz/<int:quiz_id>/quiz_finished')
def quiz_finished(user_id, quiz_id):
    time_stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    score = 0
    for question in session['answers']:
        score += int(session['answers'][question][1])
        user_attempt_record = User_attempt(user_id = user_id, quiz_id = quiz_id, question_id = question, chosen_option = session['answers'][question][0], option_result = session['answers'][question][1], time_stamp = time_stamp)
        db.session.add(user_attempt_record)
        db.session.commit()
        db.session.close()
    scores_record = Scores(user_id = user_id, quiz_id = quiz_id, time_stamp = time_stamp, quiz_time_duration = score, total_score = score)
    db.session.add(scores_record)
    db.session.commit()
    db.session.close()
    return redirect(url_for('user_dashboard', user_id = user_id))
#############################################

@app.route('/user/<int:user_id>/scores', methods=['GET'])
def scores(user_id):
    user = User.query.filter_by(user_id = user_id).first()
    user_full_name = user.full_name
    user_score = Scores.query.filter_by(user_id = user_id).all()
    return render_template('scores.html', user_id = user_id, user_full_name = user_full_name, user_score = user_score)

@app.route('/user/<int:user_id>/summary', methods=['GET'])
def user_summary(user_id):
    user = User.query.filter_by(user_id = user_id).first()
    user_full_name = user.full_name
    user_scores = Scores.query.filter_by(user_id = user_id).all()
    
    user_attempts_for_subject = {} # it will store {subject1: 'no. of attempts', subject2: 'no. of attempts'} by a user
    user_attempts_in_month = {} # it will store {month1: 'no. of attempts', month2: 'no. of attempts'} by a user
    for attempt in user_scores:
        if attempt.quiz_score.chapter.subject.subject_name in user_attempts_for_subject:
            user_attempts_for_subject[attempt.quiz_score.chapter.subject.subject_name] +=1
        else:
            user_attempts_for_subject[attempt.quiz_score.chapter.subject.subject_name] =1
        time_stamp = datetime.strptime(attempt.time_stamp, '%Y-%m-%d %H:%M:%S')
        month_num = int(time_stamp.month)
        month = calendar.month_name[month_num]
        if month in user_attempts_in_month:
            user_attempts_in_month[month] += 1
        else:
            user_attempts_in_month[month] = 1

    subjects = list(user_attempts_for_subject.keys())
    number_of_attempts_in_subject = list(user_attempts_for_subject.values())
    plt.bar(subjects, number_of_attempts_in_subject)
    plt.xlabel('Subjects Appeared')
    plt.ylabel('Number of Attempts in a Subject')
    plt.title('Subjectwise number of quizzes attempted')
    plt.savefig('static/bar.png')
    plt.clf()

    months = list(user_attempts_in_month.keys())
    number_of_attempts_in_month = list(user_attempts_in_month.values())
    print(number_of_attempts_in_month)
    plt.pie(number_of_attempts_in_month, labels=months, autopct = "%1.1f%%")
    plt.title('Monthwise number of quiz attempted')
    plt.savefig('static/pie.png')
    plt.clf()
    return render_template('summary_user.html', user_id = user_id, user_full_name = user_full_name)

@app.route('/summary_admin', methods=['GET'])
def summary_admin():
    quiz_score = Scores.query.all()
    subjects_with_max_score = {}
    subject_wise_user_attempts = {}
    for score in quiz_score:
        if score.quiz_score.chapter.subject.subject_name in subjects_with_max_score:
            if subjects_with_max_score[score.quiz_score.chapter.subject.subject_name] < score.total_score:
                subjects_with_max_score[score.quiz_score.chapter.subject.subject_name] = score.total_score
        else:
            subjects_with_max_score[score.quiz_score.chapter.subject.subject_name] = score.total_score

        if score.quiz_score.chapter.subject.subject_name in subject_wise_user_attempts:
            subject_wise_user_attempts[score.quiz_score.chapter.subject.subject_name] += 1
        else:
            subject_wise_user_attempts[score.quiz_score.chapter.subject.subject_name] = 1
    subjects_in_max = list(subjects_with_max_score.keys())
    max_score = list(subjects_with_max_score.values())
    plt.bar(subjects_in_max, max_score)
    plt.xlabel('Subjects')
    plt.ylabel('Maximum marks')
    plt.title('Subjectwise maximum Marks')
    plt.savefig('static/bar1.png')
    plt.clf()

    subjects_in_attempt = list(subject_wise_user_attempts.keys())
    number_of_attempts = list(subject_wise_user_attempts.values())
    plt.pie(number_of_attempts, labels=subjects_in_attempt, autopct='%1.1f%%')
    plt.savefig('static/pie1.png')
    plt.clf()
    return render_template('summary_admin.html')

@app.route('/admin_search', methods=['POST'])
def admin_search():
    arg = request.form.get('search').strip()
    return redirect(url_for('search_results', arg = arg))

@app.route('/admin_search/<string:arg>', methods=['GET'])
def search_results(arg):
    user_result = User.query.filter(User.full_name.like(f'%{str(arg)}%')).all()
    subject_result = Subject.query.filter(Subject.subject_name.like(f'%{str(arg)}%')).all()
    quiz_result = db.session.query(Quiz).filter(Quiz.chapter.has(Chapter.chapter_name.like(f'%{str(arg)}%'))).all()
    if not user_result and not subject_result and not quiz_result:
        return 'Please enter valid search input!'
    return render_template('admin_search.html', user_result = user_result, subject_result = subject_result, quiz_result = quiz_result)

