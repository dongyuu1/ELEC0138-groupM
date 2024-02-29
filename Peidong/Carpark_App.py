from flask import Flask, render_template, request, redirect

app = Flask(__name__)

users = {}

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



        return "Parking registration successful!"
    return render_template('parking_register.html')

if __name__ == '__main__':
    app.run(debug=True)
