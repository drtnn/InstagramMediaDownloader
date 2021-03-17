from config import *
from download_media import *
from send_media import *
from db_work import *
from inline_media import *

@bot.message_handler(commands=['start'])
def start_command(message): # Команда /start
	update_user(message.from_user.id, message.from_user.username, message.from_user.first_name)
	bot.send_message(message.from_user.id, "<b>Привет, я помогу тебе скачать фото и видео из Instagram</b>\nПросто пришли мне ссылку на пост или историю, в ответ ты получишь нужные тебе файлы. Также можешь прислать мне никнейм пользователя в Instagram, а я скачаю для тебя все актуальные истории.", parse_mode='html')

@bot.message_handler(commands=['favourites'])
def favourites_command(message): # Команда /favourites
	update_user(message.from_user.id, message.from_user.username, message.from_user.first_name)
	send_favourites(message.from_user.id)

@bot.message_handler(content_types=['text'])
def text_command(message): # Ссылка на контент или профиль пользователя
	update_user(message.from_user.id, message.from_user.username, message.from_user.first_name)
	if 'instagram.com/' in message.text.lower():
		if 'instagram.com/p/' in message.text.lower() or 'instagram.com/tv/' in message.text.lower():
			send_post(message.from_user.id, message.text)
		elif 'instagram.com/stories/' in message.text.lower():
			send_story(message.from_user.id, message.text)
		elif 'instagram.com/' in message.text.lower():
			send_profile(message.from_user.id, urllib.parse.urlparse(message.text)[2].split('/')[1])
		else:
			bot.send_message(message.from_user.id, "<b>Произошла ошибка</b>\nВведена неверная ссылка.", parse_mode='html')
	elif InstagramUser(message.text).user_id:
		send_profile(message.from_user.id, message.text)
	else:
		bot.send_message(message.from_user.id, "<b>Произошла ошибка</b>", parse_mode='html')

@bot.inline_handler(func=lambda query: len(query.query) > 0)
def inline_query(query):
	update_user(query.from_user.id, query.from_user.username, query.from_user.first_name)
	if 'instagram.com/' in query.query.lower():
		if 'instagram.com/p/' in query.query.lower() or 'instagram.com/tv/' in query.query.lower():
			inline_post(query.from_user.id, query.query, query.id)
		elif 'instagram.com/stories/' in query.query.lower():
			inline_story(query.from_user.id, query.query, query.id)
		elif 'instagram.com/' in query.query.lower():
			inline_profile(query.from_user.id, urllib.parse.urlparse(query.query)[2].split('/')[1], query.id)
		else:
			bot.answer_inline_query(query.id, [inline_error()])
	elif InstagramUser(query.query).user_id:
		inline_profile(query.from_user.id, query.query, query.id)
	else:
		bot.answer_inline_query(query.id, [inline_error()])

@bot.callback_query_handler(func=lambda c:True)
def inline(c): # Нажатие инлайн кнопок
	print(c.data)
	update_user(c.from_user.id, c.from_user.username, c.from_user.first_name)
	if c.data.startswith('stories:'):
		send_stories(c.from_user.id, c.data[8:])
	elif c.data.startswith('favourites:'):
		media_id = int(c.data[11:])
		if not is_favourite(c.from_user.id, media_id):
			add_to_favourites(c.from_user.id, media_id)
			try:
				bot.answer_callback_query(callback_query_id=c.id, text='Добавлено')
			except:
				pass
		else:
			delete_from_favourites(c.from_user.id, media_id)
			try:
				bot.answer_callback_query(callback_query_id=c.id, text='Удалено')
			except:
				pass
		try:
			bot.edit_message_reply_markup(c.from_user.id, c.message.message_id, reply_markup=favourite_button(c.from_user.id, media_id))
		except:
			pass

bot.send_message(ADMIN, "polling restart")
try:
	bot.polling(none_stop=True)
except Exception as ex:
	bot.send_message(ADMIN, ex)