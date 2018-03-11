TOKEN = "564808836:AAG_QoeMiclCT5U7TC7eHd2TcFkn21tk6FU"
import telebot
import logging
import os
import sys
import pickle
import time
from telebot import types

bot = telebot.TeleBot(TOKEN)
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

user_dict = {}
class User:
    def __init__(self):
        self.state = 0


def db_write():
	pickle.dump( user_dict, open( "db.p", "wb" ) )




@bot.message_handler(commands=['start'])
def send_welcome(message):
	chat_id = message.chat.id
	user = User()
	user_dict[chat_id] = user
	bot.reply_to(message, "سلام به بات تدریسیار امیرکبیر خوش آمدید!")
	markup = types.ReplyKeyboardMarkup(row_width=2)
	itembtn1 = types.KeyboardButton('دریافت سوال')
	itembtn2 = types.KeyboardButton('درباره ما')
	markup.add(itembtn1, itembtn2)
	bot.send_message(chat_id, "یکی از گزینه‌ها را انتهاب کنید", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def echo_message(message):
	chat_id = message.chat.id
	user = user_dict[chat_id]
	if(user.state == 0):
		if(message.text == "دریافت سوال"):
			user.state = 1
			markup = types.ReplyKeyboardRemove(selective=False)
			bot.send_message(chat_id, "چشم، به زودی یک سوال برای شما ارسال خواهد شد:)" , reply_markup=markup)
			problem_pdf = open('./problems/problem1.pdf', 'rb')
			bot.send_document(chat_id, problem_pdf)
			markup = types.ReplyKeyboardMarkup(row_width=2)
			itembtn1 = types.KeyboardButton('دریافت سوال')
			itembtn2 = types.KeyboardButton('درباره ما')
			markup.add(itembtn1, itembtn2)			
			bot.send_message(chat_id, "یکی از گزینه‌ها را انتهاب کنید", reply_markup=markup)
		elif(message.text == "درباره ما"):
			bot.reply_to(message, "باید بهت درباره ما نشون بدم")
	else:
		bot.reply_to(message, message.text)

@bot.message_handler(commands=['plus1'])
def send_welcome(message):
	chat_id = message.chat.id
	user = user_dict[chat_id]
	user.state = user.state + 1
	bot.reply_to(message, "رفتی به استیت ۱")


@bot.message_handler(commands=['show'])
def send_welcome(message):
	chat_id = message.chat.id
	user = user_dict[chat_id]
	bot.reply_to(message, str(user.state))
	db_write()

def main_loop():
	while True:
		try:
			bot.polling(none_stop=True)
		except Exception as e:
			print("Exception occurred:", e)
			break
			time.sleep(2)
			os.execv(sys.executable, ['python'] + sys.argv)
			pass
		else:
			break
	while 1:
		time.sleep(3)

time.sleep(3)

if __name__=='__main__':
	with open('db.p', 'rb') as f:
		user_dict = pickle.load(f)
	try:
		main_loop()
	except KeyboardInterrupt:
		db_write()
		sys.exit(0)
