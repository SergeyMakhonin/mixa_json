import requests
import json
import time
from simple_logger import log


class JsonUpdaterDaemon:
    def __init__(self, json_config):
        self.running = True
        self.config = json_config
        self.wait = json_config['wait']

    def update(self):
        if self.config:
            for source in self.config['data_source']:
                log('Requesting data source {url}, to be written to "{file}"'.format(url=self.config['data_source'][source]['url'],
                                                                                     file=self.config['data_source'][source]['file']))
                r = requests.get(self.config['data_source'][source]['url'])
                if r.status_code == 200:
                    with open(self.config['data_source'][source]['file'], 'w+', encoding='utf-8') as fd:
                        response_json = json.dumps(r.text, ensure_ascii=False).encode('utf-8')
                        fd.write(response_json.decode('utf-8'))
                        log('JSON from {url} written.'.format(url=self.config['data_source'][source]['url']))
                else:
                    log('Unable to get JSON: status_code = %d' % r.status_code)
        else:
            log('No data sources configured: stopping')
            self.running = False

    def run(self):
        while self.running:
            self.update()
            time.sleep(self.wait)


def json_reader(json_path):
    with open(json_path, 'r') as fd:
        json_data = fd.read()
    json_config = json.loads(json_data)
    return json_config


if __name__ == '__main__':
    ju = JsonUpdaterDaemon(json_reader('config.json'))
    ju.run()
