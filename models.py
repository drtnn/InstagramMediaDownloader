from config import *

db = peewee.PostgresqlDatabase(os.environ['db_name'], host=os.environ['db_host'], port=int(os.environ['db_port']), user=os.environ['db_user'], password=os.environ['db_password'])

class User(peewee.Model):
	user_id = peewee.IntegerField(verbose_name='User ID', unique=True)
	username = peewee.CharField(verbose_name='Username', max_length=50, null=True)
	first_name = peewee.CharField(verbose_name='First name', max_length=50, null=True)

	def __str__(self):
		return f'First name – {self.first_name}, User ID – {self.user_id}, Username – {self.username}'

	class Meta:
		database = db

class Media(peewee.Model):
	media_id = peewee.AutoField(verbose_name='Media ID')
	media_link = peewee.TextField(verbose_name='Media link', unique=True)
	media_owner = peewee.CharField(verbose_name='Media owner')

	def __str__(self):
		return f'Media ID – {self.media_id}, Media link – {self.media_link}, Media owner – {self.media_owner}'

	class Meta:
		database = db
		order_by = ('media_id',)

class SavedMedia(peewee.Model):
	user = peewee.ForeignKeyField(User, verbose_name='User', on_delete='CASCADE')
	media = peewee.ForeignKeyField(Media, verbose_name='Media', on_delete='CASCADE')

	def __str__(self):
		return f'User – {self.user}, Media – {self.media}'

	class Meta:
		database = db
