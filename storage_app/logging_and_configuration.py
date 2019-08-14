import datetime
import json


def log(to_log, fd=None):
    string_to_log = '[{timestamp}] {data}'.format(timestamp=datetime.datetime.now(),
                                                  data=to_log)
    print(string_to_log)
    if fd:
        print(string_to_log, file=fd)


def json_reader(json_path):
    with open(json_path, 'r') as fd:
        json_data = fd.read()
    json_config = json.loads(json_data)
    return json_config
