import sys
import platform
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

from python_part.processing import JsonBlazer
from python_part.simple_logger import log


# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


# Register a function under a different name
def get_os():
    return platform.platform()


if __name__ == '__main__':
    try:
        # Create server
        host = 'localhost'
        port = 8000
        server = SimpleXMLRPCServer((host, port))

        # Register methods
        server.register_introspection_functions()
        server.register_function(get_os, 'get_os')

        # Register an instance; all the methods of the instance are published as XML-RPC methods
        server.register_instance(JsonBlazer())

        # Run the server's main loop
        log('Server is running on {host}:{port}.'.format(host=host,
                                                         port=port))
        server.serve_forever()
    except KeyboardInterrupt:
        log('Interrupted from keyboard.\nStopped.')
        sys.exit(0)
