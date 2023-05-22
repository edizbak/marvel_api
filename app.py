# flask pour API et jsonify pour... faire du json !
from flask import Flask, jsonify, render_template
import hashlib  # import hashlib pour génération hash
import time  # génération timestamp
import requests  # requêtage http
from flask_bootstrap import Bootstrap
from models.character import Character

app = Flask(__name__)  # instanciation appli flask
app.config.from_pyfile('config.py')  # chargement config
Bootstrap(app)

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
    return get_any('characters')


@app.route('/comics')  # création route
def get_comics():
    """route pour récupération comics"""
    return get_any('comics')


@app.route('/series')  # création route
def get_series():
    """route pour récupération series"""
    return get_any('series')


@app.route('/events')  # création route
def get_events():
    """ route events """
    return get_any('events')


def get_any(any):
    """visu any route"""
    ts, hash = ts_hash_gen().values()
    params = {  # ajout des paramètres de la requête
        'apikey': PUBLIC_KEY,
        'ts': ts,
        'hash': hash,
        'limit': 100
    }
    response = requests.get(f"{BASE_URL}{any}", params=params)
    return jsonify(response.json())


@app.route('/characters/<int:charid>', methods=['GET'])
def get_character_uniq(charid):
    ts, hash = ts_hash_gen().values()  # on unpack directement le dict
    params = {
        'apikey': PUBLIC_KEY,
        'ts': ts,
        'hash': hash
    }
    response = requests.get(f"{BASE_URL}characters/{charid}", params=params)
    return jsonify(response.json())


def ts_hash_gen():
    ts = str(time.time())
    hash = generate_hash(ts, PRIVATE_KEY, PUBLIC_KEY)
    return {'ts': ts, 'hash': hash}


@app.route('/bs/<int:charid>', methods=['GET'])
def render_char(charid):
    ts, hash = ts_hash_gen().values()
    params = {
        'apikey': PUBLIC_KEY,
        'ts': ts,
        'hash': hash
    }
    response = requests.get(f"{BASE_URL}characters/{charid}", params=params)
    bs_char = Character.from_dict(response.json()['data']['results'][0])
    return render_template('character.html', character=bs_char)


@app.errorhandler(500)
def error_server():
    return f"500 - Erreur serveur", 500


app.run(debug=True)
