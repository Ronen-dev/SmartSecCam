import os, random, string, base64
from flask import Flask, render_template, url_for, request, redirect
from simplecrypt import encrypt, decrypt
from wifi import Cell, Scheme
from urllib.request import urlopen
from urllib.error import URLError

app = Flask(__name__)
wifiInterface = 'wlan0'

connected = False

def checkConnection():
    global connected
    try:
        urlopen('http://www.google.fr', timeout=1)
        connected = True
    except URLError:
        connected = False

def tryToConnect():
    global connected
    file = open('.known_wifi', 'r')
    for line in file:
        scheme = Scheme.find(wifiInterface, line)
        if scheme:
            try:
                scheme.activate()
            except ConnectionError:
                continue
            connected = True
    connected = False

checkConnection()

if not connected:
    tryToConnect()


@app.route('/')
def index():
    checkSecretFile()
    checkKnownWifiFile()
    if not checkPasswordFile():
        return redirect(url_for('password'))
    if not connected:
        return redirect(url_for('wifi'))
    if connected:
        return redirect(url_for('ip'))
    return 'Welcome on SmartSecCam web interface'

@app.route('/password', methods=['GET', 'POST'])
def password():
    error = None
    if checkPasswordFile():
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

@app.route('/wifi', methods=['GET', 'POST'])
def wifi():
    error = None
    if request.method == 'GET':
        return render_template('wifi.html', error=error)
    if request.method == 'POST':
        if request.form['wifi-name'] and request.form['wifi-key']:
            try:
                cell = searchCell(request.form['wifi-name'])
                if cell:
                    scheme = Scheme.for_cell(wifiInterface, request.form['wifi-name'], cell, request.form['wifi-key'])
                    scheme.save()
                    scheme.activate()
                else:
                    error = 'Le wifi n\'a pas été trouvé veuillez en renseigner un autre'
                    return render_template('wifi.html', error=error)
            except ConnectionError:
                error = 'Impossible de se connecter au réseau veuillez renseigner des informations valides'
                return render_template('wifi.html', error=error)
            file = open('.known_wifi', 'a')
            file.write(request.form['wifi-name'] + '\n')
            file.close()
            return redirect(url_for('ip'))
        else:
            error = 'Vous devez remplir les deux champs du formulaire'
            return render_template('wifi.html', error=error)

@app.route('/ip')
def ip():
    ip = urlopen('http://ip.42.pl/raw').read().decode('utf-8')
    return render_template('ip.html', ip=ip)


def checkSecretFile():
    directory = os.path.dirname(os.path.realpath(__file__))
    if not os.path.isfile(directory + '/.secret'):
        file = open('.secret', 'w')
        chars = string.ascii_letters + string.digits + string.punctuation
        result = ''.join(random.choice(chars) for _ in range(64))
        file.write(result)
        file.close()

def checkPasswordFile():
    directory = os.path.dirname(os.path.realpath(__file__))
    if not os.path.isfile(directory + '/.password'):
        return False
    return True

def checkKnownWifiFile():
    directory = os.path.dirname(os.path.realpath(__file__))
    if not os.path.isfile(directory + '/.known_wifi'):
        file = open('.known_wifi', "w")
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

def searchCell(name):
    cells = Cell.all(wifiInterface)
    for cell in cells:
        if cell.ssid == name:
            return cell
    return None
