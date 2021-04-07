from models import User


def get_user(user_id):  # Получить пользователя по ID
	user_select = User.select().where(User.user_id == user_id)
	return user_select.get() if user_select else None


def update_user(user_id, username, first_name):  # Добавить или изменить пользователя в бд
	user = get_user(user_id)
	if user:
		if user.username != username or user.first_name != first_name:
			user.username = username
			user.first_name = first_name
			user.save()
	else:
		user = User.create(user_id=user_id, username=username,
						   first_name=first_name)
	return user
