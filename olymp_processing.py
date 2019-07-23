import json
from simple_logger import log


class JsonBlazer:
    def __init__(self, path):
        self.json_data = None
        self.outcomes = {}  # outcomes is a list of dicts {'match_name': [{key: value}, {key: value}]}
        self.sports = {}  # sports is a dict of {'football': [{keys: values}, {keys: values}, {keys: values}]}
        self.json_path = path
        self.parse_json()
        log('JSON blazer initialized')

    def flush(self):
        self.json_data = None
        self.outcomes = {}
        self.sports = {}

    def parse_json(self):

        # to avoid data stacking erase existing data
        self.flush()

        # read json file
        with open(self.json_path, encoding='utf-8') as fd:
            data = fd.read()
            self.json_data = json.loads(data, encoding='utf-8')

        for i in self.json_data:
            if i['sport_type_title'] in self.sports:
                sub_dict = {'id': i['sport_type_id'],
                            'topic': i['topic'],
                            'event_id': str(i['event_id']),
                            'event_title': i['event_title'],
                            'teams': (i['team1'], i['team2'],),
                            'start_date2': i['start_date2'],
                            'start_date_timestamp': str(i['start_date_timestamp']),
                            'url': i['url'],
                            'url_mobile': i['url_mobile']
                            }
                self.sports[i['sport_type_title']].append(sub_dict)
            else:
                self.sports.update(
                    {i['sport_type_title']: [
                        {'id': i['sport_type_id'],
                         'topic': i['topic'],
                         'event_id': str(i['event_id']),
                         'event_title': i['event_title'],
                         'teams': (i['team1'], i['team2'],),
                         'start_date2': i['start_date2'],
                         'start_date_timestamp': str(i['start_date_timestamp']),
                         'url': i['url'],
                         'url_mobile': i['url_mobile']
                         }
                    ]
                    }
                )
            sub_dict_outcomes = {i['topic']: i['outcomes']}
            # if we'll need to find specific outcomes do it here
            self.outcomes.update(sub_dict_outcomes)
        return True

    def return_all_sports(self):
        log('Available sports:')
        for i in self.sports:
            log(i)
        return ','.join(self.sports.keys())

    def return_all_topics(self, topic='Футбол'):
        topics = []
        log('Available events for %s:' % topic)
        for i in self.sports[topic]:
            topics.append(i['topic'])
            log(i['topic'])
        return ','.join(topics)

    def return_bet_types(self, topic_name):
        # return all bet types for topic_name  'main,nextgoal'
        try:
            bet_types = ','.join(self.outcomes[topic_name].keys())
            log('Available bet types for {topic}: {bet_types}.'.format(topic=topic_name,
                                                                       bet_types=bet_types))
            return bet_types
        except KeyError:
            log('Unable to return bet types for %s.' % topic_name)
            log('No topic %s.' % topic_name)
            return False

    def return_outcomes(self, topic_name, bet_type):
        # return values 'П1,Х,П2;1,2,3'
        try:
            bets = {
#                'П1': None,
#                'Х': None,
#                'П2': None
            }

            # fill bets
            for outcome in self.outcomes[topic_name][bet_type]:
                for key, value in outcome.items():
                    bets[outcome['bet_title']] = str(outcome['factor_value'])

            # now sort it as commented above
            names = []
            values = []
            for key, value in bets.items():
                names.append(key)
                values.append(value)
            bets_in_string = '{bet_titles};{values}'.format(bet_titles=','.join(names),
                                                            values=','.join(values))
            log('Available bets: %s' % bets_in_string)
            return bets_in_string
        except KeyError:
            log('Unable to find outcome for {topic} and {bet_type}.'.format(topic=topic_name,
                                                                            bet_type=bet_type))
            return False


if __name__ == '__main__':
    j = JsonBlazer('data/feed.json')
#    j.return_all_sports()
#    j.return_all_topics()
    j.return_bet_types('Хёндай Стиил (жен) - Хвачхон КСПО (жен)')
    j.return_outcomes('Хёндай Стиил (жен) - Хвачхон КСПО (жен)', 'nextgoal')
