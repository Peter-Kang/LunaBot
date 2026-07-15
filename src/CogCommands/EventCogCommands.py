import discord
from discord.ext import commands, tasks
from discord import scheduled_event
import re


class EventCogCommands(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot:commands.Bot = bot

    async def cog_load(self):
        self.refreshEventForumThreads.start()

    async def cog_unload(self):
        self.refreshEventForumThreads.cancel()


#Cron Jobs
    @tasks.loop(hours=12)
    async def refreshEventForumThreads(self):
        try:
            for guild in self.bot.guilds:
                eventChannel = discord.utils.get(self.bot.get_guild(guild.id).channels, name="event-forums")
                if(isinstance(eventChannel, discord.ForumChannel)):
                    #get the scheduled event list
                    listOfEvents = await guild.fetch_scheduled_events()
                    setOfSchEventIDs = set()
                    setOfNames = set()
                    for event in listOfEvents:
                        setOfSchEventIDs.add(int(event.id))
                        setOfNames.add(str(event.name))
                    if(len(listOfEvents) != 0):
                        print(f"List Of Events: {listOfEvents}")
                        for thread in eventChannel.threads:
                            if thread.archived == False and thread.locked == False:
                                start = [message async for message in thread.history(limit=1, oldest_first = True)]
                                if(len(start) > 0):
                                    eventID = re.search('(\d+)(?!.*\d)',start[0].content)
                                    if eventID and int(eventID.group(0)) in setOfSchEventIDs or thread.name in setOfNames:
                                        #make sure the event is alive
                                        await thread.edit(name=thread.name, archived=False, locked=False, invitable= thread.invitable, auto_archive_duration=60, slowmode_delay=0, applied_tags=thread.applied_tags)
                                        #refresh it
                                        await thread.edit(name=thread.name, archived=False, locked=False, invitable= thread.invitable, auto_archive_duration=10080, slowmode_delay=0, applied_tags=thread.applied_tags)
                                    else:
                                        print(f"Event Name: {event.name} EventID: {eventID}  Not Found. Closing")
                                        #close the thread, event ended
                                        await thread.edit(name=thread.name, archived=True, locked=False, invitable= thread.invitable, auto_archive_duration=10080, slowmode_delay=0, applied_tags=thread.applied_tags)                        
        except Exception as error:
            print(error)

#Scheduled Event Events
    async def on_scheduled_event_create(self, event:scheduled_event):
        try:
            eventChannel = discord.utils.get(self.bot.get_guild(event.guild.id).channels, name="event-forums")
            if(isinstance(eventChannel, discord.ForumChannel)):
                setOfNames = set();
                for thread in eventChannel.threads:
                    if thread.archived == False and thread.locked == False:
                        setOfNames.add(str(thread.name))
                if( not event.name in setOfNames ): #check if channel already exists
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
            eventChannel = discord.utils.get(self.bot.get_guild(before.guild.id).channels, name="event-forums")
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
            eventChannel = discord.utils.get(self.bot.get_guild(event.guild.id).channels, name="event-forums")
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

async def setup(bot:commands.Bot) ->None:
    await bot.add_cog(EventCogCommands(bot=bot))