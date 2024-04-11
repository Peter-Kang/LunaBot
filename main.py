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

bot.run(DISCORD_BOT_TOKEN)