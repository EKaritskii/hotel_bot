import json
from loader import headers
import rapid_api


def dest(hotel_id, checkin, checkout, message, hotel_dest):
    count = 0
    for dt in hotel_dest:
        url_list = "https://hotels4.p.rapidapi.com/properties/list"
        querystring_list = {"destinationId": dt, "pageNumber": "1",
                            "pageSize": "25", "checkIn": checkin,
                            "checkOut": checkout, "adults1": "1",
                            "priceMin": "1", "sortOrder": "PRICE",
                            "locale": "en_US", "currency": "USD"}
        try:
            response = rapid_api.request_api.request_to_api(url_list, headers, querystring_list, message)
            if response != None:
                data = json.loads(response.text)
                if data['result'] == 'OK':
                    if data['data']['body']['query']['destination']['id'] == dt:
                        path = data['data']['body']['searchResults']['results']
                        for result in path:
                            count = list_appender(count, hotel_id, result)
        except KeyError or NameError:
            print('Данные не найдены!')


def list_appender(count: int, hotel_id, list_info):
    try:
        hotel_id.append(dict())
        hotel_id[count]['address'] = list_info['address']['streetAddress']
        hotel_id[count]['center'] = list_info['landmarks'][0]['distance']
        hotel_id[count]['price'] = list_info['ratePlan']['price']['exactCurrent']
        hotel_id[count]['name'] = list_info['name']
        hotel_id[count]['id'] = list_info['id']
        key = 1

    except KeyError:
        print("Данные не корректны!")
        hotel_id.pop(count)
        key = 0

    finally:
        if key == 1:
            return count + 1
        else:
            return count
