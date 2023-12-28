import json
from base64 import b64decode, b64encode
from os.path import exists
from django.conf import settings

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

from lineas_modular.models import SolicitudJsonViaje
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
private_key = None
public_key = None

def load_keys():
    global private_key, public_key
    if not exists(f"{CURRENT_DIR}/.key-priv"):
        #print("No se encontró una llave privada (.key-priv) en la raiz del proyecto, no se podra firmar los JSONs")
        return
    if not exists(f"{CURRENT_DIR}/.key-pub"):
        #print("No se encontró una llave publica (.key-pub) en la raiz del proyecto, no se podra firmar los JSONs")
        return
    with open(f"{CURRENT_DIR}/.key-priv", "r") as key_file:
        private_key = RSA.import_key(key_file.read())

    with open(f"{CURRENT_DIR}/.key-pub", "r") as key_file:
        public_key = RSA.import_key(key_file.read())

load_keys()

def sign_string(text, viaje, user):
    if type(text) == dict:
        text = json.dumps(text)
    text_b = bytes(text, encoding="utf-8")

    digest = SHA256.new(text_b)
    
    signature = pkcs1_15.new(private_key).sign(digest)
    signature_b64 = str(b64encode(signature), encoding="utf-8")

    SolicitudJsonViaje.objects.create(
        viaje=viaje, 
        json=text, 
        signature=signature_b64
    ) 

    return signature_b64, text


def verify_string(text, sign):
    text_b = bytes(text, encoding="utf-8")
    digest = SHA256.new(text_b)

    sign_b64less = b64decode(sign)
    try:
        pkcs1_15.new(public_key).verify(digest, sign_b64less)
        return True
    except:
        return False