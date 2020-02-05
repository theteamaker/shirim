import discord, os, dataset
from discord.ext import commands
from dotenv import load_dotenv
from env import TOKEN
from commands.configuration import get_prefix

COGS = ['configuration', 'fm', 'taste', 'charts', 'get', 'recent', 'profiles'] # upon adding a new file for a cog in the "commands" folder, add its file name here.

bot = commands.Bot(command_prefix=get_prefix)

for cog in COGS:
    bot.load_extension(f"commands.{cog}")

@bot.event
async def on_ready():
    print(f"Bot has logged in as {bot.user}!")

@bot.event
async def on_command_error(ctx, error):
    ignorable_errors = [commands.errors.CheckFailure, commands.errors.CommandNotFound] # i don't need to know about these errors this is fine
    for ignorable in ignorable_errors:
        if isinstance(error, ignorable):
            return
    raise error

bot.run(TOKEN)