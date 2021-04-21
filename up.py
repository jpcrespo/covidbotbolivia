import telebot
from telebot import types

import datos
from datos import *



bot = telebot.TeleBot(token)


bot.send_message(us, '🤖 El bot se ha actualizado correctamente'+flag_date,disable_notification= True )
sys.exit(0)


