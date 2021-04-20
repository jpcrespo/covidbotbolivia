# ==================================
# =           KungFluBot           =
# ==================================


"""

   Este bot esta pensado para desplegar 
   información respecto a covid19.


"""

#Librerias
import telebot
from telebot import types
import pandas as pd

import time, os, sys
sys.path.insert(0, 'core/')



import datos
from datos import *



userStep = {}                           
#Se almacena como clave : valor, el recorrido del usuario en el bot

knownUsers = []                         
#Registro de usuarios conocidos. Queda realizar una funcion que guarde
#el registro en disco y los vuelva a leer cada vez que el bot inicie


commands = {'start'		:	'Inicia el bot',
            'thanks'	:	'Agradecimientos y referencias',
            'help' 		:	'Información de uso',
            'exec' 		:	'Terminal (Only Admin)'}

#Comandos que el bot contiene para operar. chequear entre las opciones
#que contiene el fatherbot para desplegar los comandos 



_token_='6b697373206d7920617373'



# =======================================
# =           El Menu del bot           =
# = El esqueleto de conformación y una  =
# = clase para imprimir colores en la   = 
# = terminal.                           =
# =======================================



menu = types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True,one_time_keyboard=False)
menu.add('☢️ Esteriliza con UV','⚠️Facebook leak 🇧🇴','☣️🇧🇴 Info covid19 📈\n última actualización: '+flag_date)

info_menu = types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True,one_time_keyboard=False)
info_menu.add('📈Reporte Nacional 🇧🇴','📈Reporte por Departamento 📝','🏥 Contactos de emergencia en 🇧🇴','🔙Atrás')

inf_dep = types.ReplyKeyboardMarkup(row_width=5,resize_keyboard=True,one_time_keyboard=False)
inf_dep.add('La Paz','Cochabamba','Santa Cruz','Potosí','Oruro','Pando','Beni','Chuquisaca','Tarija','🔙Atrás')

uv_menu = types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True,one_time_keyboard=False)
uv_menu.add('Video Informativo','Consejos prácticos','🔙Atrás')

fb_menu = types.ReplyKeyboardMarkup(row_width=1,resize_keyboard=True,one_time_keyboard=False)
fb_menu.add('👁️ DISCLAIMER', '¿mi número se filtró? 🔎','🔙Atrás')

# COLOR TEXTO Control Terminal
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
#puede ser en un log sobre las respuestas tambien. 

def listener(messages):
    for m in messages:
        if m.content_type == 'text':
            print("["+str(m.chat.id)+"]"+str(m.chat.first_name)+": " + m.text + "-" + str(time.strftime("%c")) )




#Inicializamos el bot

#creamos el objeto Telegram Bot
bot = telebot.TeleBot(token)
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
        bot.send_message(cid, "Hola 👋👋 "+str(m.chat.username)+" que bueno verte nuevamente.")
        time.sleep(0.4)
        _a=1
    else:
        bot.send_message(cid, "Hola 👋👋 "+str(m.chat.username)+', te doy la Bienvenida!')
        time.sleep(0.4)
        bot.send_message(cid, "Te voy registrando...")
        _a=2
        get_user_step(cid);

    bot.send_message(cid, "Iniciando el bot...")
    bot.send_message(cid," 3️⃣ ")
    time.sleep(0.1)
    bot.delete_message(m.chat.id, m.message_id+_a+2)
    bot.send_message(cid," 2️⃣ ")
    time.sleep(0.1)
    bot.delete_message(m.chat.id, m.message_id+_a+3)
    bot.send_message(cid," 1️⃣ ")
    time.sleep(0.1)
    bot.delete_message(m.chat.id, m.message_id+_a+4)
    bot.send_message(cid, "🤖  Listo  ✅... Por favor use los botones.",reply_markup=menu)
	
   # AYUDA
