import config
import db_work
import json


def upload_error_users():
	users = json.loads(open('error_users.json', 'r').read())
	for user in users:
		db_work.update_user(user['user_id'], user['username'] if 'username' in user else None, 'first_name' in user if user['first_name'] else None)
	with open('error_users.json', 'w') as users_json:
		json.dump([], users_json)


def add_error_user(user_id, username, first_name):
	users = json.loads(open('error_users.json', 'r').read())
	with open('error_users.json', 'w') as users_json:
		error_dict = {'user_id': user_id}
		if username:
			error_dict['username'] = username
		if first_name:
			error_dict['first_name'] = first_name
		users.append(error_dict)
		json.dump(users, users_json)