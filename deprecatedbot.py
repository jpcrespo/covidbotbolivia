#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telebot
from telebot import types
import time
import os

TOKEN = "1183310581:AAGVvRfB8QAYz7raCdMZtBX97JFYCevS6k4"  # SUSTITUIR

userStep = {}
knownUsers = []

commands = {
              'start': 'Arranca el bot',
              'ayuda': 'Comandos disponibles',
              'exec': 'Ejecuta un comando'
}

menu = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True,row_width=1)
menu.add("infoydata", "TEST")

test_menu = types.ReplyKeyboardMarkup()
test_menu.add("Iniciar", "Atras")

enf_menu = types.ReplyKeyboardMarkup()
enf_menu.add("SI", "NO")




# COLOR TEXTO
class color:
    RED = '\033[91m'
    BLUE = '\033[94m'
    GREEN = '\033[32m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# USER STEP
def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        knownUsers.append(uid)
        userStep[uid] = 0
	txt='[!]nuevo user '
        print(color.RED + txt+color.ENDC)


# LISTENER
def listener(messages):
    for m in messages:
        if m.content_type == 'text':
            print("[" + str(m.chat.id) + "] " + str(m.chat.first_name) + ": " + m.text + " mmmm")

bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)


# START
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    userStep[cid] = 0
    bot.send_message(cid, "Saludos usuario " + str(m.chat.first_name) + "...")
    time.sleep(1)
    bot.send_message(cid, "tu registro esta completo!")
    time.sleep(1)
    bot.send_message(cid, "Podemos iniciar!\n", reply_markup=menu)


# AYUDA
@bot.message_handler(commands=['ayuda'])
def command_help(m):
    cid = m.chat.id
    help_text = "Grabar sesion: TermRecord -o /tmp/botlog.html\n"
    help_text += "Comandos disponibles: \n"
    for key in commands:
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)


# EXEC COMANDO
@bot.message_handler(commands=['exec'])
def command_exec(m):
    cid = m.chat.id
    if cid == 89650251:  # SUSTITUIR
        bot.send_message(cid, "Ejecutando: " + m.text[len("/exec"):])
        bot.send_chat_action(cid, 'typing')
        time.sleep(2)
        f = os.popen(m.text[len("/exec"):])
        result = f.read()
        bot.send_message(cid, "Resultado: " + result)
    else:
        bot.send_message(cid, "PERMISO DENEGADO, solo Juan 'The Creator' puede acceder")
        print(color.RED + " ¡PERMISO DENEGADO! " + color.ENDC)


# MENU PRINCIPAL
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 0)
def main_menu(m):
    cid = m.chat.id
    text = m.text
    if text == "infoydata":  # RPINFO
        bot.send_message(cid, "Se genera una grafica de infectados en Bolivia:", reply_markup=test_menu)
        userStep[cid] = 1
    elif text == "TEST":  # CAMARA
        bot.send_message(cid, "Se le realizará un breve test si sospecha covid19", reply_markup=test_menu)
        userStep[cid] = 2
    elif text == "Atras":  # ATRAS
        userStep[cid] = 0
        bot.send_message(cid, "Menu Principal:", reply_markup=menu)


    else:
        command_text(m)


# MENU INFO
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 1)
def info_opt(m):
    cid = m.chat.id
    txt = m.text
    if txt == "Iniciar":  # TEMP
        bot.send_message(cid, "Generando grafica")
        print(color.BLUE + "gnu plot covidbol" + color.ENDC)
        bot.send_chat_action(cid, 'upload_photo')
        userStep[cid] = 0
        bot.send_photo(cid, open("bolivia.png", 'rb'))
        bot.send_message(cid,'La gráfica es actualizada día a día',reply_markup=menu)
        print(color.GREEN + "covidbol enviada" + color.ENDC)

    elif txt == "Atras":  # HD
        userStep[cid] = 0
        bot.send_message(cid, "Menu Principal:", reply_markup=menu)
    else:
        command_text(m)


# MENU CAMARA
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 2)
def cam_opt(m):
        cid = m.chat.id
        text = m.text
        if text == "Iniciar":  # FOTO

            bot.send_message(cid, "Ha tenido fiebre a mas de 37,5 C??")
            bot.send_chat_action(cid,'record_audio')
            bot.send_audio(cid, open("test.m4a",'rb'), 1, 'eternnoir','Juan The Creator', reply_markup=enf_menu)
            print(color.BLUE + " Enviado audio" + color.ENDC)
            userStep[cid] = 3


        elif text == "Atras":  # ATRAS
            userStep[cid] = 0
            bot.send_message(cid, "Menu Principal:", reply_markup=menu)
        else:
                command_text(m)



@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 3)
def cam_opt(m):
        cid = m.chat.id
        text = m.text
        if text == "SI":  # FOTO

            bot.send_message(cid, "Es probable que tenga covid19\n")
            bot.send_message(cid, "Se le manda la ubicación de un experto")
            bot.send_chat_action(cid, 'find_location')

            bot.send_location(cid,-16.490305,-68.146531) 
            bot.send_message(cid, "Se añade usuario al log para seguimiento", reply_markup=menu)

            print(color.BLUE + " Enviado ubicacion" + color.ENDC)
            userStep[cid]=0


        elif text == "NO":  # ATRAS
            bot.send_message(cid, "Es dificil que tengas covid, vende humo\n")
            bot.send_chat_action(cid,'upload_video')
            bot.send_video(cid,open('coviduvc.mp4','rb'))
            userStep[cid] = 0
            bot.send_message(cid, "Menu Principal:", reply_markup=menu)
        else:
                command_text(m)





# FILTRAR MENSAJES
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_text(m):
    cid = m.chat.id
    if (m.text.lower() in ['hola', 'hi', 'buenas', 'buenos dias']):
        bot.send_message(cid, 'Muy buenas, ' + str(m.from_user.first_name) + '. Me alegra verte de nuevo.', parse_mode="Markdown")
    elif (m.text.lower() in ['adios', 'aios', 'adeu', 'ciao']):
        bot.send_message(cid, 'Hasta luego, ' + str(m.from_user.first_name) + '. Te echaré de menos.', parse_mode="Markdown")


print('Corriendo...')
bot.polling(none_stop=True)

