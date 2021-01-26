from discord.ext import commands
from discord import Guild, File
import asyncio, re, time, os, requests, pis

class mCogCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        t = time.localtime()
        self.current_time = time.strftime("%H:%M:%S", t)
        
    @commands.command(pass_context=True)
    async def ping(self, ctx):
        await ctx.send('Pong! 1')
    
    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def clear(self, ctx, amount=1):
        channel = ctx.message.channel
        messages = []
        async for message in channel.history(limit=amount):
            messages.append(message)
        await channel.delete_messages(messages)
        print(f'[{self.current_time}] Usunięto {amount} wiadomości.')
        deletemessage = await message.channel.send('Usunięto! :wink:')
        await asyncio.sleep(3)
        await deletemessage.delete()

    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def say(self, ctx, target_channel, *args):
        channel = self.bot.get_channel(int(target_channel[2:20]))
        await channel.send(" ".join(args[:]))
        print(f'[{self.current_time}] Ręcznie wysłano wiadomość: {" ".join(args[:])}.')
    
    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def shutdown(self,ctx):
        print("shutdown")
        try:
            await self.bot.logout()
        except:
            print("EnvironmentError")
            self.bot.clear()
    
    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def update(self,ctx):
        await ctx.channel.send('Restarting!')
        from subprocess import Popen
        Popen('git-pull.bat') 
        time.sleep(8)
        os.system("taskkill /f /im cmd.exe")
        os._exit(0)

    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def pis(self,ctx,*args):
        pis.generate_meme('./pis.jpg', bottom_text=" ".join(args[:]))
        await ctx.channel.send(file=File('meme-pis.jpg'))

    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def denizen(self,ctx,arg):
        denizen_source = ctx.message.attachments[0].url
        r = requests.get(denizen_source, allow_redirects=True)
        open(r'C:\MinecraftServer\plugins\Denizen\scripts\\'+arg+'.dsc', 'wb').write(r.content)
def setup(bot):
    bot.add_cog(mCogCommands(bot))