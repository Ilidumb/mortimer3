from discord.ext import commands

class mCogMisc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.send('Żeby rozmawiać na serwerze, musisz podać swój nick z minecrafta w #sito. Bez podania nicku nie możesz rozmawiać. Zrób to teraz. Albo wynocha.')

    @commands.Cog.listener()
    async def on_message(self ,message):
        if str(message.author.display_name) == 'certyq' and message.channel != 'certyq':
            if any(banned_url in message.content for banned_url in ["https://www.youtube.com/","https://youtu.be/","https://vm.tiktok.com","https://www.tiktok.com/", ".gif", "htpps://tenor.com"]):
                await message.delete()

def setup(bot):
    bot.add_cog(mCogMisc(bot))