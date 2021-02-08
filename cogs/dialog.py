from discord.ext import commands
import re, json, asyncio, os, dialogflow, time, sys
from main import config, client
from google.oauth2 import service_account
from google.protobuf.json_format import MessageToJson

# *Importing all tokens and additional info from the config
DIALOGFLOW_PROJECT_ID = config['token-dialog']
DIALOGFLOW_LANGUAGE_CODE = config['df-language-code']
SESSION_ID = config['df-session-id']
SERVICE_ACCOUNT_FILE = config['token-dialog']+'.json'
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)

class dialog(commands.Cog):
    def __init__(self, bot):
        # *Declaring some variables that are used thoughout
        self.bot = bot
        self.t = time.localtime()
        self.current_time = time.strftime('%H:%M:%S', self.t)
        self.channels = config['watched-channels']
        self.namecheck = False
        self.console = self.bot.get_channel(728252426544742510)
        
    @commands.Cog.listener()
    async def on_message(self ,message):
        # *Checking if the message was sent in a listened channel, and if it mentions the bot
        if str(message.channel) in self.channels:
            if str(self.bot.user.id) in message.content.lower() or str(self.bot.user.name).lower() in message.content.lower():
                await clean_message(self, message)
            elif self.namecheck:
                await clean_message(self, message)
                
async def clean_message(self, message):
    # *Removing the bot mention / name from the message
    if f'<@!{self.bot.user.id}>' in message.content:
        content = re.sub(f'<@!{self.bot.user.id}> ', '', message.content)
    elif f'<@{self.bot.user.id}>' in message.content:
        content = re.sub(f'<@{self.bot.user.id}> ', '', message.content)
    else:
        content = re.sub(f'{self.bot.user.name.lower()} ', '', message.content.lower())
    # *Additional case for when the message was sent from minecraft
    if message.author.bot:
        # Preventing the bot from going into an infinite loop
        if message.author.id == self.bot.user.id:
            return
        content = content.split(' » ', 1)
        author = content[0]
        content = content[1]
    else:
        author = message.author.display_name
    print(f'[{self.current_time}] Wiadomość: {author}: {content}')
    # TODO: RETRAIN TO NOT TRIGGER ON FIRST WORD (AUTHOR)
    # TO USE WHEN RETRAINED
    # content = f'{author}: {content}'
    await df_sendmessage(self, content, author, message)

async def df_sendmessage(self, content, author, message):
    # *Send request to the Dialogflow API
    session_client = dialogflow.SessionsClient(credentials=credentials)
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=(content), language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(session=session, query_input=query_input)
    json_response = MessageToJson(response)
    json_response = json.loads(json_response)
    self.console = self.bot.get_channel(728252426544742510)
    # *If available, execute the custom payload
    try:
        cCommands = json_response["queryResult"]["fulfillmentMessages"][1]["payload"]["cCommand"]
        pCommands = json_response["queryResult"]["fulfillmentMessages"][1]["payload"]["pCommand"]
        print(json_response["queryResult"]["fulfillmentMessages"][1]["payload"]["cCommand"])
        for cCommand in cCommands:
            print(f'[{self.current_time}] Wykonywanie komendy: {cCommand}')
            await self.console.send(cCommand)
            await asyncio.sleep(0.2)
        for pCommand in pCommands:
            exec(pCommand)
            await asyncio.sleep(0.2)
    except IndexError:
        pass
    print(f'[{self.current_time}] Odpowiedź: {json_response["queryResult"]["fulfillmentText"]}')

    # *Checks for annoying ass motherfuckers.
    await message.channel.send(json_response['queryResult']['fulfillmentText'])
    # TODO: NEEDS RETRAINING FOR <END OF CONVERSATION> TAG
    # if 'json_response['queryResult']['diagnosticInfo']['end_conversation']:
    #     self.namecheck = False
    # else:
    #     self.namecheck = True
    # await message.channel.send(json_response['queryResult']['fulfillmentText'])
def setup(bot):
    bot.add_cog(dialog(bot))