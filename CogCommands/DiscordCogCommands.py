import discord
from discord.ext import commands
from discord import app_commands

class DiscordCogCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def CreateChannelFromEvent(self):
        print("")
        

async def setup(bot:commands.Bot) ->None:
    await bot.add_cog(DiscordCogCommands(bot=bot))