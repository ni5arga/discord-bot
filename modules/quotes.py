import discord
from discord.ext import commands
import requests

class Quotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def quote(self, ctx):
        """Get a random quote"""
        url = "https://api.quotable.io/random"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            content = data.get('content', 'No content available')
            author = data.get('author', 'Unknown')

            embed = discord.Embed(color=discord.Color.blue())
            embed.add_field(name="Quote", value=content, inline=False)
            embed.set_footer(text=f"- {author}")

            await ctx.send(embed=embed)
        else:
            await ctx.send("Error fetching quote.")

def setup(bot):
    bot.add_cog(Quotes(bot))
