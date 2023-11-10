import discord
from discord.ext import commands
import requests

class Pokemon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pokeapi_base_url = "https://pokeapi.co/api/v2/pokemon/"
        self.image_base_url = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/"

    @commands.command(name="pokemon")
    async def pokemon_command(self, ctx, pokemon_name):
        """Get information about a Pokémon."""
        try:
            data = self.get_pokemon_data(pokemon_name.lower())
            if data:
                embed = self.create_pokemon_embed(data)
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"Pokemon '{pokemon_name}' not found.")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    def get_pokemon_data(self, pokemon_name):
        response = requests.get(f"{self.pokeapi_base_url}{pokemon_name}/")

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return None

    def create_pokemon_embed(self, data):
        if not data:
            return None

        name = data.get("name", "")
        id_number = data.get("id", "")

        types = [t["type"]["name"].capitalize() for t in data.get("types", [])]
        abilities = [a["ability"]["name"].capitalize() for a in data.get("abilities", [])]
        stats = {s["stat"]["name"].capitalize(): s["base_stat"] for s in data.get("stats", [])}

        embed = discord.Embed(
            title=f"{name.capitalize()} - #{id_number}",
            description=f"Types: {', '.join(types)}\nAbilities: {', '.join(abilities)}",
            color=discord.Color.blue()
        )

        for stat, value in stats.items():
            embed.add_field(name=stat, value=value, inline=True)

        embed.set_image(url=self.get_pokemon_image_url(id_number))
        return embed

    def get_pokemon_image_url(self, id_number):
        return f"{self.image_base_url}{id_number}.png"

def setup(bot):
    bot.add_cog(Pokemon(bot))
