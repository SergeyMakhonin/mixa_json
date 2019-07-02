import platform
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler


# Restrict to a particular path.
#class RequestHandler(SimpleXMLRPCRequestHandler):
#    rpc_paths = ('/RPC2',)


# Create server
server = SimpleXMLRPCServer(("localhost", 8000))
server.register_introspection_functions()

# Register pow() function; this will use the value of
# pow.__name__ as the name, which is just 'pow'.
server.register_function(pow)


# Register a function under a different name
def get_os():
    return platform.platform()


server.register_function(get_os, 'get_os')


# Register an instance; all the methods of the instance are
# published as XML-RPC methods (in this case, just 'mul').
class MyFuncs:
    def mul(self, x, y):
        return x * y


server.register_instance(MyFuncs())

# Run the server's main loop
server.serve_forever()
