from bson import ObjectId
from flask.json import JSONEncoder
from flask import Flask, request
import json

from logging_and_configuration import log, json_reader
from pymongo import MongoClient


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


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
    team_document = teams.find_one({"name_olimp": request.args['team']})

    # handle empty result
    try:
        return json.dumps(team_document, cls=JSONEncoder)
    except Exception as e:
        log('An exception occurred: %s' % e)
        return str(e)


if __name__ == '__main__':

    # settings
    # read config
    json_config = json_reader('config.json')
    MONGO_HOST = json_config['mongo']['host']
    MONGO_PORT = json_config['mongo']['port']
    storage_app_host = json_config['storage_app']['host']
    storage_app_port = json_config['storage_app']['port']

    # init client for 'media' database
    client = MongoClient(MONGO_HOST, int(MONGO_PORT))
    log('Created MongoDB client.')

    # starting database manager
    log('Starting database manager...')
    app.run(debug=False, host=storage_app_host, port=storage_app_port)
