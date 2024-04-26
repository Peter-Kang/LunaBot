import discord
from discord.ext import commands
from discord import app_commands

class DnDCogCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="roll", description="Rolls a dice")
    @app_commands.describe(dice = "(count of dice)d(sides of dice) ie: 2d8 is 2 eight sided dice." )
    async def roll(self,interaction:discord.Interaction, dice:str):
        result:str = self.bot.DnDService.roll(dice)
        await interaction.response.send_message(result)

async def setup(bot:commands.Bot) ->None:
    await bot.add_cog(DnDCogCommands(bot=bot))