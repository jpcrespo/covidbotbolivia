import telebot, json
from telebot import types

import time, os, sys

sys.path.insert(0, 'core/')
import datos
from datos import *


aux         = np.load('bins/knownUsers.npy', allow_pickle='TRUE') 
knownUsers  = aux.tolist()


bot = telebot.TeleBot(token)




if __name__ == '__main__':
   for us in knownUsers:
   	bot.send_message(us, '🤖 El bot entra en mantenimiento, se actualizan los datos y se crean nuevas instancias.\nVuelvo en 5 min 🏃‍♂',disable_notification= True )
   sys.exit(0)


