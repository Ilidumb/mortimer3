from discord.ext import commands
import re, json, asyncio, os, dialogflow, time
from main import config

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config['token-monolog']+'.json'

DIALOGFLOW_PROJECT_ID = config['token-monolog']
DIALOGFLOW_LANGUAGE_CODE = 'pl'
SESSION_ID = 'me'