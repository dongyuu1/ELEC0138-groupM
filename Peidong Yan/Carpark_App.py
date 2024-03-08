from flask import Flask, render_template, request, redirect
from datetime import datetime

app = Flask(__name__)

users = {}
card_payments = {}
parking_sessions = {}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        age = request.form['age']
        gender = request.form['gender']
        email = request.form['email']

        if username in users:
            return "User already exists!"
        users[username] = {
            'password': password,
            'age': age,
            'gender': gender,
            'email': email
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
        first_name = request.form['first_name']
        postcode = request.form['postcode']
        street_name = request.form['street_name']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        return redirect('/payment_options')
    return render_template('parking_register.html')

@app.route('/payment_options')
def payment_options():
    return render_template('payment_options.html')

@app.route('/card_payment', methods=['GET', 'POST'])
def card_payment():
    if request.method == 'POST':
        card_number = request.form['card_number']
        card_expiry = request.form['card_expiry']
        card_cvv = request.form['card_cvv']
        card_payments.append({
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