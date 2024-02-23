from flask import Flask, render_template, request, redirect

app = Flask(__name__)

users = {}

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/sign_up', methods=['GET', 'POST'])
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



if __name__ == '__main__':
    app.run(debug=True)
