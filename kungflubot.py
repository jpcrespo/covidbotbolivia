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
			'Iniciar' 		: 	'Inicia el bot',
			'ayuda'			: 	'Comandos disponible',
			'Mandar Logs'	:	'Mandar los Reportes (Only Admin)'
			}

menu = types.ReplyKeyboardMarkup()
menu.add('Info Covid','Info Ayuda','UVCKill')

info_menu = types.ReplyKeyboardMarkup()
info_menu.add('Bolivia','Desagregados','Atras')

ayuda_menu = types.ReplyKeyboardMarkup()
ayuda_menu.add('ProfesionalesDisponibles','Contacto')

uvc_menu = types.ReplyKeyboardMarkup()
uvc_menu.add('Informacion','Solicitar contacto')




# COLOR TEXTO
class color:
    RED = '\033[91m'
    BLUE = '\033[94m'
    GREEN = '\033[32m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
        print(color.GREEN + "USUARIO ya registrado" + color.ENDC)
    else:
        knownUsers.append(uid)
        userStep[uid] = 0
        print(color.RED + "USUARIO nuevo, registrado" + color.ENDC)


#funcion que registra los actos solo en consola servidor
#puede ser un log sobre las respuestas tambien

def listener(messages):
    for m in messages:
        if m.content_type == 'text':
            print("[" + str(m.chat.id) + "] " + str(m.chat.first_name) + " : " + m.text + " - " + str(time.strftime("%c")) )






bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)


# START
@bot.message_handler(commands=['Iniciar'])
def command_start(m):
    cid = m.chat.id
    userStep[cid] = 0
    bot.send_message(cid, "Hola estimado " + str(m.chat.username) + "...")
    time.sleep(1)
    bot.send_message(cid, "tu registro esta completo!")
    time.sleep(1)
    bot.send_message(cid, "Podemos iniciar!\n", reply_markup=menu)


# AYUDA
@bot.message_handler(commands=['ayuda'])
def command_help(m):
    cid = m.chat.id
    help_text = "Hola, este bot esta mostrara los datos covid19 en Bolivia\n"
    help_text += "Comandos disponibles: \n"
    for key in commands:
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text,reply_markup=menu)

# EXEC COMANDO
@bot.message_handler(commands=['Mandar Logs'])
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
    if text == "Info Covid":  # RPINFO
        bot.send_message(cid, "Se muestra informacion Covid19 del reporte oficial", reply_markup=info_menu)
        userStep[cid] = 1
    elif text == "Info Ayuda":  # CAMARA
        bot.send_message(cid, "Se muestra informacion de Respuesta ciudadana, sobre profesionales disponibles", reply_markup=ayuda_menu)
        userStep[cid] = 2
    
    elif text == 'UVCKill':     
    	bot.send_message(cid,'Se brinda asesoria sobre el metodo de esterilizacion con Luz Ultravioleta',reply=uvc_menu)
    	userStep[cid] = 3

    elif text == "Atras":  # ATRAS
        userStep[cid] = 0
        bot.send_message(cid, "Menu Principal:", reply_markup=menu)
    else:
        command_text(m)



# MENU INFO COVID
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 1)
def info_opt(m):
        cid = m.chat.id
        txt = m.text
        if txt == "Bolivia":  # TEMP
            bot.send_message(cid, "La grafica esta actualizada hasta "+str(time.ctime(os.path.getmtime('bolivia.png'))))
            bot.send_chat_action(cid, 'upload_photo')
	    	userStep[cid] = 1
            bot.send_photo(cid, open("bolivia.png", 'rb'))
	    	bot.send_message(cid,'La gráfica es actualizada dia a dia')
            print(color.GREEN + "bolivia enviada" + color.ENDC)

        elif txt == 'Desagregados' 
        	bot.send_message(cid, "Se muestra la evolución temporal")
        	bot.send_message(cid, "La grafica esta actualizada hasta "+str(time.ctime(os.path.getmtime('desagregado.png'))))
            bot.send_chat_action(cid, 'upload_photo')
	    	userStep[cid] = 1
            bot.send_photo(cid, open("desagregado.png", 'rb'))
	    	bot.send_message(cid,'La gráfica es actualizada dia a dia')
            print(color.GREEN + "desagregada enviada" + color.ENDC)


        elif txt == "Atras":  # HD
            userStep[cid] = 0
            bot.send_message(cid, "Menu Principal:", reply_markup=menu)
        else:
            command_text(m)




@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 2)
def cam_opt(m):
        cid = m.chat.id
        text = m.text
        if text == "ProfesionalesDisponibles":  # FOTO
                
            bot.send_message(cid, "En el siguiente enlace obtendra informacion\n")
            bot.send_message(cid, "https://bolivia.respuestaciudadana.org/hermanos-1.html#!")
            print(color.BLUE + " Enlace ubicacion" + color.ENDC)
            userStep[cid]=0
        else text == 'Contacto'
        	bot.send_message(cid, "Puede comunicarse con los siguientes numeros ante cualquier duda\n")
            userStep[cid]=0
            bot.send_message(cid, 800 10 11 04)
            bot.send_message(cid, 800 10 11 06,reply_markup=main_menu)


@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 3)

def uvc_kill(m):
	cid = m.chat.id
	txt = m.text
	if text == 'Informacion'
		bot.send_message(cid, "La luz UVC, es muy eficaz para la esterilizacion de superficies\n")
        bot.send_chat_action(cid,'upload_video')
        bot.send_video(cid, open('coviduvc.mp4'),'rb')
        lol = 'Encontrara informacion mas detallada en el siguiente link'
        lol += 'https://n9.cl/yoxa'
        lol += 'https://n9.cl/8a38' 
        bot.send_message(cid,lol)
        userStep[cid]=0
	else text == 'Solicitar contacto'
		bot.send_message(cid, "Obtenga asesoramiento experto")
		bot.send_message(cid, "https://t.me/radiontech",reply_markup=main_menu)



# FILTRAR MENSAJES
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_text(m):
    cid = m.chat.id
    if (m.text.lower() in ['hola', 'hi', 'buenas', 'buenos dias']):
        bot.send_message(cid, 'Muy buenas, ' + str(m.from_user.first_name) + '. Me alegra verte de nuevo.', parse_mode="Markdown")
    elif (m.text.lower() in ['adios', 'aios', 'adeu', 'ciao']):
        bot.send_message(cid, 'Hasta luego, ' + str(m.from_user.first_name) + '. Te echaré de menos.', parse_mode="Markdown")


print 'Corriendo...'
bot.polling(none_stop=True)

