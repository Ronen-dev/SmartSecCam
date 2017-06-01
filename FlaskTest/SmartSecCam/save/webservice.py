import os, random, string, base64
from flask import Flask, render_template, url_for, request, redirect
from simplecrypt import encrypt, decrypt

app = Flask(__name__)

@app.route('/')
def index():
    checkSecret()
    checkKnownWifi()
    if not checkPassword():
        return redirect(url_for('password'))
    # chec pasword file si pas ok redirect sur /password si ok checkwifi
    #check wifi on test tout les wifi qu'on connait si pas possible de se co on redirige sur la page pour ajoute un wifi
    return 'hello world!'

@app.route('/password', methods=['GET', 'POST'])
def password():
    error = None
    if checkPassword():
        redirect(url_for('index'))
    if request.method == 'GET':
        return render_template('password.html', error=error)
    if request.method == 'POST':
        if request.form['password'] and request.form['confirm']:
            if request.form['password'] != request.form['confirm']:
                error = "les deux mots de passes doivent être identiques"
                return render_template('password.html', error=error)
            # changer le mdp root de la machine
            file = open('.password', 'wb')
            password = appEncrypt(request.form['password'])
            file.write(password)
            file.close()
            return redirect(url_for('index'))
        else:
            error = "Vous devez remplir les deux champs ci-dessous"
            return render_template('password.html', error=error)

def checkSecret():
    directory = os.path.dirname(os.path.realpath(__file__))
    if not os.path.isfile(directory + '/.secret'):
        file = open('.secret', 'w')
        chars = string.ascii_letters + string.digits + string.punctuation
        result = ''.join(random.choice(chars) for _ in range(64))
        file.write(result)
        file.close()

def checkPassword():
    directory = os.path.dirname(os.path.realpath(__file__))
    if not os.path.isfile(directory + '/.password'):
        return False
    return True

def checkKnownWifi():
    directory = os.path.dirname(os.path.realpath(__file__))
    if not os.path.isfile(directory + '/.known_wifi'):
        file.open('.known_wifi', "w")
        file.close()

def appEncrypt(word):
    file = open('.secret', 'r')
    secret_key = file.readline()
    cipher = encrypt(secret_key, word)
    file.close()
    return cipher

def appDecrypt(word):
    file = open('.secret', 'r')
    secret_key = file.readline()
    msg = decrypt(secret_key, word).decode('utf-8')
    file.close()
    return (msg)
