import discord
from discord.ext import commands
import requests

class URLShortener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tinyurl_api_url = "http://tinyurl.com/api-create.php?url="

    @commands.command()
    async def url(self, ctx, url):
        """Shorten a URL using TinyURL."""
        try:
            response = requests.get(self.tinyurl_api_url + url)

            if response.status_code == 200:
                short_url = response.text
                await ctx.send(f"Shortened URL: {short_url}")
            else:
                await ctx.send("Error shortening URL.")
        except Exception as e:
            await ctx.send(f"Error: {e}")

def setup(bot):
    bot.add_cog(URLShortener(bot))
