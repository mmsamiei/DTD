#TOKEN = "564808836:AAG_QoeMiclCT5U7TC7eHd2TcFkn21tk6FU"
TOKEN = "488025339:AAEkCdi5LudTmYIjxsVbmCopeP2NZc7NS7w"
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
import logging
import json
import random
from telegram.error import (TelegramError, Unauthorized, BadRequest, TimedOut, ChatMigrated, NetworkError)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

class User:
	def __init__(self, **entries):
		self.state = "start"
		self.seen = []
		self.submited = []
		self.approved = []
		self.current_problem = ""
		if entries:
			self.__dict__.update(entries)
		# state is one of this: start, challenge, game_state, thinking, waiting_upload


def start(bot, update):
	chat_id = update.message.chat.id
	if str(chat_id) not in user_dict:
		user = User()
		user_dict[str(chat_id)] = user
		print(user_dict)
		print("*******************************************************************************************")
	user = user_dict[str(chat_id)]
	user.state = "start"
	update.message.reply_text('بسم الله الرحمن الرحیم')
	reply_keyboard = [['مسابقه عید', 'درباره ما', 'امکانات دیگر']]
	update.message.reply_text('سلام', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
	write_json()

def help(bot, update):
	update.message.reply_text("با آقای محمدمهدی سمیعی پاقلعه تماس بگیرید")

def update_handler(bot, update):
	if update.message:
		chat_id = update.message.chat.id
		user = user_dict[str(chat_id)]
		if(user.state == "start"):
			if(update.message.text):
				if(update.message.text == "مسابقه عید"):
					user.state = "challenge"
				if(update.message.text == "درباره ما"):
					update.message.reply_text('این بات با همکاری مشترک احسان مهرعلیان و محمدمهدی سمیعی پاقلعه نوشته شده است! ')
		elif(user.state == "challenge"):
			if(update.message.text):
				if(update.message.text == "توضیحات"):
					update.message.reply_text('توضیحات مسابقه اینجا نوشته خواهد شد')
					user.state = "challenge"
				if(update.message.text == "شرکت در مسابقه"):
					user.state = "game_state"
				if(update.message.text == "بازگشت"):
					user.state = "start"
		elif(user.state == "game_state"):
			if(update.message.text):
				if(update.message.text == "رسیدگی به وضع سوال فعلی"):
					update.message.reply_text('حلش کن دیگه!')
					user.state = "thinking"
				if(update.message.text == "دریافت سوال جدید"):
					if len(user.seen) >= len(problem_list):
						update.message.reply_text('فعلا سوال جدیدی وجود ندارد! منتظر سوالات جدید ما باشید!')
						user.state = "game_state"
					else:
						try:
							random_question = random.choice(list(set(problem_list) ^ set(user.seen)))
							bot.send_document(chat_id, document=open('./problems/'+random_question, 'rb'))
							user.current_problem = random_question
							user.seen.append(random_question)
							user.state = "thinking"
						except:
							update.message.reply_text("به علت خطا در شبکه شرمنده ام یه بار دیگه بزن رو دریافت سوال جدید :) باز هم عذر میخوام :) ")
				if(update.message.text == "وضعیت سوال‌های ارسال شده"):
					user.state = "game_state"
					text =  "\n".join(user.seen)
					update.message.reply_text("سوالات مشاهده شده توسط شما: \n"+text)
					text =  "\n".join(user.approved)
					update.message.reply_text("سوالات با پاسخ صحیح شما: \n"+text)
				if(update.message.text == "جدول امتیازات"):
					pass
					user.state = "game_state"
					#TODO جدول امتیازات
				if(update.message.text == "بازگشت"):
					user.state = "challenge"
		elif(user.state == "thinking"):
			if(update.message.text):
				if(update.message.text):
					if(update.message.text == "ارسال پاسخ"):
						update.message.reply_text('فایل خود را آپلود کنید')
						user.state = "waiting_upload"
					if(update.message.text == "انصراف"):
						update.message.reply_text('شما این سوال را باختید!')
						user.current_problem = ""
						user.state = "game_state"
					if(update.message.text == "بازگشت"):
						update.message.reply_text('امیدوارم که برگردی و سوال را حل کنی!')
						user.state = "game_state"
		elif(user.state == "waiting_upload"):
			if(update.message.document):
				try:
					user.submited.append(user.current_problem)
					update.message.document.get_file().download(".//"+user.current_problem)
					user.current_problem = None
					update.message.reply_text("فایل دریافت شد")
					update.message.forward(73675932)#ehssan_me chat_id
					user.current_problem = ""
					user.state = "game_state"
				except:
					update.message.reply_text("دوباره بفرست لعنتی")
			else:
				update.message.reply_text("لطفا فقط pdf ارسال کنید")
		
		#show state keyboard!!!!!! 
		if(user.state == "start"):
			reply_keyboard = [['مسابقه عید', 'درباره ما', 'امکانات دیگر']]
			update.message.reply_text('سلام', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
		elif(user.state == "challenge"):
			reply_keyboard = [['توضیحات', 'شرکت در مسابقه'],['بازگشت']]
			update.message.reply_text('یکی از گزینه‌های زیر را انتخاب فرمایید', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
		elif(user.state == "game_state"):
			if user.current_problem is "":
				reply_keyboard = [['دریافت سوال جدید'],['وضعیت سوال‌های ارسال شده'],['جدول امتیازات']]
			else:
				reply_keyboard = [['رسیدگی به وضع سوال فعلی'],['وضعیت سوال‌های ارسال شده'],['جدول امتیازات']]
			update.message.reply_text('لطفا یکی از گزینه‌های زیر را انتخاب کنید', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
			pass
		elif(user.state == "thinking"):
			reply_keyboard = [['ارسال پاسخ', 'انصراف'],['بازگشت']]
			update.message.reply_text('لطفا یکی از گزینه‌های زیر را انتخاب کنید', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
			pass
		elif(user.state == "waiting_upload"):
			update.message.reply_text('فایل خود را آپلود کنید')
			pass

		write_json()

def error_callback(bot, update, error):
	try:
		raise error
	except Unauthorized:
		pass
		# remove update.message.chat_id from conversation list
	except BadRequest:
		pass
		# handle malformed requests - read more below!	
	except TimedOut:
		update.message.reply_text("لطفا مجددا تلاش فرمایید")
		# handle slow connection problems
	except NetworkError:
		pass
	except ChatMigrated as e:
		pass
		# the chat_id of a group has changed, use e.new_chat_id instead
	except TelegramError:
		pass
		# handle all other telegram related errors

def write_json():
	with open('data.json', 'w') as fp:
		json.dump(user_dict, fp, default=lambda o: o.__dict__)

def main():
	global user_dict
	global problem_list
	try:
		with open('data.json', 'r') as fp:
			temp_dict = json.load(fp)
			user_dict = {}
			for k, v in temp_dict.items():
				user_dict[k] = User(**v)
	except:
		print("it is execpt at line 101")
		user_dict = {}
	try:
		with open('problems.json', 'r') as fp:
			problem_list = json.load(fp)["problems"]
			print(problem_list)
	except:
		print("it is execpt at line 107")
		problem_list = []
	updater = Updater(TOKEN)
	dp = updater.dispatcher

	dp.add_handler(CommandHandler("start", start))
	dp.add_handler(CommandHandler("help", help))
	dp.add_handler(MessageHandler(Filters.all, update_handler))
	dp.add_error_handler(error_callback)
	
	updater.start_polling()
	updater.idle()

if __name__ == '__main__':
	main()