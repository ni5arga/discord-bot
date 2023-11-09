
import discord
from discord.ext import commands
import requests

class UrbanDictionary(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.urbandictionary_api_url = "http://api.urbandictionary.com/v0/define"

    @commands.command(name="urbandictionary", aliases=["ud"])
    async def urbandictionary_command(self, ctx, *, query):
        """Get the definition of a word from Urban Dictionary."""
        try:
            data = self.get_urbandictionary_data(query)
            if data:
                embed = self.create_embed(data)
                await ctx.send(embed=embed)
            else:
                await ctx.send("No definition found for the given query.")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    def get_urbandictionary_data(self, query):
        params = {"term": query}
        response = requests.get(self.urbandictionary_api_url, params=params)

        if response.status_code == 200:
            data = response.json()
            return data.get("list", [])
        else:
            return None

    def create_embed(self, data):
        if not data:
            return None

        first_definition = data[0]
        query = first_definition.get("word", "")
        definition = first_definition.get("definition", "").strip()
        author = first_definition.get("author", "")
        example = first_definition.get("example", "").strip()

        embed = discord.Embed(
            title="Urban Dictionary",
            color=discord.Color.blue()
        )
        embed.add_field(name="Query", value=query, inline=False)
        embed.add_field(name="Definition", value=definition, inline=False)
        embed.add_field(name="Author", value=author, inline=False)
        embed.add_field(name="Example", value=example, inline=False)

        return embed

def setup(bot):
    bot.add_cog(UrbanDictionary(bot))
