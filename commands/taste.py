import requests, matplotlib, discord, dataset
import numpy as np 
import matplotlib.pyplot as plt
from discord.ext import commands
from io import BytesIO
from commands.configuration import return_fm, users_db
from env import USERS_DB, LASTFM_API_KEY

class CommonArtists:
    def __init__(self, user1, user2):
        self.user1 = user1
        self.user2 = user2
    
    def get_common(self):
        limit = 100
        url = "http://ws.audioscrobbler.com/2.0/"
        headers = {"User-Agent": "shirim-skiffskiffles"}

        def get_artists(username): # gets a user's top artists, a function for the two users being compared
            shared_params = {
                "method": "user.getTopArtists",
                "api_key": LASTFM_API_KEY,
                "limit": limit,
                "format": "json",
                "user": username
            }

            return requests.get(url=url, headers=headers, params=shared_params).json()
        
        def gen_list(request):
            generated_list = []

            for artist in request["topartists"]["artist"]:
                generated_list.append({
                    "name": artist["name"],
                    "url": artist["url"],
                    "playcount": artist["playcount"]
                })

            return generated_list
        
        u1_request = get_artists(self.user1)
        u2_request = get_artists(self.user2)

        u1_list = gen_list(u1_request) # these are lists of all of their top artists
        u2_list = gen_list(u2_request)

        comparisons = []

        for x in range(len(u1_list)): # using length instead of the number 100 so that a user with under 100 listened artists can still run this cmd
            u1_artist = u1_list[x]
            for y in range(len(u2_list)): 
                u2_artist = u2_list[y]
                if u1_artist["url"] == u2_artist["url"]: # check by URL's, not names! Two different artists can have the same name.
                    a = int(u1_artist["playcount"]) # these a/b values do not clearly define what we are doing and are only to be used by the weight calculation
                    b = int(u2_artist["playcount"])
                    comparisons.append({
                        "name": u1_artist["name"],
                        self.user1: u1_artist["playcount"],
                        self.user2: u2_artist["playcount"],
                        "weight": a / b * (a + b) if a < b else b / a * (a + b)
                    })
        
        def takeWeight(elem):
            return elem["weight"]
        
        comparisons.sort(key=takeWeight, reverse=True)
        for _i in range(10, len(comparisons)):
            comparisons.remove(comparisons[10]) # Keep removing elements from the comparisons list until only ten remain. These will go on the graph.

        # the following just straight up pulls from a bar graph example I saw for matplotlib but I thought it looked nice

        labels = [i["name"] for i in comparisons]
        u1_scores = [int(i[self.user1]) for i in comparisons]
        u2_scores = [int(i[self.user2]) for i in comparisons]
        
        _fig, ax = plt.subplots()

        # Example data
        y_pos = np.arange(len(labels))

        ax.barh(y_pos, u1_scores, height=0.4, align='center', color="#B894FF", label=self.user1)
        ax.barh(y_pos + 0.4, u2_scores, height=0.4, align='center', color="#6743FF", label=self.user2)
        ax.set_yticks(np.arange(len(labels)))
        ax.set_yticklabels(labels)
        ax.invert_yaxis()  # labels read top-to-bottom
        plt.legend()

        for spine in plt.gca().spines.values():
            spine.set_visible(False)
        
        buf = BytesIO()
        plt.savefig(buf, bbox_inches="tight", format="png")
        buf.seek(0)
        return buf

class Taste(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def taste(self, ctx, *args):
        await ctx.trigger_typing()
        usage = "usage: `taste <username/mention>`"
        user = users_db.find_one(user_id=ctx.author.id)

        if len(args) == 0: # all the cute little checks to make sure everyone exists and is hangin' tight
            await ctx.send(usage)
            return
        if user is None:
            await ctx.send(f"**Error:** You haven't set a last.fm username yet! Use the `set` command to set your username.")
            return

        username = user["username"]
        compared_username = return_fm(args[0])
        if compared_username == 404:
            await ctx.send("**Error:** That user doesn't seem to exist. Perhaps you've mistyped their username?")
            return
        elif compared_username == 678:
            await ctx.send(f"**Error:** That user doesn't seem to have set their last.fm username yet.")        
        
        comparison = CommonArtists(username, compared_username)
        chart = comparison.get_common()

        await ctx.send(file=discord.File(fp=chart,filename="image.png"))

def setup(bot):
    bot.add_cog(Taste(bot))