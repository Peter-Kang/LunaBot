import discord
from discord.ext import commands
class DiscordInit():
    '''
    def __init__(self, bot:discord.Client, tree:discord.app_commands.tree,status:str):
        self.bot:discord.Client = bot
        self.tree:discord.app_commands.tree = tree
        self.status:str = status
        self.guilds:list =[]

    async def sync(self):
        for a_guild in self.bot.guilds:
            results = await self.tree.sync(guild = a_guild)
            count = len(results)
            self.guilds.append(discord.Object(a_guild.id))
            print(f'{count} Commands, tree of {a_guild.id}, {a_guild.name}, has been sync')

        await self.bot.change_presence(activity=discord. Activity(type=discord.ActivityType.playing, name=self.status))
'''

    def __init__(self, bot:commands.Bot, status:str):
        self.bot:commands.Bot = bot
        self.status:str = status
        self.guilds:list =[]

    async def on_ready(self):
        for a_guild in self.bot.guilds:
            self.guilds.append(discord.Object(a_guild.id))
            print(f'{a_guild.id}, {a_guild.name} Connected')
        await self.bot.change_presence(activity=discord. Activity(type=discord.ActivityType.playing, name=self.status))