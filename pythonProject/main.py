import os
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps

app = Flask(__name__)
# app.secret_key = '0'
app.secret_key = os.urandom(24)

# Statik dosya konfigürasyonu
app.config['STATIC_FOLDER'] = 'static'


class stc:
    i = 0

# add your localhost username and password
DB_USERNAME = "your_username"
DB_PASSWORD = "your_password"


# MySQL bağlantısı oluştur
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user=DB_USERNAME,
        password=DB_PASSWORD,
        db="graduateeducation",
        port="3306"
    )


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            flash('You need to login first.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the entered username and password match the database credentials
        if username == DB_USERNAME and password == DB_PASSWORD:
            session['logged_in'] = True
            flash('Login successful!', 'success')
            return redirect(url_for('indexx'))  # Redirect to the main page after login
        else:
            flash('Invalid username or password. Please try again.', 'danger')

    # If already logged in, redirect to the index page
    # if 'logged_in' in session and session['logged_in']:
    #     return redirect(url_for('index'))

    return render_template('login.html')


# Logout route
@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))


# Main login page
@app.route('/')
@login_required
def index():
    return render_template('login.html')


# index page
@app.route('/index')
@login_required
def indexx():
    return render_template('index.html')


# İşlem seçildiğinde yönlendirme yap
@app.route('/select_operation', methods=['POST'])
@login_required
def select_operation():
    operation = request.form.get('operation')

    if operation == 'ogrenci_ekle':
        stc.i = 1
        return redirect(url_for('ogrenci_ekle'))
    elif operation == 'kurs_ekle':
        stc.i = 2
        return redirect(url_for('kurs_ekle'))
    elif operation == 'akademisyen_ekle':
        stc.i = 3
        return redirect(url_for('akademisyen_ekle'))
    elif operation == 'enstitu_ekle':
        stc.i = 4
        return redirect(url_for('enstitu_ekle'))
    elif operation == 'program_ekle':
        stc.i = 5
        return redirect(url_for('program_ekle'))
    elif operation == 'tez_ekle':
        stc.i = 6
        return redirect(url_for('tez_ekle'))
    elif operation == 'seminar_ekle':
        stc.i = 7
        return redirect(url_for('seminar_ekle'))
    else:
        return redirect(url_for('index'))


# Öğrenci ekleme formu
@app.route('/ogrenci_ekle')
@login_required
def ogrenci_ekle():
    return render_template('ogrenci_ekle.html')


# Kurs ekleme formu
@app.route('/kurs_ekle')
@login_required
def kurs_ekle():
    return render_template('kurs_ekle.html')


# Akademisyen ekleme formu
@app.route('/akademisyen_ekle')
@login_required
def akademisyen_ekle():
    return render_template('akademisyen_ekle.html')


@app.route('/enstitu_ekle')
@login_required
def enstitu_ekle():
    return render_template('enstitu_ekle.html')


@app.route('/program_ekle')
@login_required
def program_ekle():
    return render_template('program_ekle.html')


@app.route('/tez_ekle')
@login_required
def tez_ekle():
    return render_template('tez_ekle.html')


@app.route('/seminar_ekle')
@login_required
def seminar_ekle():
    return render_template('seminar_ekle.html')


# MySQL veritabanında ogrenciler tablosunu oluştur
@app.route('/add_student', methods=['POST'])
@login_required
def add_student():
    student_id = request.form['student_id']
    student_name = request.form['student_name']
    student_surname = request.form['student_surname']
    phone = request.form['phone']
    address = request.form['address']
    mail = request.form['mail']
    birth_date = request.form['birth_date']
    start_date = request.form['start_date']
    edu_degree_id = request.form['edu_degree_id']
    advisor_id = request.form['advisor_id']
    program_id = request.form['program_id']

    conn = get_db_connection()
    cursor = conn.cursor()
    query = (
        "INSERT INTO students (Student_ID, Student_Name, Student_Surname, Phone, Address, Mail, Birth_Date, Start_Date, Edu_Degree_ID, Advisor_ID, Program_ID) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    cursor.execute(query, (
    student_id, student_name, student_surname, phone, address, mail, birth_date, start_date, edu_degree_id, advisor_id,
    program_id))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Öğrenci başarıyla eklendi.', 'success')
    return redirect(url_for('ogrenci_ekle'))


