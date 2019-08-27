import requests
from logging_and_configuration import log, json_reader


class StorageRavager:
    __slots__ = ['config']

    def __init__(self, config):
        self.config = config
        log('Storage Ravager initialized.')

    def get_team_logos(self, team):

        # form request url
        url = 'http://{host}:{port}/api/{database}/Teams'.format(host=self.config['storage']['host'],
                                                                 port=self.config['storage']['port'],
                                                                 database=self.config['storage']['database_name'])
        payload = {'team': team}
        r = requests.get(url, params=payload)

        # get logo paths
        team_logo_path = r.text

        # returns string of a kind: 'topic_name,team1,team1_logo_path,team2,team2_logo_path
        return ','.join(team_logo_path)

    def get_team_short_name_localized(self, team):
        pass


if __name__ == '__main__':
    s = StorageRavager(json_reader('config.json'))
    s.get_team_logos("Хёндай Стиил (жен)")  # "Хвачхон КСПО (жен)"
