from discord.ext import commands, tasks
import re, json, asyncio, dialogflow, time
from main import config
from random import randint, choice
from google.oauth2 import service_account
from google.protobuf.json_format import MessageToJson

DIALOGFLOW_PROJECT_ID = config['token-monolog']
DIALOGFLOW_LANGUAGE_CODE = config['df-language-code']
SESSION_ID = config['df-session-id']
SERVICE_ACCOUNT_FILE = config['token-monolog']+'.json'
CREDENTIALS = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)

class Monolog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.monolog_loop = True

    @commands.Cog.listener()
    async def on_ready(self):
        self.loop_zaczepka.start()
        await asyncio.sleep(randint(120,300))
        self.loop_reklama.start()

    @commands.command(pass_context=True)
    async def toggle_monolog(self):
        self.monolog_loop = not self.monolog_loop

    @commands.command(pass_context=True)
    async def trigger_monolog(self, ctx):
        await send_monolog(self, 'community2nSH')

    @tasks.loop(minutes=randint(1, 5))
    async def loop_reklama(self):
        if self.monolog_loop:
            await send_monolog(self, 'community2nSH')
    
    @tasks.loop(minutes=randint(7, 10))
    async def loop_zaczepka(self):
        if self.monolog_loop:
            channel = self.bot.get_channel(728252426544742510)
            await channel.send('!c playerlist')

    @commands.Cog.listener()
    async def on_message(self, message):
        if (message.channel.name == "console-io" and
                message.author.bot and not message.author.id == self.bot.user.id):
            if "default" in message.content:
                await zaczepka(self, message)

async def zaczepka(self, message):
    playername = re.search(r'(?<=default: )[^\n]*', message.content).group(0)
    playername = re.sub(r",", "", playername)
    playername = re.split(r'\s', playername)
    playername = choice(playername)

    await send_monolog(self, f'1234UnrealSucks {playername}')

async def send_monolog(self, phrase):
    json_response = json.loads(df_request(phrase))
    channel = self.bot.get_channel(702951480201838763)

    await channel.send(f'{json_response["queryResult"]["fulfillmentText"]}')
    print(f'[{current_time()}] Monolog: {json_response["queryResult"]["fulfillmentText"]}')

def df_request(monolog_input):
    session_client = dialogflow.SessionsClient(credentials=CREDENTIALS)
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=(monolog_input), language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(session=session, query_input=query_input)
    json_response = MessageToJson(response)
    return json_response

def current_time():
    return time.strftime('%H:%M:%S')


def setup(bot):
    bot.add_cog(Monolog(bot))