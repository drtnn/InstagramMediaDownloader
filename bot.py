from config import *
from download_media import *

@bot.message_handler(content_types=['text'])
def contentText(message):
	if message.text == '/start':
		bot.send_message(message.chat.id, "<b>Привет, я помогу тебе скачать фото и видео из Instagram</b>\nПросто пришли мне ссылку на пост.", parse_mode='html')
	elif validators.url(message.text) and ('instagram.com/p/' in message.text or 'instagram.com/tv/' in message.text):
		send_media(message)
	else:
		bot.send_message(message.chat.id, "<b>Произошла ошибка</b>\nНеизвестная команда.", parse_mode='html')

def send_media(message):
	medias =  get_media_json(message.text)
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
				    

bot.send_message(144589481, "polling restart")
try:
    bot.polling(none_stop=True)
except Exception as ex:
    bot.send_message(144589481, ex)
