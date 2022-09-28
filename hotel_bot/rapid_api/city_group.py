import re
import json
from loader import bot, headers
import rapid_api


def city_api(message, hotel_dest, loc):
    querystring_search = {"query": loc, "locale": "en_US", "currency": "USD"}
    url_search = "https://hotels4.p.rapidapi.com/locations/v2/search"

    response = rapid_api.request_api.request_to_api(url_search, headers, querystring_search, message)
    if response != None:
        try:
            pattern = r'(?<="CITY_GROUP",).+?[\]]'
            find = re.search(pattern, response.text)
            if find:
                data_search = json.loads(f"{{{find[0]}}}")
            else:
                bot.send_message(message.from_user.id, "Название города введено не коррестно!")
                return
            for entitle in data_search['entities']:
                hotel_dest.append(entitle['destinationId'])
            return hotel_dest
        except NameError:
            bot.send_message(message.from_user.id, "Название города введено не коррестно!")
            return
    else:
        return
