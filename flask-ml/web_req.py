import json
import requests

url = 'http://0.0.0.0:5000/heatmap'
#url = 'http://safetyassistant.us-east-1.elasticbeanstalk.com/api'
data = json.dumps({'day': 'Friday', 'place': '185 Berry st, San Francisco'})
print(data)
r = requests.get(url)
print(r.json())
