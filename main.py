#!/usr/bin/env python3.11
import discord
from discord.ext import commands
from discord import scheduled_event

from LeagueDiscordBot import LeagueDiscordBot

bot = LeagueDiscordBot()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send("That command wasn't found! Sorry :(")

@bot.event
async def on_scheduled_event_create(event:scheduled_event):
    try:
        eventChannel = discord.utils.get(bot.get_guild(event.guild.id).channels, name="event-forums")
        if(isinstance(eventChannel, discord.ForumChannel)):
            await eventChannel.create_thread(name = event.name, content=event.url)
    except Exception as error:
        print(error)

@bot.event
async def on_scheduled_event_user_add(event:scheduled_event, user:discord.user):
    try:
        eventChannel = discord.utils.get(bot.get_guild(event.guild.id).channels, name="event-forums")
        if(isinstance(eventChannel, discord.ForumChannel)):
            for thread in eventChannel.threads:
                start = [message async for message in thread.history(limit=1, oldest_first = True)]
                if(len(start) > 0 and str(event.id) in start[0].content):
                    await thread.add_user(user)
                    break

    except Exception as error:
        print(error)
     
@bot.command(name="sync")
@commands.guild_only()
async def sync(ctx:commands.context):
        #sync global
        ctx.bot.tree.copy_global_to(guild=ctx.guild)
        synced = await ctx.bot.tree.sync(guild=ctx.guild)
        print(f"Synced {len(synced)} commands for {ctx.guild}({ctx.guild.name})")

bot.run(bot.DISCORD_BOT_TOKEN)