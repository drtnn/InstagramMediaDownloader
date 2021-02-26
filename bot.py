from config import *
from download_media import *

@bot.message_handler(commands=['start'])
def startCommand(message):
	bot.send_message(message.chat.id, "<b>Привет, я помогу тебе скачать фото и видео из Instagram</b>\nПросто пришли мне ссылку на пост или историю, в ответ ты получишь нужные тебе файлы. Также можешь прислать мне никнейм пользователя в Instagram, а я скачаю для тебя все актуальные истории.", parse_mode='html')

@bot.message_handler(content_types=['text'])
def textCommand(message):
	message_text = message.text.lower()
	if message_text == '/start':
		startCommand(message)
	elif validators.url(message_text):
		if 'instagram.com/p/' in message_text or 'instagram.com/tv/' in message_text:
			send_media(message.chat.id, message_text)
		elif 'instagram.com/stories/' in message_text:
			send_story(message.chat.id, message_text)
		elif 'instagram.com/' in message_text:
			send_profile(message.chat.id, urllib.parse.urlparse(message_text)[2].split('/')[1])
		else:
			bot.send_message(message.chat.id, "<b>Произошла ошибка</b>\nВведена неверная ссылка.", parse_mode='html')
	elif InstagramUser(message_text).user_id:
		send_profile(message.chat.id, message_text)
	else:
		bot.send_message(message.chat.id, "<b>Произошла ошибка</b>\nАккаунт не найден.", parse_mode='html')

def send_media(chat_id, post_link):
	post = InstagramPost(post_link)
	medias = post.media
	if post.user.is_private:
		bot.send_message(chat_id, "<b>Произошла ошибка</b>\nПрофиль пользователя закрыт.", parse_mode='html')
	elif not medias:
		bot.send_message(chat_id, "<b>Произошла ошибка</b>\nВведена неверная ссылка.", parse_mode='html')
	else:
		medias_content = [ types.InputMediaDocument(media) for media in medias ]
		try:
			bot.send_media_group(chat_id, medias_content)
		except:
			for media in medias:
				bot.send_message(chat_id, f'🎞 <a href=\'{media}\'>Содержимое поста <b>@{post.user.username}</b></a>', parse_mode='html')
		if post.caption:
			bot.send_message(chat_id, f'<a href=\'https://www.instagram.com/{post.user.username}/\'>@{post.user.username}</a>: {post.caption}', parse_mode='html')

def send_profile(chat_id, username):
	user = InstagramUser(username)
	if not user.user_id:
		bot.send_message(chat_id, "<b>Произошла ошибка</b>\nПрофиль не существует.", parse_mode='html')
	else:
		key = types.InlineKeyboardMarkup()
		key.add(
			types.InlineKeyboardButton("🎞 Истории", callback_data=f'stories:{user.username}')
		)
		text = 	'{}{}{}{}{}{}'.format(
					f"{'🔒' if user.is_private else '👤'} <a href='https://www.instagram.com/{user.username}/'>{user.username}</a>\n",
					f"📷 Количество постов – <b>{user.posts_count}</b>\n" if user.posts_count else '',
					f"📥 Количество подписчиков – <b>{user.followers}</b>\n" if user.followers else '',
					f"📤 Количество подписок – <b>{user.followings}</b>\n\n" if user.followings else '\n',
					f"<b>{user.full_name}</b>\n" if user.full_name and user.biography else '',
					f"<i>{user.biography}</i>\n" if user.biography else ''
				)
		bot.send_photo(chat_id, user.profile_pic_url, text, reply_markup=key, parse_mode='html')


def send_stories(chat_id, username):
	user = InstagramUser(username)
	if user.is_private:
		bot.send_message(chat_id, "<b>Произошла ошибка</b>\nПрофиль пользователя закрыт.", parse_mode='html')
	elif not user.user_id:
		bot.send_message(chat_id, "<b>Произошла ошибка</b>\nПрофиль не существует.", parse_mode='html')
	else:
		stories = user.get_stories()
		if not stories:
			bot.send_message(chat_id, "<b>Нет актуальных историй.</b>", parse_mode='html')
		else:
			stories_content = [ types.InputMediaDocument(story) for story in stories ]
			try:
				bot.send_media_group(chat_id, stories_content) #Поправить ошибку при отправлении слишком больших файлов
			except:
				for story in stories:
					bot.send_message(chat_id, f'📹 <a href=\'{story}\'>История <b>@{username}</b></a>', parse_mode='html')

def send_story(chat_id, story_link):
	story = InstagramStory(story_link)
	user = story.user
	if user.is_private:
		bot.send_message(chat_id, "<b>Произошла ошибка</b>\nПрофиль пользователя закрыт.", parse_mode='html')
	elif not user.user_id:
		bot.send_message(chat_id, "<b>Произошла ошибка</b>\nПрофиль не существует.", parse_mode='html')
	else:
		if not story.story_media:
			bot.send_message(chat_id, "<b>История отсутствует.</b>", parse_mode='html')
		else:
			key = types.InlineKeyboardMarkup()
			if story.swipe_link:
				key.add(
					types.InlineKeyboardButton('🔗 Прикрепленная ссылка', url=story.swipe_link)
				)
			try:
				bot.send_document(chat_id, story.story_media, reply_markup=key) #Поправить ошибку при отправлении слишком больших файлов
			except:
				bot.send_message(chat_id, f'📹 <a href=\'{story.story_media}\'>История <b>@{user.username}</b></a>', parse_mode='html', reply_markup=key)

@bot.callback_query_handler(func=lambda c:True)
def inline(c):
	if c.data.startswith('stories:'):
		send_stories(c.message.chat.id, c.data[8:])


bot.send_message(144589481, "polling restart")
try:
	bot.polling(none_stop=True)
except Exception as ex:
    bot.send_message(144589481, ex)