from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
  
  
app = Flask(__name__)
  
app.secret_key = 'xyzsdfg'
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'elec0138'
  
mysql = MySQL(app)
  
@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        email = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM user WHERE user_name = '%s' AND password = '%s'" % (email, password))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['u_id'] = user['u_id']
            session['first_name'] = user['first_name']
            session['user_name'] = user['user_name']
            mesage = 'Logged in successfully !'
            return redirect('/user_page')
        else:
            return 'Please enter correct email / password !'
    return render_template('login.html', mesage = mesage)

@app.route('/user_page', methods =['GET', 'POST'])
def user_page():
    if session.get('user_name'):
        if request.method == 'POST' and 'number_plate' in request.form :
            number_plate = request.form['number_plate']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM history WHERE number_plate = '%s'" % (number_plate))
            history = cursor.fetchall()
            if history:
                return render_template('parking_history.html', history = history)
            else:
                return 'Plate Number does not exist!'
        return render_template('user_page.html')
    else:
        return 'Please Login'

@app.route('/parking_register')
def parking_register():
    if session.get('user_name'):
        return render_template('parking_register.html')
    else:
        return 'Please Login'

@app.route('/parking_history')
def parking_history():
    if session.get('user_name'):
        return render_template('parking_history.html')
    else:
        return 'Please Login'
    
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('u_id', None)
    session.pop('first_name', None)
    session.pop('last_name', None)
    return redirect('/')
  
@app.route('/register', methods =['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        password = request.form['password']
        dob = request.form['dob']
        email = request.form['email']
        address = request.form['address']
        postcode = request.form['postcode']
        
        query = "Insert into user (first_name, last_name, user_name, password, date_of_birth, email, street_name, " \
                "postcode, account_balance) values ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', 0)" \
                .format(first_name, last_name, username, password, dob, email, address, postcode)
            
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query)
        mysql.connection.commit()
        
        return redirect('/')
        
    return render_template('register.html', message = message)
    
if __name__ == "__main__":
    app.run()
    
'''
login credentials:

user: 92WhVpAOxt
pass: pty0HI5sQi

plate: TEF1NX5

'''