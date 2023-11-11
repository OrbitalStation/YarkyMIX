from properties import *
from telebot import TeleBot


def init():
    load_properties("assets")
    return TeleBot(const("token"))
