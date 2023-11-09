import discord
from discord.ext import commands
import requests

class Commit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="commit")
    async def commit_message(self, ctx):
        """Get a random commit message"""
        commit_message = requests.get("http://whatthecommit.com/index.txt").text.strip()
        await ctx.send(f"{commit_message}")

def setup(bot):
    bot.add_cog(Commit(bot))
