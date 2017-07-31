import json
import requests

url = 'http://safetyassistant.eu-west-2.elasticbeanstalk.com/api'
data = json.dumps({'day': 'Monday', 'place': 'California St, San Francisco, CA'})
r = requests.post(url, data)
print(r.json())
