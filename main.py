import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discordServices.discordInit import discordInit
from leagueServices.league import league
from DatabaseLayer.LeagueDatabase import LeagueDatabase

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

bot = commands.Bot(command_prefix='/', intents=intents_LeagueDiscBot)
discordInitBot:discordInit = discordInit(bot,BOT_STATUS)
db:LeagueDatabase = LeagueDatabase(SQLITE3_PATH,SQLITE3_DB_FILE)
leagueStuff = league(RIOT_API_KEY, db)

@bot.event
async def on_ready():
        await discordInitBot.sync()
        print(f'{bot.user} has connected to Discord!')

@bot.command(name="random", description="Gets a random Champion")
async def random(ctx: commands.Context):
        result = leagueStuff.randomChampion()
        await ctx.send(result)

@bot.command(name="syncTree", description="syncs the command tree")
async def syncTree(ctx: commands.Context):
        await discordInitBot.sync()

@bot.command(name="reg", description="registers the user and a summoner name")
async def registerSummoner(ctx:commands.Context, sumName:str = None):
        if(sumName == None):
                await ctx.send("Please enter a summoner name")
        else:
                result:str = leagueStuff.register(str(ctx.author.id), sumName)
                responseString:str = "Couldn't add it"
                if result != "":
                        responseString = "Registered"
                await ctx.send(responseString)

@bot.command(name="stats", description="gets the user's current stats")
async def stats(ctx:commands.Context):
        userId = str(ctx.author.id)
        if(userId not in leagueStuff.userToSummonerPUUID):
                await ctx.send("You are not registered")
        else:   
                result:str = await leagueStuff.getUserStatus(userId)
                await ctx.send(result) 

bot.run(DISCORD_BOT_TOKEN)