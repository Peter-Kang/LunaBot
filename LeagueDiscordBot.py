import os
from dotenv import load_dotenv

import discord
from discord import app_commands
from discord.ext import commands


from Services.DiscordServices.discordInit import DiscordInit


class LeagueDiscordBot(commands.Bot):
    def __init__(self):
        load_dotenv()
        #api keys
        DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
        RIOT_API_KEY = os.getenv('RIOT_API_KEY')
        #discord bot info
        BOT_STATUS = os.getenv('BOT_STATUS')
        #sqlite database
        SQLITE3_PATH = os.getenv('SQLITE3_PATH')
        SQLITE3_DB_FILE = os.getenv('SQLITE3_DB_FILE')
                
        #discord bot settings
        intents_LeagueDiscBot = discord.Intents.default()
        intents_LeagueDiscBot.members = True
        intents_LeagueDiscBot.message_content = True

        #discord


    async def on_ready(self):
        for a_guild in self.bot.guilds:
            self.guilds.append(discord.Object(a_guild.id))
            print(f'{a_guild.id}, {a_guild.name} Connected')
        await self.bot.change_presence(activity=discord. Activity(type=discord.ActivityType.playing, name=self.status))