@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "Hola, este bot muestra los datos covid19 en Bolivia\n"
    help_text += "Tambien despliega información de utilidad \n"
    help_text += "Comandos disponibles: \n"
    bot.send_message(cid, help_text,reply_markup=menu)
    for key in commands:
        help_textk = "/" + key + ": "
        help_textk += commands[key] + "\n"
        bot.send_message(cid, help_textk,reply_markup=menu)


# EXEC COMANDO
@bot.message_handler(commands=['exec'])
def command_exec(m):
    cid = m.chat.id
    if cid == 89650251:  # cid del admin!
        bot.send_message(cid, "Ejecutan en consola: " + m.text[len("/exec"):])
        bot.send_chat_action(cid, 'typing')
        time.sleep(1)
        f = os.popen(m.text[len("/exec"):])
        result = f.read()
        bot.send_message(cid, "Resultado: " + result)
    else:
        bot.send_message(cid, "PERMISO DENEGADO, solo Juan The Creator puede acceder")
        print(color.RED + " ¡PERMISO DENEGADO! " + color.ENDC)


# thanks COMANDO
@bot.message_handler(commands=['thanks'])
def command_exec(m):
    cid = m.chat.id
    bot.send_message(cid,"Agradecimientos a: ")
    bot.send_message(cid,'Un capo total',reply_markup=menu)



# =========================================================================
# =           Sección de despligue de menus internos y acciones           =
# =========================================================================



# MENU PRINCIPAL
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 0)
def main_menu(m):
    cid = m.chat.id
    text = m.text
    if text == "☢️ Esteriliza con UV":
    	bot.send_message(cid, "Use un método fácil, barato y eficiente de esterilización: Luz UVC", reply_markup =uv_menu)
    	userStep[cid] = 1
    elif text == "⚠️Facebook leak 🇧🇴":  # CAMARA
        bot.send_message(cid, "Averígue si sus datos fueron comprometidos (solo Bolivia)", reply_markup=fb_menu)
        userStep[cid] = 4

    elif text == '☣️🇧🇴 Info covid19 📈\n última actualización: '+flag_date:
        bot.send_message(cid,'Información Actualizada respecto al covid19',reply_markup=info_menu)
        userStep[cid] = 2

    else:
        command_text(m)



# MENU INFO COVID
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 1)
def uvmain_menu(m):
    cid = m.chat.id
    txt = m.text
    if txt == "Video Informativo":
    	bot.send_chat_action(cid,'upload_video')
    	bot.send_video(cid, open('bins/video.mp4', 'rb'), supports_streaming=True)
    	bot.send_message(cid,'Si desea asesoramiento no dude en contactar:\nhttps://t.me/radiontech ',reply_markup=uv_menu)
    	print(color.GREEN + "video enviado" + color.ENDC)

    elif txt == 'Consejos prácticos':
    	bot.send_chat_action(cid,'typing')
    	time.sleep(1)
    	bot.send_message(cid,datos.getMessage(),reply_markup=uv_menu)
    	print(color.GREEN + "consejo enviado" + color.ENDC)

    elif txt == "🔙Atrás":  # HD
        userStep[cid] = 0
        bot.send_message(cid, "Menu Principal:", reply_markup=menu)
    else:
        command_text(m)




