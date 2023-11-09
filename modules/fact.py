import discord
from discord.ext import commands
import requests

class Fact(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.nekos_life_api_url = "https://nekos.life/api/v2/fact"

    @commands.command(name="fact")
    async def fact_command(self, ctx):
        """Get a random fact."""
        try:
            data = self.get_fact_data()
            if data:
                embed = self.create_embed(data)
                await ctx.send(embed=embed)
            else:
                await ctx.send("Failed to fetch a random fact.")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    def get_fact_data(self):
        response = requests.get(self.nekos_life_api_url)

        if response.status_code == 200:
            data = response.json()
            return data.get("fact", "")
        else:
            return None

    def create_embed(self, fact):
        if not fact:
            return None

        embed = discord.Embed(
            title="Random Fact",
            description=fact,
            color=discord.Color.green()
        )

        return embed

def setup(bot):
    bot.add_cog(Fact(bot))
