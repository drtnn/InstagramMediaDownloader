from config import *
from download_media import *
from db_work import *

def favourite_button(user_id, media_id, swipe_link=None): # Сгенерировать кнопку избранного
	key = types.InlineKeyboardMarkup()
	media = get_media(media_id)
	user = get_user(user_id)
	if swipe_link:
		key.add(types.InlineKeyboardButton('🔗 Прикрепленная ссылка', url=swipe_link))
	if media and user and is_favourite(user.user_id, media.media_id):
		key.add(types.InlineKeyboardButton('📤 Удалить из избранного', callback_data=f'favourites:{media.media_id}'))
	else:
		if media and user:
			key.add(types.InlineKeyboardButton('📥 Добавить в избранное', callback_data=f'favourites:{media.media_id}'))
	return key

def send_post(chat_id, post_link): # Отправить пост
	post = InstagramPost(post_link)
	medias = post.media
	if not medias:
		bot.send_message(chat_id, "<b>Произошла ошибка</b>\nВведена неверная ссылка.", parse_mode='html')
	elif post.user and medias:
		print(medias)
		try:
			for media in medias:
				bot.send_document(chat_id=chat_id, data=media, reply_markup=favourite_button(chat_id, add_to_media(media, post.user.username).media_id))
		except:
			for media in medias:
				bot.send_message(chat_id, f'🎞 <a href=\'{media}\'>Содержимое поста <b>@{post.user.username}</b></a>', parse_mode='html', reply_markup=favourite_button(chat_id, add_to_media(media, post.user.username).media_id))
		if post.caption:
			bot.send_message(chat_id, f'<a href=\'https://www.instagram.com/{post.user.username}/\'>@{post.user.username}</a>: {post.caption}', parse_mode='html')
	else:
		bot.send_message(chat_id, "<b>Произошла ошибка</b>", parse_mode='html')

def send_profile(chat_id, username): # Отправить профиль пользователя
	user = InstagramUser(username)
	if user and not user.user_id:
		bot.send_message(chat_id, "<b>Произошла ошибка</b>\nПрофиль не существует.", parse_mode='html')
	elif user:
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
	else:
		bot.send_message(chat_id, "<b>Произошла ошибка</b>", parse_mode='html')

def send_stories(chat_id, username): # Отправить истории
	user = InstagramUser(username)
	if user and user.is_private:
		bot.send_message(chat_id, "<b>Произошла ошибка</b>\nПрофиль пользователя закрыт.", parse_mode='html')
	elif user and not user.user_id:
		bot.send_message(chat_id, "<b>Произошла ошибка</b>\nПрофиль не существует.", parse_mode='html')
	elif user:
		stories = user.get_stories()
		if not stories:
			bot.send_message(chat_id, "<b>Нет актуальных историй.</b>", parse_mode='html')
		else:
			try:
				for story in stories:
					bot.send_document(chat_id=chat_id, data=story.story_media, reply_markup=favourite_button(chat_id, add_to_media(story.story_media, username).media_id, story.swipe_link))
			except:
				for story in stories:
					bot.send_message(chat_id, f'📹 <a href=\'{story.story_media}\'>История <b>@{username}</b></a>', parse_mode='html', reply_markup=favourite_button(chat_id, add_to_media(story.story_media, username).media_id, story.swipe_link))
	else:
		bot.send_message(chat_id, "<b>Произошла ошибка</b>", parse_mode='html')

def send_story(chat_id, story_link): # Отправить историю
	story = InstagramStory(story_link)
	user = story.user
	if user and user.is_private:
		bot.send_message(chat_id, "<b>Произошла ошибка</b>\nПрофиль пользователя закрыт.", parse_mode='html')
	elif user and not user.user_id:
		bot.send_message(chat_id, "<b>Произошла ошибка</b>\nПрофиль не существует.", parse_mode='html')
	elif user:
		if not story.story_media:
			bot.send_message(chat_id, "<b>История отсутствует.</b>", parse_mode='html')
		else:
			key = favourite_button(chat_id, add_to_media(story.story_media, user.username).media_id)
			if story.swipe_link:
				key.add(
					types.InlineKeyboardButton('🔗 Прикрепленная ссылка', url=story.swipe_link)
				)
			try:
				bot.send_document(chat_id, story.story_media, reply_markup=key)
			except:
				bot.send_message(chat_id, f'📹 <a href=\'{story.story_media}\'>История <b>@{user.username}</b></a>', parse_mode='html', reply_markup=key)
	else:
		bot.send_message(chat_id, "<b>Произошла ошибка</b>", parse_mode='html')

def send_favourites(user_id, first_media=0, last_media=10):
	favourites = get_favourites(user_id)
	if favourites:
		for i in range(first_media, last_media):
			if i >= len(favourites):
				break
			try:
				bot.send_document(user_id, favourites[i].media.media_link, reply_markup=favourite_button(user_id, favourites[i].media.media_id))
			except:
				bot.send_message(user_id,  f'📹 <a href=\'{favourites[i].media.media_link}\'>История <b>@{favourites[i].media.media_owner}</b></a>', reply_markup=favourite_button(user_id, favourites[i].media.media_id), parse_mode='html')
	else:
		bot.send_message(user_id, 'Избранного пока нет!', parse_mode='html')