@app.route('/delete_student', methods=['POST'])
@login_required
def delete_student():
    student_id = request.form['student_id']

    conn = get_db_connection()
    cursor = conn.cursor()
    query = "DELETE FROM students WHERE Student_ID = %s"
    cursor.execute(query, (student_id,))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Öğrenci başarıyla silindi.', 'success')
    return redirect(url_for('ogrenci_ekle'))


@app.route('/add_academic', methods=['POST'])
@login_required
def add_academic():
    academic_id = request.form['academic_id']
    academic_name = request.form['academic_name']
    academic_surname = request.form['academic_surname']
    phone = request.form['phone']
    address = request.form['address']
    birth_date = request.form['birth_date']
    title_id = request.form['title_id']

    conn = get_db_connection()
    cursor = conn.cursor()
    query = (
        "INSERT INTO academic_staff (Academic_ID, Academic_Name, Academic_Surname, Phone, Address, Birth_Date, Title_ID) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s)")
    cursor.execute(query, (academic_id, academic_name, academic_surname, phone, address, birth_date, title_id))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Akademisyen başarıyla eklendi.', 'success')
    return redirect(url_for('akademisyen_ekle'))


@app.route('/delete_academic', methods=['POST'])
@login_required
def delete_academic():
    academic_id = request.form['academic_id']

    conn = get_db_connection()
    cursor = conn.cursor()
    query = "DELETE FROM academic_staff WHERE Academic_ID = %s"
    cursor.execute(query, (academic_id,))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Akademisyen başarıyla silindi.', 'success')
    return redirect(url_for('akademisyen_ekle'))


@app.route('/add_course', methods=['POST'])
@login_required
def add_course():
    course_code = request.form['course_code']
    course_name = request.form['course_name']
    credit = request.form['credit']
    lecture_hours = request.form['lecture_hours']
    lab_hours = request.form['lab_hours']
    instructor_id = request.form['instructor_id']

    conn = get_db_connection()
    cursor = conn.cursor()
    query = ("INSERT INTO courses (Course_Code, Course_Name, Credit, Lecture_Hours, Lab_Hours, Instructor_ID) "
             "VALUES (%s, %s, %s, %s, %s, %s)")
    cursor.execute(query, (course_code, course_name, credit, lecture_hours, lab_hours, instructor_id))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Kurs başarıyla eklendi.', 'success')
    return redirect(url_for('kurs_ekle'))


@app.route('/delete_course', methods=['POST'])
@login_required
def delete_course():
    course_code = request.form['course_code']

    conn = get_db_connection()
    cursor = conn.cursor()
    query = "DELETE FROM courses WHERE Course_Code = %s"
    cursor.execute(query, (course_code,))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Kurs başarıyla silindi.', 'success')
    return redirect(url_for('kurs_ekle'))


@app.route('/add_institute', methods=['POST'])
@login_required
def add_institute():
    institute_id = request.form['institute_id']
    institute_name = request.form['institute_name']
    webpage = request.form['webpage']
    phone = request.form['phone']
    address = request.form['address']
    conn = get_db_connection()
    cursor = conn.cursor()
    query = ("INSERT INTO institutes (Institute_ID, Institute_Name, Webpage, Phone, Address) "
             "VALUES (%s, %s, %s, %s, %s)")
    cursor.execute(query, (institute_id, institute_name, webpage, phone, address))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Enstitü başarıyla eklendi.', 'success')
    return redirect(url_for('enstitu_ekle'))


@app.route('/delete_institute', methods=['POST'])
@login_required
def delete_institute():
    institute_id = request.form['institute_id']

    conn = get_db_connection()
    cursor = conn.cursor()
    query = "DELETE FROM institutes WHERE Institute_ID = %s"
    cursor.execute(query, (institute_id,))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Enstitü başarıyla silindi.', 'success')
    return redirect(url_for('enstitu_ekle'))


@app.route('/add_prog', methods=['POST'])
@login_required
def add_prog():
    program_id = request.form['program_id']
    program_name = request.form['program_name']
    manager_id = request.form['manager_id']
    institute_id = request.form['institute_id']

    conn = get_db_connection()
    cursor = conn.cursor()
    query = ("INSERT INTO programs (Program_ID, Program_Name, Manager_ID, Institute_ID) "
             "VALUES (%s, %s, %s, %s)")
    cursor.execute(query, (program_id, program_name, manager_id, institute_id))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Program başarıyla eklendi.', 'success')
    return redirect(url_for('program_ekle'))


