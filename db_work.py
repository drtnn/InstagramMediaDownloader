from models import *

def get_user(user_id): # Получить пользователя по ID
	user_select = User.select().where(User.user_id == user_id)
	return user_select.get() if user_select else None

def get_media(media_id): # Получить фото/видео по ID
	media_select = Media.select().where(Media.media_id == media_id)
	return media_select.get() if media_select else None

def update_user(user_id, username, first_name): # Добавить или изменить пользователя в бд
	user = get_user(user_id)
	if user: 
		if user.username != username or user.first_name != first_name:
			user.username = username
			user.first_name = first_name
			user.save()
	else:
		user = User.create(user_id=user_id, username=username, first_name=first_name)
	return user

def add_to_media(media_link, media_owner): # Добавить или получить существующий фото/видео по ссылке
	media = Media.select().where(Media.media_link == media_link)
	if media:
		try:
			return media.get()
		except:
			return None
	else:
		return Media.create(media_link=media_link, media_owner=media_owner)

def add_to_favourites(user_id, media_id): # Добавить в избранное пользователя
	user = get_user(user_id)
	media = get_media(media_id)
	return SavedMedia.create(user=user, media=media) if user and media and not is_favourite(user_id, media_id) else None

def delete_from_favourites(user_id, media_id): # Удалить из избранного пользователя
	user = get_user(user_id)
	media = get_media(media_id)
	if user and media and is_favourite(user_id, media_id):
		SavedMedia.delete().where((SavedMedia.user == user) & (SavedMedia.media == media)).execute()
		return True
	else:
		return False

def get_favourites(user_id): # Получить список избранного пользователя
	user = get_user(user_id)
	return SavedMedia.select().where(SavedMedia.user == user) if user else None

def is_favourite(user_id, media_id): # Фото/видео в избранном пользователя
	user = get_user(user_id)
	media = get_media(media_id)
	return (True if SavedMedia.select().where((SavedMedia.user == user) & (SavedMedia.media == media)) else False) if user and media else False