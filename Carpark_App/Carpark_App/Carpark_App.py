from flask import Flask, render_template, request, redirect, session
from datetime import datetime
from db_operations import DBOperator

app = Flask(__name__)
db = DBOperator("localhost", "root", "020327", "ELEC0138")
u_id = -1

login_attempts = {}
MAX_LOGIN_ATTEMPTS = 100


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        password = request.form['password']
        dob = request.form['dob']
        email = request.form['email']
        address = request.form['address']
        postcode = request.form['postcode']

        db.create_user(first_name, last_name, username, password, dob, email, address, postcode)
        return redirect('/')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    global u_id
    ip_address = request.remote_addr
    if ip_address in login_attempts:
        if login_attempts[ip_address] >= MAX_LOGIN_ATTEMPTS:
            return "Maximum login attempts exceeded."
    else:
        login_attempts[ip_address] = 0
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_details = db.get_user_details(username, password)
        if not user_details:
            login_attempts[ip_address] += 1
            return "Invalid username or password!"
        u_id = user_details[0][0]
        return redirect('/parking_register')
    return render_template('login.html')

@app.route('/parking_register', methods=['GET', 'POST'])
def parking_register():
    global u_id
    if request.method == 'POST':
        street_name = request.form['street_name']
        postcode = request.form['postcode']
        car_plate = request.form['car_plate']
        start_time = request.form['start_time'].replace("T", " ")+ ":00"
        end_time = request.form['end_time'].replace("T", " ") + ":00"
        p_id = db.get_parking_lot_details(postcode)[0][0]
        db.post_parking(u_id, p_id, start_time, end_time, car_plate)
        
        return redirect('/payment_options')
        
    
    return render_template('parking_register.html')



@app.route('/payment_options')
def payment_options():
    return render_template('payment_options.html')

@app.route('/card_payment', methods=['GET', 'POST'])
def card_payment():
    if request.method == 'POST':
        cardholder_name = request.form['cardholder_name']
        card_number = request.form['card_number']
        card_expiry = request.form['expiry_date']
        card_cvv = request.form['cvv']

        return redirect('/parking_view')
    
    return render_template('card_payment.html')

@app.route('/balance_payment', methods=['GET', 'POST'])
def balance_payment():
    if request.method == 'POST':
        top_up_amount = float(request.form['top_up_amount'])

        top_up(u_id, top_up_amount)

    user_balance_data = db.get_user_details_by_id(u_id)

    if user_balance_data:
        user_balance = user_balance_data[0][8]
    else:
        user_balance = None

    return render_template('balance_payment.html', balance=user_balance)

def top_up(user_id, amount):

    user_info = db.get_user_details_by_id(user_id)
    if user_info:
        user_balance = user_info[0][8]
        new_balance = user_balance + amount
        return db.update_balance(user_id, new_balance)
    else:
        return False

@app.route('/parking_view', methods=['GET', 'POST'])
def parking_view():
    global u_id
    if request.method == 'POST':
        pass

    parking_history = db.get_parking_history_of_user(u_id)

    return render_template('parking_view.html', parking_history=parking_history)

if __name__ == '__main__':
    app.run(host='0.0.0.0')