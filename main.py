#!/usr/bin/env python3.11
import discord
from discord.ext import commands


from LeagueDiscordBot import LeagueDiscordBot

bot = LeagueDiscordBot()

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

bot.run(bot.DISCORD_BOT_TOKEN)