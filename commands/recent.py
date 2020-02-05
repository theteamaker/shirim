import discord, dataset, requests
from discord.ext import commands
from commands.fm import Scrobbles, Scrobble
from commands.configuration import return_fm, users_db, FMUser
from env import LASTFM_API_KEY

def setup(bot):
    bot.add_cog(Recent(bot))

def recent_embed(username, ctx, get=False):
    limit = 10
    scrobbler = Scrobbles(username, limit=limit)
    scrobbles = scrobbler.scrobbles

    scrobbles_list = [] # where all the scrobbles get added to

    for i in range(limit):
        scrobble = Scrobble(scrobbles["recenttracks"]["track"][i])
        scrobbles_list.append(str(f"**{i+1}**. [{scrobble.artist} - {scrobble.name}]({scrobble.url})"))

    content = ""
    for element in scrobbles_list:
        content += f"{element}\n"
    
    if ctx.author.color == "#000000":
        color = "#ffffff"
    else:
        color = ctx.author.color
    
    # parsing the username for proper grammar lol
    parsed_username = f"{scrobbler.username}'s"

    if scrobbler.username.endswith("s"):
        parsed_username = f"{scrobbler.username}'"

    embed = discord.Embed(
    title=f"{parsed_username} Recent Scrobbles",
    description=content,
    color=color
    )

    user = FMUser(username)

    if user.avatar != "":
        try:
            embed.set_thumbnail(url=user.avatar)
        except:
            pass

    embed.set_author(
        name=f"last.fm",
        icon_url="https://secure.last.fm/static/images/lastfm_avatar_twitter.66cd2c48ce03.png",
        url=scrobbler.user_url
    )

    embed.set_footer(
        text="Feature in beta testing. May break in odd places." # my silly little scapegoat for my bad coding
    )

    return embed

class Recent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def recent(self, ctx):
        await ctx.trigger_typing()
        _usage = "usage: `last <number, 0-100>`"
        
        user = users_db.find_one(user_id=ctx.author.id)

        if user is None:
            await ctx.send(f"**Error:** You haven't set a last.fm username yet! Use the `set` command to set your username.")
            return
        
        await ctx.send(embed=recent_embed(user["username"], ctx))