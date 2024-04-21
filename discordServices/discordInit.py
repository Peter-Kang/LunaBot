import discord
from discord.ext import commands
class DiscordInit():
    def __init__(self, bot:commands.Bot, status:str):
        self.bot:commands.Bot = bot
        self.status:str = status
        self.guilds:list =[]

    async def on_ready(self):
        for a_guild in self.bot.guilds:
            self.guilds.append(discord.Object(a_guild.id))
            print(f'{a_guild.id}, {a_guild.name} Connected')
        await self.bot.change_presence(activity=discord. Activity(type=discord.ActivityType.playing, name=self.status))