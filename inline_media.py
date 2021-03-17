from config import *
from download_media import *
from db_work import *


def inline_error():
	 return types.InlineQueryResultArticle(
			id=0,
			title='Ошибка',
			description='Неизвестная команда',
			input_message_content=types.InputTextMessageContent(
				message_text=f'Переходи в <b>@InstagramMediaDownloadBot</b> и скачивай посты из Instagram!',
				parse_mode='html'
			),
			thumb_url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/271/videocassette_1f4fc.png',
			thumb_width=48,
			thumb_height=48
		)

def inline_post(chat_id, post_link, query_id): # Отправить пост инлайн
	post = InstagramPost(post_link)
	medias = post.media
	data = []
	if post.user and medias:
		for media_id, media in enumerate(medias):
			add_to_media(media, post.user.username)
			data.append(types.InlineQueryResultArticle(
				id=media_id,
				title=f'🎞 Содержимое поста @{post.user.username}',
				input_message_content=types.InputTextMessageContent(
					message_text=f'🎞 <a href=\'{media}\'>Содержимое поста <b>@{post.user.username}</b></a>',
					parse_mode='html'
				),
				url=post_link,
				thumb_url=post.preview[media_id],
				thumb_width=48,
				thumb_height=48
			))
	else:
		data.append(inline_error())
	bot.answer_inline_query(query_id, data)

def inline_profile(chat_id, username, query_id): # Отправить профиль пользователя инлайн
	user = InstagramUser(username)
	data = []
	if user and user.user_id:
		data.append(types.InlineQueryResultArticle(
			id=0,
			title=user.full_name if user.full_name else user.username,
			description=user.biography if user.biography else '',
			input_message_content=types.InputTextMessageContent(
				message_text='{}{}{}{}{}{}'.format(
					f"<a href='{user.profile_pic_url}'>{'🔒' if user.is_private else '👤'}</a> <a href='https://www.instagram.com/{user.username}/'>{user.username}</a>\n",
					f"📷 Количество постов – <b>{user.posts_count}</b>\n" if user.posts_count else '',
					f"📥 Количество подписчиков – <b>{user.followers}</b>\n" if user.followers else '',
					f"📤 Количество подписок – <b>{user.followings}</b>\n\n" if user.followings else '\n',
					f"<b>{user.full_name}</b>\n" if user.full_name and user.biography else '',
					f"<i>{user.biography}</i>\n" if user.biography else ''
				),
				parse_mode='html'
			),
			thumb_url=user.profile_pic_url,
			thumb_width=48,
			thumb_height=48
		))
		stories = user.get_stories()
		if stories:
			for story_id, story in enumerate(stories):
				add_to_media(story.story_media, user.username)
				key = types.InlineKeyboardMarkup()
				if story.swipe_link:
					key.add(types.InlineKeyboardButton('🔗 Прикрепленная ссылка', url=story.swipe_link))
				data.append(types.InlineQueryResultArticle(
					id=story_id + 1,
					title=f'📹 История @{user.username}',
					reply_markup=key,
					input_message_content=types.InputTextMessageContent(
						message_text=f'📹 <a href=\'{story.story_media}\'>История <b>@{user.username}</b></a>',
						parse_mode='html'
					),
					thumb_url=story.preview,
					thumb_width=48,
					thumb_height=48
				))
	else:
		data.append(inline_error())
	bot.answer_inline_query(query_id, data)

def inline_story(chat_id, story_link, query_id): # Отправить историю инлайн
	story = InstagramStory(story_link)
	user = story.user
	data = []
	if user and user.user_id and not user.is_private:
		add_to_media(story.story_media, user.username)
		key = types.InlineKeyboardMarkup()
		if story.swipe_link:
			key.add(types.InlineKeyboardButton('🔗 Прикрепленная ссылка', url=story.swipe_link))
		data.append(types.InlineQueryResultArticle(
			id=0,
			title=f'📹 История @{user.username}',
			reply_markup=key,
			input_message_content=types.InputTextMessageContent(
				message_text=f'📹 <a href=\'{story.story_media}\'>История <b>@{user.username}</b></a>',
				parse_mode='html'
			),
			thumb_url=story.preview,
			thumb_width=48,
			thumb_height=48
		))
	else:
		data.append(inline_error())
	bot.answer_inline_query(query_id, data)
