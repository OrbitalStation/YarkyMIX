import telebot
import sqlite3
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from init import init
from database import db
from commands.class_register import class_register

if __name__ == '__main__':
    bot = init()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Зарегистрировать класс")
    markup.add(btn1)
    bot.reply_to(message,
                 "Привет, я яркий MIX средств для помощи в обучении. Если Ваш одноклассник уже зарегистрировал Ваш "
                 "класс, то оправьте мне код, его можно узнать у того, кто регистрировал класс. Если Ваш класс ещё не "
                 "зарегистрирован, то давайте это исправим!",
                 reply_markup=markup)


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "im gay")


@bot.message_handler(func=lambda message: True)
def send_text(message):
    if message.text.strip() == '👋 Зарегистрировать класс':
        class_register(bot, message)
    if message.text.strip() == 'Запись ДЗ':
        daykb = types.InlineKeyboardMarkup(row_width=2)
        button1 = types.InlineKeyboardButton("понедельник", callback_data='monday')
        button2 = types.InlineKeyboardButton("вторник", callback_data='tuesday')
        button3 = types.InlineKeyboardButton("среда", callback_data='wednesday')
        button4 = types.InlineKeyboardButton("черверг", callback_data='thursday')
        button5 = types.InlineKeyboardButton("пятница", callback_data='friday')
        button6 = types.InlineKeyboardButton("суббота", callback_data='saturday')
        daykb.add(button1, button2, button3, button4, button5, button6)
        bot.send_message(message.chat.id, "Выберите день недели", reply_markup=daykb)
    if message.text.strip() == 'Просмотр ДЗ':
        daykb = types.InlineKeyboardMarkup(row_width=2)
        button1 = types.InlineKeyboardButton("понедельник", callback_data='monday')
        button2 = types.InlineKeyboardButton("вторник", callback_data='tuesday')
        button3 = types.InlineKeyboardButton("среда", callback_data='wednesday')
        button4 = types.InlineKeyboardButton("черверг", callback_data='thursday')
        button5 = types.InlineKeyboardButton("пятница", callback_data='friday')
        button6 = types.InlineKeyboardButton("суббота", callback_data='saturday')
        daykb.add(button1, button2, button3, button4, button5, button6)
        bot.send_message(message.chat.id, "Выберите день недели", reply_markup=daykb)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global day
    req = call.data.split('_')
    if req[0] == "monday":
        day = "monday"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text=f"физика", callback_data='physics'),
                   InlineKeyboardButton(text=f"математика", callback_data=f'math'))
        markup.add(InlineKeyboardButton(text=f"история", callback_data='history'),
                   InlineKeyboardButton(text=f"русский язык", callback_data='russian'))
        markup.add(InlineKeyboardButton(text=f"назад", callback_data=f"week"))
        bot.edit_message_text(f'расписание на понедельник', reply_markup=markup, chat_id=call.message.chat.id,
                              message_id=call.message.message_id)
    if req[0] == "physics":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text=f"назад", callback_data=day))
        bot.edit_message_text(f'п19 и номера 123,124', reply_markup=markup, chat_id=call.message.chat.id,
                              message_id=call.message.message_id)
    if req[0] == "week":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text=f"понедельник", callback_data='monday'),
                   InlineKeyboardButton(text=f"вторник", callback_data='tuesday'))
        markup.add(InlineKeyboardButton(text=f"среда", callback_data='wednesday'),
                   InlineKeyboardButton(text=f"черверг", callback_data='thursday'))
        markup.add(InlineKeyboardButton(text=f"пятница", callback_data='friday'),
                   InlineKeyboardButton(text=f"суббота", callback_data='saturday'))
        bot.edit_message_text(f'Выберите день недели', reply_markup=markup, chat_id=call.message.chat.id,
                              message_id=call.message.message_id)
    if req[0] == "nolessonsSaturday":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Просмотр ДЗ")
        btn2 = types.KeyboardButton("Запись ДЗ")
        markup.add(btn1, btn2)
        bot.send_message(call.message.chat.id, "Поздравляю! Вы заполнили расписание. Теперь можно записывать и "
                                               "просматривать дз", reply_markup=markup)

        '''
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
'''


bot.polling(none_stop=True)
