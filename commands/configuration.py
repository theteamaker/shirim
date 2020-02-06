import dataset, requests, os, re
from discord.ext import commands
from env import USERS_DB, SERVERS_DB, LASTFM_API_KEY

users_db = dataset.connect(USERS_DB)["users"]
servers_db = dataset.connect(SERVERS_DB)["servers"]

DEFAULT_PREFIX = "!"
general_error = "Something went wrong! Feel free to submit an issue at https://github.com/theteamaker/shirim."

def setup(bot):
    bot.add_cog(Configuration(bot))

def get_prefix(bot, message):
    server = servers_db.find_one(server_id=message.guild.id)

    if server != None:
        try:
            if type(server["prefix"]) is str:
                return server["prefix"]
        except:
            pass
    
    return DEFAULT_PREFIX

class FMUser:
    def __init__(self, username):
        self.username = username

        headers = {"User-Agent": "shirim-skiffskiffles"}
        query_params = {
            "method": "user.getInfo",
            "api_key": LASTFM_API_KEY,
            "user": username,
            "format": "json"}
        
        url = "http://ws.audioscrobbler.com/2.0/"
        user = requests.get(url=url, headers=headers, params=query_params).json()

        self.avatar = user["user"]["image"][3]["#text"].replace(".png", ".gif")
        self.playcount = user["user"]["playcount"]

def is_guild_owner():
    def predicate(ctx):
        if ctx.guild is not None:
            if ctx.guild.owner_id == ctx.author.id:
                return True
            elif ctx.author.id == ctx.bot.owner_id:
                return True
            else:
                return False
        else:
            return False
    return commands.check(predicate)

def user_check(username): # A check used in different files to see if a user exists.
    return requests.get(f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={username}&api_key={LASTFM_API_KEY}&format=json").status_code

def return_fm(argument): 
    # A function designed to return a last.fm username based on whether a user uses a mention or a legitimate last.fm username.
    # I put this here because this could be a function very well used in other things, such as getting others' charts/fms, comparing tastes, etc.

    if re.search(r"^(<@)(\!)*([0-9])+", argument) != None: # checking if the user entered something that looks like a mention. honestly i have no idea how to use regex
        user_id = ""
        for i in re.findall(r"\d", argument):
            user_id += i
        
        searched_user = users_db.find_one(user_id=int(user_id))
        
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
                users_db.upsert(dict(user_id=ctx.author.id, username=args[0]), ["user_id"])
                await ctx.send(f"Your last.fm username has been successfully set to `{args[0]}`!")
            except:
                await ctx.send(general_error)
    
    @commands.command()
    async def set_prefix(self, ctx, *args):
        await ctx.trigger_typing()
        usage = "usage: `set_prefix <prefix>`"

        if len(args) != 1:
            await ctx.send(usage)
            return
        
        if re.match(r"^.{,3}$", args[0]) is None:
            await ctx.send("**Error:** The specified prefix for this bot must be *at most* 3 characters, and contain no spaces.")
            return
        
        try:
            servers_db.upsert(dict(server_id=int(ctx.guild.id), prefix=args[0]), ["server_id"])
            await ctx.send(f"The bot's prefix for this server has been successfully set to `{args[0]}`!")
        except:
            await ctx.send(general_error)
    
    @commands.command()
    @is_guild_owner()
    async def set_reactions(self, ctx, *args):
        await ctx.trigger_typing()
        usage = "usage: `reactions on | off`"

        if len(args) == 0:
            await ctx.send(usage)
            return
        
        if args[0] != "on" and args[0] != "off":
            await ctx.send(usage)
        
        if args[0].lower() == "on":
            try:
                servers_db.upsert(dict(server_id=ctx.guild.id, reactions=True), ["server_id"])
                await ctx.send("Reactions have now been turned on for this server.")
            except:
                await ctx.send(general_error)
        
        if args[0].lower() == "off":
            try:
                servers_db.upsert(dict(server_id=ctx.guild.id, reactions=False), ["server_id"])
                await ctx.send("Reactions have now been turned off for this server.")
            except:
                await ctx.send(general_error)