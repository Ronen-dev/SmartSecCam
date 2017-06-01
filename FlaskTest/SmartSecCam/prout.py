# from Crypto.Cipher import AES

# file = open('.secret', 'r')
# line = file.readline()
# secret_key = line
# print(secret_key)

# cipher = AES.new(secret_key, AES.MODE_ECB)
# crypt = cipher.encrypt("coucou maman".rjust(32))
# print(crypt)
# msg = cipher.decrypt(crypt).strip().decode('utf-8')
# print(msg)

# file2 = open('.password', 'r')
# line2 = file2.readline()
# line2 = bytes(line2)
# msg2 = cipher.decrypt(line2).strip().decode('utf-8')
# print(msg2)
# from simplecrypt import encrypt, decrypt
# import base64

# file = open('.secret', 'r')
# secret = file.readline()
# file.close()

# file = open('.password', 'rb')
# password = file.read()
# file.close()

# passwd = decrypt(secret, password)
# print(passwd.decode('utf-8'))

# ciphertext = encrypt(secret, "coucou maman")
# print(ciphertext)
# plaintext = decrypt(secret, ciphertext)
# print(plaintext.decode('utf-8'))

from urllib.request import urlopen
my_ip = urlopen('http://ip.42.pl/raw').read()
print(my_ip.decode('utf-8'))

connected = False

def checkConnection():
    global connected
    try:
        urlopen('http://www.google.fr', timeout=1)
        connected = True
    except URLError:
        connected = False

checkConnection()

print(connected)
