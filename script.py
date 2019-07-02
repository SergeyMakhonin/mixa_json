import json
import sys


class RootObject:
    def __init__(self):
        self.json_data = None
        self.sports = []
        self.league = []
        self.event = []

    def load_json_data(self, path):
        # this works on python 3 only
        with open(path, encoding='utf-8') as fd:
            data = fd.read()
            self.json_data = json.loads(data)

    def load_json_from_string(self, json_string):
        self.json_data = json.loads(json_string, encoding='utf-8')

    def parse_json_data(self):
        for key in self.json_data:
            # get all sport types on this level
            self.sports.append({self.json_data[key]['name']: {self.json_data[key]['id']}})

            # get all league types on this level
            for league_id in self.json_data[key]['league']:
                self.league.append({self.json_data[key]['league'][league_id]['name']:
                                        (key,
                                         'league',
                                         self.json_data[key]['league'][league_id])
                                    }
                                   )

                # get all events per league
                for event_id in self.json_data[key]['league'][league_id]['event']:
                    self.event.append({self.json_data[key]['league'][league_id]['event'][event_id]['name']:
                                           (key,
                                            'league',
                                            self.json_data[key]['league'][league_id],
                                            'event',
                                            self.json_data[key]['league'][league_id]['event'][event_id]
                                            )
                                       }
                                      )

    def return_all_sports(self):
        print('Sport types available:')
        sport_names = []
        for sport in self.sports:
            sport_names.extend([*sport])
            print([*sport][0])
        return sport_names


if __name__ == '__main__':
    # set path
    # if not path provided set path to 'live.json'
    try:
        path = sys.argv[1]
    except IndexError as e:
        path = 'live.json'
        print('Exception: %s.' % e)
        print('No input file provided, using default "%s".' % path)

    # init RootObject that will contain all JSON data parsed
    rt = RootObject()

    # load JSON file
    rt.load_json_data(path)
    #from test_string import json_data
    #rt.load_json_from_string(json_data)

    # parse loaded JSON file
    rt.parse_json_data()

    # return all sports available
    rt.return_all_sports()
