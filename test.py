import time

import requests
import json

url = "https://api.iot.yandex.net/v1.0/devices/actions"

headers = {
  'Authorization': 'Bearer ***',
  'Content-Type': 'application/json'
}
def lamp(state):
    payload = {
        "devices": [
            {
                "id": "334a267c-e81e-4a1d-8d18-64282cb6fd24",
                "actions": [
                    {
                        "type": "devices.capabilities.on_off",
                        "state": {
                            "instance": "on",
                            "value": state
                        }
                    }
                ]
            }
        ]
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    return response.json()
while True:
    time.sleep(5)
    lamp(True)
    time.sleep(5)
    lamp(False)
