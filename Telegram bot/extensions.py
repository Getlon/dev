import requests
import json
from config import keys


class ConverterException(Exception):
    pass


class ApiException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(base: str, quote: str, amount: float):

        if base == quote:
            raise ConverterException(f'Невезможно перевести одинаковые валюты {base}.')

        try:
            keys[base]
        except KeyError:
            raise ConverterException(f'Не удалось обработать валюту {base}.')

        try:
            keys[quote]
        except KeyError:
            raise ConverterException(f'Не удалось обработать валюту {quote}.')

        try:
            float(amount)
        except ValueError:
            raise ConverterException(f'Количество валюты должно быть целым или вещественным числом {amount}.')

        r = requests.get(f'https://free.currconv.com/api/v7/convert?q={keys[base]}_{keys[quote]},%20PHP_EU&compact=ultra&apiKey=7bb03ab0640182318fe9')
        text = json.loads(r.content)
        return text[f'{keys[base]}_{keys[quote]}'] * float(amount)
