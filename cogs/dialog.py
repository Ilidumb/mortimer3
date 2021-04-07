import re, json, asyncio, dialogflow
from discord.ext import commands
from time import strftime
from main import config
from google.oauth2 import service_account
from google.protobuf.json_format import MessageToJson

# * Importing all tokens and additional info from the config
DIALOGFLOW_PROJECT_ID = config['token-dialog']
DIALOGFLOW_LANGUAGE_CODE = config['df-language-code']
SESSION_ID = config['df-session-id']
SERVICE_ACCOUNT_FILE = config['token-dialog']+'.json'
CREDENTIALS = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)

CHANNELS = config['watched-channels']

class Dialog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # * Getting the messages and checking for mentions
    @commands.Cog.listener()
    async def on_message(self, message):
        # Checking if the message was sent in a listened channel, and if it mentions the bot
        if str(message.channel) in CHANNELS:
            if (str(self.bot.user.id) in message.content.lower() or
                    str(self.bot.user.name).lower() in message.content.lower()):
                await clean_message(self, message)
                
# * Splitting the message into content and author
async def clean_message(self, message):
    # Removing the bot mention / name from the message:
    # TODO: find a better way to do this:
    if f'<@!{self.bot.user.id}>' in message.content:
        content = re.sub(f'<@!{self.bot.user.id}> ', '', message.content)
    elif f'<@{self.bot.user.id}>' in message.content:
        content = re.sub(f'<@{self.bot.user.id}> ', '', message.content)
    else:
        content = re.sub(f'{self.bot.user.name.lower()} ', '', message.content.lower())
    # If the message was sent from minecraft:
    if message.author.bot:
        # Preventing the bot from going into an infinite loop
        if message.author.id == self.bot.user.id:
            return
        # Separate the username and the message:
        content = content.split(' » ', 1)
        author = content[0]
        content = content[1]
    # If the message was sent from discord:
    else:
        author = message.author.display_name
    print(f'[{current_time()}] Wiadomość: {author}: {content}')
    # RETRAIN TO NOT TRIGGER ON FIRST WORD (AUTHOR)
    # TO USE WHEN RETRAINED:
    # content = f'{author}: {content}'
    if author in ['kipi','\~kipior']:
        pass
    else:
        await df_sendmessage(self, content, author, message)

async def df_sendmessage(self, content, author, message):
    # Send request to the Dialogflow API:
    json_response = json.loads(df_request(content))
    
    # If available, execute the custom payload:
    # await exec_payload(self, json_response)

    print(f'[{current_time()}] Odpowiedź: {json_response["queryResult"]["fulfillmentText"]}')
    await message.channel.send(json_response['queryResult']['fulfillmentText'])

async def exec_payload(self, json_response):
    try:
        cCommands = json_response["queryResult"]["fulfillmentMessages"][1]["payload"]["cCommand"]
        pCommands = json_response["queryResult"]["fulfillmentMessages"][1]["payload"]["pCommand"]
        self.console = self.bot.get_channel(728252426544742510)
        for cCommand in cCommands:
            print(f'[{current_time()}] Wykonywanie komendy: {cCommand}')
            await self.console.send(cCommand)
            await asyncio.sleep(0.2)
        for pCommand in pCommands:
            exec(pCommand)
            await asyncio.sleep(0.2)
    except (IndexError, KeyError) as exception:
        pass

# * Send request to the Dialogflow API
def df_request(dialog_input):
    session_client = dialogflow.SessionsClient(credentials=CREDENTIALS)
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=(dialog_input), language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(session=session, query_input=query_input)
    json_response = MessageToJson(response)
    return json_response

def current_time():
    return strftime('%H:%M:%S')

def setup(bot):
    bot.add_cog(Dialog(bot))