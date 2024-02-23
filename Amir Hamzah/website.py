from flask import Flask, render_template
test = Flask(__name__)

@test.route('/html')
def home():
   return render_template('index.html')

test.config['TEMPLATES_AUTO_RELOAD'] = True

if __name__ == '__main__':
    test.run()