"""
Delete this file if not being used.
"""

import requests
from customLibrary.custom_settings import FCM_SERVER_KEY
from customLibrary.views_lib import obj_to_json_str


def send_http(device_id, data_dict):
    url = 'https://fcm.googleapis.com/fcm/send'
    headers = {'Content-Type': 'application/json', 'Authorization': 'key='+FCM_SERVER_KEY}
    json_data = {'to': device_id, 'data': data_dict}
    json_str = obj_to_json_str(json_data)
    response = requests.post(url=url, data=json_str, headers=headers)
    if response.status_code == 200:
        return True
    else:
        return False


def send_xmpp(device_id, data_dict):
    pass