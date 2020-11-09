import telebot
import time

TOKEN = "1183310581:AAGVvRfB8QAYz7raCdMZtBX97JFYCevS6k4"  # SUSTITUIR

# 4 Thread worker for message listener.
tb = telebot.TeleBot(TOKEN, True, 4)

def echo_messages(*messages):
    """
    Echoes all incoming messages of content_type 'text'.
    """
    for m in messages:
        chatid = m.chat.id
        if m.content_type == 'text':
            text = m.text
            bot.send_message(chatid, text)
            
#logger = telebot.logger
#formatter = logging.Formatter('[%(asctime)s] %(thread)d {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s','%m-%d %H:%M:%S')



# Setup telebot handler to telebot logger. If you want to get some information from telebot.
# More information at Logging section
#handler = logging.StreamHandler(sys.stdout)
#telebot.logger.addHandler(handler)
#telebot.logger.setLevel(logging.INFO)

# getMe
user = tb.get_me()

# sendMessage
tb.send_message(chatid, text)

# forwardMessage
# tb.forward_message(10894,926,3)
tb.forward_message(to_chat_id, from_chat_id, message_id)

# sendPhoto
photo = open('bolivia.png', 'rb')
tb.send_photo(chat_id, photo)
file_id = 'AAAaaaZZZzzz'
tb.send_photo(chat_id, file_id)

# sendAudio
audio = open('test.m4a', 'rb')
tb.send_audio(chat_id, audio)
file_id = 'Macri Gato'
tb.send_audio(chat_id, file_id)

# sendDocument
doc = open('README.md', 'rb')
tb.send_document(chat_id, doc)
file_id = 'AAAaaaZZZzzz'
tb.send_document(chat_id, file_id)


# sendVideo
video = open('coviduvc.mp4', 'rb')
tb.send_video(chat_id, video)
file_id = 'AAAaaaZZZzzz'
tb.send_video(chat_id, file_id)

# sendLocation
#tb.send_location(chat_id, lat, lon)

# sendChatAction
# action_string can be one of the following strings: 'typing', 'upload_photo', 'record_video', 'upload_video',
# 'record_audio', 'upload_audio', 'upload_document' or 'find_location'.
tb.send_chat_action(chat_id, 'find_location')
# Use the ReplyKeyboardMarkup class.
# Thanks pevdh.
from telebot import types

markup = types.ReplyKeyboardMarkup()
markup.add('a', 'v', 'd')
tb.send_message(chat_id, message, reply_markup=markup)

# or add strings one row at a time:
markup = types.ReplyKeyboardMarkup()
markup.row('a', 'v')
markup.row('c', 'd', 'e')
tb.send_message(chat_id, message, reply_markup=markup)