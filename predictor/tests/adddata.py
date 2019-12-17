from datetime import datetime

import requests
from django.utils import timezone

url = 'http://127.0.0.1:8000/predictor/capture/'
message = dict(x='', y='', z='')

for i in range(5):
    message['accelx'] = 1
    message['accely'] = 1
    message['accelz'] = 1
    message['gyrox'] = 1
    message['gyroy'] = 1
    message['gyroz'] = 1
    message['velx'] = 1
    message['vely'] = 1
    message['velz'] = 1
    message['activity'] = "pescar"

    message['instant'] = datetime.now(tz=timezone.utc)
    x = requests.post(url, data=message)
    print(x.content)
for i in range(5):
    message['accelx'] = 2
    message['accely'] = 2
    message['accelz'] = 2
    message['gyrox'] = 2
    message['gyroy'] = 2
    message['gyroz'] = 2
    message['velx'] = 2
    message['vely'] = 2
    message['velz'] = 2
    message['activity'] = "cantar"

    message['instant'] = datetime.now(tz=timezone.utc)
    x = requests.post(url, data=message)
    print(x.content)
for i in range(5):
    message['accelx'] = 3
    message['accely'] = 3
    message['accelz'] = 3
    message['gyrox'] = 3
    message['gyroy'] = 3
    message['gyroz'] = 3
    message['velx'] = 3
    message['vely'] = 3
    message['velz'] = 3
    message['activity'] = "dormir"

    message['instant'] = datetime.now(tz=timezone.utc)
    x = requests.post(url, data=message)
    print(x.content)
print("ok")
