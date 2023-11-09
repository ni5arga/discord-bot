import discord
from discord.ext import commands
import requests

class AnimeQuote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.anime_quote_api_url = "https://animechan.xyz/api/random"

    @commands.command()
    async def aniquote(self, ctx):
        """Get a random anime quote."""
        try:
            response = requests.get(self.anime_quote_api_url)

            if response.status_code == 200:
                data = response.json()
                quote = data.get('quote', 'No quote available.')
                character = data.get('character', 'Unknown')
                anime = data.get('anime', 'Unknown')

                embed = discord.Embed(color=discord.Color.orange())
                embed.title = f"Anime Quote"
                embed.description = f"{quote}\n\n- {character} from {anime}"

                await ctx.send(embed=embed)
            else:
                await ctx.send("Error fetching anime quote.")
        except Exception as e:
            await ctx.send(f"Error: {e}")

def setup(bot):
    bot.add_cog(AnimeQuote(bot))
