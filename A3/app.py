import json

from Crypto.PublicKey import RSA
from flask import Flask, request, jsonify
import base64
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

app = Flask(__name__)
# Load the private key
with open('private_key.txt', 'r') as f:
    private_key = RSA.import_key(f.read())

with open('public_key.txt', 'r') as f1:
    public_key = RSA.import_key(f1.read())


@app.route('/decrypt', methods=['POST'])
def decrypt():
    message = request.json['message']
    with open("./private_key.txt","rb") as file:
        privateKey = file.read()

    message = str.encode(message)

    decryptedMsg = base64.b64decode(message)

    # https://www.delftstack.com/howto/python/rsa-encryption-python/
    RSAprivateKey = RSA.importKey(privateKey)
    OAEP_cipher = PKCS1_OAEP.new(RSAprivateKey)
    decrypted_msg = OAEP_cipher.decrypt(decryptedMsg)
    print(decrypted_msg,"final_decrypted>>")
    my_response = {"response" : decrypted_msg.decode('utf-8')}
    return my_response


@app.route('/encrypt', methods=['POST'])
def encrypt():
    message = request.json['message']
    with open("./public_key.txt","rb") as file:
        publicKey = file.read()

    message = str.encode(message)

    # https://www.delftstack.com/howto/python/rsa-encryption-python/
    RSApublicKey = RSA.importKey(publicKey)
    OAEP_cipher = PKCS1_OAEP.new(RSApublicKey)
    encrypted_msg = OAEP_cipher.encrypt(message)

    print('encrypted_msg text:', encrypted_msg)

    encrypted_msg = base64.b64encode(encrypted_msg)
    base64_string = encrypted_msg.decode('utf-8')
    print('base64_string text:', base64_string)
    my_response = {"response": base64_string}
    return my_response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
