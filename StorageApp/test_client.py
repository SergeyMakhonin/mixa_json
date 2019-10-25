import requests

# teams
url = 'http://127.0.0.1:5000/api/media/teams'
r = requests.get(url)
print(r.text)

# commentors
url2 = 'http://127.0.0.1:5000/api/media/commentors'
r = requests.get(url2)
print(r.text)