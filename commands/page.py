import discord
from discord.ext import commands
from commands.fm import Scrobbles, Scrobble

def setup(bot):
    bot.add_cog(Last(bot))

class Last(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.current_index = 0

    @commands.command()
    async def page(self, ctx, *args):
        await ctx.trigger_typing()
        usage = "usage: `reactions on | off`"

        if len(args) == 0:
            await ctx.send(usage)
            return

        amount = int(args[0])
        scrobbler = Scrobbles("skiffskiffles", limit=amount)
        scrobbles = scrobbler.scrobbles

        master_list = []

        for i in range(amount):
            try:
                scrobble = Scrobble(scrobbles["recenttracks"]["track"][i])
                master_list.append(str(f"{scrobble.name} - {scrobble.artist}"))
            except:
                pass

        limit = 10

        sublists = []
        to_add = []

        for i in range(len(master_list)):
            to_add.append(master_list[i])
    
            if len(to_add) == limit or i == (len(master_list) - 1):
                sublists.append(to_add.copy())
                to_add.clear()

        def make_content(index):
            content = ""
            counter = index * 10 + 1
            for element in sublists[index]:
                content += f"**{counter}**) {element}\n"
                counter += 1
            
            if ctx.author.color == "#000000":
                color = "#ffffff"
            else:
                color = ctx.author.color
            
            embed = discord.Embed(
            title=f"{scrobbler.username}'s Recent Scrobbles",
            description=content,
            color=color # i thought this would be cute
            )

            try:
                embed.set_thumbnail(url=ctx.author.avatar_url)
            except:
                pass
        
            embed.set_author(
                name=f"last.fm",
                icon_url="https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fimages1.wikia.nocookie.net%2F__cb20130411230810%2Flogopedia%2Fimages%2F1%2F1d%2FLast_fm_logo.png&f=1&nofb=1",
                url=scrobbler.user_url
            )

            return embed

        global msg
        msg = await ctx.send(embed=make_content(self.current_index))
        
        await msg.add_reaction("⬅️")
        await msg.add_reaction("➡️")

        def reaction_check(ctx, reaction, user):
            if user.id == ctx.author.id:
                if user.id != self.bot.user.id:
                    if reaction.message.id == msg.id:
                        return True
            return False

        @self.bot.listen("on_reaction_add")
        async def _on_reaction_add(reaction, user):
            if reaction_check(ctx, reaction, user) is True:
                if str(reaction) == "⬅️":
                    if self.current_index == 0:
                        pass
                    else:
                        self.current_index -= 1
                        await msg.edit(embed=make_content(self.current_index))

                elif str(reaction) == "➡️":
                    if self.current_index == (len(sublists) - 1):
                        pass
                    else:
                        self.current_index += 1
                        await msg.edit(embed=make_content(self.current_index))
            return

        @self.bot.listen("on_reaction_remove")
        async def _on_reaction_remove(reaction, user):
            if reaction_check(ctx, reaction, user) is True:
                if str(reaction) == "⬅️":
                    if self.current_index == 0:
                        return
                    self.current_index -= 1
                    await msg.edit(embed=make_content(self.current_index))
                
                elif str(reaction) == "➡️":
                    if self.current_index == (len(sublists) - 1):
                        return
                    self.current_index += 1
                    await msg.edit(embed=make_content(self.current_index))
            return