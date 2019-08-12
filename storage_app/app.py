from flask import Flask, jsonify
from ...mixa_json.logging_and_configuration import log, json_reader
from pymongo import MongoClient
from storage_app.settings import *

app = Flask(__name__)


@app.route('/api', methods=['GET'])
def index():
    # should return an api reference
    return jsonify(supported_methods=['GET', 'POST', 'UPDATE', 'DELETE'])


@app.route('/api/<schema_name>', methods=['GET'])
def return_schema_collections(schema_name):
    # should return all available collections
    db = client[schema_name]
    return jsonify(collection_names=db.list_collection_names())


@app.route('/api/<path:sub_path>', methods=['GET'])
def return_collection_content(sub_path):
    # should return available collections content (records)
    schema, collection = sub_path.split(',', 1)
    db = client[schema]
    return jsonify(db[collection].find())


@app.route('/api/<path:sub_path>', methods=['GET'])
def get_team1_logo(sub_path):
    return ''


@app.route('/api/<path:sub_path>', methods=['GET'])
def get_team2_logo(sub_path):
    return ''


if __name__ == '__main__':

    # init client for 'media' database
    client = MongoClient(MONGO_HOST, MONGO_PORT)
    log('Created MongoDB client.')

    # starting database manager
    log('Starting database manager...')
    app.run(debug=True)
