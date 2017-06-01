from flask import Flask
from flask import render_template 
from flask import request
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html', error=None)

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        print("username :", request.form['username'])
        print("password :", request.form['password'])
    else:
        error = 'Invalid username/password'
        # the code below is executed if the request method
        # was GET or the credentials were invalid
        return render_template('login.html', error=error)
