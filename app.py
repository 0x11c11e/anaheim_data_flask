import hashlib
import pickle
import uuid
from datetime import datetime
import collections

from flask import Flask, render_template, session
from flask_session import Session

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


r = {}
rr = {}
with open('data/data.pickle', 'rb') as handle:
    r = pickle.load(handle)
try:
    rr = pickle.load(open("data/checkbox.pickle", "rb"))
except (OSError, IOError) as e:
    pickle.dump(rr, open("data/checkbox.pickle", "wb"))

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

@app.route('/search/voters/printable/<string:street_name>', methods=['GET'])
def search_voters_printable(street_name):
    grouped_voters, street_name, dt = search_voters(street_name)

    return render_template('search_voters_printable.html', grouped_voters=grouped_voters, street_name=street_name, dt=dt)

@app.route('/search/voters/<string:street_name>', methods=['GET'])
def search_voters_html(street_name):
    grouped_voters, street_name, dt = search_voters(street_name)
    
    return render_template('search_voters.html', grouped_voters=grouped_voters, street_name=street_name, dt=dt, rr=rr)


@app.route('/search/voter/<string:voter_id>', methods=['GET'])
def search_voter(voter_id):
    street_name_hash = session.get('street_name_hash', 'not set')
    if street_name_hash in 'not set':
        return render_template('error.html', error='No street name hash found in session')
    voter = r[street_name_hash][voter_id]

    return render_template('voter.html', voter=voter)

def search_voters(street_name):
    voters = {}
    street_name_hash = md5_hash(street_name)
    voter_ids = list(r[street_name_hash].keys())
    for voter_id in voter_ids:
        voters[voter_id] = r[street_name_hash][voter_id]
    session['street_name_hash'] = street_name_hash
    dt = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
    grouped_voters = {}
    for voter_id in voters.keys():
        if voters[voter_id][9] not in grouped_voters:
            grouped_voters[voters[voter_id][9]] = [voters[voter_id]]
        else:
            grouped_voters[voters[voter_id][9]].append(voters[voter_id])
    grouped_voters = collections.OrderedDict(sorted(grouped_voters.items()))
    grouped_odds = {}
    grouped_evens = {}
    for group in grouped_voters.keys():
        if int(str(group).split(' ')[0]) % 2 == 0:
            grouped_evens[group] = grouped_voters[group]
        elif int(str(group).split(' ')[0]) % 2 == 1:
            grouped_odds[group] = grouped_voters[group]
    grouped_voters = grouped_odds | grouped_evens

    return grouped_voters, street_name, dt

@app.route('/search/voter/is_checked/<string:checkbox_id>', methods=['GET'])
def voter_checkbox(checkbox_id):
    try:
        rr[checkbox_id] = not rr[checkbox_id]
    except KeyError:
        rr[checkbox_id] = True
        
    pickle.dump(rr, open("data/checkbox.pickle", "wb"))
    print(rr[checkbox_id])
    
    return('', 200)
    
def md5_hash(string):

    return str(hashlib.md5(string.encode('utf-8')).hexdigest())

def get_uuid():

    return str(uuid.UUID(int=uuid.getnode()))


if __name__ == '__main__':
    port = 80
    host = '0.0.0.0'
    if get_uuid() == '00000000-0000-0000-0000-6aa20e141e0f':
        port = 5000
        host = '127.0.0.1'
    app.run(debug=True, port=port, host=host)
