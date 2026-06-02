import discord
from discord.ext import commands
from discord import app_commands
from Services.HALService.RaspberryPi.RaspberryPi import RPI

class DevicesCogCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="temperature", description="Gets the temperature and humidity")
    async def temperature(self,interaction:discord.Interaction):
        result:str = "Down"#self.bot.RPIService.GetTemperatureAndHumidity()
        await interaction.response.send_message(result)

async def setup(bot:commands.Bot) ->None:
    await bot.add_cog(DevicesCogCommands(bot=bot))