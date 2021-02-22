from discord.ext import commands
from discord import Guild, File
import asyncio, time, os, requests, pis
from os import listdir
from os.path import isfile, join

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
    
    # * Update command, mega janky (it works though)
    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def update(self,ctx):
        await ctx.channel.send('Restarting!')
        # Run git pull and restart
        from subprocess import Popen
        Popen('git-pull.bat') 
        # Stop the current window non-async, giving git pull enough time to run (might fail in case of a big pull... oh well.)
        time.sleep(8)
        # Kill the current bot terminal
        os.system("taskkill /f /im cmd.exe")
        # If that fails, close the python terminal (the cmd window remains up)
        os._exit(0)

    # * TVPiS Generator
    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def pis(self,ctx,*args):
        pis.generate_meme('./pis.jpg', bottom_text=" ".join(args[:]))
        await ctx.channel.send(file=File('meme-pis.jpg'))
        print(f'[{self.current_time}] Wygenerowano pasek TVPiS o wartości: {" ".join(args[:])}.')

    # * Upload Denizen script
    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def denizen(self,ctx):
        try:
            denizen_source = ctx.message.attachments[0].url
        except IndexError:
            pass
        r = requests.get(denizen_source, allow_redirects=True)
        try:
            open(r'C:\MinecraftServer\plugins\Denizen\scripts\\'+ctx.message.attachments[0].filename, 'wb').write(r.content)
            # Backup scripts
            open(r'C:\MinecraftServer\plugins\Denizen\backup\\'+ctx.message.attachments[0].filename, 'wb').write(r.content)
            await ctx.channel.send(f'Uploading {ctx.message.attachments[0].filename}!')
            print(f'[{self.current_time}] Wgrano skrypt denizen o nazwie: {ctx.message.attachments[0].filename}')
        except FileNotFoundError:
            await ctx.channel.send('Uh oh! Coś poszło nie tak!')
            print(f'[{self.current_time}] Błąd przy wgrywaniu skryptu denizen o nazwie: {ctx.message.attachments[0].filename}')

    # * List all Denizen scripts
    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def lsdenizen(self,ctx):
        denizen_list = [f for f in listdir(r'C:\MinecraftServer\plugins\Denizen\scripts\\') if isfile(join(r'C:\MinecraftServer\plugins\Denizen\scripts\\', f))]
        lsoutput = ''
        # Loop though the list, for postion in list add position + newline
        for file in denizen_list:
            lsoutput = f'{lsoutput}`{file}`\n'
        await ctx.channel.send(lsoutput)
        print(f'[{self.current_time}] Podano listę skryptów denizen.')

    # * Download Denizen script
    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def getdenizen(self,ctx,arg):
        await ctx.channel.send(file=File(r'C:\MinecraftServer\plugins\Denizen\scripts\\'+arg+'.dsc'))
        print(f'[{self.current_time}] Wysłano skrypt denizen o nazwie: {arg}')

    # * Delete Denizen script
    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def deldenizen(self,ctx,arg):
        try:
            os.remove(r"C:\MinecraftServer\plugins\Denizen\scripts\\"+arg+".dsc")
            await ctx.channel.send(f'Removing {arg}!')
            print(f'[{self.current_time}] Usunięto skrypt denizen o nazwie: {arg}')
        except FileNotFoundError:
            await ctx.channel.send('Uh oh! Ten plik nie istnieje! (nie musisz dawać .dsc w nazwie pliku)')
            print(f'[{self.current_time}] Błąd podczas usuwania skrypt denizen o nazwie: {arg}')
            
    # * Upload schematic
    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def schem(self,ctx):
        schem_source = ctx.message.attachments[0].url
        r = requests.get(schem_source, allow_redirects=True)
        try:
            ctx.channel.send(f'Uploading {ctx.message.attachments[0].filename}')
            open(r'C:\MinecraftServer\plugins\WorldEdit\schematics\\'+ctx.message.attachments[0].filename, 'wb').write(r.content)
            print(f'[{self.current_time}] Wgrano schematic o nazwie: {ctx.message.attachments[0].filename}')
        except FileNotFoundError:
            ctx.channel.send('Uh oh! Coś poszło nie tak!')
            print(f'[{self.current_time}] Błąd podczas wgrywania schematic o nazwie: {ctx.message.attachments[0].filename}')

def setup(bot):
    bot.add_cog(mCogCommands(bot))