import discord
from discord.ext import commands

class Avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["avatar", "av"])
    async def get_avatar(self, ctx, user: discord.Member = None):
        """Get a user's avatar."""
        user = user or ctx.author
        avatar_url = user.avatar_url_as(size=1024)

        embed = discord.Embed(title=f"{user.name}'s Avatar", color=user.color)
        embed.set_image(url=avatar_url)
        
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Avatar(bot))
