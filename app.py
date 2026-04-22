from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'mysecretkey'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'hw13.db')


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if username == 'admin' and password == 'password':
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid username or password'

    return render_template('login.html', error=error)


@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    quizzes = conn.execute('SELECT * FROM quizzes').fetchall()
    conn.close()

    return render_template('dashboard.html', students=students, quizzes=quizzes)


@app.route('/student/add', methods=['GET', 'POST'])
def add_student():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    error = None

    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()

        if first_name == '' or last_name == '':
            error = 'Both first name and last name are required.'
        else:
            conn = get_db_connection()
            conn.execute(
                'INSERT INTO students (first_name, last_name) VALUES (?, ?)',
                (first_name, last_name)
            )
            conn.commit()
            conn.close()
            return redirect(url_for('dashboard'))

    return render_template('add_student.html', error=error)


@app.route('/quiz/add', methods=['GET', 'POST'])
def add_quiz():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    error = None

    if request.method == 'POST':
        subject = request.form.get('subject', '').strip()
        num_questions = request.form.get('num_questions', '').strip()
        quiz_date = request.form.get('quiz_date', '').strip()

        if subject == '' or num_questions == '' or quiz_date == '':
            error = 'All fields are required.'
        else:
            conn = get_db_connection()
            conn.execute(
                'INSERT INTO quizzes (subject, num_questions, quiz_date) VALUES (?, ?, ?)',
                (subject, num_questions, quiz_date)
            )
            conn.commit()
            conn.close()
            return redirect(url_for('dashboard'))

    return render_template('add_quiz.html', error=error)


@app.route('/student/<int:id>')
def student_results(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    conn = get_db_connection()

    student = conn.execute(
        'SELECT * FROM students WHERE id = ?',
        (id,)
    ).fetchone()

    results = conn.execute(
        'SELECT quiz_id, score FROM results WHERE student_id = ?',
        (id,)
    ).fetchall()

    conn.close()

    return render_template('student_results.html', student=student, results=results)


@app.route('/results/add', methods=['GET', 'POST'])
def add_result():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    quizzes = conn.execute('SELECT * FROM quizzes').fetchall()

    error = None

    if request.method == 'POST':
        student_id = request.form.get('student_id', '').strip()
        quiz_id = request.form.get('quiz_id', '').strip()
        score = request.form.get('score', '').strip()

        if student_id == '' or quiz_id == '' or score == '':
            error = 'All fields are required.'
        else:
            conn.execute(
                'INSERT INTO results (student_id, quiz_id, score) VALUES (?, ?, ?)',
                (student_id, quiz_id, score)
            )
            conn.commit()
            conn.close()
            return redirect(url_for('dashboard'))

    conn.close()
    return render_template('add_result.html', students=students, quizzes=quizzes, error=error)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)