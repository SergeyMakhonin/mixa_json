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

    def parse_json(self):

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

    def return_outcomes(self, topic_name):
        # return values 'П1,Х,П2'
        try:
            outcomes_to_return = []
            for bet in self.outcomes[topic_name]:
                bet_value = str(bet['factor_value'])
                outcomes_to_return.append(bet_value)
                log(bet_value)
            return ','.join(outcomes_to_return)
        except KeyError:
            log('Unable to find %s in current JSON data.' % topic_name)
            return False


if __name__ == '__main__':
    j = JsonBlazer('data/feed_4.json')
#    j.return_all_sports()
    j.return_all_topics()
    j.return_outcomes('Вест Хэм - Манчестер Сити')
