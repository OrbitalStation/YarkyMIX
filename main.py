import telebot
import sqlite3
from telebot import types

bot = telebot.TeleBot("6416571576:AAHVyBe42u5V2wphhMeYWlerGVS7_30MDro")

user = ""


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Зарегистрировать класс")
    markup.add(btn1)
    bot.reply_to(message,
                 "Привет, я яркий MIX средств для помощи в обучении. Если Ваш одноклассник уже зарегистрировал Ваш класс, то оправьте мне код, его можно узнать у того, кто регистрировал класс. Если Ваш класс ещё не зарегистрирован, то давайте это исправим!",
                 reply_markup=markup)


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "im gay")


@bot.message_handler(func=lambda message: True)
def send_text(message):
    if message.text.strip() == '👋 Зарегистрировать класс':
        daykb = types.InlineKeyboardMarkup(row_width=2)
        button1 = types.InlineKeyboardButton("понедельник", callback_data='monday')
        button2 = types.InlineKeyboardButton("вторник", callback_data='tuesday')
        button3 = types.InlineKeyboardButton("среда", callback_data='wednesday')
        button4 = types.InlineKeyboardButton("черверг", callback_data='thursday')
        button5 = types.InlineKeyboardButton("пятница", callback_data='friday')
        button6 = types.InlineKeyboardButton("суббота", callback_data='saturday')
        daykb.add(button1, button2, button3, button4, button5, button6)
        bot.send_message(message.chat.id, "выберете день недели", reply_markup=daykb)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "monday":
            monday(call)

        if call.data == "tuesday":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Пыщь")

        if call.data == "wednesday":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Пыщь")

        if call.data == "thursday'":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Пыщь")

        if call.data == "friday":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Пыщь")

        if call.data == "saturday":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Пыщь")

        if call.data == "phisics":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Пыщь")

def monday(call):
    lessonskb = types.InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton("физика", callback_data='physics')
    button2 = types.InlineKeyboardButton("математика", callback_data='math')
    button3 = types.InlineKeyboardButton("история", callback_data='history')
    button4 = types.InlineKeyboardButton("русский язык", callback_data='russian')
    lessonskb.add(button1, button2, button3, button4)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="расписание "
                                                                                                 "на "
                                                                                                 "понедельник",
                          reply_markup=lessonskb)

bot.infinity_polling()
