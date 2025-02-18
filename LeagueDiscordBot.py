import os
from dotenv import load_dotenv
import re

import discord
from discord.ext import commands, tasks
from discord import scheduled_event

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
#On boot tasks, please try to keep this skinny, use Cron jobs if needed
    async def on_ready(self):
        #can remove the init service
        for a_guild in self.guilds:
            print(f'{a_guild.id}, {a_guild.name} Connected')
        await self.load_extensions()
        #set the status for the bot
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=self.BOT_STATUS))#services
        await self.refreshEventForumThreads.start()
#Scheduled Event Events
    async def on_scheduled_event_create(self, event:scheduled_event):
        try:
            eventChannel = discord.utils.get(self.get_guild(event.guild.id).channels, name="event-forums")
            if(isinstance(eventChannel, discord.ForumChannel)):
                #set embed image
                if event.cover_image != None:
                    embedToUse:discord.Embed = discord.Embed()
                    embedToUse.set_image(url=event.cover_image.url)
                    await eventChannel.create_thread(name = event.name, embed=embedToUse, content=event.url)
                else:
                    await eventChannel.create_thread(name = event.name, content=event.url)
            else:
                print("Could not find event-forums channel")
        except Exception as error:
            print(error)

    async def on_scheduled_event_update(self, before:scheduled_event, after:scheduled_event):
        try:
            eventChannel = discord.utils.get(self.get_guild(before.guild.id).channels, name="event-forums")
            if(isinstance(eventChannel, discord.ForumChannel) and (after.status == discord.EventStatus.completed) or (after.status == discord.EventStatus.ended)):
                for thread in eventChannel.threads:
                    #check if thread is archived 
                    if thread.archived == False and thread.locked == False:
                        start = [message async for message in thread.history(limit=1, oldest_first = True)]
                        if(len(start) > 0 and str(before.id) in start[0].content):
                            await thread.edit(name=thread.name, archived=True, locked=False, invitable= thread.invitable, auto_archive_duration=60, slowmode_delay=0, applied_tags=thread.applied_tags)
                            break
            else:
                print("Could not find event-forums channel")
        except Exception as error:
            print(error)

    async def on_scheduled_event_user_add(self, event:scheduled_event, user:discord.user):
        try:
            eventChannel = discord.utils.get(self.get_guild(event.guild.id).channels, name="event-forums")
            if(isinstance(eventChannel, discord.ForumChannel)):
                for thread in eventChannel.threads:
                    #check if thread is archived 
                    if thread.archived == False and thread.locked == False:
                        start = [message async for message in thread.history(limit=1, oldest_first = True)]
                        if(len(start) > 0 and str(event.id) in start[0].content):
                            await thread.add_user(user)
                            break

        except Exception as error:
            print(error)
#Cron Jobs
    @tasks.loop(hours=12)
    async def refreshEventForumThreads(self):
        try:
            for guild in self.guilds:
                eventChannel = discord.utils.get(self.get_guild(guild.id).channels, name="event-forums")
                if(isinstance(eventChannel, discord.ForumChannel)):
                    #get the scheduled event list
                    listOfEvents = await guild.fetch_scheduled_events()
                    setOfSchEventIDs = set()
                    for event in listOfEvents:
                        setOfSchEventIDs.add(int(event.id))
                    if(len(listOfEvents) != 0):
                        for thread in eventChannel.threads:
                            if thread.archived == False and thread.locked == False:
                                start = [message async for message in thread.history(limit=1, oldest_first = True)]
                                if(len(start) > 0):
                                    eventID = re.search('(\d+)(?!.*\d)',start[0].content)
                                    if eventID and int(eventID.group(0)) in setOfSchEventIDs:
                                        #make sure the event is alive
                                        await thread.edit(name=thread.name, archived=False, locked=False, invitable= thread.invitable, auto_archive_duration=60, slowmode_delay=0, applied_tags=thread.applied_tags)
                                        #refresh it
                                        await thread.edit(name=thread.name, archived=False, locked=False, invitable= thread.invitable, auto_archive_duration=10080, slowmode_delay=0, applied_tags=thread.applied_tags)
                                    else:
                                        print(f"EventID: {eventID} Not Found. Closing")
                                        #close the thread, event ended
                                        await thread.edit(name=thread.name, archived=True, locked=False, invitable= thread.invitable, auto_archive_duration=10080, slowmode_delay=0, applied_tags=thread.applied_tags)                        
        except Exception as error:
            print(error)
#Loading all Cogsjhgjhgjh
    async def load_extensions(self):
        #attach cogs
        for Filename in os.listdir('./CogCommands'):
            if Filename.endswith('.py'):
                await self.load_extension(f"CogCommands.{Filename[:-3]}")