# MENU INFO COVID
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 2)
def infomain_menu(m):
    cid = m.chat.id
    txt = m.text
    if txt == "📈Reporte Nacional 🇧🇴":
        bot.send_message(cid,'Curva de variación diaria de casos')
        bot.send_chat_action(cid,'upload_photo')
        bot.send_photo(cid, open('core/pics/covNac.png', 'rb'))
        bot.send_message(cid,'Vacunación a nivel Nacional 💉')
        bot.send_chat_action(cid,'upload_photo')
        bot.send_photo(cid, open('core/pics/vacNac.png', 'rb'),reply_markup=info_menu)

    elif txt == '📈Reporte por Departamento 📝':
    	userStep[cid] = 3
    	bot.send_message(cid,'Se muestran los datos desagregados por Departamento',reply_markup=inf_dep)

    elif txt == '🏥 Contactos de emergencia en 🇧🇴':
        bot.send_chat_action(cid,'typing')
        bot.send_message(cid,'Caja Petrolera de Salud https://www.cps.org.bo/')
        bot.send_message(cid,'Caja Nacional de Salud https://www.cns.gob.bo/')
        bot.send_message(cid,'Caja de Salud de la Banca Privada https://portal.csbp.com.bo/')
        bot.send_message(cid,'Caja Nacional de Caminos http://www.cajasaludcaminos.gob.bo/')
        bot.send_message(cid,'Caja de Salud Cordes https://www.sistemacordes.org/')
        bot.send_message(cid,'Caja Bancaria Estatal de salud  https://www.cbes.org.bo/')
        bot.send_message(cid,'Cossmil https://www.cossmil.mil.bo/#/inicio')
        bot.send_message(cid,'Seguro Integral de Salud SINEC http://sinec.org.bo/')
        bot.send_message(cid,'Seguro Social Universitario http://www.ssulapaz.org/',reply_markup=info_menu)


    elif txt == "🔙Atrás":  # HD
        userStep[cid] = 0
        bot.send_message(cid, "Menu Principal:", reply_markup=menu)
    else:
        command_text(m)



@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 3)
def infodep_menu(m):
    cid = m.chat.id
    txt = m.text
    if txt == "La Paz":
        bot.send_message(cid,'Curva de variación diaria de casos')
        bot.send_chat_action(cid,'upload_photo')
        bot.send_photo(cid, open('core/pics/covLa Paz.png', 'rb'))
        bot.send_message(cid,'Vacunación 💉')
        bot.send_chat_action(cid,'upload_photo')
        bot.send_photo(cid, open('core/pics/vacLa Paz.png', 'rb'),reply_markup=inf_dep)

    elif txt == 'Cochabamba':
        bot.send_message(cid,'Curva de variación diaria de casos')
        bot.send_chat_action(cid,'upload_photo')
        bot.send_photo(cid, open('core/pics/covCochabamba.png', 'rb'))
        bot.send_message(cid,'Vacunación 💉')
        bot.send_chat_action(cid,'upload_photo')
        bot.send_photo(cid, open('core/pics/vacCochabamba.png', 'rb'),reply_markup=inf_dep)

    elif txt == 'Santa Cruz':
        bot.send_message(cid,'Curva de variación diaria de casos')
        bot.send_chat_action(cid,'upload_photo')
        bot.send_photo(cid, open('core/pics/covSanta Cruz.png', 'rb'))
        bot.send_message(cid,'Vacunación 💉')
        bot.send_chat_action(cid,'upload_photo')
        bot.send_photo(cid, open('core/pics/vacSanta Cruz.png', 'rb'),reply_markup=inf_dep)

    elif txt == 'Potosí':
        bot.send_message(cid,'Curva de variación diaria de casos')
        bot.send_chat_action(cid,'upload_photo')
        bot.send_photo(cid, open('core/pics/covPotosí.png', 'rb'))
        bot.send_message(cid,'Vacunación 💉')
        bot.send_chat_action(cid,'upload_photo')
        bot.send_photo(cid, open('core/pics/vacPotosi.png', 'rb'),reply_markup=inf_dep)

    elif txt == 'Oruro':
        bot.send_message(cid,'Curva de variación diaria de casos')
        bot.send_chat_action(cid,'upload_photo')
        bot.send_photo(cid, open('core/pics/covOruro.png', 'rb'))
        bot.send_message(cid,'Vacunación 💉')
        bot.send_chat_action(cid,'upload_photo')
        bot.send_photo(cid, open('core/pics/vacOruro.png', 'rb'),reply_markup=inf_dep)

    elif txt == 'Pando':
        bot.send_message(cid,'Curva de variación diaria de casos')
        bot.send_chat_action(cid,'upload_photo')
        bot.send_photo(cid, open('core/pics/covPando.png', 'rb'))
        bot.send_message(cid,'Vacunación 💉')
        bot.send_chat_action(cid,'upload_photo')
        bot.send_photo(cid, open('core/pics/vacPando.png', 'rb'),reply_markup=inf_dep)
    elif txt == 'Beni':
        bot.send_message(cid,'Curva de variación diaria de casos')
        bot.send_chat_action(cid,'upload_photo')
        bot.send_photo(cid, open('core/pics/covBeni.png', 'rb'))
        bot.send_message(cid,'Vacunación 💉')
        bot.send_chat_action(cid,'upload_photo')
        bot.send_photo(cid, open('core/pics/vacBeni.png', 'rb'),reply_markup=inf_dep)
    elif txt == 'Chuquisaca':
        bot.send_message(cid,'Curva de variación diaria de casos')
        bot.send_chat_action(cid,'upload_photo')
        bot.send_photo(cid, open('core/pics/covChuquisaca.png', 'rb'))
        bot.send_message(cid,'Vacunación 💉')
        bot.send_chat_action(cid,'upload_photo')
        bot.send_photo(cid, open('core/pics/vacChuquisaca.png', 'rb'),reply_markup=inf_dep)

    elif txt == 'Tarija':
        bot.send_message(cid,'Curva de variación diaria de casos')
        bot.send_chat_action(cid,'upload_photo')
        bot.send_photo(cid, open('core/pics/covTarija.png', 'rb'))
        bot.send_message(cid,'Vacunación 💉')
        bot.send_chat_action(cid,'upload_photo')
        bot.send_photo(cid, open('core/pics/vacTarija.png', 'rb'),reply_markup=inf_dep)

    elif txt == '🔙Atrás':
        userStep[cid] = 2
        bot.send_message(cid, "Menu Principal:", reply_markup=info_menu)
    else:
        command_text(m)



