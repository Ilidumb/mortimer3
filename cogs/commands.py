from discord.ext import commands
from discord import Guild, File
import asyncio, re, time, os, requests, pis
from os import listdir
from os.path import isfile, join

class mCogCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        t = time.localtime()
        self.current_time = time.strftime("%H:%M:%S", t)
        
    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def spam(self, ctx, target_channel, user, *args):
        print(ctx.message.content)
        channel = self.bot.get_channel(int(target_channel[2:20]))
        i = 1
        while i < 3:
            await channel.send(f"{user} "+" ".join(args[:]))
            i += 1
            await asyncio.sleep(0.5)
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
    async def denizen(self,ctx):
        denizen_source = ctx.message.attachments[0].url
        r = requests.get(denizen_source, allow_redirects=True)
        try:
            open(r'C:\MinecraftServer\plugins\Denizen\scripts\\'+ctx.message.attachments[0].filename, 'wb').write(r.content)
            open(r'C:\MinecraftServer\plugins\Denizen\backup\\'+ctx.message.attachments[0].filename, 'wb').write(r.content)
        except FileNotFoundError:
            await ctx.channel.send('Uh oh! Coś poszło nie tak!')

    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def lsdenizen(self,ctx):
        denizen_list = [f for f in listdir(r'C:\MinecraftServer\plugins\Denizen\scripts\\') if isfile(join(r'C:\MinecraftServer\plugins\Denizen\scripts\\', f))]
        lsoutput = ''
        for file in denizen_list:
            lsoutput = f'{lsoutput}`{file}`\n'
        await ctx.channel.send(lsoutput)

    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def getdenizen(self,ctx,arg):
        await ctx.channel.send(file=File(r'C:\MinecraftServer\plugins\Denizen\scripts\\'+arg+'.dsc'))

    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def deldenizen(self,ctx,arg):
        try:
            os.remove(r"C:\MinecraftServer\plugins\Denizen\scripts\\"+arg+".dsc")
        except FileNotFoundError:
            await ctx.channel.send('Uh oh! Ten plik nie istnieje! (nie musisz dawać .dsc w nazwie pliku)')

    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def schem(self,ctx):
        schem_source = ctx.message.attachments[0].url
        r = requests.get(schem_source, allow_redirects=True)
        open(r'C:\MinecraftServer\plugins\WorldEdit\schematics\\'+ctx.message.attachments[0].filename, 'wb').write(r.content)

    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def insult(self,ctx,user,target_channel):
        insults = """ty świński ryju, ty świński ogonie, ty świńska nóżko, ty golonko, ty fałdo, ty grubasie, ty pyzo, ty klucho, ty kicho, ty pulpecie, ty żłobie, ty gnomie, ty glisto, ty cetyńcu, ty zarazo pełzakowa, ty gadzie, ty jadzie, ty ospo, dyfteroidzie, ty pasożycie, ty trutniu, ty trądzie, ty swądzie, ty hieno, ty szakalu, ty kanalio, ty katakumbo, ty hekatombo, ty przykry typie, ty koszmarku, ty bufonie, ty farmazonie, ty kameleonie, ty chorągiewko na dachu, ty taki nie taki, ty ni w pięć ni w dziewięć ni w dziewiętnaście, ty smutasie, ty jaglico, ty zaćmo, ty kaprawe oczko, ty zezowate oczko, ty kapusiu, ty wiraszko, ty ślipku, ty szpiclu, ty hyclu, ty przykry typie, ty kicie, ty kleju, ty gumozo, ty gutaperko, ty kalafonio, ty wazelino, ty gliceryno, ty lokaju, ty lizusie, ty smoczku, ty klakierze, ty pozerze, ty picerze, ty picusiu, ty lalusiu, ty kabotynie, ty luju pasiaty, ty kowboju na garbatym koniu, ty klocu, ty młocie, ty piło, ty szprycho, ty graco, ty ruro nieprzeczyszczona, ty zadro, ty drapaku, ty drucie, ty draniu, ty przykry typie, ty kapitalisto, ty neokolonialisto, ty burżuju rumiany,"""
        insult_list = insults.split(', ')
        channel = self.bot.get_channel(int(target_channel[2:20]))
        for insult in insult_list:
            await channel.send(f'{user}, {insult}')
            await asyncio.sleep(0.5)

def setup(bot):
    bot.add_cog(mCogCommands(bot))