from loader import bot
import rapid_api
from .best_deal_help import print_teleg_best
from .history_com import hist_add


def sorting(hotel_dict):
    return hotel_dict['price']


def get_1(message):
    hotel_dest = list()

    with bot.retrieve_data(message.from_user.id, message.message.chat.id) as data:
        loc = data["loc"]

    hotel_dest = rapid_api.city_group.city_api(message, hotel_dest, loc)
    if hotel_dest == None:
        return
    get_2(message, hotel_dest)


def get_2(message, hotel_dest):
    hotel_id = list()
    with bot.retrieve_data(message.from_user.id, message.message.chat.id) as data:
        checkin = data['check_in']
        checkout = data['check_out']
        mode = data['mode']

    rapid_api.destination.dest(hotel_id, checkin, checkout, message, hotel_dest)
    if mode == 'low' or mode == 'best':
        hotel_id.sort(key=sorting, reverse=False)
    else:
        hotel_id.sort(key=sorting, reverse=True)
    hotel_info = hotel_id
    if mode != 'best':
        print_teleg(message, hotel_info)
    else:
        print_teleg_best(message, hotel_info)


def print_teleg(message, hotel_info):
    with bot.retrieve_data(message.from_user.id, message.message.chat.id) as data:
        max_hotel = data["max_hotel"]
        photo = data['photo']
        checkin = data['check_in']
        checkout = data['check_out']
        all_1 = checkin - checkout
        all_time = str(all_1)
        time_list = all_time.split()
        all_time_int = int(time_list[0][1:])
    name_check = ''
    count_right = 0
    for i_hotel in range(0, int(max_hotel)):
        hotel = i_hotel + count_right
        try:
            if name_check == hotel_info[hotel]['name']:
                while name_check == hotel_info[hotel]['name']:
                    count_right += 1
                    hotel = i_hotel + count_right
            string = "Отель номер {0}\nНазвание: {1}\nАдрес: {2}\n" \
                     "Расположен в {3} от центра\n" \
                     "Цена за комнату(в день): {4} долларов\n" \
                     "Цена за комнату(за все время): {5} долларов\n" \
                     "Ссылка: hotels.com/ho{6}".\
                format(i_hotel + 1, hotel_info[hotel]['name'],
                       hotel_info[hotel]['address'],
                       hotel_info[hotel]['center'], hotel_info[hotel]['price'],
                       round(float(hotel_info[hotel]['price']) * all_time_int, 2),
                       hotel_info[hotel]['id'])
            hist_add(message.from_user.id, message.message.chat.id, 'text' + string)
            bot.send_message(message.from_user.id, string)
            name_check = hotel_info[hotel]['name']
            if photo != 0:
                rapid_api.photo.photo_send(photo, message, hotel_info, hotel)
        except IndexError:
            bot.send_message(message.from_user.id, 'Название города не корректно!')
            return

