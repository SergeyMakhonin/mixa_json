from JsonBlazer import JsonBlazer
from StorageRavager import StorageRavager
from logging_and_configuration import json_reader


class DevourersEater(JsonBlazer, StorageRavager):
    def __init__(self, config):
        super(DevourersEater, self).__init__(config)
        self.config = config

if __name__ == '__main__':
    config = json_reader('config.json')
    d = DevourersEater(config)
    pass
