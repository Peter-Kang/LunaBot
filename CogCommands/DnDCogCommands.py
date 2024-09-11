import discord
from discord.ext import commands
from discord import app_commands
from Services.DnDServices.Monsters.DnDMonsters import DnDEnvironments

class DnDCogCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="roll", description="Rolls a dice")
    @app_commands.describe(dice = "(count of dice)d(sides of dice)(optional +additions) ie: 2d8+3 is 2 eight sided dice plus 3. 4d6 is 4 six sided dice.")
    async def roll(self,interaction:discord.Interaction, dice:str):
        result:str = self.bot.DnDService.roll(dice)
        await interaction.response.send_message(result)

    def getEnvironmentChoices(self) ->app_commands.Choice[int]:
        result = []
        for env in DnDEnvironments:
            if( env != 0 and env<25 ):
                result.append(app_commands.Choice(name=env.name,value=env))

    @app_commands.command(name="encounter", description="Makes an encounter for a monster")
    @app_commands.describe(challenge = "The Challenge rating of the encounter", environment = "The environment")
    async def encounter(self,interaction:discord.Interaction, challenge:float=-1.0, environment:DnDEnvironments = DnDEnvironments.All):
        result:discord.Embed = self.bot.DnDService.Encounter(challenge,environment)
        await interaction.response.send_message(embed=result)

async def setup(bot:commands.Bot) ->None:
    await bot.add_cog(DnDCogCommands(bot=bot))