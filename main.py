import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discordServices.discordInit import discordInit
from leagueServices.league import league

load_dotenv()
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
RIOT_API_KEY = os.getenv('RIOT_API_KEY')

intents_LeagueDiscBot = discord.Intents.default()
intents_LeagueDiscBot.members = True
intents_LeagueDiscBot.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents_LeagueDiscBot)
discordInitBot = discordInit(bot)
leagueStuff = league(RIOT_API_KEY)

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
                await ctx.send(sumName)
        else:
                success:bool = leagueStuff.register(ctx.author.id, sumName)
                reponseString:str = "Couldn't add it"
                if success:
                        reponseString = "Registered"
                await ctx.send(reponseString)

@bot.command(name="stats", description="gets the user's current stats")
async def stats(ctx:commands.Context):
        if(not ctx.author.id in leagueStuff.UserSummonerData.userToSummonerPUUID):
                await ctx.send("You are not registered")
        else:   
                result:str = await leagueStuff.getUserStatus(ctx.author.id)
                await ctx.send(result) 

bot.run(DISCORD_BOT_TOKEN)