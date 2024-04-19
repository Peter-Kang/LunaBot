import os
from dotenv import load_dotenv
import discord
from discord import app_commands
from discord.ext import commands
from DiscordServices.DiscordInit import DiscordInit
from LeagueServices.league import league
from DataAccess.LeagueDatabase import LeagueDatabase

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
client:discord.Client = discord.Client(intents=intents_LeagueDiscBot)
tree:app_commands.tree = app_commands.CommandTree(client)

discordInitBot:DiscordInit = DiscordInit(client,tree,BOT_STATUS)
db:LeagueDatabase = LeagueDatabase(SQLITE3_PATH,SQLITE3_DB_FILE)
leagueStuff = league(RIOT_API_KEY, db)


@client.event
async def on_ready():
        await discordInitBot.sync()
        print(f'{client.user} has connected to Discord!')

@tree.command(name="random", description="Gets a random Champion")
async def random(ctx: commands.Context):
        result = leagueStuff.randomChampion()
        await ctx.send(result)

@tree.command(name="reg", description="registers the user and a summoner name")
async def registerSummoner(ctx:commands.Context, sumName:str = None):
        if(sumName == None):
                await ctx.send("Please enter a summoner name")
        else:
                result:str = leagueStuff.register(str(ctx.author.id), sumName)
                responseString:str = "Couldn't add it"
                if result != "":
                        responseString = "Registered"
                await ctx.send(responseString)

@tree.command(name="stats", description="gets the user's current stats")
async def stats(ctx:commands.Context):
        userId = str(ctx.author.id)
        if(userId not in leagueStuff.userToSummonerPUUID):
                await ctx.send("You are not registered")
        else:   
                result:str = await leagueStuff.getUserStatus(userId)
                await ctx.send(result) 

client.run(DISCORD_BOT_TOKEN)