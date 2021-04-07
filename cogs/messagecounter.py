import time, json
from discord.ext import commands, tasks
from main import config

class MessageCounter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channels = config['watched-channels']
        self.act = 0

    @commands.Cog.listener()
    async def on_ready(self):
        self.autosave_activity.start()

    # * Message Counter, if a player sent a message in minecraft, it gets counted
    @commands.Cog.listener()
    async def on_message(self ,message):
        if str(message.channel) == self.channels[0] and message.author.id != self.bot.user.id:
            self.act += 1

    # * Count save loop, runs every 30 minutes
    @tasks.loop(minutes=30)
    async def autosave_activity(self):
        save_activity(self)
    
    # * Force save messagecount
    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def force_save_activity(self, ctx):
        save_activity(self)

    # * Show todays messagecount
    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def activity_today(self, ctx):
        with open('messagecount.json') as messagecount_json:
            data = json.load(messagecount_json)
            await ctx.channel.send(f'Ilość wiadomości dzisiaj: {data[today()]}')
    
    # * Show total messagecount
    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def activity_total(self, ctx):
        with open('messagecount.json') as messagecount_json:
            data = json.load(messagecount_json)
            await ctx.channel.send(f'Ilość wszystkich wiadomości: {data["total"]}')

    # * Show average messagecount
    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def activity_average(self, ctx):
        with open('messagecount.json') as messagecount_json:
            data = json.load(messagecount_json)
            await ctx.channel.send(f'Średnia ilość wiadomości: {round(data["total"] / (len(data)-1))}')

def save_activity(self):
    with open('messagecount.json') as messagecount_json:
        data = json.load(messagecount_json)
        try:
            data[today()] += self.act
        except KeyError:
            data.update({today(): self.act})
        data["total"] += self.act
        self.act = 0
    # Save the messagecount, indent = 4 formats the file to be readable by humans
    with open('messagecount.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)

def today():
    return time.strftime('%m-%d')

def setup(bot):
    bot.add_cog(MessageCounter(bot))