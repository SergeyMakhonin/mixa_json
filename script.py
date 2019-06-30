import json
import pprint

path = 'live.json'



class RootObject:
    def __init__(self):
        self.json_data = None
        self.sports = []
        self.league = []
        self.event = []

    def load_json_data(self, path):
        with open(path, encoding='utf-8') as fd:
            data = fd.read()
            self.json_data = json.loads(data)

    def parse_json_data(self):
        for key, value in self.parsed_json:
