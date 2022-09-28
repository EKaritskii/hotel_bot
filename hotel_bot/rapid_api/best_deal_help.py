from loader import bot
import rapid_api
from .history_com import hist_add


def print_teleg_best(message, hotel_info):
    with bot.retrieve_data(message.from_user.id, message.message.chat.id) as data:
        max_hotel = data["max_hotel"]
        photo = data['photo']
        highest = (data['highest'])
        lowest = (data['lowest'])
        checkin = data['check_in']
        checkout = data['check_out']
        all_1 = checkin - checkout
        all_time = str(all_1)
        time_list = all_time.split()
        all_time_int = int(time_list[0][1:])
    name_check = ''
    count_right = 0
    count = 0
    count_1 = 0
    while True:
        if count >= int(max_hotel):
            break
        try:

            hotel = count_1 + count_right
            if name_check == hotel_info[hotel]['name']:
                while name_check == hotel_info[hotel]['name']:
                    count_right += 1
                    hotel = count_1 + count_right
            if int(lowest) < int(hotel_info[hotel]['price']) < int(highest):
                count += 1
                string = "Отель номер {0}\nНазвание: {1}\nАдрес: {2}\n" \
                         "Расположен в {3} от центра\n" \
                         "Цена за комнату(в день): {4} долларов\n" \
                         "Цена за комнату(за все время): {5} долларов\n" \
                         "Ссылка: hotels.com/ho{6}". \
                    format(count, hotel_info[hotel]['name'],
                           hotel_info[hotel]['address'],
                           hotel_info[hotel]['center'],
                           hotel_info[hotel]['price'],
                           round(float(hotel_info[hotel]['price']) * all_time_int, 2),
                           hotel_info[hotel]['id'])
                hist_add(message.from_user.id, message.message.chat.id, 'text' + string)
                bot.send_message(message.from_user.id, string)
                name_check = hotel_info[hotel]['name']
                if photo != 0:
                    rapid_api.photo.photo_send(photo, message, hotel_info, hotel)
            count_1 += 1
        except IndexError:
            bot.reply_to(message, "Отелей удовлетворяющих диапазон цен больше нет/Название города введено не корректно")

