from flask import Flask, jsonify, request
from logging_and_configuration import log, json_reader
from pymongo import MongoClient
from storage_app.settings import *

app = Flask(__name__)


@app.route('/api/<path:sub_path>', methods=['GET'])
def return_team_data(sub_path):
    # should return available collections content (records)
    schema, collection = sub_path.split('/', 1)
    db = client[schema]
    teams = db[collection]
    team_document = teams.find_one({"name_olimp":request.args['team']})
    team_logo_destination = team_document['logo_destination']
    return team_logo_destination


if __name__ == '__main__':

    # init client for 'media' database
    client = MongoClient(MONGO_HOST, MONGO_PORT)
    log('Created MongoDB client.')

    # starting database manager
    log('Starting database manager...')
    app.run(debug=False)
