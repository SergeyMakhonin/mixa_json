import sys
import platform
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from DevourersEater import DevourersEater
from logging_and_configuration import log, json_reader, prepare_logfile
from JsonUpdater import JsonUpdaterDaemon
import threading


# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


# Register a function under a different name
def get_os():
    return platform.platform()


if __name__ == '__main__':
    try:
        # prepare server log
        prepare_logfile()

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
        server.register_instance(DevourersEater(json_config))

        # init json updater and put it in its own thread
        ju = JsonUpdaterDaemon(json_config)
        updater_thread = threading.Thread(target=ju.run)
        updater_thread.start()

        # Run the server's main loop
        log('Server is running on {host}:{port}.'.format(host=host, port=port))
        server.serve_forever()
    except KeyboardInterrupt:
        log('Interrupted from keyboard. Stopped.')
        sys.exit(0)
