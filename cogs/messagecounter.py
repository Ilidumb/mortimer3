import time, json
from discord.ext import commands, tasks
from main import config

class mCogMessageCounter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channels = config['watched-channels']
        self.messagecount = 0
        self.save_messagecount.start()

    # * Message Counter, if a player sent a message in minecraft, it gets counted
    @commands.Cog.listener()
    async def on_message(self ,message):
        if ' » ' in message.content and str(message.channel) in self.channels and message.author.bot and message.author.id != self.bot.user.id:
            self.messagecount += 1

    # * Count save loop, runs every 30 minutes
    @tasks.loop(minutes=30)
    async def save_messagecount(self):
        saveactivity(self)
    
    # * Force save messagecount
    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def fsaveactivity(self, ctx):
        saveactivity(self)
        await ctx.channel.send('Zapisano!')
        
    # * Show todays messagecount
    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def activitytoday(self, ctx):
        with open('messagecount.json') as messagecount_json:
            data = json.load(messagecount_json)
            await ctx.channel.send(f'Ilość wiadomości dzisiaj: {data[today()]}')
    
    # * Show total messagecount
    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def activitytotal(self, ctx):
        with open('messagecount.json') as messagecount_json:
            data = json.load(messagecount_json)
            await ctx.channel.send(f'Ilość wszystkich wiadomości: {data["total"]}')

    # * Show average messagecount
    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def activityaverage(self, ctx):
        with open('messagecount.json') as messagecount_json:
            data = json.load(messagecount_json)
            await ctx.channel.send(f'Średnia ilość wiadomości: {round(data["total"] / (len(data)-1))}')

def saveactivity(self):
    with open('messagecount.json') as messagecount_json:
        data = json.load(messagecount_json)
        try:
            # Update todays messagecount
            data[today()] += self.messagecount
        # If no data from that day:
        except KeyError:
            # Create new key with the current messagecount
            data.update({today(): self.messagecount})
        # Update the total messagecount
        data["total"] += self.messagecount
        # Reset the messagecount
        self.messagecount = 0
    # Save the messagecount, indent = 4 formats the file to be readable by humans
    with open('messagecount.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)

def today():
    return time.strftime('%m-%d')

def setup(bot):
    bot.add_cog(mCogMessageCounter(bot))