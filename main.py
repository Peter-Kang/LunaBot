import os
from dotenv import load_dotenv

import discord
from discord import app_commands
from discord.ext import commands

from Services.DiscordServices.discordInit import DiscordInit
from Services.LeagueServices.league import league
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


bot = commands.Bot(
    command_prefix="/",  
    case_insensitive=True,  
  intents=intents_LeagueDiscBot 
)
#services
discordInitBot:DiscordInit = DiscordInit(bot, BOT_STATUS)

db:LeagueDatabase = LeagueDatabase(SQLITE3_PATH,SQLITE3_DB_FILE)
leagueStuff:league = league(RIOT_API_KEY, db)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send("That command wasn't found! Sorry :(")

@bot.command(name="sync")
@commands.guild_only()
async def sync(ctx:commands.context):
        #sync global
        ctx.bot.tree.copy_global_to(guild=ctx.guild)
        synced = await ctx.bot.tree.sync(guild=ctx.guild)
        print(f"Synced {len(synced)} commands for {ctx.guild}({ctx.guild.name})")

@bot.tree.command(name="random",  description="Gets a random Champion")
async def random(interaction:discord.Interaction):
        result:str = leagueStuff.randomChampion()
        await interaction.response.send_message(result)

@bot.tree.command(name="reg", description="registers the user and a Riot ID ")
@app_commands.describe(riot = "A Riot ID (GameName#TagName ie: Peterchan#NA1)" )
async def registerSummoner(interaction:discord.Interaction, riot:str = None):
        if(riot == None):
                await interaction.response.send_message("Please enter a Riot ID.")
        else:
                result:str = leagueStuff.register(str(interaction.user.id), riot)
                responseString:str = f"Couldn't add the Riot ID: {riot} \nPlease check use a Riot id ie Petechan#NA1"
                if result != "":
                        responseString = "Registered"
                await interaction.response.send_message(responseString)

@bot.tree.command(name="stats", description="gets the user's current stats")
async def stats(interaction:discord.Interaction):
        userId = str(interaction.user.id)
        if(userId not in leagueStuff.userToSummonerPUUID):
                await interaction.response.send_message("You are not registered")
        else:   
                await interaction.response.defer()
                result:str = await leagueStuff.getUserStatus(userId)
                await interaction.followup.send(result) 

@bot.event
async def on_ready():
        await discordInitBot.on_ready()
        print(f'{bot.user} has connected to Discord!')

bot.run(DISCORD_BOT_TOKEN)