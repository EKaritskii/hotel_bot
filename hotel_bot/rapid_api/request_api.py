import requests
from loader import bot
from requests.exceptions import ConnectTimeout


def request_to_api(url, headers, querystring, message):
    try:
        response = requests.request(
            "GET", url, headers=headers, params=querystring, timeout=60
        )
        if response.status_code == requests.codes.ok:
            return response
    except ConnectTimeout:
        bot.send_message(message.from_user.id, "данные не коррестны!")
        return
