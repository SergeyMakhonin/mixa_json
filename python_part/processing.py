import json
from python_part.simple_logger import log


class JsonBlazer:
    def __init__(self, path):
        self.json_data = None
        self.sports = {}
        self.json_path = path
        self.parse_json()
        log('JSON blazer initialized')

    def parse_json(self):

        # read json file
        with open(self.json_path, encoding='utf-8') as fd:
            data = fd.read()
            self.json_data = json.loads(data)

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

    def return_all_sports(self):
        log('Available sports:')
        for i in self.sports:
            log(i)
        return ','.join(self.sports.keys())

    def return_all_topics(self, topic):
        topics = []
        log('Available events for %s:' % topic)
        for i in self.sports[topic]:
            topics.append(i['topic'])
            log(i['topic'])
        return ','.join(topics)


if __name__ == '__main__':
    j = JsonBlazer('../data/remote.json')
    j.return_all_sports()
    j.return_all_topics('Футбол')
