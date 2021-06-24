from environs import Env
from telebot import TeleBot

env = Env()
env.read_env()

ADMINS = [int(user_id) for user_id in env.list('ADMINS')]
BOT_TOKEN = env.str('BOT_TOKEN')
COOKIE = env.str('COOKIE')
DATABASE_URL = env.str('DATABASE_URL')

bot = TeleBot(token=BOT_TOKEN)