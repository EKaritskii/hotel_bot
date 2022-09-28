import json
from loader import bot, headers
import rapid_api
from rapid_api.history_com import hist_add


def photo_send(photo, message, hotel_info, hotel):
    url_photo = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
    querystring_photo = {"id": hotel_info[hotel]['id']}

    response = rapid_api.request_api.request_to_api(url_photo, headers, querystring_photo, message)
    if response != None:
        data_photo = json.loads(response.text)
        for i_photo in range(0, int(photo)):
            try:
                p_url = data_photo["hotelImages"][i_photo]["baseUrl"]
                bot.send_photo(
                    message.message.chat.id, p_url.format(size='z')
                )
                hist_add(message.from_user.id, message.message.chat.id, p_url)
            except FileNotFoundError:
                print('Фото не загрузилось')

