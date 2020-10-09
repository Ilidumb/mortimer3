from discord.ext import commands
import re, json, asyncio, os, dialogflow, time
from main import config, client

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config['token-dialog']+'.json'

DIALOGFLOW_PROJECT_ID = config['token-dialog']
DIALOGFLOW_LANGUAGE_CODE = 'pl'
SESSION_ID = 'me'

class dialog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.t = time.localtime()
        self.current_time = time.strftime("%H:%M:%S", self.t)
        self.channels = config['watched-channels']
        self.namecheck = False
        
        
    @commands.Cog.listener()
    async def on_message(self ,message):
        if str(message.channel) in self.channels:
            if str(self.bot.user.id) in message.content.lower() or str(self.bot.user.name).lower() in message.content.lower():
                await clean_message(self, message)
            elif self.namecheck:
                await clean_message(self, message)
                
async def clean_message(self, message):
    if f'<@!{self.bot.user.id}>' in message.content:
        content = re.sub(f"<@!{self.bot.user.id}> ", "", message.content)
    elif f'<@{self.bot.user.id}>' in message.content:
        content = re.sub(f"<@{self.bot.user.id}> ", "", message.content)
    else:
        content = re.sub(f"{self.bot.user.name.lower()} ", "", message.content.lower())
    if message.author.bot:   
        if message.author.id == self.bot.user.id:
            return
        content = content.split(" » ", 1)
        author = content[0]
        content = content[1]
    else:
        author = message.author.display_name
    # NEEDS TO BE RETRAINED TO NOT TRIGGER ON FIRST WORD
    print(f'[{self.current_time}] Wiadomość: {author}: {content}')
    await apiai_sendmessage(self, content, author, message)

async def apiai_sendmessage(self, content, author, message):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=(f'{author}: {content}'), language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(session=session, query_input=query_input)
    print("Fulfillment text:", response.query_result.fulfillment_text)
    # await client.logout()

    # shit code, check for end_conversation, response json isnt valid
    if 'true' in str(response.query_result.diagnostic_info.fields):
        print('end convo')
        self.namecheck = False
    else:
        print('not end convo')
        self.namecheck = True
    await message.channel.send(response.query_result.fulfillment_text)
def setup(bot):
    bot.add_cog(dialog(bot))