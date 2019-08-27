import json
from logging_and_configuration import log, json_reader


class JsonBlazer(StorageRavager):
    def __init__(self, config):
        super().__init__(config)
        self.outcome_dict = {}  # a dict of a kind 'П1': '2.22' for managing multiple bet types
        self.json_data = None
        self.outcomes = {}  # outcomes is a list of dicts {'match_name': [{key: value}, {key: value}]}
        self.sports = {}  # sports is a dict of {'football': [{keys: values}, {keys: values}, {keys: values}]}
        self.json_path = config['server_data_file']
        self.parse_json()
        log('JSON blazer initialized')

    def flush(self):
        self.json_data = None
        self.outcomes = {}
        self.sports = {}

    def parse_json(self):
        # to avoid json_data stacking erase existing json_data
        self.flush()

        # read json file
        with open(self.json_path, encoding='utf-8') as fd:
            data = fd.read()
        self.json_data = json.loads(data)

        # check if json json_data is a dict
        if type(self.json_data) == str:
            self.json_data = json.loads(self.json_data)

        # check if its empty, then parse
        if len(self.json_data) > 0:
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
        else:
            log('JSON file is empty.')
            return False

    def return_all_sports(self):
        log('Available sports:')
        for i in self.sports:
            log(i)
        return ','.join(self.sports.keys())

    def return_logos(self, sport='Футбол'):
        # check on empty
        if len(self.sports) == 0:
            log('JSON is empty.')
            return False

        # call Storage Ravager
        logo1, logo2 = self.get_team_logos(team1=self.sports['Футбол'][0]['teams'][0],
                                           team2=self.sports['Футбол'][0]['teams'][1])
        log('Requesting logos by Storage Ravager for: {sport}'.format(sport=sport))
        return ','.join([logo1, logo2])

    def return_all_topics(self, topic='Футбол'):
        # check on empty
        if len(self.sports[topic]) == 0:
            log('JSON is empty.')
            return False

        # proceed if not empty
        topics = []
        log('Available events for %s:' % topic)
        for i in self.sports[topic]:
            topics.append(i['topic'])
            log(i['topic'])
        return ','.join(topics)

    def return_bet_types(self, topic_name):
        # check on empty
        if len(self.outcomes[topic_name]) == 0:
            log('JSON is empty.')
            return False

        # return all bet types for topic_name 'main,nextgoal'
        try:
            bet_types = ','.join(self.outcomes[topic_name].keys())
            log('Available bet types for {topic}: {bet_types}.'.format(topic=topic_name,
                                                                       bet_types=bet_types))
            return bet_types
        except KeyError:
            log('Unable to return bet types for %s.' % topic_name)
            log('No topic %s.' % topic_name)
            return False

    def return_outcome(self, topic_name, bet_type):
        # return values 'П1,Х,П2;1,2,3'
        try:
            bets = {}

            # fill bets
            for outcome in self.outcomes[topic_name][bet_type]:
                bets[outcome['bet_title']] = str(outcome['factor_value'])

            # now sort it as commented above
            names = []
            values = []
            for key, value in bets.items():
                names.append(key)
                values.append(value)
            bets_in_string = '{bet_titles}\n{values}'.format(bet_titles=','.join(names),
                                                             values=','.join(values))
            log('Available bets for {bet_type}: {bets}'.format(bet_type=bet_type,
                                                               bets=bets_in_string))
            return bets_in_string
        except KeyError:
            log('Unable to find outcome for {topic} and {bet_type}.'.format(topic=topic_name,
                                                                            bet_type=bet_type))
            return False

    def return_outcomes(self, topic_name, bet_types):
        # check bet_types
        if not bet_types:
            log('No bet types found for {topic}.'.format(topic=topic_name))
            return False

        # ensure that bet_types is actually a several comma-separated types of bets
        if not ',' in bet_types:
            if len(bet_types) > 0:
                bet_types += ','
            else:
                log('Incorrect input: bet_types should be a csv json_data or a single string which is a bet type name.')
                return False

        # ensure that outcome_dict is empty
        if self.outcome_dict:
            self.outcome_dict = {}

        # loop via bet types and get all outcomes from each bet type
        for bet_type in bet_types.split(','):
            if bet_type:
                outcome = self.return_outcome(topic_name, bet_type)
                self.parse_single_outcome(outcome)

        # parse fresh formed outcomes dict to provide output string of a kind 'П1,П2,Х,П3,П4,Ч;1,2,0,3,4'
        outcomes = self.prepare_outcomes_string()
        log('All available bets for {bet_types}: {outcomes}'.format(bet_types=bet_types,
                                                                    outcomes=outcomes))
        return outcomes

    def return_outcomes_no_names(self, topic_name, bet_types):
        outcomes = self.return_outcomes(topic_name, bet_types)
        noname_outcomes = outcomes.split('\n')[1]
        log('Returning outcomes without names: {noname_outcomes}'.format(noname_outcomes=noname_outcomes))
        return noname_outcomes

    def parse_single_outcome(self, outcome):
        if outcome:
            names, values = outcome.split('\n')
            names_list = names.split(',')
            values_list = values.split(',')

            # values and names lists should be same length, else below method wont work
            if len(names_list) == len(values_list):
                for name in names_list:
                    self.outcome_dict[name] = values_list[names_list.index(name)]
            else:
                log('Length discrepancy: {names} -- {values}'.format(names=names_list,
                                                                     values=values_list))
                return False
        else:
            log('Unable to parse outcome because its empty.')

    def prepare_outcomes_string(self):
        keys = []
        values = []
        for key, value in self.outcome_dict.items():
            keys.append(key)
            values.append(value)
        return ','.join(keys) + '\n' + ','.join(values)


if __name__ == '__main__':
    # Хёндай Стиил (жен) - Хвачхон КСПО (жен)
    # Ливерпуль - Норвич Сити
    j = JsonBlazer(json_reader('config.json'))
    j.return_all_topics()
    j.parse_json()
    # j.return_bet_types('Ливерпуль - Норвич Сити')
    # j.return_outcomes('Ливерпуль - Норвич Сити', 'main')
    j.return_outcomes_no_names('Ливерпуль - Норвич Сити', 'main')
    # j.return_outcome('Хёндай Стиил (жен) - Хвачхон КСПО (жен)', 'main')
