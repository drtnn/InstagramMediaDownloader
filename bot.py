import config
import db_work
from download_media import InstagramPost, InstagramStory, InstagramUser
import inline_media
import send_media
import error_users
import urllib


@config.bot.message_handler(commands=['start'])
def start_command(message):  # Команда /start
	try:
		db_work.update_user(
			message.from_user.id, message.from_user.username, message.from_user.first_name)
	except:
		config.bot.send_message(config.ADMIN, f'[DB ERROR] – {message.from_user.id}, {message.from_user.username}, {message.from_user.first_name}')
		error_users.add_error_user(message.from_user.id, message.from_user.username, message.from_user.first_name)
	config.bot.send_message(message.from_user.id, "🙋🏻‍♂️ Привет, я бот для скачивания публикаций из <pre>Instagram</pre>.\n\n🔗 Просто отправь ссылку на пост, историю или никнейм.\n\n💬 Информация по всем функциям бота доступна по команде /help", parse_mode='html')


@config.bot.message_handler(commands=['help'])
def help_command(message):  # Команда /help
	config.bot.send_message(message.from_user.id, "💭 Скачиваю весь контент из <pre>Instagram</pre>.\n\n🔗 Просто отправь ссылку на пост, историю или никнейм.\n\n\t🎞: <code>instagram.com/p/*****/</code>\n\t📹: <code>instagram.com/stories/drtagram/*****/</code>\n\t👤: <code>drtagram</code>\n\n💬 Чтобы отправить публикацию другу в диалог, воспользуйся <pre>inline</pre>-режимом бота.\n\n\t🎞: <code>@InstagramMediaDownloadBot instagram.com/p/*****/</code>\n\t📹: <code>@InstagramMediaDownloadBot instagram.com/stories/drtagram/*****/</code>\n\t👤: <code>@InstagramMediaDownloadBot drtagram</code>", parse_mode='html')


@config.bot.message_handler(content_types=['text'])
def text_command(message):  # Ссылка на контент или профиль пользователя
	if not ('via_bot' in message.json and message.json['via_bot']['is_bot']):
		if 'instagram.com/' in message.text.lower():
			if 'instagram.com/p/' in message.text.lower() or 'instagram.com/tv/' in message.text.lower():
				send_media.send_post(message.from_user.id, message.text)
			elif 'instagram.com/s/' in message.text.lower() or 'instagram.com/stories/highlights/' in message.text.lower():
				send_media.send_highlights(message.from_user.id, message.text)
			elif 'instagram.com/stories/' in message.text.lower():
				send_media.send_story(message.from_user.id, message.text)
			elif 'instagram.com/' in message.text.lower():
				send_media.send_profile(message.from_user.id, urllib.parse.urlparse(
					message.text)[2].split('/')[1])
		elif InstagramUser(message.text).user_id:
			send_media.send_profile(message.from_user.id, message.text)


@config.bot.inline_handler(func=lambda query: len(query.query) > 0)
def inline_query(query):
	if 'instagram.com/' in query.query.lower():
		if 'instagram.com/p/' in query.query.lower() or 'instagram.com/tv/' in query.query.lower():
			inline_media.inline_post(query.from_user.id, query.query, query.id)
		elif 'instagram.com/s/' in query.query.lower() or 'instagram.com/stories/highlights/' in query.query.lower():
			inline_media.inline_highlight(
				query.from_user.id, query.query, query.id)
		elif 'instagram.com/stories/' in query.query.lower():
			inline_media.inline_story(
				query.from_user.id, query.query, query.id)
		elif 'instagram.com/' in query.query.lower():
			inline_media.inline_profile(query.from_user.id, urllib.parse.urlparse(
				query.query)[2].split('/')[1], query.id)
		else:
			config.bot.answer_inline_query(
				query.id, [inline_media.inline_error()])
	elif InstagramUser(query.query).user_id:
		inline_media.inline_profile(query.from_user.id, query.query, query.id)
	else:
		config.bot.answer_inline_query(query.id, [inline_media.inline_error()])


@config.bot.callback_query_handler(func=lambda c: True)
def inline(c):  # Нажатие инлайн кнопок
	if c.data.startswith('stories:'):
		send_media.send_stories(c.from_user.id, c.data[8:])


config.bot.send_message(config.ADMIN, "polling restart")
try:
	config.bot.infinity_polling(timeout=5)
except Exception as ex:
	config.bot.send_message(config.ADMIN, ex)
