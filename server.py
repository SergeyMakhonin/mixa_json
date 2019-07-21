import sys
import platform
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from olymp_processing import JsonBlazer
from simple_logger import log
from json_updater import json_reader
from json_updater import JsonUpdaterDaemon
import threading


# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


# Register a function under a different name
def get_os():
    return platform.platform()


if __name__ == '__main__':
    try:
        # read config
        json_config = json_reader('config.json')

        # Create server
        host = json_config['server_host']
        port = json_config['server_port']
        server = SimpleXMLRPCServer((host, int(port)))

        # Register methods
        server.register_introspection_functions()
        server.register_function(get_os, 'get_os')

        # Register an instance; all the methods of the instance are published as XML-RPC methods
        server.register_instance(JsonBlazer('data/feed_4.json'))

        # init json updater and put it to own thread
        ju = JsonUpdaterDaemon(json_reader('config.json'))
        updater_thread = threading.Thread(target=ju.run)
        updater_thread.start()

        # Run the server's main loop
        log('\nServer is running on {host}:{port}.'.format(host=host, port=port))
        server.serve_forever()
    except KeyboardInterrupt:
        log('Interrupted from keyboard.\nStopped.')
        sys.exit(0)
