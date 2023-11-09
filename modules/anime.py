import discord
from discord.ext import commands
import aiohttp

class Anime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def fetch_data(self, ctx, query, type_):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.jikan.moe/v4/{type_}?q={query}") as response:
                if response.status == 200:
                    data = await response.json()
                    if data and 'data' in data:
                        return data['data'][0]
                    else:
                        await ctx.send(f"{type_.capitalize()} not found.")
                else:
                    await ctx.send(f"An error occurred while fetching {type_} information.")

    @commands.command(name="anime")
    async def anime_info(self, ctx, *, query):
        """Get information about an anime."""
        anime_info = await self.fetch_data(ctx, query, 'anime')
        if anime_info:
            embed = discord.Embed(title=anime_info['title'], color=discord.Color.blue())
            embed.add_field(name="Synopsis", value=anime_info['synopsis'][:500] + "...")
            embed.add_field(name="Type", value=anime_info['type'])
            embed.add_field(name="Episodes", value=anime_info['episodes'])
            embed.add_field(name="Score", value=anime_info['score'])
            embed.add_field(name="Status", value=anime_info['status'])
            embed.add_field(name="Aired", value=anime_info['aired']['string'])
            embed.add_field(name="Duration", value=anime_info['duration'])
            embed.add_field(name="Genres", value=", ".join(genre['name'] for genre in anime_info['genres']))
            embed.set_image(url=anime_info['images']['jpg']['large_image_url'])
            embed.add_field(name="MAL Link", value=f"[{anime_info['title']}]({anime_info['url']})")
            await ctx.send(embed=embed)

    @commands.command(name="animecharacter", aliases=["anichar", "animechar"])
    async def anime_character_info(self, ctx, *, query):
        """Get information about an anime character."""
        character_info = await self.fetch_data(ctx, query, 'characters')
        if character_info:
            embed = discord.Embed(title=character_info['name'], color=discord.Color.blue())
           # anime_title = character_info.get('anime', {}).get('title', 'Unknown Anime')
         #  embed.add_field(name="Anime", value=anime_title)
            embed.add_field(name="Nicknames", value=", ".join(character_info.get('nicknames', ['None'])))
            embed.add_field(name="Favorites", value=character_info.get('favorites', 'Unknown'))
            about = character_info.get('about', 'No information available.')
            embed.add_field(name="About", value=about[:500] + "...")
            embed.set_image(url=character_info['images']['jpg']['image_url'])
            embed.add_field(name="MAL Link", value=f"[{character_info['name']}]({character_info['url']})")
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Anime(bot))
