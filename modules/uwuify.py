import discord
from discord.ext import commands
import uwuify

class Uwuify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def uwu(self, ctx, *, text):
        """UwUify text."""
        uwu_flags = uwuify.SMILEY | uwuify.YU | uwuify.STUTTER
        uwuified_text = uwuify.uwu(text, flags=uwu_flags)
        await ctx.send(uwuified_text)

def setup(bot):
    bot.add_cog(Uwuify(bot))
