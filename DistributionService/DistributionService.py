import os
import shutil
import time

from logging_and_configuration import log, json_reader


class DistributionService:
    def __init__(self, config):
        self.refresh_interval = config['distribution_service']['refresh_interval']
        self.delimiter = config['distribution_service']['delimiter']
        self.roots = config['distribution_service']['roots']
        self.file_dict = {}  # this file list is a dict of a kind 'file name': 'generated destination'
        log('Distribution service initialized.')

    def lookup(self, root):
        # form a file list to distribute
        log('Looking for files in {root}...'.format(root=root))
        for s in os.listdir(root):
            if '.' and self.delimiter in s:
                self.file_dict[s] = ''
        time.sleep(self.refresh_interval)

    def process_filename(self, name, root):
        log('Parsing filename: {name}'.format(name=name))
        parsed_name = name.split(self.delimiter, 2)
        generated_path = os.path.join(root, parsed_name[0], parsed_name[1])
        self.file_dict[name] = os.path.join(root, generated_path)

    def move_to_new_path(self, path, name, root):
        # preparing to move
        original_full_file_path = os.path.join(root, name)
        new_file_path = os.path.join(root, path)
        log('Checking dir {dir}...'.format(dir=new_file_path))
        os.makedirs(new_file_path, exist_ok=True)

        # moving here
        log('Moving {name} to {path}...'.format(name=name, path=path))
        shutil.move(original_full_file_path, new_file_path)

    def run(self):
        log('Distribution service is running...')
        while True:
            for root in self.roots:
                # update file list
                self.lookup(root)

                # generate paths for found files
                for name in self.file_dict:
                    self.process_filename(name, root)

                # move files and delete (not copy), log it
                names_to_delete = []
                for name, path in self.file_dict.items():
                    self.move_to_new_path(path, name, root)
                    names_to_delete.append(name)

                # deleting processed file from files_dict
                for name in names_to_delete:
                    log('Removing deleted file name from files dict: %s' % self.file_dict.pop(name, None))


if __name__ == '__main__':
    config = json_reader('./../config.json')
    ds = DistributionService(config)
    ds.run()
