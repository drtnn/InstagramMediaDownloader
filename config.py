from headers import *
import os
import random
import requests
import urllib.parse
import telebot
from telebot import types

bot = telebot.TeleBot(os.environ['token'])