import dataset, requests, os
from discord.ext import commands
from env import USERS_DB, LASTFM_API_KEY

def setup(bot):
    bot.add_cog(Configuration(bot))

def user_check(username): # A check used in different files to see if a user exists.
    return requests.get(f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={username}&api_key={LASTFM_API_KEY}&format=json").status_code

class Configuration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
        DATABASE = dataset.connect(USERS_DB)
        self.db = DATABASE["users"]

    # The command that handles setting the prefix for a given server.
    @commands.command(name="set")
    async def fm_set(self, ctx, *args):
        await ctx.trigger_typing()
        usage = "usage: `set <username>`"

        if len(args) != 1:
            await ctx.send(usage)
            return
        
        # Check if a user exists on last.fm. We'll use status codes for this; don't want any dud usernames being added.

        check = user_check(args[0])

        if check == 404:
            await ctx.send("**Error:** That user doesn't seem to exist. Perhaps you've mistyped your username?")
            return
        
        elif check == 200:
            try:
                self.db.insert(dict(user_id=ctx.author.id, username=args[0]))
                await ctx.send(f"Your last.fm username has been successfully set to `{args[0]}`!")
            except:
                await ctx.send("Something went wrong! Feel free to submit an issue at https://github.com/theteamaker/shirim.")
