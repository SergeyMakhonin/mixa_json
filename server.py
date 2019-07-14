import platform
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from script import RootObject


# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


# Register a function under a different name
def get_os():
    return platform.platform()


# Create server
server = SimpleXMLRPCServer(("localhost", 8000))

# Register methods
server.register_introspection_functions()
server.register_function(get_os, 'get_os')

# Register an instance; all the methods of the instance are published as XML-RPC methods
server.register_instance(RootObject())

# Run the server's main loop
print('Server is running.')
server.serve_forever()
