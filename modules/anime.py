import discord
from discord.ext import commands
import aiohttp

class Anime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def fetch_image(self, ctx, command):
        base_url = "https://api.waifu.pics/sfw/"
        url = f"{base_url}{command}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    image_url = data['url']
                    embed = discord.Embed(color=discord.Color.purple())
                    embed.set_image(url=image_url)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(f"Error fetching image for {command}.")

    @commands.command()
    async def waifu(self, ctx):
        """Get a random waifu image."""
        await self.fetch_image(ctx, 'waifu')

    @commands.command()
    async def neko(self, ctx):
        """Get a random neko image."""
        await self.fetch_image(ctx, 'neko')

    @commands.command()
    async def shinobu(self, ctx):
        """Get a random Shinobu image."""
        await self.fetch_image(ctx, 'shinobu')

    @commands.command()
    async def megumin(self, ctx):
        """Get a random Megumin image."""
        await self.fetch_image(ctx, 'megumin')

    @commands.command()
    async def bully(self, ctx):
        """Get a random bully image."""
        await self.fetch_image(ctx, 'bully')

    @commands.command()
    async def cuddle(self, ctx):
        """Get a random cuddle image."""
        await self.fetch_image(ctx, 'cuddle')

    @commands.command()
    async def cry(self, ctx):
        """Get a random cry image."""
        await self.fetch_image(ctx, 'cry')

    @commands.command()
    async def hug(self, ctx):
        """Get a random hug image."""
        await self.fetch_image(ctx, 'hug')

    @commands.command()
    async def awoo(self, ctx):
        """Get a random awoo image."""
        await self.fetch_image(ctx, 'awoo')

    @commands.command()
    async def kiss(self, ctx):
        """Get a random kiss image."""
        await self.fetch_image(ctx, 'kiss')

    @commands.command()
    async def lick(self, ctx):
        """Get a random lick image."""
        await self.fetch_image(ctx, 'lick')

    @commands.command()
    async def pat(self, ctx):
        """Get a random pat image."""
        await self.fetch_image(ctx, 'pat')

    @commands.command()
    async def smug(self, ctx):
        """Get a random smug image."""
        await self.fetch_image(ctx, 'smug')

    @commands.command()
    async def bonk(self, ctx):
        """Get a random bonk image."""
        await self.fetch_image(ctx, 'bonk')

    @commands.command()
    async def yeet(self, ctx):
        """Get a random yeet image."""
        await self.fetch_image(ctx, 'yeet')

    @commands.command()
    async def blush(self, ctx):
        """Get a random blush image."""
        await self.fetch_image(ctx, 'blush')

    @commands.command()
    async def smile(self, ctx):
        """Get a random smile image."""
        await self.fetch_image(ctx, 'smile')

    @commands.command()
    async def wave(self, ctx):
        """Get a random wave image."""
        await self.fetch_image(ctx, 'wave')

    @commands.command()
    async def highfive(self, ctx):
        """Get a random highfive image."""
        await self.fetch_image(ctx, 'highfive')

    @commands.command()
    async def handhold(self, ctx):
        """Get a random handhold image."""
        await self.fetch_image(ctx, 'handhold')

    @commands.command()
    async def nom(self, ctx):
        """Get a random nom image."""
        await self.fetch_image(ctx, 'nom')

    @commands.command()
    async def bite(self, ctx):
        """Get a random bite image."""
        await self.fetch_image(ctx, 'bite')

    @commands.command()
    async def glomp(self, ctx):
        """Get a random glomp image."""
        await self.fetch_image(ctx, 'glomp')

    @commands.command()
    async def slap(self, ctx):
        """Get a random slap image."""
        await self.fetch_image(ctx, 'slap')

    @commands.command()
    async def kill(self, ctx):
        """Get a random kill image."""
        await self.fetch_image(ctx, 'kill')

    @commands.command()
    async def happy(self, ctx):
        """Get a random happy image."""
        await self.fetch_image(ctx, 'happy')

    @commands.command()
    async def wink(self, ctx):
        """Get a random wink image."""
        await self.fetch_image(ctx, 'wink')

    @commands.command()
    async def poke(self, ctx):
        """Get a random poke image."""
        await self.fetch_image(ctx, 'poke')

    @commands.command()
    async def dance(self, ctx):
        """Get a random dance image."""
        await self.fetch_image(ctx, 'dance')

    @commands.command()
    async def cringe(self, ctx):
        """Get a random cringe image."""
        await self.fetch_image(ctx, 'cringe')

def setup(bot):
    bot.add_cog(Anime(bot))
