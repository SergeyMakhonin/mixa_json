import requests
import json
import time
import xmlrpc.client
from simple_logger import log


class JsonUpdaterDaemon:
    def __init__(self, json_config):
        self.running = True
        self.config = json_config
        self.wait = json_config['wait']
        self.xmlrpc_client = xmlrpc.client.ServerProxy('http://{host}:{port}/RPC2'.format(host=self.config['server_host'],
                                                                                          port=self.config['server_port']))
        log('JSON Updater initialized.')

    def refresh_data(self):
        self.xmlrpc_client.parse_json()
        log('In-memory JSON refreshed.')

    def update(self):
        if self.config:
            for source in self.config['data_source']:
                log('Requesting data source {url}, to be written to "{file}"'.format(url=self.config['data_source'][source]['url'],
                                                                                     file=self.config['data_source'][source]['file']))
                try:
                    r = requests.get(self.config['data_source'][source]['url'])
                    if r.status_code == 200:
                        with open(self.config['data_source'][source]['file'], 'w+', encoding='utf-8') as fd:
                            response_json = json.dumps(r.text, ensure_ascii=False).encode('utf-8')
                            fd.write(response_json.decode('utf-8'))
                            log('JSON from {url} written.'.format(url=self.config['data_source'][source]['url']))
                            log('JSON file {file} updated.'.format(file=self.config['data_source'][source]['file']))
                    else:
                        log('Unable to get JSON: status_code = %d' % r.status_code)
                except requests.ConnectionError:
                    log('Unable to connect to {url}.'.format(url=self.config['data_source']['test_source']['url']))
        else:
            log('No data sources configured: stopping')
            self.running = False

    def run(self):
        while self.running:
            self.update()

            # wait after update, before asking server to re-read json
            time.sleep(self.wait/2)
            self.refresh_data()

            # wait before starting next update
            time.sleep(self.wait/2)


def json_reader(json_path):
    with open(json_path, 'r') as fd:
        json_data = fd.read()
    json_config = json.loads(json_data)
    return json_config


if __name__ == '__main__':
    ju = JsonUpdaterDaemon(json_reader('config.json'))
    ju.run()
