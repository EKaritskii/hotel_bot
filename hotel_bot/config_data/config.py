import os

from dotenv import find_dotenv, load_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('token')
RAPID_API_KEY = os.getenv('api_key')
DEFAULT_COMMANDS = (
    ('start', "Запустить бота"),
    ('help', "Вывести справку"),
    ('hello_world', "Привет мир"),
    ('lowprice', "Отель с сортировкой по цене (возрастание)"),
    ('highprice', "Отель с сортировкой по цене (убывание)"),
    ('bestdeal', "Отель с сортировкой по диапазону цен (возрастание)"),
    ('history', "История запросов")
)
