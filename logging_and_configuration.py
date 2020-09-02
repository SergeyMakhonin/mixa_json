import datetime
import json

name = 'server_log.txt'


def prepare_logfile():
    a = open(name, 'w')
    a.close()
    log("server log file {name} prepared.".format(name=name), fd=False)


def log(to_log, fd=True):
    string_to_log = '[{timestamp}] {data}'.format(timestamp=datetime.datetime.now(), data=to_log)
    print(string_to_log)
    if fd:
        with open(name, 'a', encoding="utf-8") as log_file_descriptor:
            print(string_to_log, file=log_file_descriptor)


def json_reader(json_path):
    with open(json_path, 'r') as fd:
        json_data = fd.read()
    json_config = json.loads(json_data)
    return json_config
