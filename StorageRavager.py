import requests


class StorageRavager:
    __slots__ = ['config']

    def __init__(self, config):
        self.config = config

    def get_team_logos(self):
        url = 'http://{host}:{port}/api/'.format(host=self.config['storage']['host'],
                                                 port=self.config['storage']['port'])
        r = requests.get(url)

    def get_all_players_of_team(self):
        url = ''
        r = requests.get(url)
