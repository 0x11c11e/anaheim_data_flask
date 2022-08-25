import hashlib
import json
import pickle
import re
import shelve
from datetime import datetime

import boto3
from boto3.dynamodb.conditions import Attr, Key
from flask import (Flask, flash, json, jsonify, redirect, render_template,
                   request, url_for)
import urllib.request as urllib2

app = Flask(__name__)

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

    dt = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))

    return render_template('search_voters.html', voters=voters, voter_ids=voter_ids, dt=dt, street_name=street_name)


def md5_hash(string):

    return str(hashlib.md5(string.encode('utf-8')).hexdigest())


if __name__ == '__main__':
    with open('data/data.pickle', 'rb') as handle:
        r = pickle.load(handle)
    app.run(debug=True)
