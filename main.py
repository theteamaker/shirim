import discord, os, dataset
from discord.ext import commands
from dotenv import load_dotenv

### Loading Environment Variables. ###
# Plans to add custom server-specific prefixes are in the works.

load_dotenv()
TOKEN = os.getenv("TOKEN")
DEFAULT_PREFIX = os.getenv("DEFAULT_PREFIX")

COGS = ['configuration', 'fm'] # upon adding a new file for a cog in the "commands" folder, add its file name here.

bot = commands.Bot(command_prefix=DEFAULT_PREFIX)

for cog in COGS:
    bot.load_extension(f"commands.{cog}")

@bot.event
async def on_ready():
    print(f"Bot has logged in as {bot.user}!")

bot.run(TOKEN)