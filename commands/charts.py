import requests, aiohttp, io, discord, dataset
from discord.ext import commands
from commands.configuration import general_error
from env import USERS_DB

users_db = dataset.connect(USERS_DB)["users"]

def setup(bot):
    bot.add_cog(Chart(bot))

async def get_chart(username, chart_type, size="3x3", nc=False):

    chart_types = { # different chart types that tap.music can generate.
        "weekly": "7day",
        "monthly": "1month",
        "3months": "3month",
        "6months": "6month",
        "yearly": "12month",
        "alltime": "overall"
    }

    selected_type = ""
    for arg, header in chart_types.items():
        if chart_type == arg:
            selected_type = header
            break
    
    headers = {
        "user": username,
        "size": size,
        "type": selected_type
    }

    link = f"http://tapmusic.net/collage.php?user={headers['user']}&type={headers['type']}&size={headers['size']}&caption=true"

    async with aiohttp.ClientSession() as session:
        async with session.get(link) as resp:
            var = await resp.read()
            return io.BytesIO(var)

class Chart(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def parse(self, context, chart_type, usage, *args):
        await context.trigger_typing()

        size = "3x3" # 3x3 by default
        appropriate_sizes = ["3x3", "4x4", "5x5", "2x6"]

        if len(args) >= 1:
            if args[0] in appropriate_sizes:
                size = args[0]
            else:
                pass
        
        user = users_db.find_one(user_id=context.author.id)
        if user is None:
            await context.send(f"**Error:** You haven't set a last.fm username yet! Use the `set` command to set your username.")
            return
        
        try:
            chart = await get_chart(user["username"], chart_type, size)
            await context.send(file=discord.File(fp=chart,filename="weekly.png"))
        except Exception as e:
            await context.send(general_error)
            raise e

    @commands.command()
    async def weekly(self, ctx, *args):
        usage = "usage: `weekly <optional: size (3x3, 4x4, 5x5, 2x6)>`"
        await self.parse(ctx, "weekly", usage, *args)

    @commands.command()
    async def monthly(self, ctx, *args):
        usage = "usage: `monthly <optional: size (3x3, 4x4, 5x5, 2x6)>`"
        await self.parse(ctx, "monthly", usage, *args)

    @commands.command(name="3months")
    async def quarterly(self, ctx, *args):
        usage = "usage: `3months <optional: size (3x3, 4x4, 5x5, 2x6)>`"
        await self.parse(ctx, "3months", usage, *args)
    
    @commands.command(name="6months")
    async def biannually(self, ctx, *args):
        usage = "usage: `6months <optional: size (3x3, 4x4, 5x5, 2x6)>`"
        await self.parse(ctx, "6months", usage, *args)
    
    @commands.command()
    async def yearly(self, ctx, *args):
        usage = "usage: `yearly <optional: size (3x3, 4x4, 5x5, 2x6)>`"
        await self.parse(ctx, "yearly", usage, *args)

    @commands.command()
    async def alltime(self, ctx, *args):
        usage = "usage: `alltime <optional: size (3x3, 4x4, 5x5, 2x6)>`"
        await self.parse(ctx, "alltime", usage, *args)