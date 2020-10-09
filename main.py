'''
# MORTIMER VERSION 3.0 #
TODO:
    - AUTOMATED GIT PULL
    - SEPARATE DIALOG AND MONOLOGUE
    - CONFIG SYSTEM
    - NEW MESSAGE SYNTAX
    - MINECRAFT COMMANDS VIA BOT
'''
import discord, json
from discord.ext import commands

with open('config.json', 'r') as j:
    config = json.loads(j.read())
    # print(config['command-prefix'])

token = config['token-discord']
client = commands.Bot(command_prefix=config['command-prefix'])
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config['token-dialog']+'.json'

# Change the "Playing" info to "Watching Smoltoki"
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=config['server-name']))

client.load_extension('cogs.dialog')
try:
    client.run(token)
except (RuntimeError, RuntimeWarning) as e:
    pass