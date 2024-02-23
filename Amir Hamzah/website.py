from flask import Flask, render_template
test = Flask(__name__)

@test.route('/')
def home():
   return render_template('index.html')

if __name__ == '__main__':
    test.run()