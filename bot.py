import telebot
import json
import time
from telebot import types
from config import token

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Показать квартиры")
    markup.add(item1)
    bot.send_message(message.chat.id,'Привет', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def show_data(message):
    with open('all_cards.json', 'r') as file:
        data = json.load(file)

    for index, item in enumerate(data):
        try:
            card = f"{item['Название']} \n" \
                   f"{item['Картинка']} \n" \
                   f"{item['Цена']}\n\n" \
                   f"{item['Адрес']} \n\n" \
                   f"{item['Описание']}\n" \
                   f"{item['Ссылка']}\n"
            bot.send_message(message.chat.id, card)
        except:
            time.sleep(1)
bot.polling()