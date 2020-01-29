import requests, os, dataset, discord
from discord.ext import commands
from env import LASTFM_API_KEY, USERS_DB

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
    
    @commands.command()
    async def fm(self, ctx):
        user = db.find_one(user_id=ctx.author.id)
        
        if user is None:
            await ctx.send(f"*You haven't set a last.fm username yet! Use the `set` command to set your username.*")
            return

        scrobbles = Scrobbles(username=user["username"])
        recent = scrobbles.recent_scrobble
        previous = scrobbles.previous_scrobble

        # Embed information/format.

        def color(color):
            if color == "#000000":
                return "#ffffff"
            else:
                return color

        try: # put in a try/catch block to catch if anyone hasn't scrobbled anything yet.
            embed = discord.Embed(
                title=recent.artist,
                url=recent.url,
                description=f"{recent.name} [{recent.album}]",
                color=color(ctx.author.color) # i thought this would be cute
            )
        
        except Exception as e:
            await ctx.send("*You haven't seemed to have scrobbled anything yet!*")
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
            pass
        
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(FM(bot))
