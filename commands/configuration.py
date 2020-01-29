import dataset, requests, os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

USERS_DB = os.getenv("USERS_DB")

def setup(bot):
    bot.add_cog(Configuration(bot))

class Configuration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
        DATABASE = dataset.connect(USERS_DB)
        self.db = DATABASE["users"]

    def is_guild_owner(ctx): # useful for configuration commands.
        return ctx.message.author.id == ctx.guild.owner.id
    
    # The command that handles setting the prefix for a given server.
    @commands.command(name="set")
    async def fm_set(self, ctx, *args):
        usage = "usage: `set <username>`"

        if len(args) != 1:
            await ctx.send(usage)
            return
        
        # Check if a user exists on last.fm. We'll use status codes for this; don't want any dud usernames being added.

        user_check = requests.get(f"http://www.last.fm/user/{args[0]}").status_code

        if user_check == 404:
            await ctx.send("*Error: That user doesn't seem to exist. Perhaps you've mistyped your username?*")
            return
        
        elif user_check == 200:
            try:
                self.db.insert(dict(user_id=ctx.author.id, username=args[0]))
                await ctx.send(f"Your last.fm username has been successfully set to `{args[0]}`!")
            except:
                await ctx.send("Something went wrong! Feel free to submit an issue at https://github.com/theteamaker/bladee.")