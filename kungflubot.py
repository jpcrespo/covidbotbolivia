# ==================================
# =           KungFluBot           =
# ==================================


"""

   Este bot esta pensado para desplegar 
   información de Respuesta Ciudadana respecto 
   al covid. 
   Despliega los datos a solicitud, y tambien
   cuando se actualiza la información.

   Tiene una forma de registro para seguimiento
   de casos, donde periodicamente se mandan consejos 
   e informacion

"""


#Librerias
import telebot
from telebot import types
import time, os
from PIL import Image


#token del fatherbot
TOKEN = "1183310581:AAGVvRfB8QAYz7raCdMZtBX97JFYCevS6k4"  # SUSTITUIR
#Este token debe ser privado!!

userStep = {}                           
#Se almacena como clave : valor, el recorrido del usuario en el bot

knownUsers = []                         
#Registro de usuarios conocidos. Queda realizar una funcion que guarde
#el registro en disco y los vuelva a leer cada vez que el bot inicie


commands = {		'start' 		: 	'Inicia el bot',
                    'ayuda'			: 	'Comandos disponible',
                    'Mandar Logs'	:	'Mandar los Reportes (Only Admin)'
}

#Comandos que el bot contiene para operar. chequear entre las opciones
#que contiene el fatherbot para desplegar los comandos 



# =======================================
# =           El Menu del bot           =
# = El esqueleto de conformación y una  =
# = clase para imprimir colores en la   = 
# = terminal.                           =
# =======================================


menu = types.ReplyKeyboardMarkup(row_width=1,resize_keyboard=True,one_time_keyboard=True)
menu.add('☣️🇧🇴☣️ Info Covid','🔬 Info Ayuda de profesionales','☢️ Esterilización con Tecnología UV ☢️')

info_menu = types.ReplyKeyboardMarkup(row_width=1,resize_keyboard=True)
info_menu.add('La gráfica de Bolivia 🇧🇴','Datos Desagregados en el tiempo 📝 ','Atras')

ayuda_menu = types.ReplyKeyboardMarkup(row_width=1,resize_keyboard=True)
ayuda_menu.add('Profesionales Disponibles','Contacto','Atras')

uvc_menu = types.ReplyKeyboardMarkup(row_width=1,resize_keyboard=True)
uvc_menu.add('Video Informativo', 'Publicaciones de Bolivia','Solicitar contacto y asesoria','Atras')



# COLOR TEXTO
class color:
    RED = '\033[91m'
    BLUE = '\033[94m'
    GREEN = '\033[32m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# ======  End of El Menu del bot  =======


#La función get_user_step, se usa para registrar a un nuevo cliente
#y si este existe en el registro, obtener donde se encuentra en el bot

def get_user_step(uid):
       if uid in userStep:      #Busca si existe la llave uid 
           return userStep[uid] #y retorna el valor almacenado de ubicacion 
           print(color.GREEN + "USUARIO ya registrado" + color.ENDC)  
       else:
           knownUsers.append(uid)   #En caso de no existir el uid registrado 
           userStep[uid] = 0        #se lo almacena y se inicia su ubicacion en cero
           print(color.RED + "USUARIO nuevo, registrado" + color.ENDC)
         



#La funcion que registra los actos solo en consola servidor
#puede ser un log sobre las respuestas tambien

def listener(messages):
    for m in messages:
        if m.content_type == 'text':
            print("["+str(m.chat.id)+"]"+str(m.chat.first_name)+": " + m.text + "-" + str(time.strftime("%c")) )



#Inicializamos el bot

#creamos el objeto Telegram Bot
bot = telebot.TeleBot(TOKEN)
#asignamos nuestra funcion listener al bot
bot.set_update_listener(listener)



# =======================================
# = Flujo de trabajo y comandos del Bot =
# =======================================


# START
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    if cid in knownUsers:
        userStep[cid] = 0
        bot.send_message(cid, "Hola "+str(m.chat.username)+" que bueno verte nuevamente, iniciemos!",reply_markup=menu)
    else:
        bot.send_message(cid, "Hola "+str(m.chat.username)+', te doy la Bienvenida!')
        bot.send_message(cid, "Soy un bot creado para informar sobre el Covid19 y Bolivia")
        bot.send_message(cid, "dame un momento, que quiero registrarte...")
        get_user_step(cid);
        bot.send_message(cid, "Listo! Iniciemos!\n", reply_markup=menu)

        

# AYUDA
@bot.message_handler(commands=['ayuda'])
def command_help(m):
    cid = m.chat.id
    help_text = "Hola, este bot muestra los datos covid19 en Bolivia\n"
    help_text += "Tambien despliega información de utilidad \n"
    help_text += "Comandos disponibles: \n"
    for key in commands:
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
        bot.send_message(cid, help_text,reply_markup=menu)



# EXEC COMANDO
@bot.message_handler(commands=['Mandar Logs'])
def command_exec(m):
    cid = m.chat.id
    if cid == 89650251:  # cid del admin!
        bot.send_message(cid, "Ejecutan en consola: " + m.text[len("/exec"):])
        bot.send_chat_action(cid, 'typing')
        time.sleep(2)
        f = os.popen(m.text[len("/exec"):])
        result = f.read()
        bot.send_message(cid, "Resultado: " + result)
    else:
        bot.send_message(cid, "PERMISO DENEGADO, solo Juan The Creator puede acceder")
        print(color.RED + " ¡PERMISO DENEGADO! " + color.ENDC)



