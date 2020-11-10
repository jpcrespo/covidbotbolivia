import telebot
import time, os

TOKEN = "1183310581:AAGVvRfB8QAYz7raCdMZtBX97JFYCevS6k4"  # SUSTITUIR

chat_id = 89650251

bot = telebot.TeleBot(TOKEN)

# sendVideo
video = open('coviduvc.mp4', 'rb')
bot.send_video(chat_id, video)
file_id = 'AAAaaaZZZzzz'
bot.send_video(chat_id, file_id)
