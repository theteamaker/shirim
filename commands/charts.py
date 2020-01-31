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

    link = f"http://tapmusic.net/collage.php?user={headers['user']}&type={headers['type']}&size={headers['size']}"

    if nc == True:
        link += "&caption=true"

    async with aiohttp.ClientSession() as session:
        async with session.get(link) as resp:
            var = await resp.read()
            return io.BytesIO(var)

async def parse(context, chart_type, usage, *args, get=False):
    await context.trigger_typing()

    size = "3x3" # 3x3 by default
    appropriate_sizes = ["3x3", "4x4", "5x5", "2x6"]
    captions = True

    if len(args) >= 1:
        if args[0] in appropriate_sizes:
            size = args[0]
            if args[1] == "-nc":
                captions = False

        elif args[0] == "-nc": # no captions flag
            captions = False
        
        else:
            pass
    
    user = users_db.find_one(user_id=context.author.id)
    if user is None:
        await context.send(f"**Error:** You haven't set a last.fm username yet! Use the `set` command to set your username.")
        return
    
    message_content = context.message.author.mention

    try:
        chart = await get_chart(user["username"], chart_type, size, nc=captions)
        await context.send(content=message_content, file=discord.File(fp=chart,filename="chart.png"))
    except Exception as e:
        await context.send(general_error)
        raise e

class Chart(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def weekly(self, ctx, *args):
        usage = "usage: `weekly <optional: size (3x3, 4x4, 5x5, 2x6)>`"
        await parse(ctx, "weekly", usage, *args)
    
    @commands.command()
    async def monthly(self, ctx, *args):
        usage = "usage: `monthly <optional: size (3x3, 4x4, 5x5, 2x6)>`"
        await parse(ctx, "monthly", usage, *args)

    @commands.command(name="3months")
    async def quarterly(self, ctx, *args):
        usage = "usage: `3months <optional: size (3x3, 4x4, 5x5, 2x6)>`"
        await parse(ctx, "3months", usage, *args)
    
    @commands.command(name="6months")
    async def biannually(self, ctx, *args):
        usage = "usage: `6months <optional: size (3x3, 4x4, 5x5, 2x6)>`"
        await parse(ctx, "6months", usage, *args)
    
    @commands.command()
    async def yearly(self, ctx, *args):
        usage = "usage: `yearly <optional: size (3x3, 4x4, 5x5, 2x6)>`"
        await parse(ctx, "yearly", usage, *args)

    @commands.command()
    async def alltime(self, ctx, *args):
        usage = "usage: `alltime <optional: size (3x3, 4x4, 5x5, 2x6)>`"
        await parse(ctx, "alltime", usage, *args)