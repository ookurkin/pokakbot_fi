# -*- coding: utf-8 -*-
import telebot
import schedule
import datetime
import sqlite3 as sq
from sqlite3 import Error as e

bot = telebot.TeleBot('5271086085:AAEuSbtQOUp7XGZrJVWyDHzpdenl1ntZIfE')

currentTime = datetime.datetime.now()



with sq.connect("pokakbot.db", check_same_thread=False) as connection:
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users(user_id INTEGER, user_login TEXT, shit_type INTEGER, shit_date TEXT)")

def db_table_val(user_id: int, shit_type: int, user_login: str, shit_date: str):
	cursor.execute('INSERT INTO users (user_id, user_login,  shit_type, shit_date) VALUES (?, ?, ?, ?)', (user_id, user_login, shit_type, shit_date))
	connection.commit()


@bot.message_handler(content_types=['text','sticker'])
def default_answers(message):

 if message.text == "/help":
  bot.reply_to(message, "Я - бот для отслеживания покаков, напиши /shit number, где number - тип кала по Бристольской шкале, подробнее про шкалу /type")
 elif message.text == "/start":
  bot.reply_to(message, "Я уже работаю")
 elif message.text.startswith("/shit"):
   messageSplit = message.text.split()
   secondElementOfMessageSplit = int(messageSplit[1])
   if secondElementOfMessageSplit > 7 or secondElementOfMessageSplit < 1:
       bot.reply_to(message, "Некорректное значение шкалы")
   else :
    us_id = message.from_user.id
    us_login = message.from_user.username
    sh_type = messageSplit[1]
    sh_date = currentTime
    db_table_val(user_id=us_id, user_login=us_login, shit_type=sh_type, shit_date=sh_date)
    bot.reply_to(message, 'Данные учтены')
 elif message.text == "/type":
  bot.reply_to(message, "Тип 1: Отдельные жёсткие куски, похожие на орехи, прямую кишку проходят с трудом. \n Тип 2: Колбасовидный комковатый кал (диаметр больше, чем у типа 3). \n Тип 3: Колбасовидный кал с поверхностью, покрытой трещинами (диаметр меньше, чем у типа 2). \n Тип 4: Колбасовидный или змеевидный кал с мягкой и гладкой поверхностью. \n Тип 5: Кал в форме мягких комочков с чёткими краями, легко проходящий через прямую кишку. \n Тип 6: Пористый, рыхлый, мягкий кал в форме пушистых комочков с рваными краями. \n Тип 7: Водянистый кал, без твёрдых кусочков; либо полностью жидкий")
 elif message.text == "/history":
  historyOutput = cursor.execute("SELECT user_id || user_login || shit_type || shit_date FROM users")
  rows = cursor.fetchall()
  for row in rows:
    bot.reply_to(message,row),





 else:
  bot.send_sticker(message.chat.id,"CAACAgEAAxkBAAEExC5ihjwhxvNTw84Rks1AoxH7SYFDaQACAwADf3BGHENZiEtY50bNJAQ", reply_to_message_id = message.message_id)



bot.polling(none_stop=True, interval=0)





