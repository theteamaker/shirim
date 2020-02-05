import requests, discord, dataset
from discord.ext import commands
from commands.configuration import return_fm, servers_db
from commands.fm import Scrobbles, embedify, fmyt
from commands.charts import get_chart
from commands.recent import recent_embed
from commands.profiles import charter, profiler

### A consistent command for "getting" other users' data. This will hopefully feel consistent.
### usage should be as follows: ::get <username/mention> <optional arguments, such as 'fm', 'weekly' etc>

def setup(bot):
    bot.add_cog(Get(bot))

class Get(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def get(self, ctx, *args):
        await ctx.trigger_typing()
        usage = "usage: `get <username/mention> <optional: chart_type chart_size -nc (no captions)>`"

        if len(args) == 0:
            await ctx.send(usage)
            return

        elif len(args) >= 1:
            appropriate_charts = ["weekly", "monthly", "3months", "6months", "yearly", "alltime"]
            appropriate_sizes = ["3x3", "4x4", "5x5", "2x6"]
            
            username = return_fm(args[0])
            
            # really hacky logic here to get things to parse correctly, i really wanna refactor this when I get the chance
            if username != 404 and username != 678:
                if len(args) == 1 or len(args) >= 2 and args[1] != "chart" and args[1] != "profile":
                    if len(args) >= 2:
                        if args[1] in appropriate_charts:
                            chart_type = args[1]
                            chart_size = "3x3" #default
                            captions = True
                            
                            if len(args) >= 3:
                                if args[2] == '-nc':
                                    captions = False
                                
                                elif args[2] in appropriate_sizes:
                                    chart_size = args[2]

                                    if len(args) >= 4:
                                        if args[3] == "-nc":
                                            captions = False
                                
                            chart = await get_chart(username, chart_type, size=chart_size, nc=captions)
                            await ctx.send(content=ctx.message.author.mention, file=discord.File(fp=chart,filename="chart.png"))
                            return
                        
                        elif args[1] == "recent":
                            await ctx.send(embed=recent_embed(username, ctx, get=True))
                            return

                        elif args[1] == "yt":
                            await ctx.send(fmyt(Scrobbles(username).recent_scrobble))
                            return
        
                    scrobbles = Scrobbles(username=username)
                    embed = await embedify(scrobbles, ctx)
                    msg = await ctx.send(embed=embed)

                    emojis = [':bigW:659616111414870026', ':bigL:659616123444133888']

                    reactions = False

                    if servers_db.find_one(server_id=ctx.guild.id, reactions=True) is not None:
                        reactions = True
                    
                    if reactions is True:
                        for emoji in emojis:
                            await msg.add_reaction(emoji)

            # look I understand that these if statements look like they came straight out of yandere simulator but they work
            elif username == 404 and len(args) == 1 or username == 404 and len(args) >= 2 and args[1] != "chart" and args[1] != "profile":
                await ctx.send("**Error:** That user doesn't seem to exist. Perhaps you've mistyped their username?")
                return
            
            elif username == 678 and len(args) == 1 or username == 678 and len(args) >= 2 and args[1] != "chart" and args[1] != "profile":
                await ctx.send(f"**Error:** That user doesn't seem to have set their last.fm username yet.")
                return
            
            if len(args) >= 2 and args[1] == "chart":
                try:
                    mention = ctx.message.mentions[0]
                except:
                    await ctx.send("usage: `get <mention> chart`")
                    return
                
                await charter(ctx, mention.id, get=True)
            
            elif len(args) >= 2 and args[1] == "profile":
                try:
                    mention = ctx.message.mentions[0]
                except:
                    await ctx.send("usage: `get <mention> profile`")
                    return
                    
                await profiler(ctx, ctx.message.mentions[0], get=True)