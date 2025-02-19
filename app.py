# https://docs.google.com/document/d/e/2PACX-1vQ9bIdyfpUwdevF2bRSPGsFIGKfxaw9tytEyK2bZixrGgPKHMFFajBm8f_MZ7faTfjCdCH0d0_QvDau/pub 

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dash():
    return render_template('admin_dashboard.html')

@app.route('/new_subject', methods=['GET', 'POST'])
def new_sub():
    return render_template('new_subject.html')


@app.route('/new_chapter', methods=['GET', 'POST'])
def new_chap():
    return render_template('new_chapter.html')


@app.route('/quiz_mgmt', methods=['GET', 'POST'])
def quiz_mgmt():
    return render_template('quiz_mgmt.html')


@app.route('/add_quiz', methods=['GET', 'POST'])
def add_quiz():
    return render_template('add_quiz.html')

@app.route('/new_question', methods=['GET', 'POST'])
def new_que():
    return render_template('new_question.html')

@app.route('/summary_admin', methods=['GET', 'POST'])
def summary_admin():
    return render_template('summary_admin.html')

@app.route('/user_dashboard', methods=['GET', 'POST'])
def user_dashboard():
    return render_template('user_dashboard.html')

@app.route('/scores', methods=['GEt', 'POST'])
def scores():
    return render_template('scores.html')

@app.route('/summary_user', methods=['GET', 'POST'])
def summary_user():
    return render_template('summary_user.html')

@app.route('/view_quiz', methods=['GET', 'POST'])
def view_quiz():
    return render_template('view_quiz.html')

@app.route('/start_quiz', methods=['GET', 'POST'])
def start_quiz():
    return render_template('start_quiz.html')
app.run(debug=True, port=5050)