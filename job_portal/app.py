import os
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import sqlite3
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'job_portal_pavan_key'
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)',
                         (username, email, password, role))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return "Email already registered!"
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password)).fetchone()
        conn.close()
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            return redirect(url_for('index'))
        else:
            return "Invalid email or password!"
    return render_template('login.html')

@app.route('/jobs')
def jobs():
    search = request.args.get('search')
    conn = get_db_connection()
    if search:
        query = "SELECT * FROM jobs WHERE title LIKE ? OR location LIKE ? ORDER BY posted_date DESC"
        jobs = conn.execute(query, ('%' + search + '%', '%' + search + '%')).fetchall()
    else:
        jobs = conn.execute('SELECT * FROM jobs ORDER BY posted_date DESC').fetchall()
    conn.close()
    return render_template('jobs.html', jobs=jobs)

@app.route('/post-job', methods=['GET', 'POST'])
def post_job():
    if not session.get('user_id') or session.get('role') != 'employer':
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        company_name = request.form['company_name']
        company_email = request.form['company_email']
        description = request.form['description']
        location = request.form['location']
        salary = request.form['salary']
        category = request.form['category']
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO jobs (employer_id, title, company_name, company_email, description, location, salary, category)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (session['user_id'], title, company_name, company_email, description, location, salary, category))
        conn.commit()
        conn.close()
        return redirect(url_for('jobs'))
    return render_template('post_job.html')

@app.route('/apply/<int:job_id>', methods=['GET', 'POST'])
def apply(job_id):
    if not session.get('user_id') or session.get('role') != 'seeker':
        return redirect(url_for('login'))
    if request.method == 'POST':
        file = request.files['resume']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            conn = get_db_connection()
            conn.execute('INSERT INTO applications (job_id, seeker_id, resume_file) VALUES (?, ?, ?)', 
                         (job_id, session['user_id'], filename))
            conn.commit()
            conn.close()
            return redirect(url_for('my_applications'))
    return render_template('apply.html', job_id=job_id)

@app.route('/view-applicants')
def view_applicants():
    if not session.get('user_id') or session.get('role') != 'employer':
        return redirect(url_for('login'))
    conn = get_db_connection()
    query = '''
        SELECT applications.id, users.username, users.email, jobs.title, applications.resume_file, applications.status 
        FROM applications 
        JOIN users ON applications.seeker_id = users.id 
        JOIN jobs ON applications.job_id = jobs.id 
        WHERE jobs.employer_id = ?
    '''
    applicants = conn.execute(query, (session['user_id'],)).fetchall()
    conn.close()
    return render_template('view_applicants.html', applicants=applicants)

@app.route('/update-status/<int:app_id>', methods=['POST'])
def update_status(app_id):
    new_status = request.form['status']
    conn = get_db_connection()
    conn.execute('UPDATE applications SET status = ? WHERE id = ?', (new_status, app_id))
    conn.commit()
    conn.close()
    return redirect(url_for('view_applicants'))

@app.route('/my-applications')
def my_applications():
    if not session.get('user_id') or session.get('role') != 'seeker':
        return redirect(url_for('login'))
    conn = get_db_connection()
    query = '''
        SELECT jobs.title, jobs.company_name, applications.status 
        FROM applications 
        JOIN jobs ON applications.job_id = jobs.id 
        WHERE applications.seeker_id = ?
    '''
    apps = conn.execute(query, (session['user_id'],)).fetchall()
    conn.close()
    return render_template('my_applications.html', applications=apps)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/hired')
def hired(): return render_template('hired.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST': return "Message Sent! Our team will contact you soon."
    return render_template('contact.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)