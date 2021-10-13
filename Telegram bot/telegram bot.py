import telebot
from config import TOKEN, currencies, keys
from extensions import Converter, ConverterException


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['help', 'start'])
def help(message: telebot.types.Message):
    bot.reply_to(message, '<имя валюты, цену которой вы хотите узнать> \
<имя валюты, в которой надо узнать цену первой валюты>\
<количество первой валюты>\n /values - показывает доступные валюты.')


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    bot.reply_to(message, 'Доступные валюты: {0}'.format(currencies))


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        if len(message.text.split(' ')) != 3:
            raise ConverterException('Неправильное количество аргументов.')

        base, quote, amount = message.text.split(' ')
        result = Converter.get_price(base, quote, amount)
        bot.send_message(message.chat.id, f'Цена {amount} {base} в {quote} - {result}')
    except ConverterException as e:
        bot.send_message(message.chat.id, str(e))
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')


bot.polling()
