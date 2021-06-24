from config import DATABASE_URL
import peewee
import sqlalchemy

DATABASE_FORM = sqlalchemy.engine.url.make_url(DATABASE_URL)
db = peewee.PostgresqlDatabase(DATABASE_FORM.database, host=DATABASE_FORM.host, port=DATABASE_FORM.port,
                               user=DATABASE_FORM.username,
                               password=DATABASE_FORM.password)


class User(peewee.Model):
	user_id = peewee.IntegerField(verbose_name='User ID', unique=True)
	username = peewee.CharField(
		verbose_name='Username', max_length=128, null=True)
	first_name = peewee.CharField(
		verbose_name='First name', max_length=128, null=True)

	def __str__(self):
		return f'First name – {self.first_name}, User ID – {self.user_id}, Username – {self.username}'

	class Meta:
		database = db
