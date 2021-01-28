from discord.ext import commands
import re, json, asyncio, os, dialogflow, time
from main import config
from random import randint
from google.oauth2 import service_account

DIALOGFLOW_PROJECT_ID = config['token-monolog']
DIALOGFLOW_LANGUAGE_CODE = config['df-language-code']
SESSION_ID = config['df-session-id']
SERVICE_ACCOUNT_FILE = config['token-monolog']+'.json'
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)

class monolog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        t = time.localtime()
        self.current_time = time.strftime("%H:%M:%S", t)
        self.chat_channel = self.bot.get_channel(int(config['chat-channel']))
        
    @commands.Cog.listener()
    async def on_ready(self):
        await main(self)

async def main(self):
    self.chat_channel = self.bot.get_channel(int(config['chat-channel']))
    session_client = dialogflow.SessionsClient(credentials=credentials)
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=('community2nSH'), language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(session=session, query_input=query_input)
    await self.chat_channel.send(f"{response.query_result.fulfillment_text}")
    print(f"[{self.current_time}] Monolog: {response.query_result.fulfillment_text}")

    await asyncio.sleep(randint(1800,2700))
    await main(self)


def setup(bot):
    bot.add_cog(monolog(bot))