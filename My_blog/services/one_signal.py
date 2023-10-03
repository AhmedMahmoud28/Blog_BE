import json

import requests
from decouple import config

# onesignal app_id
ONESIGNAL_APP_ID = config("ONESIGNAL_APP_ID", default="", cast=str)
url = "https://onesignal.com/api/v1/notifications/"
headers = {"content-type": "application/json"}


def one_signal_notification(player_ids, text, data=None):
    if not player_ids:
        return "no player ids"
    payload = {
        "include_player_ids": player_ids,
        "app_id": ONESIGNAL_APP_ID,
        "ios_badgeType": "Increase",
        "ios_badgeCount": 1,
        "contents": {"en": text},
    }
    if data:
        payload["data"] = data
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    return response.text
