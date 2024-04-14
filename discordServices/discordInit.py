import discord

class discordInit():

    def __init__(self, bot:discord.Client):
        self.bot = bot

    async def sync(self):
        for a_guild in self.bot.guilds:
            await self.bot.tree.sync(guild = a_guild)
            print(f'Tree of {a_guild.id} ,{a_guild.name}, has been sync')