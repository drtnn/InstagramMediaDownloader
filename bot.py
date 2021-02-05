from config import *
from download_media import *

@bot.message_handler(content_types=['text'])
def textCommand(message):
	if message.text == '/start':
		startCommand(message)
	elif validators.url(message.text):
		if 'instagram.com/p/' in message.text or 'instagram.com/tv/' in message.text:
			send_media(message)
		elif 'instagram.com/stories/' in message.text:
			send_story(message)
		elif 'instagram.com/' in message.text:
			message.text = urllib.parse.urlparse(message.text)[2].split('/')[1]
			send_stories(message)
		else:
			bot.send_message(message.chat.id, "<b>Произошла ошибка</b>\nВведена неверная ссылка.", parse_mode='html')
	elif InstagramUser(message.text).user_id:
		send_stories(message)
	else:
		bot.send_message(message.chat.id, "<b>Произошла ошибка</b>\nАккаунт не найден.", parse_mode='html')

@bot.message_handler(commands=['start'])
def startCommand(message):
	bot.send_message(message.chat.id, "<b>Привет, я помогу тебе скачать фото и видео из Instagram</b>\nПросто пришли мне ссылку на пост или историю, в ответ ты получишь нужные тебе файлы. Также можешь прислать мне никнейм пользователя в Instagram, а я скачаю для тебя все актуальные истории.", parse_mode='html')

@bot.message_handler(commands=['get_post'])
def getPostCommand(message):
	bot.send_message(message.chat.id, "Пришли мне ссылку на пост.", parse_mode='html')
	bot.register_next_step_handler(message, send_media)

def send_media(message):
	post = InstagramPost(message.text)
	medias = post.media
	if post.user.is_private:
		bot.send_message(message.chat.id, "<b>Произошла ошибка</b>\nПрофиль пользователя закрыт.", parse_mode='html')
	elif not medias:
		bot.send_message(message.chat.id, "<b>Произошла ошибка</b>\nВведена неверная ссылка.", parse_mode='html')
	else:
		medias_content = [ types.InputMediaDocument(media) for media in medias ]
		try:
			bot.send_media_group(message.chat.id, medias_content)
		except:
			text = ''
			for media in medias:
				bot.send_message(message.chat.id, f'🎞 <a href=\'{media}\'>Содержимое поста <b>@{post.user.username}</b></a>', parse_mode='html')
		if post.caption:
			bot.send_message(message.chat.id, f'<a href=\'https://www.instagram.com/{post.user.username}/\'>@{post.user.username}</a>: {post.caption}', parse_mode='html')

@bot.message_handler(commands=['get_stories'])
def getStoriesCommand(message):
	bot.send_message(message.chat.id, "Пришли мне имя пользователя Instagram.", parse_mode='html')
	bot.register_next_step_handler(message, send_stories)

def send_stories(message):
	user = InstagramUser(message.text)
	if user.is_private or not user.user_id:
		bot.send_message(message.chat.id, "<b>Произошла ошибка</b>\nПрофиль закрыт или не существует.", parse_mode='html')
	else:
		medias = user.get_stories()
		if not medias:
			bot.send_message(message.chat.id, "<b>Нет актуальных историй.</b>", parse_mode='html')
		else:
			medias_content = [ types.InputMediaDocument(media) for media in medias ]
			try:
				bot.send_media_group(message.chat.id, medias_content) #Поправить ошибку при отправлении слишком больших файлов
			except:
				text = ''
				for media in medias:
					bot.send_message(message.chat.id, f'📹 <a href=\'{media}\'>История <b>@{message.text}</b></a>', parse_mode='html') #Поправить ошибку при отправлении очень длинных сообщений: ENTITIES_TOO_LONG	    

@bot.message_handler(commands=['get_story'])
def getStoryCommand(message):
	bot.send_message(message.chat.id, "Пришли мне ссылку на историю пользователя Instagram.", parse_mode='html')
	bot.register_next_step_handler(message, send_story)

def send_story(message):
	story = InstagramStory(message.text)
	user = story.user
	if user.is_private or not user.user_id:
		bot.send_message(message.chat.id, "<b>Произошла ошибка</b>\nПрофиль закрыт или не существует.", parse_mode='html')
	else:
		if not story.story_media:
			bot.send_message(message.chat.id, "<b>История отсутствует.</b>", parse_mode='html')
		else:
			key = types.InlineKeyboardMarkup()
			if story.swipe_link:
				key.add(
					types.InlineKeyboardButton('🔗 Прикрепленная ссылка', url=story.swipe_link)
				)
			try:
				bot.send_document(message.chat.id, story.story_media, reply_markup=key) #Поправить ошибку при отправлении слишком больших файлов
			except:
				bot.send_message(message.chat.id, f'📹 <a href=\'{story.story_media}\'>История <b>@{user.username}</b></a>', parse_mode='html', reply_markup=key) #Поправить ошибку при отправлении очень длинных сообщений: ENTITIES_TOO_LONG	    

bot.send_message(144589481, "polling restart")
try:
	bot.polling(none_stop=True)
except Exception as ex:
    bot.send_message(144589481, ex)
