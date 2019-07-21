import xmlrpc.client

s = xmlrpc.client.ServerProxy('http://localhost:8000/RPC2')

# Print list of available methods

#print(s.system.listMethods())
#print(s.get_os())
#print(s.load_json_data('live.json'))
#print(s.parse_json_data())
#print(s.return_all_sports())
print(s.return_all_topics())
#print(s.return_outcomes('Ливерпуль - Норвич Сити'))
