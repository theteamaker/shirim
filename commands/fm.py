import requests, os, dataset, discord, re
from discord.ext import commands
from env import LASTFM_API_KEY, USERS_DB, SERVERS_DB, YOUTUBE_API_KEY
from commands.configuration import user_check, return_fm, users_db, servers_db, FMUser

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
        headers = {"User-Agent": "shirim-skiffskiffles"}

        query_params = {
            "method": "user.getRecentTracks",
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

def fmyt(recent_scrobble):

    search_link = "https://www.googleapis.com/youtube/v3/search"
    scrobble = f"{recent_scrobble.name} - {recent_scrobble.artist}"
    query = scrobble.replace(" ", "+")
    query_params = {
        "key": YOUTUBE_API_KEY,
        "part": "snippet",
        "q": query,
        "maxResults": "1",
        "type": "video"
    }

    request = requests.get(url=search_link, params=query_params).json()
    
    try:
        return f"https://www.youtube.com/watch?v={request['items'][0]['id']['videoId']}"
    except:
        return f"**Error:** No search results were found for {scrobble}."

async def embedify(scrobbles, ctx): # A function for creating an embed.
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
    
    user = FMUser(scrobbles.user)
    
    if user.avatar != "":
        embed.set_author(
            name=scrobbles.user,
            url=scrobbles.user_url,
            icon_url=user.avatar
        )
    else:
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

    return embed

class FM(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def fm(self, ctx):
        await ctx.trigger_typing()
        user = users_db.find_one(user_id=ctx.author.id)

        if user is None:
            await ctx.send(f"**Error:** You haven't set a last.fm username yet! Use the `set` command to set your username.")
            return
        
        scrobbles = Scrobbles(username=user["username"])
        embed = await embedify(scrobbles, ctx)

        msg = await ctx.send(embed=embed)

        # for the reaction functionality you MUST specify emojis within your server in this list, or at least a server that the current instance of the bot is in.
        emojis = [':bigW:659616111414870026', ':bigL:659616123444133888']

        reactions = False

        if servers_db.find_one(server_id=ctx.guild.id, reactions=True) is not None:
            reactions = True
        
        if reactions is True:
            for emoji in emojis:
                await msg.add_reaction(emoji)
    
    @commands.command()
    async def fmyt(self, ctx):
        await ctx.trigger_typing()
        user = users_db.find_one(user_id=ctx.author.id)

        if user is None:
            await ctx.send(f"**Error:** You haven't set a last.fm username yet! Use the `set` command to set your username.")
            return
        
        scrobbles = Scrobbles(username=user["username"])

        await ctx.send(fmyt(scrobbles.recent_scrobble))

def setup(bot):
    bot.add_cog(FM(bot))