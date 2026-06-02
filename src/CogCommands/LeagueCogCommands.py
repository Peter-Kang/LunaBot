import discord
from discord.ext import tasks, commands
from discord import app_commands
from discord import Embed

class LeagueCogCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.updateChampionList.start()

    @app_commands.command(name="random",  description="Gets a random Champion")
    async def random(self,interaction:discord.Interaction):
        result:Embed = self.bot.LeagueService.randomChampion()
        await interaction.response.send_message(embed=result)

    @app_commands.command(name="reg", description="registers the user and a Riot ID ")
    @app_commands.describe(riot = "A Riot ID (GameName#TagName ie: Peterchan#NA1)" )
    async def registerSummoner(self,interaction:discord.Interaction, riot:str = None):
        if(riot == None):
            await interaction.response.send_message("Please enter a Riot ID.")
        else:
            result:str = self.bot.LeagueService.register(str(interaction.user.id), riot)
            responseString:str = f"Couldn't add the Riot ID: {riot} \nPlease check use a Riot id ie Petechan#NA1"
            if result != "":
                    responseString = "Registered"
            await interaction.response.send_message(responseString)

    @app_commands.command(name="stats", description="gets the user's current stats")
    async def stats(self,interaction:discord.Interaction):
        userId = str(interaction.user.id)
        if(userId not in self.bot.LeagueService.userToSummonerPUUID):
            await interaction.response.send_message("You are not registered")
        else:   
            await interaction.response.defer()
            result:str = await self.bot.LeagueService.getUserStatus(userId)
            await interaction.followup.send(result) 

    @tasks.loop(minutes=15)
    async def updateChampionList(self):
        self.bot.LeagueService.UpdateChampionList()

async def setup(bot:commands.Bot) ->None:
    await bot.add_cog(LeagueCogCommands(bot=bot))