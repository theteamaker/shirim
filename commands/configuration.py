import dataset, requests, os, re
from discord.ext import commands
from env import USERS_DB, LASTFM_API_KEY

DATABASE = dataset.connect(USERS_DB)
db = DATABASE["users"]

def setup(bot):
    bot.add_cog(Configuration(bot))

def user_check(username): # A check used in different files to see if a user exists.
    return requests.get(f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={username}&api_key={LASTFM_API_KEY}&format=json").status_code

def return_fm(argument): 
    # A function designed to return a last.fm username based on whether a user uses a mention or a legitimate last.fm username.
    # I put this here because this could be a function very well used in other things, such as getting others' charts/fms, comparing tastes, etc.

    if re.search("^<@![0-9]*>$", argument) is not None: # checking if the user entered something that looks like a mention. honestly i have no idea how to use regex
        user_id = ""
        for i in re.findall(r"\d", argument):
            user_id += i
        
        searched_user = db.find_one(user_id=int(user_id))
        
        if searched_user != None:
            return searched_user["username"]
        else:
            return 678 # idk why i chose this error code, it's not reserved so whatever
    
    check = user_check(argument) # They entered an actual last.fm username! Let's check if it exists, and return it back to them if it does.

    if check == 404:
        return 404
    
    elif check == 200:
        return argument

### Commands designed for configuring user profiles. There will be a separate server configuration class later.

class Configuration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
                db.upsert(dict(user_id=ctx.author.id, username=args[0]), ["user_id"])
                await ctx.send(f"Your last.fm username has been successfully set to `{args[0]}`!")
            except:
                await ctx.send("Something went wrong! Feel free to submit an issue at https://github.com/theteamaker/shirim.")