@app.route('/delete_prog', methods=['POST'])
@login_required
def delete_prog():
    program_id = request.form['program_id']

    conn = get_db_connection()
    cursor = conn.cursor()
    query = "DELETE FROM programs WHERE Program_ID = %s"
    cursor.execute(query, (program_id,))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Program başarıyla silindi.', 'success')
    return redirect(url_for('program_ekle'))


@app.route('/add_thesis', methods=['POST'])
@login_required
def add_thesis():
    thesis_id = request.form['thesis_id']
    research_topic = request.form['research_topic']
    status = request.form['status']
    grade = request.form['grade']
    publication_date = request.form['publication_date']
    defense_date = request.form['defense_date']
    student_id = request.form['student_id']
    supervisor_id = request.form['supervisor_id']

    conn = get_db_connection()
    cursor = conn.cursor()
    query = (
        "INSERT INTO thesis_information (Thesis_ID, Research_Topic, Status, Grade, Publication_Date, Defense_Date, Student_ID, Supervisor_ID) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
    cursor.execute(query, (
    thesis_id, research_topic, status, grade, publication_date, defense_date, student_id, supervisor_id))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Tez başarıyla eklendi.', 'success')
    return redirect(url_for('tez_ekle'))


@app.route('/delete_thesis', methods=['POST'])
@login_required
def delete_thesis():
    thesis_id = request.form['thesis_id']

    conn = get_db_connection()
    cursor = conn.cursor()
    query = "DELETE FROM thesis_information WHERE Thesis_ID = %s"
    cursor.execute(query, (thesis_id,))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Tez başarıyla silindi.', 'success')
    return redirect(url_for('tez_ekle'))


@app.route('/add_seminar', methods=['POST'])
@login_required
def add_seminar():
    seminar_id = request.form['seminar_id']
    seminar_name = request.form['seminar_name']
    duration = request.form['duration']
    seminar_leader_id = request.form['seminar_leader_id']

    conn = get_db_connection()
    cursor = conn.cursor()
    query = ("INSERT INTO seminar_information (Seminar_ID, Seminar_Name, Duration, Seminar_Leader_ID) "
             "VALUES (%s, %s, %s, %s)")
    cursor.execute(query, (seminar_id, seminar_name, duration, seminar_leader_id))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Seminer başarıyla eklendi.', 'success')
    return redirect(url_for('seminar_ekle'))


@app.route('/delete_seminar', methods=['POST'])
@login_required
def delete_seminar():
    seminar_id = request.form['seminar_id']

    conn = get_db_connection()
    cursor = conn.cursor()
    query = "DELETE FROM seminar_information WHERE Seminar_ID = %s"
    cursor.execute(query, (seminar_id,))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Seminer başarıyla silindi.', 'success')
    return redirect(url_for('seminar_ekle'))


@app.route('/execute_query', methods=['POST'])
@login_required
def execute_query():
    user_query = request.form['query']
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(user_query)
        results = cursor.fetchall()
        column_names = [column[0] for column in cursor.description]
    except Exception as e:
        results = []
        column_names = ['Hata']
        results.append([str(e)])
    finally:
        cursor.close()
        conn.close()
    if stc.i == 1:
        return render_template('ogrenci_ekle.html', query_results=results, column_names=column_names)
    elif stc.i == 2:
        return render_template('kurs_ekle.html', query_results=results, column_names=column_names)
    elif stc.i == 3:
        return render_template('akademisyen_ekle.html', query_results=results, column_names=column_names)
    elif stc.i == 4:
        return render_template('enstitu_ekle.html', query_results=results, column_names=column_names)
    elif stc.i == 5:
        return render_template('program_ekle.html', query_results=results, column_names=column_names)
    elif stc.i == 6:
        return render_template('tez_ekle.html', query_results=results, column_names=column_names)
    elif stc.i == 7:
        return render_template('seminar_ekle.html', query_results=results, column_names=column_names)
    else:
        return render_template('index.html', query_results=results, column_names=column_names)


if __name__ == '__main__':
    app.run(debug=True)
