import hashlib
import pickle
from datetime import datetime
from flask import Flask, session
from flask_session import Session

from flask import (Flask, render_template)

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

r = {}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search/streets/<string:streetname>', methods=['GET'])
def search_streets(streetname):
    streetname = streetname.lower()
    streets = []
    file = open("data/street_names.txt", "r")
    for line in file.readlines():
        if streetname in line:
            streets.append(line)
    
    return render_template('results_streets.html', streets=streets, md5_hash=md5_hash, results=len(streets))


@app.route('/search/voters/<string:street_name>', methods=['GET'])
def search_voters(street_name):
    voters = {}
    street_name_hash = md5_hash(street_name)
    voter_ids = list(r[street_name_hash].keys())
    for voter_id in voter_ids:
        voters[voter_id] = r[street_name_hash][voter_id]
    session['street_name_hash'] = street_name_hash
    dt = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))

    return render_template('search_voters.html', voters=voters, voter_ids=voter_ids, dt=dt, street_name=street_name)


@app.route('/search/voter/<string:voter_id>', methods=['GET'])
def search_voter(street_name, voter_id):

    street_name_hash = session.get('street_name_hash', 'not set')
    if street_name_hash == 'not set':
        return render_template('error.html', error='No street name hash set')
    return render_template('voter.html', voter=r[street_name_hash][voter_id])
    
def md5_hash(string):

    return str(hashlib.md5(string.encode('utf-8')).hexdigest())


if __name__ == '__main__':
    with open('data/data.pickle', 'rb') as handle:
        r = pickle.load(handle)
    app.run(debug=True)
