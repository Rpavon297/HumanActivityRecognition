from datetime import datetime

import requests
import json
from django.utils import timezone

url = 'http://127.0.0.1:8000/predictor/getdataset/'
message = dict(x='', y='', z='')

message['activity'] = "cantar"

x = requests.post(url, data=message)

resp = json.loads(x.content.decode('utf-8'))

print(resp)