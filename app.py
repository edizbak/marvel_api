# flask pour API et jsonify pour... faire du json !
from flask import Flask, jsonify
import hashlib  # import hashlib pour génération hash
import time  # génération timestamp
import requests  # requêtage http

app = Flask(__name__)  # instanciation appli flask
app.config.from_pyfile('config.py')  # chargement config

# récupération constantes
PUBLIC_KEY = app.config['MARVEL_PUBLIC_KEY']
PRIVATE_KEY = app.config['MARVEL_PRIVATE_KEY']
BASE_URL = 'http://gateway.marvel.com/v1/public/'


def generate_hash(ts, private_key, public_key):
    """Génération de hash pour l'API Marvel"""
    m = hashlib.md5()  # instanciation algo md5
    m.update(f"{ts}{private_key}{public_key}".encode(
        'utf-8'))  # ajout chaîne dans instance en attente d'enco
    return m.hexdigest()  # enco + retour hash en hexa


@app.route('/characters')  # création route
def get_character():
    """route pour récupération personnages"""
    ts = str(time.time())  # timestamp
    hash = generate_hash(ts, PRIVATE_KEY, PUBLIC_KEY)  # génération hash
    params = {  # ajout des paramètres de la requête
        'apikey': PUBLIC_KEY,
        'ts': ts,
        'hash': hash,
        'limit': 100
    }
    response = requests.get(f"{BASE_URL}characters", params=params)
    return jsonify(response.json())


@app.route('/characters/<charid>')
def get_character_uniq(charid):
    ts = str(time.time())
    hash = generate_hash(ts, PRIVATE_KEY, PUBLIC_KEY)
    params = {
        'apikey': PUBLIC_KEY,
        'ts': ts,
        'hash': hash
    }
    response = requests.get(f"{BASE_URL}characters/{charid}", params=params)
    return jsonify(response.json())


app.run(debug=True)
