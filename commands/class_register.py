from database import db
from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def class_register(bot, message):
    reply = bot.send_message(message.chat.id, 'Привет! Чтобы у меня была возможность помогать тебе, мне надо '
                                              'узнать твоё расписание. Напиши мне своё расписание на понедельник. '
                                              'Пример:\nМатематика\nРусский\nФизра\nОБЖ\nАнглийский')
    bot.register_next_step_handler(reply, weekday(bot, [
        '',
        'воскресение',
        'субботу',
        'пятницу',
        'четверг',
        'среду',
        'вторник'
    ], []))


def weekday(bot, remains: list[str], subs):
    if len(remains) != 0:
        day = remains.pop()

    def inner(message):
        subs.extend(message.text.strip().split("\n"))
        reply = bot.send_message(message.chat.id, f'На {day}')
        bot.register_next_step_handler(reply, weekday(bot, remains, subs))

    if len(remains) == 0:
        return lambda m: finish_weekdays(bot, m, subs)
    return inner


def finish_weekdays(bot, message, subs):
    subs.extend(message.text.strip().split("\n"))
    print(subs)
    subs = list(set(subs))
    userssub = ";".join(subs)
    db.update_user(message.from_user.id, subjects_str_repr=userssub)
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("Просмотр ДЗ")
    btn2 = KeyboardButton("Запись ДЗ")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Поздравляю! Вы заполнили расписание. Теперь можно записывать и "
                                      "просматривать дз", reply_markup=markup)
