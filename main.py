'''
# MORTIMER VERSION 3.0 #
TODO:
    - SEPARATE DIALOG AND MONOLOGUE
    - MINECRAFT COMMANDS VIA BOT
DONE:
- AUTOMATED GIT PULL (needs implementation)
- CONFIG SYSTEM (needs creation file)
- NEW MESSAGE SYNTAX (needs retraining)
'''
import discord, json
from discord.ext import commands

with open('config.json', 'r') as j:
    config = json.loads(j.read())

token = config['token-discord']
# !DO NOT REMOVE!!!
intents = discord.Intents.default()  # All but the two privileged ones 
intents.members = True  # Subscribe to the Members intent
client = commands.Bot(command_prefix=config['command-prefix'],intents=intents)

# Change the "Playing" info to "Watching ['server-name']"
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=config['server-name']))
    print('Bot online!')

# Load in the cogs
client.load_extension('cogs.dialog')
client.load_extension('cogs.commands')
client.load_extension('cogs.monolog')
client.load_extension('cogs.misc')
client.run(token)