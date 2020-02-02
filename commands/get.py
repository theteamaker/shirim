import requests, discord, dataset
from discord.ext import commands
from commands.configuration import return_fm, servers_db
from commands.fm import Scrobbles, embedify
from commands.charts import get_chart

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

            if username == 404:
                await ctx.send("**Error:** That user doesn't seem to exist. Perhaps you've mistyped their username?")
                return
            
            elif username == 678:
                await ctx.send(f"**Error:** That user doesn't seem to have set their last.fm username yet.")
            
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