@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 4)
def fbmain_menu(m):
    cid = m.chat.id
    txt = m.text
    if txt == '👁️ DISCLAIMER':
        bot.send_chat_action(cid,'typing')
        bot.send_message(cid,"En el filtrado de datos de Facebook del 2021 se expusieron casi 3 millones de cuentas Bolivianas, puede buscar si su número se encuentra vulnerable.")
        bot.send_message(cid,'Puede asociar a su número con: ')
        bot.send_message(cid,'Nombres, apellidos, sexo, ciudades, estado civil, trabajo',reply_markup=fb_menu)
    elif txt == '¿mi número se filtró? 🔎':
        markup = types.ForceReply(selective=False)
        target_n =  bot.send_message(cid,"Ingrese su número 591: ",reply_markup=markup);
        bot.register_next_step_handler(target_n,busqueda)
    elif txt == '🔙Atrás':
        userStep[cid] = 0
        bot.send_message(cid, "Menu Principal:", reply_markup=menu)
        
    else:
        command_text(m)
 
def busqueda(m):
    cid=m.chat.id
    nn=m.text
    if nn.isdigit():
        n1=int(nn)
        n2=59100000000+n1
        if(n1>60000000 and n1<79999999):
            bot.send_message(cid,"Revisando en la base . . .🔍️🔍️🔍️")
            index=df[df['A']==n2]
            if index.empty:
                bot.send_message(cid,"Su número no esta en la filtración ✔️",reply_markup=fb_menu)
            else:
                bot.send_message(cid,"Su número ESTA en la filtración, tenga cuidado ⚠️",reply_markup=fb_menu)
            
        else:
            bot.send_message(cid,"No es un número de Bolivia o esta mal escrito.",reply_markup=fb_menu)
    
    else:
        bot.send_message(cid,"Dato introducido no válido",reply_markup=fb_menu)
    



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


if __name__ == '__main__':
    df = pd.read_csv('Bolivia.csv',sep=',',names=["A","B",'C',"D","E","F","G","H","I","J","K","L","M","N","O"])
    try:
        main_loop()
    
    except KeyboardInterrupt:
        print('\nExiting by user request.\n')
        sys.exit(0)


