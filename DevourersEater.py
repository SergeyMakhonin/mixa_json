from JsonBlazer import JsonBlazer
from StorageRavager import StorageRavager
from logging_and_configuration import json_reader


class DevourersEater(JsonBlazer, StorageRavager):
    """
    This class is a proxy class to ease XML-RPC interaction.
       It mixes classes methods into one class and when initialized,
       all methods of mixed classes are available via XML-RPC server in one registration.
    """
    def __init__(self, config):
        super(DevourersEater, self).__init__(config)
        self.config = config

if __name__ == '__main__':
    config = json_reader('config.json')
    d = DevourersEater(config)
    pass
