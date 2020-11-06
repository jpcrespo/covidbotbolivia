# ==================================
# =           KungFluBot           =
# ==================================

#Librerias

import telebot
from telebot import types
import time, os

#token del fatherbot
TOKEN = "1183310581:AAGVvRfB8QAYz7raCdMZtBX97JFYCevS6k4"  # SUSTITUIR

userStep = {}
knownUsers = []
			
commands = {
			'start' 		: 	'Inicia el bot',
			'ayuda'			: 	'Comandos disponible',
			'Mandar Logs'	:	'Mandar los Reportes'
			}



