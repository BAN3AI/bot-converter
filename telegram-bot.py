import telebot
from telebot import types
import json
import requests
import bs4

response = requests.get('https://bankiros.ru/currency/cbrf')
# print(type(response))
# print(response.status_code)
# print(response.text)
# print(response.content)
page = bs4.BeautifulSoup(response.content, 'html5lib')
USD = page.find('span', 'cursor-pointer')
# print(USD)
# print(USD.name)
print(USD.text)
EUR = page.find('span', 'cursor-pointer')
# print(EUR)
# print(EUR.name)
print(EUR.text)
bot = telebot.TeleBot('<your_token_here>')


@bot.message_handler(content_types=['text'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('€')
    markup.row('$')
    msg = bot.send_message(message.chat.id, 'Выберите валюту', reply_markup=markup)
    bot.register_next_step_handler(msg, currency)


def currency(message):
    if message.text == '€':
        msg = bot.send_message(message.chat.id, 'Введите сумму в рублях')
        bot.register_next_step_handler(msg, eur)
    elif message.text == '$':
        msg = bot.send_message(message.chat.id, 'Введите сумму в рублях')
        bot.register_next_step_handler(msg, usd)
    else:
        msg = bot.send_message(message.chat.id, 'Введите корректные данные')
        bot.register_next_step_handler(msg, currency)


def eur(message):
    try:
        bot.send_message(message.chat.id, float(message.text) / EUR)
    except ValueError:
        bot.send_message(message.chat.id, 'Введите число')


def usd(message):
    try:
        bot.send_message(message.chat.id, float(message.text) / USD)
    except ValueError:
        bot.send_message(message.chat.id, 'Введите число')


bot.polling(none_stop=True)