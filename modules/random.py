import discord
from discord.ext import commands
import random

class Random(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def randommember(self, ctx):
        """Pick a random member and mention them."""
        members = ctx.guild.members
        random_member = random.choice(members)
        await ctx.send(f"Random Member: {random_member.mention}")

    @commands.command()
    async def randomnumber(self, ctx, lower: int = 1, upper: int = 1000):
        """Pick a random number in the specified range. Example !randommumber 1 and 1000"""
        if lower > upper:
            lower, upper = upper, lower
        random_num = random.randint(lower, upper)
        await ctx.send(f"Random Number: {random_num}")

def setup(bot):
    bot.add_cog(Random(bot))
