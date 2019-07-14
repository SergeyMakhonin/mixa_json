import json
import sys
import datetime


class JsonGrinder:
    def __init__(self):
        self.path = 'python_part/live.json'
        self.json_data = None
        self.sports = []
        self.league = []
        self.event = []
        self.load_json_data()
        self.parse_json_data()

    def load_json_data(self):
        # this works on python 3 only
        with open(self.path, encoding='utf-8') as fd:
            data = fd.read()
            self.json_data = json.loads(data)
        return True

    def load_json_from_string(self, json_string):
        self.json_data = json.loads(json_string, encoding='utf-8')
        return self.json_data

    def parse_json_data(self):
        for key in self.json_data:
            # get all sport types on this level
            self.sports.append({self.json_data[key]['name']: str(self.json_data[key]['id'])})

            # get all league types on this level
            for league_id in self.json_data[key]['league']:
                self.league.append({self.json_data[key]['league'][league_id]['name']:
                                        (key,
                                         'league',
                                         self.json_data[key]['league'][league_id]['id'])
                                    }
                                   )

                # get all events per league
                for event_id in self.json_data[key]['league'][league_id]['event']:
                    self.event.append({self.json_data[key]['league'][league_id]['event'][event_id]['name']:
                                           (key,
                                            'league',
                                            self.json_data[key]['league'][league_id]['id'],
                                            'event',
                                            event_id
                                            )
                                       }
                                      )
        return True

    def return_all_sports(self):
        print('Sport types available:')
        sport_names = []
        for sport in self.sports:
            sport_names.extend([*sport])

            # show found sports
            print([*sport][0])

        # return comma separated string
        return ','.join(sport_names)

    def return_leagues(self, sport_type):
        print('Leagues available for %s:' % sport_type)
        for sport_dict in self.sports:
            if sport_type in sport_dict.keys():
                sport_id = sport_dict[sport_type]
                break
        try:
            league_names = []
            for league in self.league:
                for league_name, league_info in league.items():
                    if sport_id == league_info[0]:
                        league_names.append(league_name)

            # return found leagues
            for l in league_names:
                print(l)

            # return comma separated string
            return ','.join(league_names)
        except NameError:
            print('[{time}] {sport_type} does not exist in current JSON version.'.format(time=datetime.datetime.now(),
                                                                                         sport_type=sport_type))


if __name__ == '__main__':
    # set path
    # if not path provided set path to 'live.json'
    try:
        path = sys.argv[1]
    except IndexError as e:
        path = 'python_part/live.json'
        print('Exception: %s.' % e)
        print('No input file provided, using default "%s".' % path)

    # init JsonGrinder that will contain all JSON data parsed
    rt = JsonGrinder()

    # load JSON file
    #rt.load_json_data()
    #from test_string import json_data
    #rt.load_json_from_string(json_data)

    # parse loaded JSON file
    #rt.parse_json_data()

    # return all sports available
    #rt.return_all_sports()
    rt.return_leagues('Футбол')