# =========================================================================
# =           Sección de despligue de menus internos y acciones           =
# =========================================================================


# MENU PRINCIPAL
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 0)
def main_menu(m):
    cid = m.chat.id
    text = m.text
    if text == "☣️🇧🇴☣️ Info Covid":
        bot.send_message(cid, "Se muestra informacion Covid19 del reporte oficial", reply_markup=info_menu)
        userStep[cid] = 1
    elif text == "🔬 Info Ayuda de profesionales":  # CAMARA
        bot.send_message(cid, "Se muestra informacion de Respuesta ciudadana, sobre profesionales disponibles", reply_markup=ayuda_menu)
        userStep[cid] = 2

    elif text == '☢️ Esterilización con Tecnología UV ☢️':
        bot.send_message(cid,'Se brinda asesoria sobre el metodo de esterilizacion con Luz Ultravioleta',reply_markup=uvc_menu)
        userStep[cid] = 3

    else:
        command_text(m)



# MENU INFO COVID
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 1)
def info_opt(m):
    cid = m.chat.id
    txt = m.text
    if txt == "La gráfica de Bolivia 🇧🇴":  
        bot.send_message(cid, "La grafica esta actualizada hasta "+str(time.ctime(os.path.getmtime('bolivia.png'))))
        bot.send_chat_action(cid, 'upload_photo')
        bot.send_photo(cid, open("bolivia.png", 'rb'))
        bot.send_message(cid,'La grafica es actualizada dia a dia',reply_markup=info_menu)
        print(color.GREEN + "bolivia enviada" + color.ENDC)

    elif txt == 'Datos Desagregados en el tiempo 📝':
        bot.send_message(cid, "Se muestra la curva de evolución 2020")
        bot.send_message(cid, "La grafica esta actualizada hasta "+str(time.ctime(os.path.getmtime('desagregado.png'))))
        bot.send_chat_action(cid, 'upload_photo')
        bot.send_photo(cid, open("desagregado.png", 'rb'))
        bot.send_message(cid,'La grafica es actualizada dia a dia',reply_markup=info_menu)
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
    if text == "Profesionales Disponibles":  # FOTO
        bot.send_message(cid, "En el siguiente enlace obtendra informacion\n")
        bot.send_message(cid, "https://bolivia.respuestaciudadana.org/hermanos-1.html#!",reply_markup=ayuda_menu)
        print(color.BLUE + " Enlace ubicacion" + color.ENDC)
        
    elif text == "Contacto":
        bot.send_message(cid, "Puede comunicarse con los siguientes numeros OFICIALES ante cualquier duda\n")
        bot.send_message(cid,'800 10 11 04')
        bot.send_message(cid,'800 10 11 06',reply_markup=ayuda_menu)
    
    elif text == "Atras":  # HD
        userStep[cid] = 0
        bot.send_message(cid, "Menu Principal:", reply_markup=menu)
    else:
        command_text(m)


@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 3)
def uvc_kill(m):
    cid = m.chat.id
    text = m.text
    if text == 'Video Informativo':
        bot.send_message(cid, "La luz UVC, es muy eficaz para la esterilizacion de superficies\n")
        bot.send_chat_action(cid,'upload_video')
        bot.send_video(cid, open('coviduvc.mp4','rb'),reply_markup=uvc_menu)

    elif text == 'Publicaciones de Bolivia':

        bot.send_message(cid, "La luz UVC, es muy eficaz para la esterilizacion de superficies\n")
        bot.send_chat_action(cid,'typing')
        #link original https://medium.com/@RadIONTech/la-luz-ultravioleta-contra-el-coronavirus-parte-1-encontrando-un-arma-efectiva-a52b994e6ed0
        #link logger https://grabify.link/5HJIKQ   https://leancoding.co/5HJIKQ
        #link deep logger SZEBYS
        bot.send_message(cid, 'En el siguiente enlace se detalla como la luz uv DESTRUYE a cualquier patógeno')
        bot.send_message(cid, "https://leancoding.co/5HJIKQ")
        bot.send_chat_action(cid,'typing')    

        #link original https://medium.com/@RadIONTech/la-luz-ultravioleta-contra-el-coronavirus-parte-2-una-punto-d%C3%A9bil-brutal-3813a87d0b5e
        #link logger https://grabify.link/VQYV3B   https://leancoding.co/VQYV3B
        #link deep logger 28335K

        bot.send_message(cid, 'En el siguiente enlace se detalla como que tan eficaz es UVC contra el CoronaVirus')
        bot.send_message(cid, "https://leancoding.co/VQYV3B",reply_markup=uvc_menu)
  
    elif text == 'Solicitar contacto y asesoria':
        bot.send_message(cid, "https://t.me/radiontech",reply_markup=uvc_menu)


    elif text == 'Atras':
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


def main_loop():
    print('Corriendo...')
    bot.polling(True)
    
    while 1:
        time.sleep(3)

if __name__ == '__main__':
    try:
        main_loop()
    
    except KeyboardInterrupt:
        print('\nExiting by user request.\n')
        sys.exit(0)