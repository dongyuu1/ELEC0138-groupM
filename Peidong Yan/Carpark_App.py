from flask import Flask, render_template, request, redirect
from datetime import datetime

app = Flask(__name__)

users = {}
card_payments = {}
parking_info = {}

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

        if username in users:
            return "User already exists!"
        
        users[username] = {
            'first_name': first_name,
            'last_name': last_name,
            'password': password,
            'dob': dob,
            'email': email,
            'address': address,
            'postcode': postcode
        }

        return redirect('/')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username not in users or users[username]['password'] != password:
            return "Invalid username or password!"
        return redirect('/parking_register')
    return render_template('login.html')

@app.route('/parking_register', methods=['GET', 'POST'])
def parking_register():
    if request.method == 'POST':
        street_name = request.form['street_name']
        postcode = request.form['postcode']
        car_plate = request.form['car_plate']
        start_time = request.form['start_time']
        duration = int(request.form['duration'])

        parking_info[car_plate] = {
            'street_name': street_name,
            'postcode': postcode,
            'start_time': start_time,
            'duration': duration
        }
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
        
        card_payments.append({
            'cardholder_name': cardholder_name,
            'card_number': card_number,
            'card_expiry': card_expiry,
            'card_cvv': card_cvv
        })

        return redirect('/parking_view')
    
    return render_template('card_payment.html')

@app.route('/balance_payment')
def balance_payment():
    if request.method == 'POST':

        return redirect('/parking_view')
    return render_template('balance_payment.html')

@app.route('/parking_view', methods=['GET', 'POST'])
def parking_view():
    if request.method == 'POST':
        pass
    return render_template('parking_view.html')

if __name__ == '__main__':
    app.run(debug=True)