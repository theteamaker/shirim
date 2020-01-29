import requests, os, dataset, discord, re
from discord.ext import commands
from env import LASTFM_API_KEY, USERS_DB
from commands.configuration import user_check

USERS_DB = dataset.connect(USERS_DB)
db = USERS_DB["users"]

class Scrobble:
    def __init__(self, scrobble):
        self.name = scrobble["name"]
        self.artist = scrobble["artist"]["#text"]
        self.album = scrobble["album"]["#text"]
        self.image = scrobble["image"][3]["#text"]
        self.url = scrobble["url"]

class Scrobbles:
    def __init__(self, username, limit=2):
        self.username = username
        self.limit = limit

        # Parameters/settings for the JSON link we'll use to grab data.
        headers = {"User-Agent": "echo-skiffskiffles"}

        query_params = {
            "method": "user.getrecenttracks",
            "api_key": LASTFM_API_KEY,
            "limit": self.limit,
            "user": self.username,
            "format": "json",
        }

        scrobble_url = "http://ws.audioscrobbler.com/2.0/"
        self.scrobbles = requests.get(url=scrobble_url, headers=headers, params=query_params).json()

        self.user = self.scrobbles["recenttracks"]["@attr"]["user"]
        self.user_url = f"https://last.fm/user/{self.user}"

        try: # try/catch blocks here are implemented in the rare case that someone doesn't have any scrobbles.
            self.recent_scrobble = Scrobble(self.scrobbles["recenttracks"]["track"][0])
        except:
            return
        
        try:
            self.previous_scrobble = Scrobble(self.scrobbles["recenttracks"]["track"][1])
        except:
            return

class FM(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def embedify(self, scrobbles, ctx): # A function for creating an embed.
        recent = scrobbles.recent_scrobble
        previous = scrobbles.previous_scrobble

        if ctx.author.color == "#000000":
            color = "#ffffff"
        else:
            color = ctx.author.color

        try: # put in a try/catch block to catch if anyone hasn't scrobbled anything yet.
            embed = discord.Embed(
                title=recent.artist,
                url=recent.url,
                description=f"{recent.name} [{recent.album}]",
                color=color # i thought this would be cute
            )
        
        except Exception as e:
            await ctx.send("**Huh!** You haven't seemed to have scrobbled anything yet!")
            raise e
            return

        embed.set_author(
            name=scrobbles.user,
            url=scrobbles.user_url,
            icon_url=ctx.message.author.avatar_url,
        )

        embed.set_thumbnail(url=recent.image)

        try: # if someone really hasn't had a previous scrobble, then just ignore the footer.
            embed.set_footer(
                text=f"Previous: {previous.artist} - {previous.name}",
                icon_url=previous.image,
            )
        except Exception as e:
            raise e
            pass

        return embed

    @commands.command()
    async def fm(self, ctx):
        await ctx.trigger_typing()
        user = db.find_one(user_id=ctx.author.id)
        
        if user is None:
            await ctx.send(f"**Error:** You haven't set a last.fm username yet! Use the `set` command to set your username.")
            return
        
        scrobbles = Scrobbles(username=user["username"])
        embed = await self.embedify(scrobbles, ctx)

        await ctx.send(embed=embed)
    
    @commands.command()
    async def get(self, ctx, *args):
        await ctx.trigger_typing()
        usage = "usage: `set <username>`"

        if len(args) == 0:
            await ctx.send(usage)
            return
        
        if re.search("^<@![0-9]*>$", args[0]) is not None: # checking if the user entered something that looks like a mention. honestly i have no idea how to use regex
            user_id = ""
            for i in re.findall("\d", args[0]):
                user_id += i
            
            user = db.find_one(user_id=int(user_id))

            if user is None:
                await ctx.send("**Error:** The user you specified hasn't set their last.fm account.")
                return
            
            scrobbles = Scrobbles(username=user["username"])
            embed = await self.embedify(scrobbles, ctx)

            await ctx.send(embed=embed)
            return

        ### Here, we'll do a case in which the person specified a last.fm username instead of mentioning a Discord user.

        check = user_check(args[0])

        if check == 404:
            await ctx.send("**Error:** The last.fm user you specified doesn't seem to exist.")
        
        elif check == 200:
            scrobbles = Scrobbles(username=args[0])
            embed = await self.embedify(scrobbles, ctx)

            await ctx.send(embed=embed)
            return

def setup(bot):
    bot.add_cog(FM(bot))