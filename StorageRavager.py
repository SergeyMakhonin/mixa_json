import json

import requests
from logging_and_configuration import log, json_reader


class StorageRavager(object):
    __slots__ = ['config']

    def __init__(self, config):
        super(StorageRavager, self).__init__()
        self.config = config
        log('Storage Ravager initialized.')

    def get_team_logo(self, team):

        # form request url
        url = 'http://{host}:{port}/api/{database}/teams'.format(host=self.config['storage']['host'],
                                                                 port=self.config['storage']['port'],
                                                                 database=self.config['storage']['database_name'])
        payload = {'team': team}
        r = requests.get(url, params=payload)

        if r.status_code != 200:
            log('Database returned response code %d.' % r.status_code)
            log('Please check StorageApp log, collection or collection field may not exist.')
            return r.status_code

        # parse text
        response_dict = json.loads(r.text)

        # get logo path
        logo_path = response_dict['logo_path']

        # returns string of a kind: 'team,team1_logo_path'
        log('Returning logo_path: %s' % logo_path)
        return logo_path

    def get_team_short_name_localized(self, team):
        # form request url
        url = 'http://{host}:{port}/api/{database}/teams'.format(host=self.config['storage']['host'],
                                                                 port=self.config['storage']['port'],
                                                                 database=self.config['storage']['database_name'])
        payload = {'team': team}
        r = requests.get(url, params=payload)

        if r.status_code != 200:
            log('Database returned response code %d.' % r.status_code)
            log('Please check StorageApp log, collection or collection field may not exist.')
            return r.status_code

        # parse text
        response_dict = json.loads(r.text)

        # get logo path
        name_short_localized = response_dict['name_short_localized']

        # returns string
        log('Returning short name localized: %s' % name_short_localized)
        return name_short_localized


if __name__ == '__main__':
    s = StorageRavager(json_reader('config.json'))
    s.get_team_logo("Arsenal")  # "Хвачхон КСПО (жен)"
    s.get_team_short_name_localized('Arsenal')
