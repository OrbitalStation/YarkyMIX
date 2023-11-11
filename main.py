import telebot
import sqlite3
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from init import init
from database import db
from commands.class_register import class_register

if __name__ == '__main__':
    bot = init()

lessons = list()
lessonsid = list()
day = ""


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
        print(message.chat.id)
        daykb = types.InlineKeyboardMarkup(row_width=2)
        button1 = types.InlineKeyboardButton("понедельник", callback_data='mondayentry')
        button2 = types.InlineKeyboardButton("вторник", callback_data='tuesdayentry')
        button3 = types.InlineKeyboardButton("среда", callback_data='wednesdayentry')
        button4 = types.InlineKeyboardButton("черверг", callback_data='thursdayentry')
        button5 = types.InlineKeyboardButton("пятница", callback_data='fridayentry')
        button6 = types.InlineKeyboardButton("суббота", callback_data='saturdayentry')
        button7 = types.InlineKeyboardButton("суббота", callback_data='sundayentry')
        daykb.add(button1, button2, button3, button4, button5, button6, button7)
        bot.send_message(message.chat.id, "Выберите день недели", reply_markup=daykb)
    if message.text.strip() == 'Просмотр ДЗ':
        daykb = types.InlineKeyboardMarkup(row_width=2)
        button1 = types.InlineKeyboardButton("понедельник", callback_data='mondayread')
        button2 = types.InlineKeyboardButton("вторник", callback_data='tuesdayread')
        button3 = types.InlineKeyboardButton("среда", callback_data='wednesdayread')
        button4 = types.InlineKeyboardButton("черверг", callback_data='thursdayread')
        button5 = types.InlineKeyboardButton("пятница", callback_data='fridayread')
        button6 = types.InlineKeyboardButton("суббота", callback_data='saturdayread')
        button7 = types.InlineKeyboardButton("воскресенье", callback_data='sundayread')
        daykb.add(button1, button2, button3, button4, button5, button6, button7)
        bot.send_message(message.chat.id, "Выберите день недели", reply_markup=daykb)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # global lessons, lessonsid, day
    req = call.data.split('_')
    if req[0] == "adress_":
        print(1)
        # user = db.fetch_user(call.message.from_user.id)
        # print(getattr(user.get_hw_db().fetch_user(1), f"wd{day}"))
    if req[0] == "weekentry":
        daykb = types.InlineKeyboardMarkup(row_width=2)
        button1 = types.InlineKeyboardButton("понедельник", callback_data='mondayentry')
        button2 = types.InlineKeyboardButton("вторник", callback_data='tuesdayentry')
        button3 = types.InlineKeyboardButton("среда", callback_data='wednesdayentry')
        button4 = types.InlineKeyboardButton("черверг", callback_data='thursdayentry')
        button5 = types.InlineKeyboardButton("пятница", callback_data='fridayentry')
        button6 = types.InlineKeyboardButton("суббота", callback_data='saturdayentry')
        button7 = types.InlineKeyboardButton("воскресенье", callback_data='sundayentry')
        daykb.add(button1, button2, button3, button4, button5, button6, button7)
        bot.edit_message_text(f"Выберите день недели", reply_markup=daykb, chat_id=call.message.chat.id,
                              message_id=call.message.message_id)
    if req[0] == "mondayentry":
        day = "1"
        lessonsid = db.fetch_user(call.message.chat.id).subjects.decode()
        lessons = db.fetch_user(call.message.chat.id).general_schedule.wd1.lessons.decode()
        user = db.fetch_user(call.message.chat.id)
        print(lessonsid)
        print(lessons)
        print(user)
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        for i in range(0, len(lessons)):
            markup.add(InlineKeyboardButton(lessonsid[int(lessons[i].idx)].name, callback_data=f"adress_"))
        markup.add(InlineKeyboardButton(text=f"назад", callback_data=f"weekentry"))
        bot.edit_message_text(f'расписание на понедельник', reply_markup=markup, chat_id=call.message.chat.id,
                              message_id=call.message.message_id)
    if req[0] == "tuesdayentry":
        day = "2"
        lessonsid = db.fetch_user(call.message.chat.id).subjects.decode()
        lessons = db.fetch_user(call.message.chat.id).general_schedule.wd2.lessons.decode()
        user = db.fetch_user(call.message.chat.id)
        print(lessonsid)
        print(lessons)
        print(user)
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        for i in range(0, len(lessons)):
            markup.add(InlineKeyboardButton(lessonsid[int(lessons[i].idx)].name, callback_data=f"adress_{lessons[i]}"))
        markup.add(InlineKeyboardButton(text=f"назад", callback_data=f"weekentry"))
        bot.edit_message_text(f'расписание на вторник', reply_markup=markup, chat_id=call.message.chat.id,
                              message_id=call.message.message_id)
    if req[0] == "wednesdayentry":
        day = "3"
        lessonsid = db.fetch_user(call.message.chat.id).subjects.decode()
        lessons = db.fetch_user(call.message.chat.id).general_schedule.wd3.lessons.decode()
        user = db.fetch_user(call.message.chat.id)
        print(lessonsid)
        print(lessons)
        print(user)
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        for i in range(0, len(lessons)):
            markup.add(InlineKeyboardButton(lessonsid[int(lessons[i].idx)].name, callback_data=f"adress_{lessons[i]}"))
        markup.add(InlineKeyboardButton(text=f"назад", callback_data=f"weekentry"))
        bot.edit_message_text(f'расписание на среду', reply_markup=markup, chat_id=call.message.chat.id,
                              message_id=call.message.message_id)
    if req[0] == "thursdayentry":
        day = "4"
        lessonsid = db.fetch_user(call.message.chat.id).subjects.decode()
        lessons = db.fetch_user(call.message.chat.id).general_schedule.wd4.lessons.decode()
        user = db.fetch_user(call.message.chat.id)
        print(lessonsid)
        print(lessons)
        print(user)
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        for i in range(0, len(lessons)):
            markup.add(InlineKeyboardButton(lessonsid[int(lessons[i].idx)].name, callback_data=f"adress_{lessons[i]}"))
        markup.add(InlineKeyboardButton(text=f"назад", callback_data=f"weekentry"))
        bot.edit_message_text(f'расписание на четверг', reply_markup=markup, chat_id=call.message.chat.id,
                              message_id=call.message.message_id)
    if req[0] == "fridayentry":
        day = "5"
        lessonsid = db.fetch_user(call.message.chat.id).subjects.decode()
        lessons = db.fetch_user(call.message.chat.id).general_schedule.wd5.lessons.decode()
        user = db.fetch_user(call.message.chat.id)
        print(lessonsid)
        print(lessons)
        print(user)
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        for i in range(0, len(lessons)):
            markup.add(InlineKeyboardButton(lessonsid[int(lessons[i].idx)].name, callback_data=f"adress_{lessons[i]}"))
        markup.add(InlineKeyboardButton(text=f"назад", callback_data=f"weekentry"))
        bot.edit_message_text(f'расписание на пятница', reply_markup=markup, chat_id=call.message.chat.id,
                              message_id=call.message.message_id)
    if req[0] == "saturdayentry":
        day = "6"
        lessonsid = db.fetch_user(call.message.chat.id).subjects.decode()
        lessons = db.fetch_user(call.message.chat.id).general_schedule.wd6.lessons.decode()
        user = db.fetch_user(call.message.chat.id)
        print(lessonsid)
        print(lessons)
        print(user)
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        for i in range(0, len(lessons)):
            markup.add(InlineKeyboardButton(lessonsid[int(lessons[i].idx)].name, callback_data=f"adress_{lessons[i]}"))
        markup.add(InlineKeyboardButton(text=f"назад", callback_data=f"weekentry"))
        bot.edit_message_text(f'расписание на суббота', reply_markup=markup, chat_id=call.message.chat.id,
                              message_id=call.message.message_id)
    if req[0] == "sundayentry":
        day = "7"
        lessonsid = db.fetch_user(call.message.chat.id).subjects.decode()
        lessons = db.fetch_user(call.message.chat.id).general_schedule.wd7.lessons.decode()
        user = db.fetch_user(call.message.chat.id)
        print(lessonsid)
        print(lessons)
        print(user)
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        for i in range(0, len(lessons)):
            markup.add(InlineKeyboardButton(lessonsid[int(lessons[i].idx)].name, callback_data=f"adress_{lessons[i]}"))
        markup.add(InlineKeyboardButton(text=f"назад", callback_data=f"weekentry"))
        bot.edit_message_text(f'расписание на воскресенье', reply_markup=markup, chat_id=call.message.chat.id,
                              message_id=call.message.message_id)


bot.polling(none_stop=True)
