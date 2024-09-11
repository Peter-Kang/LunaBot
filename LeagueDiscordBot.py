import os
from dotenv import load_dotenv

import discord
from discord.ext import commands

from Services.LeagueServices.league import league
from DataAccess.LeagueDatabase import LeagueDatabase
from Services.DnDServices.DnDService import DnD

from Services.HALService.RaspberryPi.RaspberryPi import RPI

class LeagueDiscordBot(commands.Bot):


    def __init__(self):
        #member variables
        #Services
        self.db:LeagueDatabase = None
        self.LeagueService:league = None
        self.DnDService:DnD = None
        self.RPIService:RPI = None
        #Keys
        self.DISCORD_BOT_TOKEN:str= None

        #Populate
        load_dotenv()
        #api keys
        self.DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
        self.RIOT_API_KEY = os.getenv('RIOT_API_KEY')
        #discord bot info
        self.BOT_STATUS = os.getenv('BOT_STATUS')
        #sqlite database
        self.SQLITE3_PATH = os.getenv('SQLITE3_PATH')
        self.SQLITE3_DB_FILE = os.getenv('SQLITE3_DB_FILE')
                
        #league settings
        #services
        self.db:LeagueDatabase = LeagueDatabase(self.SQLITE3_PATH,self.SQLITE3_DB_FILE)
        self.LeagueService:league = league(self.RIOT_API_KEY, self.db)
        self.DnDService:DnD = DnD()

        #discord bot settings
        intents_LeagueDiscBot = discord.Intents.default()
        intents_LeagueDiscBot.members = True
        intents_LeagueDiscBot.message_content = True
        super().__init__(command_prefix="/",  case_insensitive=True,  intents=intents_LeagueDiscBot )

        #Check if we are on a Raspberry Pi
        self.RPIService:RPI = RPI()
        print(f'Is RPI {self.RPIService.is_RPI()}')

    async def on_ready(self):
        #can remove the init service
        for a_guild in self.guilds:
            print(f'{a_guild.id}, {a_guild.name} Connected')
        await self.load_extensions()
        #set the status for the bot
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=self.BOT_STATUS))#services

    async def load_extensions(self):
        #attach cogs
        for Filename in os.listdir('./CogCommands'):
            if Filename.endswith('.py'):
                await self.load_extension(f"CogCommands.{Filename[:-3]}")