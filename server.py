import sys
import datetime
import platform
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from script import JsonGrinder


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
        port = 55999
        server = SimpleXMLRPCServer((host, port))

        # Register methods
        server.register_introspection_functions()
        server.register_function(get_os, 'get_os')

        # Register an instance; all the methods of the instance are published as XML-RPC methods
        server.register_instance(JsonGrinder())

        # Run the server's main loop
        print('[{timestamp}] Server is running on {host}:{port}.'.format(timestamp=datetime.datetime.now(),
                                                                         host=host,
                                                                         port=port))
        server.serve_forever()
    except KeyboardInterrupt:
        print('[%s] Interrupted from keyboard.\nStopped.' % datetime.datetime.now())
        sys.exit(0)
