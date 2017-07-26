import json
import requests

url = 'http://0.0.0.0:5000/api'
data = json.dumps({'day': 'Monday', 'place': 'California St, San Francisco, CA'})
r = requests.post(url, data)
print(r.json())