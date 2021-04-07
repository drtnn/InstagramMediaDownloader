import os
import peewee


db = peewee.PostgresqlDatabase(os.environ['db_name'], host=os.environ['db_host'], port=int(
	os.environ['db_port']), user=os.environ['db_user'], password=os.environ['db_password'])


class User(peewee.Model):
	user_id = peewee.IntegerField(verbose_name='User ID', unique=True)
	username = peewee.CharField(
		verbose_name='Username', max_length=50, null=True)
	first_name = peewee.CharField(
		verbose_name='First name', max_length=50, null=True)

	def __str__(self):
		return f'First name – {self.first_name}, User ID – {self.user_id}, Username – {self.username}'

	class Meta:
		database = db
