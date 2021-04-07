import config
from download_media import InstagramPost, InstagramStory, InstagramUser
from telebot import types


def send_post(chat_id, post_link):  # Отправить пост
	post = InstagramPost(post_link)
	medias = post.media
	if not medias:
		config.bot.send_message(
			chat_id, "🛑 <b>Введена неверная ссылка</b>", parse_mode='html')
	elif post.user and medias:
		try:
			for media in medias:
				config.bot.send_document(chat_id=chat_id, data=media)
		except:
			for media in medias:
				config.bot.send_message(
					chat_id, f'🎞 <a href=\'{media}\'>Содержимое поста <b>@{post.user.username}</b></a>', parse_mode='html')
		if post.caption:
			config.bot.send_message(
				chat_id, f'<a href=\'https://www.instagram.com/{post.user.username}/\'>@{post.user.username}</a>: {post.caption}', parse_mode='html')
	else:
		config.bot.send_message(
			chat_id, "🛑 <b>Ошибка</b>", parse_mode='html')


def send_profile(chat_id, username):  # Отправить профиль пользователя
	user = InstagramUser(username)
	if user and not user.user_id:
		config.bot.send_message(
			chat_id, "🛑 <b>Профиль не существует</b>", parse_mode='html')
	elif user:
		key = types.InlineKeyboardMarkup()
		key.add(
			types.InlineKeyboardButton(
				"📹 Истории", callback_data=f'stories:{user.username}')
		)
		text = '{}{}{}{}{}{}'.format(
			f"{'🔒' if user.is_private else '👤'} <a href='https://www.instagram.com/{user.username}/'>{user.username}</a>\n",
			f"📷 Количество постов – <b>{user.posts_count}</b>\n" if user.posts_count else '',
			f"📥 Количество подписчиков – <b>{user.followers}</b>\n" if user.followers else '',
			f"📤 Количество подписок – <b>{user.followings}</b>\n\n" if user.followings else '\n',
			f"<b>{user.full_name}</b>\n" if user.full_name and user.biography else '',
			f"<i>{user.biography}</i>\n" if user.biography else ''
		)
		config.bot.send_photo(chat_id, user.profile_pic_url,
							  text, reply_markup=key, parse_mode='html')
	else:
		config.bot.send_message(
			chat_id, "🛑 <b>Ошибка</b>", parse_mode='html')


def send_stories(chat_id, username):  # Отправить истории
	user = InstagramUser(username)
	if user and user.is_private:
		config.bot.send_message(
			chat_id, "🛑 <b>Профиль пользователя закрыт</b>", parse_mode='html')
	elif user and not user.user_id:
		config.bot.send_message(
			chat_id, "🛑 <b>Профиль не существует</b>", parse_mode='html')
	elif user:
		stories = user.get_stories()
		if not stories:
			config.bot.send_message(
				chat_id, "🛑 <b>Нет актуальных историй</b>", parse_mode='html')
		else:
			try:
				for story in stories:
					key = types.InlineKeyboardMarkup()
					if story.swipe_link:
						key.add(
							types.InlineKeyboardButton(
								'🔗 Прикрепленная ссылка', url=story.swipe_link)
						)
					config.bot.send_document(
						chat_id=chat_id, data=story.story_media, reply_markup=key)
			except:
				for story in stories:
					key = types.InlineKeyboardMarkup()
					if story.swipe_link:
						key.add(
							types.InlineKeyboardButton(
								'🔗 Прикрепленная ссылка', url=story.swipe_link)
						)
					config.bot.send_message(
						chat_id, f'📹 <a href=\'{story.story_media}\'>История <b>@{username}</b></a>', parse_mode='html', reply_markup=key)
	else:
		config.bot.send_message(
			chat_id, "🛑 <b>Ошибка</b>", parse_mode='html')


def send_story(chat_id, story_link):  # Отправить историю
	story = InstagramStory(story_link)
	user = story.user
	if user and user.is_private:
		config.bot.send_message(
			chat_id, "🛑 <b>Профиль пользователя закрыт</b>", parse_mode='html')
	elif user and not user.user_id:
		config.bot.send_message(
			chat_id, "🛑 <b>Профиль не существует</b>", parse_mode='html')
	elif user:
		if not story.story_media:
			config.bot.send_message(
				chat_id, "🛑 <b>История отсутствует</b>", parse_mode='html')
		else:
			key = types.InlineKeyboardMarkup()
			if story.swipe_link:
				key.add(
					types.InlineKeyboardButton(
						'🔗 Прикрепленная ссылка', url=story.swipe_link)
				)
			try:
				config.bot.send_document(
					chat_id, story.story_media, reply_markup=key)
			except:
				config.bot.send_message(
					chat_id, f'📹 <a href=\'{story.story_media}\'>История <b>@{user.username}</b></a>', parse_mode='html', reply_markup=key)
	else:
		config.bot.send_message(
			chat_id, "🛑 <b>Ошибка</b>", parse_mode='html')
