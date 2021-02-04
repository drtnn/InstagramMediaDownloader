from config import *
from download_media import *

@bot.message_handler(commands=['start'])
def startCommand(message):
	bot.send_message(message.chat.id, "<b>Привет, я помогу тебе скачать фото и видео из Instagram</b>", parse_mode='html')

@bot.message_handler(commands=['get_post'])
def getPostCommand(message):
	bot.send_message(message.chat.id, "Пришли мне ссылку на пост, а я тебе фото и видео.", parse_mode='html')
	bot.register_next_step_handler(message, send_media)

def send_media(message):
	medias = InstagramPost(message.text).get_media()
	if not medias:
		bot.send_message(message.chat.id, "<b>Произошла ошибка</b>\nВведена неверная ссылка или профиль пользователя закрыт.", parse_mode='html')
	else:
		medias_content = [ types.InputMediaDocument(media) for media in medias ]
		try:
			bot.send_media_group(message.chat.id, medias_content)
		except:
			text = ''
			for index, media in enumerate(medias):
				text += f'🎞 <a href=\'{media}\'>Файл №{index + 1}</a>\n'
			bot.send_message(message.chat.id, text, parse_mode='html')

@bot.message_handler(commands=['get_stories'])
def getStoriesCommand(message):
	bot.send_message(message.chat.id, "Пришли мне имя пользователя Instagram, а я тебе истории.", parse_mode='html')
	bot.register_next_step_handler(message, send_stories)

def send_stories(message):
	user = InstagramUser(message.text)
	if user.is_private:
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
				for index, media in enumerate(medias):
					text += f'🎞 <a href=\'{media}\'>Файл №{index + 1}</a>\n'
				bot.send_message(message.chat.id, text, parse_mode='html') #Поправить ошибку при отправлении очень длинных сообщений: ENTITIES_TOO_LONG	    

bot.send_message(144589481, "polling restart")
try:
    bot.polling(none_stop=True)
except Exception as ex:
    bot.send_message(144589481, ex)
