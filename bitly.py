import json

import requests

from environment import get_env

BITLY_HEDER = {'Authorization': f'Bearer {get_env().BITLY}', 'Content-Type': 'application/json'}



def bitly_shorter(url: str) -> str:
    data = json.dumps({"long_url":url})
    response = requests.post("https://api-ssl.bitly.com/v4/shorten", headers=BITLY_HEDER, data=data)

    return response.json()["link"]


def bitly_counter(short_url: str) -> int:
    response = requests.get(f'https://api-ssl.bitly.com/v4/bitlinks/{short_url}/clicks/summary', headers=BITLY_HEDER)
    return int(response.json()["total_clicks"])



