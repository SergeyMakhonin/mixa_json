from flask import Flask, request
import json
from logging_and_configuration import log
from pymongo import MongoClient
from StorageApp.settings import *

app = Flask(__name__)


@app.route('/api/<path:sub_path>', methods=['GET'])
def return_team_data(sub_path):
    # should return available collections content (records)
    schema, collection = sub_path.split('/', 1)

    # get schema (database) access
    db = client[schema]

    # get a collection (table) access
    teams = db[collection]

    # search in collection
    team_document = teams.find_one({"name_epl": request.args['team']})
    del team_document['_id']
    return json.dumps(team_document, ensure_ascii=False)


if __name__ == '__main__':

    # init client for 'media' database
    client = MongoClient(MONGO_HOST, MONGO_PORT)
    log('Created MongoDB client.')

    # starting database manager
    log('Starting database manager...')
    app.run(debug=False)
