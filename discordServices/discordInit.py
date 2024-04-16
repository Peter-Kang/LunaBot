import discord

class discordInit():

    def __init__(self, bot:discord.Client, status:str):
        self.bot = bot
        self.status

    async def sync(self):
        for a_guild in self.bot.guilds:
            await self.bot.tree.sync(guild = a_guild)
            print(f'Tree of {a_guild.id} ,{a_guild.name}, has been sync')
        await self.bot.change_presence(activity=discord. Activity(type=discord.ActivityType.playing, name=self.status))