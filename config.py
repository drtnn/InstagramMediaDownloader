from headers import *
import os
import peewee
import random
import requests
import urllib.parse
import telebot
from telebot import types

ADMIN = 144589481
bot = telebot.TeleBot(os.environ['token'])