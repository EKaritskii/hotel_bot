import datetime
from loader import bot


def hist_add(us_id, chat_id, message_add):
    name = str(us_id) + str(chat_id)
    with open(name, 'a', encoding='utf-8') as file:
        if message_add.startswith('/'):
            string = str(message_add) + ' ' + str(datetime.datetime.today())[:19] + '\n'
        elif message_add.startswith('text'):
            string = str(message_add)[4:] + '\n'
        else:
            string = 'pic' + str(message_add) + '\n'
        file.write(string)


def hist_write(us_id, chat_id):
    name = str(us_id) + str(chat_id)
    with open(name, 'r', encoding='utf-8') as file:
        string_help = ''
        for string in file:
            print(string)
            if string.startswith('pic'):
                if string_help != '':
                    bot.send_message(us_id, string_help)
                    string_help = ''
                p_url = string[3:]
                bot.send_photo(
                    chat_id, p_url.format(size='z')
                )
            elif string.startswith('/'):
                if string_help != '':
                    bot.send_message(us_id, string_help)
                    string_help = ''
                bot.send_message(us_id, string)
            else:
                string_help = string_help + string
