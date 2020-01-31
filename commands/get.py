import requests, discord, dataset
from discord.ext import commands
from commands.configuration import return_fm
from commands.fm import Scrobbles, embedify

### A consistent command for "getting" other users' data. This will hopefully feel consistent.
### usage should be as follows: ::get <username/mention> <optional arguments, such as 'fm', 'weekly' etc>

class Get(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def get(self, ctx, *args):
        await ctx.trigger_typing()
        usage = "usage: `get <username/mention>`"

        if len(args) == 0:
            await ctx.send(usage)
            return
        
        username = return_fm(args[0])

        if username == 404:
            await ctx.send("**Error:** That user doesn't seem to exist. Perhaps you've mistyped their username?")
            return
        
        elif username == 678:
            await ctx.send(f"**Error:** That user doesn't seem to have set their last.fm username yet.")

        scrobbles = Scrobbles(username=username)
        embed = await embedify(scrobbles, ctx)

        await ctx.send(embed=embed)
        return