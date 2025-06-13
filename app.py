

# from flask import Flask, render_template, request,redirect
# from flask_mysqldb import MySQL
# import mysql.connector

# app = Flask(__name__)
# db=mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="",
#     database="alumni_db"
# )
# cursor=db.cursor()

# mysql=MySQL(app)

# @app.route('/')
# def home():
#     return render_template('index.html')
# @app.route('/register')
# def register():
#     return render_template('register_alumni.html')

# @app.route('/register_alumni', methods=['GET', 'POST'])
# def register_alumni():
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#         batch = request.form['batch']
#         department = request.form['department']
#         company = request.form['company']
#         position = request.form['position']
#         linkedin_url = request.form['linkedin_url']


#         cursor.execute('''INSERT INTO alumni(name, email, batch, department, company, position, linkedin_url)
#             VALUES (%s, %s, %s, %s, %s, %s, %s)
#         ''', (name, email, batch, department, company, position, linkedin_url))
#         db.commit()
        

#         return redirect('/alumni')  


# @app.route('/alumni')
# def alumni_list():
#     # db=mysql.connector.connect(
#     #         host="localhost",
#     #         user="root",
#     #         password="",
#     #         database="alumni_db"
#     #     )
#     # cursor=db.cursor()
    
#     cursor.execute("SELECT * FROM alumni_db WHERE status = 'Approved' ORDER BY submitted_on DESC")
#     alumni = cursor.fetchall()
    
#     return render_template('alumni_list.html',alumni=alumni)

# @app.route('/admin_alumni', methods=['GET', 'POST'])
# def admin_alumni():
#     cursor=db.cursor()
#     if request.method =='POST':
#         alumni_id = request.form['alumni_id']
#         status = request.form['status']
    
#         cursor.execute("UPDATE alumni SET status = %s WHERE alumni_id = %s", (status, alumni_id))
#         db.commit()
   
#     cursor.execute("SELECT * FROM alumni ORDER BY submitted_on DESC")
#     data = cursor.fetchall()
#     cursor.close()
    
#     alumni=[]
#     for row in data:
#         alumni.append({'name':row[0],'batch':row[1],'department':row[2],'company':row[3],'position':row[4],'linkedin_url':row[5],'status':row[6],'action':row[7]})
#         return render_template('admin_alumni.html',alumni=alumni)
    

# @app.route('/thank')
# def thank():
#     return render_template('thank.html')
      
    

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template, request, redirect,session,url_for
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="alumni_db"
)
cursor = db.cursor()

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

    cursor.execute('''
        INSERT INTO alumni(name, email, batch, department, company, position, linkedin_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    ''', (name, email, batch, department, company, position, linkedin_url))
    db.commit()

    return redirect('/alumni')

@app.route('/alumni')
def alumni_list():
    cursor.execute("SELECT * FROM alumni WHERE status = 'Approved' ORDER BY submitted_on DESC")
    alumni = cursor.fetchall()
    return render_template('alumni_list.html', alumni=alumni)


# Dummy credentials
VALID_USERNAME = "admin"
VALID_PASSWORD = "janani20"

@app.route('/admin_login',methods=['GET'])
def admin_login():
    return render_template('admin_login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    if username == VALID_USERNAME and password == VALID_PASSWORD:
        return redirect(url_for('admin_alumni'))
    else:
        return "Invalid credentials. Please try again."  


@app.route('/admin_alumni', methods=['GET', 'POST'])
def admin_alumni():
    if request.method == 'POST':
        alumni_id = request.form['alumni_id']
        status = request.form['status']
        cursor.execute("UPDATE alumni SET status = %s WHERE alumni_id = %s", (status, alumni_id))
        db.commit()

    cursor.execute("SELECT * FROM alumni ORDER BY submitted_on DESC")
    data = cursor.fetchall()

    alumni = []
    for row in data:
        alumni.append({
            'alumni_id': row[0],
            'name': row[1],
            'email': row[2],
            'batch': row[3],
            'department': row[4],
            'company': row[5],
            'position': row[6],
            'linkedin_url': row[7],
            'status': row[8]
        })

    return render_template('admin_alumni.html', alumni=alumni)

@app.route('/thank')
def thank():
    return render_template('thank.html')





if __name__ == '__main__':
    app.run(debug=True)