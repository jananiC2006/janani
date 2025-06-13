from flask import Flask, render_template, request, redirect, session, url_for, flash
import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key')  # Required for session management

# Database connection function with error handling
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            port=os.getenv('DB_PORT', '3306')  # Default MySQL port
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register_alumni.html')

@app.route('/register_alumni', methods=['POST'])
def register_alumni():
    name = request.form['name']
    email = request.form['email']
    batch = request.form['batch']
    department = request.form['department']
    company = request.form['company']
    position = request.form['position']
    linkedin_url = request.form['linkedin_url']

    db = get_db_connection()
    if db is None:
        flash('Database connection failed. Please try again later.', 'error')
        return redirect('/register')

    try:
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO alumni (name, email, batch, department, company, position, linkedin_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (name, email, batch, department, company, position, linkedin_url))
        db.commit()
        flash('Registration successful!', 'success')
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
        flash('An error occurred while registering. Please try again.', 'error')
    finally:
        cursor.close()
        db.close()

    return redirect('/alumni')

@app.route('/alumni')
def alumni_list():
    db = get_db_connection()
    if db is None:
        flash('Database connection failed. Please try again later.', 'error')
        return render_template('alumni_list.html', alumni=[])

    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM alumni WHERE status = 'Approved' ORDER BY submitted_on DESC")
        alumni = cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error fetching data: {err}")
        flash('An error occurred while fetching alumni data.', 'error')
        alumni = []
    finally:
        cursor.close()
        db.close()

    return render_template('alumni_list.html', alumni=alumni)

@app.route('/admin_login', methods=['GET'])
def admin_login():
    if 'logged_in' in session:
        return redirect(url_for('admin_alumni'))
    return render_template('admin_login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    valid_username = os.getenv('ADMIN_USERNAME', 'admin')
    valid_password = os.getenv('ADMIN_PASSWORD', 'janani20')

    if username == valid_username and password == valid_password:
        session['logged_in'] = True
        flash('Login successful!', 'success')
        return redirect(url_for('admin_alumni'))
    else:
        flash('Invalid credentials. Please try again.', 'error')
        return redirect(url_for('admin_login'))

@app.route('/admin_alumni', methods=['GET', 'POST'])
def admin_alumni():
    if 'logged_in' not in session:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('admin_login'))

    db = get_db_connection()
    if db is None:
        flash('Database connection failed. Please try again later.', 'error')
        return render_template('admin_alumni.html', alumni=[])

    try:
        cursor = db.cursor()
        if request.method == 'POST':
            alumni_id = request.form['alumni_id']
            status = request.form['status']
            cursor.execute("UPDATE alumni SET status = %s WHERE alumni_id = %s", (status, alumni_id))
            db.commit()
            flash(f'Alumni status updated to {status}.', 'success')

        cursor.execute("SELECT * FROM alumni ORDER BY submitted_on DESC")
        data = cursor.fetchall()

        alumni = [
            {
                'alumni_id': row[0],
                'name': row[1],
                'email': row[2],
                'batch': row[3],
                'department': row[4],
                'company': row[5],
                'position': row[6],
                'linkedin_url': row[7],
                'status': row[8]
            } for row in data
        ]
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        flash('An error occurred while fetching or updating alumni data.', 'error')
        alumni = []
    finally:
        cursor.close()
        db.close()

    return render_template('admin_alumni.html', alumni=alumni)

@app.route('/thank')
def thank():
    return render_template('thank.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=False)
