
import telebot
import time, os

TOKEN = "1183310581:AAGVvRfB8QAYz7raCdMZtBX97JFYCevS6k4"  # SUSTITUIR

CHAT_ID = 89650251

bot = telebot.TeleBot(TOKEN)

ret_msg = bot.send_voice(CHAT_ID, open('test.m4a', 'rb'))

file_info = bot.get_file(ret_msg.voice.file_id)

downloaded_file = bot.download_file(file_info.file_path)

with open('new_file.ogg', 'wb') as new_file:
    new_file.write(downloaded_file)

